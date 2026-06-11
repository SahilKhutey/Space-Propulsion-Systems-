# Contributing to PropSim

## Branching Strategy
We use GitFlow:
- `main`: Production stable releases (tagged).
- `develop`: Main development integration branch.
- Feature branches `feature/*` branched off `develop`.
- Hotfix branches `hotfix/*` branched off `main`.

## Code Review Guidelines
- Minimum 2 approvals from code owners required (see `.github/CODEOWNERS`).
- All tests, including physics validation tests, must pass in CI.
- No decrease in unit test coverage.
- Add an ADR in `docs/adr/` for any breaking architectural changes.
