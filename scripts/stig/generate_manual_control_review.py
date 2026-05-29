#!/usr/bin/env python3
"""Generate identifier-only working lists for PostgreSQL 16 STIG manual review."""

import argparse
import json
from collections import Counter
from pathlib import Path


REVIEW_ARTIFACT_NOTICE = (
    "This review artifact is generated from committed project metadata. "
    "It uses control identifiers and project-authored review prompts only; "
    "do not add benchmark prose, local source paths, or secrets."
)
CONTROL_TOPICS = {
    "V-261866": "audit event coverage",
    "V-261871": "audit identity fields",
    "V-261872": "organization-defined audit fields",
    "V-261888": "external executable access",
    "V-261891": "password storage",
    "V-261892": "password authentication transport",
    "V-261919": "audit storage monitoring",
    "V-261921": "timestamp timezone",
    "V-261922": "timestamp precision",
    "V-261925": "configuration change auditing",
    "V-261934": "invalid input behavior",
    "V-261942": "privilege change auditing",
    "V-261952": "security object deletion auditing",
    "V-261953": "failed security object deletion auditing",
    "V-261954": "information category deletion auditing",
    "V-261967": "audit log offload",
    "V-283674": "vendor support lifecycle",
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traceability", type=Path)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("output", type=Path)
    return parser.parse_args()


def csv(values):
    return ", ".join(values) if values else "none"


def table_row(values):
    return "| " + " | ".join(str(value) for value in values) + " |"


def topic(control_id):
    return CONTROL_TOPICS.get(control_id, "unclassified")


def count_rows(counter, names):
    return [table_row([name, counter.get(name, 0)]) for name in names]


def severity_mismatch_controls(mappings):
    return [
        item
        for item in mappings
        if item["mapping_status"] == "unmapped"
        and item["candidate_warnings"].get("severity_mismatch")
    ]


def reviewed_severity_mismatch_controls(mappings):
    return [
        item
        for item in mappings
        if item["mapping_status"] != "unmapped"
        and item["candidate_warnings"].get("severity_mismatch")
    ]


def no_candidate_controls(mappings):
    return [
        item
        for item in mappings
        if item["mapping_status"] == "unmapped"
        and not item["candidate_legacy_control_ids"]
    ]


def manual_only_controls(mappings):
    return [item for item in mappings if item["mapping_status"] == "manual_only"]


def write_section(lines, title, rows, headers):
    lines.extend([f"## {title}", "", table_row(headers), table_row(["---"] * len(headers))])
    lines.extend(rows)
    lines.append("")


def main():
    args = parse_args()
    traceability = json.loads(args.traceability.read_text())
    mapping = json.loads(args.mapping.read_text())
    mappings = mapping["mappings"]

    mapping_counts = Counter(item["mapping_status"] for item in mappings)
    automation_counts = Counter(item["automation_status"] for item in mappings)
    traceability_counts = Counter(item["status"] for item in traceability["controls"])

    lines = [
        "# PostgreSQL 16 Manual Control Reduction Review",
        "",
        REVIEW_ARTIFACT_NOTICE,
        "",
        "## Current Counts",
        "",
        "### Mapping Status",
        "",
        table_row(["Status", "Count"]),
        table_row(["---", "---"]),
        *count_rows(
            mapping_counts,
            [
                "mapped",
                "manual_only",
                "unmapped",
                "replaced_by_overlay",
                "deployment_owned",
                "exception",
            ],
        ),
        "",
        "### Automation Status",
        "",
        table_row(["Status", "Count"]),
        table_row(["---", "---"]),
        *count_rows(
            automation_counts,
            [
                "automated",
                "partially_automated",
                "manual",
                "not_yet_assessed",
                "deployment_owned",
                "exception",
            ],
        ),
        "",
        "### Traceability Status",
        "",
        table_row(["Status", "Count"]),
        table_row(["---", "---"]),
        *count_rows(
            traceability_counts,
            [
                "image_enforced",
                "deployment_owned",
                "validation_only",
                "manual",
                "exception",
                "not_yet_reviewed",
            ],
        ),
        "",
    ]

    severity_rows = [
        table_row(
            [
                item["control_id"],
                item["stig_id"],
                item["severity"],
                csv(item["candidate_legacy_control_ids"]),
                csv(item["candidate_srg_ids"]),
                "Review candidate logic and severity change before reuse.",
            ]
        )
        for item in severity_mismatch_controls(mappings)
    ]
    write_section(
        lines,
        "Severity-Mismatch Unmapped Controls",
        severity_rows,
        ["Control ID", "STIG ID", "Severity", "Candidate IDs", "Candidate SRG IDs", "Review Prompt"],
    )

    reviewed_severity_rows = [
        table_row(
            [
                item["control_id"],
                item["stig_id"],
                item["mapping_status"],
                item["automation_status"],
                item["container_validation"],
                item["deployment_responsibility"],
                item["notes"],
            ]
        )
        for item in reviewed_severity_mismatch_controls(mappings)
    ]
    write_section(
        lines,
        "Reviewed Severity-Mismatch Decisions",
        reviewed_severity_rows,
        [
            "Control ID",
            "STIG ID",
            "Mapping Status",
            "Automation Status",
            "Container Validation",
            "Deployment Responsibility",
            "Project Rationale",
        ],
    )

    no_candidate_rows = [
        table_row(
            [
                item["control_id"],
                item["stig_id"],
                topic(item["control_id"]),
                item["severity"],
                csv(item["cci_refs"]),
                "Group by topic and compare against repository-owned or deployment-owned evidence.",
            ]
        )
        for item in no_candidate_controls(mappings)
    ]
    write_section(
        lines,
        "No-Candidate Unmapped Controls",
        no_candidate_rows,
        ["Control ID", "STIG ID", "Topic", "Severity", "CCI Refs", "Review Prompt"],
    )

    manual_rows = [
        table_row(
            [
                item["control_id"],
                item["stig_id"],
                item["severity"],
                csv(item["legacy_control_ids"]),
                item["container_validation"],
                "Reassess for concrete overlay, deployment, or manual evidence.",
            ]
        )
        for item in manual_only_controls(mappings)
    ]
    write_section(
        lines,
        "Manual-Only Controls",
        manual_rows,
        ["Control ID", "STIG ID", "Severity", "Legacy IDs", "Container Validation", "Review Prompt"],
    )

    args.output.write_text("\n".join(lines) + "\n")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
