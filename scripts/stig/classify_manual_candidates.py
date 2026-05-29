#!/usr/bin/env python3
"""Classify non-executable same-severity legacy candidates as manual-only."""

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


def has_executable_assertions(path):
    text = path.read_text(errors="replace")
    return any(marker in text for marker in EXECUTABLE_MARKERS)


def main():
    args = parse_args()
    mapping_path = _safe_path(args.mapping)
    data = json.loads(mapping_path.read_text())
    classified = 0

    for item in data["mappings"]:
        candidates = item["candidate_legacy_control_ids"]
        if item["mapping_status"] != "unmapped":
            continue
        if not candidates:
            continue
        if item["candidate_warnings"].get("severity_mismatch"):
            continue

        legacy_paths = [args.legacy_controls_dir / f"{candidate}.rb" for candidate in candidates]
        if any(has_executable_assertions(path) for path in legacy_paths if path.exists()):
            continue

        item["mapping_status"] = "manual_only"
        item["legacy_control_ids"] = candidates
        item["automation_status"] = "manual"
        item["container_validation"] = "not_supported"
        item["validation_owner"] = "manual"
        item["deployment_responsibility"] = "manual"
        item["notes"] = (
            "Manual-only classification based on matching normalized STIG ID suffix, "
            "same severity, and no executable assertions in the legacy candidate."
        )
        classified += 1

    mapping_path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"classified {classified} mappings as manual_only")


if __name__ == "__main__":
    main()
