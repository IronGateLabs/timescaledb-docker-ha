#!/usr/bin/env python3
"""Promote conservative legacy validation candidates in the mapping file."""

import argparse
import json
import os
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[2]


def _safe_path(path):
    """Resolve a CLI-supplied path and reject anything outside the repo root.

    Sanitizes an operator-supplied argparse path before filesystem I/O so a
    traversal value cannot escape the repository tree.
    """
    resolved = Path(path).resolve()
    if os.path.commonpath([str(_REPO_ROOT), str(resolved)]) != str(_REPO_ROOT):
        raise SystemExit(f"refusing path outside repository root: {path}")
    return resolved


EXECUTABLE_MARKERS = (
    "sql.query",
    "postgres_session",
    "describe command(",
    "describe file(",
    "describe directory(",
    "describe package(",
)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("legacy_controls_dir", type=Path)
    return parser.parse_args()


def control_traits(path):
    traits = {}
    for item in path.glob("V-*.rb"):
        text = item.read_text(errors="replace")
        traits[item.stem] = {
            "executable": any(marker in text for marker in EXECUTABLE_MARKERS),
            "has_skip": "skip " in text,
        }
    return traits


def main():
    args = parse_args()
    mapping_path = _safe_path(args.mapping)
    data = json.loads(mapping_path.read_text())
    traits = control_traits(args.legacy_controls_dir)

    promoted = 0
    partial_skip = 0
    for item in data["mappings"]:
        candidates = item["candidate_legacy_control_ids"]
        if item["mapping_status"] != "unmapped":
            continue
        if not candidates:
            continue
        if item["candidate_warnings"].get("severity_mismatch"):
            continue
        if not all(traits.get(candidate, {}).get("executable") for candidate in candidates):
            continue

        item["mapping_status"] = "mapped"
        item["legacy_control_ids"] = candidates
        item["automation_status"] = "partially_automated"
        item["container_validation"] = "partial"
        item["validation_owner"] = "validation_profile"
        item["notes"] = (
            "Initial reusable validation link based on matching normalized STIG ID suffix, "
            "same severity, and executable legacy control; verify PostgreSQL 16 logic before "
            "treating as authoritative coverage."
        )
        promoted += 1
        if any(traits.get(candidate, {}).get("has_skip") for candidate in candidates):
            partial_skip += 1

    mapping_path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"promoted {promoted} mappings ({partial_skip} include legacy skip paths)")


if __name__ == "__main__":
    main()
