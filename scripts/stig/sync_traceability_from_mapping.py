#!/usr/bin/env python3
"""Sync reviewed mapping decisions into traceability."""

import argparse
import json
from pathlib import Path


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
    traceability = json.loads(args.traceability.read_text())
    mapping = json.loads(args.mapping.read_text())
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

    args.traceability.write_text(json.dumps(traceability, indent=2) + "\n")
    print(f"synced {updated} mapping decisions into traceability")


if __name__ == "__main__":
    main()
