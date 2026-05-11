# Deviations

Log of deviations from the build prompt with justification.

## v0.1.0

| Deviation | Justification |
|-----------|---------------|
| `cffconvert` and `cyclonedx-bom` not in pyproject.toml dev extras | jsonschema version conflict between cffconvert (requires <4) and cyclonedx-bom (requires >=4.18). These tools are installed as standalone tools via `uv tool` or `pipx` in CI. |
| Manifest model field named `col_schema` instead of `schema` | `schema` shadows a Pydantic v2 BaseModel attribute, causing a warning that is promoted to an error under strict test configuration. |
| `mike` versioning plugin not activated in mkdocs build | mike requires a git repository with tags for versioning; deferred to first tagged release. |

Last updated: 2026-05-11
