#!/usr/bin/env python3
"""Update one PostgreSQL 16 STIG control mapping entry."""

import argparse
import json
from pathlib import Path


ALLOWED_MAPPING_STATUS = {
    "unmapped",
    "direct_match",
    "mapped",
    "replaced_by_overlay",
    "manual_only",
    "deployment_owned",
    "exception",
}
ALLOWED_AUTOMATION_STATUS = {
    "not_yet_assessed",
    "automated",
    "partially_automated",
    "manual",
    "deployment_owned",
    "exception",
}
ALLOWED_CONTAINER_VALIDATION = {
    "not_yet_assessed",
    "supported",
    "partial",
    "not_supported",
}
ALLOWED_OWNER = {
    "unassigned",
    "image",
    "deployment",
    "validation_profile",
    "overlay",
    "documentation",
    "manual",
    "exception",
}
ALLOWED_DEPLOYMENT_RESPONSIBILITY = {
    "undetermined",
    "none",
    "kubernetes",
    "operator",
    "organization_policy",
    "identity_and_access",
    "networking",
    "secrets",
    "manual",
}


def csv(value):
    if value is None or value == "":
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("control_id")
    parser.add_argument("--mapping-status", choices=sorted(ALLOWED_MAPPING_STATUS))
    parser.add_argument("--legacy-control-ids")
    parser.add_argument("--overlay-checks")
    parser.add_argument("--automation-status", choices=sorted(ALLOWED_AUTOMATION_STATUS))
    parser.add_argument("--container-validation", choices=sorted(ALLOWED_CONTAINER_VALIDATION))
    parser.add_argument("--implementation-owner", choices=sorted(ALLOWED_OWNER))
    parser.add_argument("--validation-owner", choices=sorted(ALLOWED_OWNER))
    parser.add_argument(
        "--deployment-responsibility",
        choices=sorted(ALLOWED_DEPLOYMENT_RESPONSIBILITY),
    )
    parser.add_argument("--notes")
    return parser.parse_args()


def main():
    args = parse_args()
    data = json.loads(args.mapping.read_text())
    for item in data["mappings"]:
        if item["control_id"] == args.control_id:
            break
    else:
        raise SystemExit(f"unknown control_id: {args.control_id}")

    updates = {
        "mapping_status": args.mapping_status,
        "automation_status": args.automation_status,
        "container_validation": args.container_validation,
        "implementation_owner": args.implementation_owner,
        "validation_owner": args.validation_owner,
        "deployment_responsibility": args.deployment_responsibility,
        "notes": args.notes,
    }
    for key, value in updates.items():
        if value is not None:
            item[key] = value

    legacy_control_ids = csv(args.legacy_control_ids)
    if legacy_control_ids is not None:
        item["legacy_control_ids"] = legacy_control_ids

    overlay_checks = csv(args.overlay_checks)
    if overlay_checks is not None:
        item["overlay_checks"] = overlay_checks

    args.mapping.write_text(json.dumps(data, indent=2) + "\n")
    print(f"updated {args.control_id}")


if __name__ == "__main__":
    main()
