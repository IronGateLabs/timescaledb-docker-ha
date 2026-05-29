#!/usr/bin/env python3
"""Sync reviewed mapping decisions into traceability."""

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


SYNC_STATUSES = {
    "mapped": {
        "status": "validation_only",
        "implementation_owner": "unassigned",
        "validation_owner": "validation_profile",
        "deployment_responsibility": "none",
        "implemented_by": [],
    },
    "replaced_by_overlay": {
        "status": "image_enforced",
        "implementation_owner": "image",
        "validation_owner": "overlay",
        "deployment_responsibility": "none",
        "implemented_by": ["stig:image-stig-mode"],
    },
    "manual_only": {
        "status": "manual",
        "implementation_owner": "manual",
        "validation_owner": "manual",
        "deployment_responsibility": "manual",
        "implemented_by": [],
    },
    "deployment_owned": {
        "status": "deployment_owned",
        "implementation_owner": "deployment",
        "validation_owner": "documentation",
        "implemented_by": [],
    },
    "exception": {
        "status": "exception",
        "implementation_owner": "exception",
        "validation_owner": "exception",
        "deployment_responsibility": "none",
        "implemented_by": [],
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traceability", type=Path)
    parser.add_argument("mapping", type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    traceability_path = _safe_path(args.traceability)
    mapping_path = _safe_path(args.mapping)
    traceability = json.loads(traceability_path.read_text())
    mapping = json.loads(mapping_path.read_text())
    mapping_by_id = {item["control_id"]: item for item in mapping["mappings"]}

    updated = 0
    for control in traceability["controls"]:
        mapped = mapping_by_id[control["control_id"]]
        sync = SYNC_STATUSES.get(mapped["mapping_status"])
        if not sync:
            continue
        for key, value in sync.items():
            control[key] = value
        if (
            mapped["mapping_status"] == "deployment_owned"
            and mapped["deployment_responsibility"] != "undetermined"
        ):
            control["deployment_responsibility"] = mapped["deployment_responsibility"]
        control["validated_by"] = []
        if mapped["legacy_control_ids"]:
            control["validated_by"].extend(f"legacy:{legacy_id}" for legacy_id in mapped["legacy_control_ids"])
        if mapped["overlay_checks"]:
            control["validated_by"].extend(f"overlay:{check}" for check in mapped["overlay_checks"])
        control["notes"] = mapped["notes"]
        updated += 1

    traceability_path.write_text(json.dumps(traceability, indent=2) + "\n")
    print(f"synced {updated} mapping decisions into traceability")


if __name__ == "__main__":
    main()
