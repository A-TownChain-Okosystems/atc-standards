# SCR-0145 — KAI-OS Unified Product, Version & Build Contract

Status: PROPOSED / DRAFT; non-normative, not approved, not implemented.

Owner decisions (2026-11-25): one common product SemVer; Native, Linux-hosted and Windows-hosted variants; x86_64 and ARM64 for all variants (six mandatory targets); maximum achievable feature parity; all six targets mandatory for each unified stable release.

Architecture blocker: approved ATC-ARCH-001 v1.0.0 says KAI-OS is an architecture term, not a product, and assigns the OS role to GlobusOS and kernel role to ShivaCore. An existing unmerged branch scr-0144-kai-begriff contains SCR-0144 and explicitly says KAI is never a product. SCR-0145 must reconcile that prior proposal and amend the product boundary before normative adoption. Native must be precisely defined against GlobusOS/ShivaCore; Linux and Windows remain host-integrated software variants. No duplicate kernel, VM, wallet, consensus, algorithm or capability authority.

SSOT: ATC-STD-VERSION-001 remains the SemVer/release/build-manifest authority; ATC-STD-UPDATE-001 remains update/rollback authority. Candidate ID ATC-STD-VERSION-002 is provisional and requires registry allocation.

Targets: native-x86_64, native-aarch64, linux-x86_64, linux-aarch64, windows-x86_64, windows-aarch64. Cross-compilation is not runtime or hardware verification. Every feature is classified per target as NATIVE, ADAPTED, LIMITED, UNAVAILABLE, NOT_TESTED or EXCLUDED; NOT_TESTED never means supported.

Each target manifest binds exact Unified Source Set digest, repository commit SHAs, Build ID, target, toolchain/SDK/runner, dependency-lock SHA-256, tests, artifact SHA-256, signature, SBOM and provenance. All six targets must pass applicable build, unit, integration, runtime, security, compatibility and integrity gates. Any mandatory failure or missing evidence blocks the whole release. CI green alone is not VERIFIED.

Backup risk: Phase-1 backup remains NOT VERIFIED; Owner lifted the freeze explicitly. Use isolated branches/PRs, small commits, exact SHA records, no force-push, no secrets in GitHub, and continue backup work in parallel.

Status: SCR PROPOSED; architecture amendment BLOCKED; standard ID NOT ALLOCATED; schemas DRAFT/NOT VALIDATED; six-target builds NOT STARTED; runtime/hardware NOT TESTED; unified release BLOCKED.