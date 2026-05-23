#!/usr/bin/env python3
"""Sync manual/deployment/exception mapping decisions into traceability."""

import argparse
import json
from pathlib import Path


SYNC_STATUSES = {
    "manual_only": {
        "status": "manual",
        "implementation_owner": "manual",
        "validation_owner": "manual",
        "deployment_responsibility": "manual",
    },
    "deployment_owned": {
        "status": "deployment_owned",
        "implementation_owner": "deployment",
        "validation_owner": "documentation",
    },
    "exception": {
        "status": "exception",
        "implementation_owner": "exception",
        "validation_owner": "exception",
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
        if mapped["legacy_control_ids"]:
            control["validated_by"] = [f"legacy:{legacy_id}" for legacy_id in mapped["legacy_control_ids"]]
        if mapped["overlay_checks"]:
            control["validated_by"].extend(f"overlay:{check}" for check in mapped["overlay_checks"])
        control["notes"] = mapped["notes"]
        updated += 1

    args.traceability.write_text(json.dumps(traceability, indent=2) + "\n")
    print(f"synced {updated} mapping decisions into traceability")


if __name__ == "__main__":
    main()
