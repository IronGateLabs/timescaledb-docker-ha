# Upstream Validation Profile Contributions

Use this checklist before proposing changes to a forked PostgreSQL STIG validation profile.

## Scope

Keep upstreamable changes focused on portable PostgreSQL 16 behavior: profile metadata, inputs, package names, PostgreSQL paths, SQL compatibility, and reusable controls. TimescaleDB HA image-specific assumptions belong in this repository's overlay unless they apply broadly to PostgreSQL 16 containers.

## Content Rules

Do not copy DISA benchmark prose, local file paths, secrets, or workstation-specific values into profile changes. Use control identifiers, rule identifiers, tags, input names, and project-authored rationale only.

## Review Steps

1. Run `cicd/check-stig-workflow` in this repository.
2. Run the forked profile against the local hardened image with portable inputs.
3. Confirm examples use placeholders such as `path/to/source-xccdf.xml` and `<set-at-runtime>`.
4. Document any controls that remain manual, deployment-owned, or image-specific.
5. Open upstream pull requests as small compatibility changes, separate from local overlay additions.
