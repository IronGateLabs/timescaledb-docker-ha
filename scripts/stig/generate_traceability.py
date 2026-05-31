#!/usr/bin/env python3
"""Generate STIG traceability metadata from an XCCDF file.

This intentionally extracts identifiers and simple metadata only. Do not add
title, description, check text, fix text, or other benchmark prose here.
"""

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xccdf", type=Path, help="Path to the source XCCDF XML file")
    parser.add_argument("output", type=Path, help="Path for generated traceability JSON")
    parser.add_argument(
        "--source-label",
        default="PostgreSQL 16 STIG V1R2 XCCDF",
        help="Portable source label to store in the generated file",
    )
    return parser.parse_args()


def ns_for(root):
    if root.tag.startswith("{"):
        return {"xccdf": root.tag.split("}")[0].strip("{")}
    return {}


def findall(node, path, ns):
    return node.findall(path, ns) if ns else node.findall(path.replace("xccdf:", ""))


def find(node, path, ns):
    return node.find(path, ns) if ns else node.find(path.replace("xccdf:", ""))


def control_from_group(group, ns):
    rule = find(group, "xccdf:Rule", ns)
    if rule is None:
        return None

    version = find(rule, "xccdf:version", ns)
    cci_refs = []
    for ident in findall(rule, "xccdf:ident", ns):
        value = (ident.text or "").strip()
        if value.startswith("CCI-"):
            cci_refs.append(value)

    return {
        "control_id": group.get("id", ""),
        "rule_id": rule.get("id", ""),
        "stig_id": (version.text or "").strip() if version is not None else "",
        "severity": rule.get("severity", ""),
        "cci_refs": sorted(set(cci_refs)),
        "status": "not_yet_reviewed",
        "implementation_owner": "unassigned",
        "validation_owner": "unassigned",
        "deployment_responsibility": "undetermined",
        "implemented_by": [],
        "validated_by": [],
        "notes": "",
    }


def main():
    args = parse_args()
    root = ET.parse(args.xccdf).getroot()
    ns = ns_for(root)

    controls = []
    for group in findall(root, ".//xccdf:Group", ns):
        control = control_from_group(group, ns)
        if control is not None:
            controls.append(control)

    controls.sort(key=lambda item: item["control_id"])
    traceability = {
        "schema_version": 1,
        "benchmark": {
            "id": root.get("id", ""),
            "source": args.source_label,
            "content_policy": "Control identifiers and metadata only; do not copy benchmark prose.",
        },
        "controls": controls,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(traceability, indent=2) + "\n")
    print(f"Wrote {len(controls)} controls to {args.output}")


if __name__ == "__main__":
    main()
