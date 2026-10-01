# Frozen source hashes

`manifest.json` binds seven candidate source paths to their SHA-256 and Git blob SHA-1, and records the a43 base, earlier 32a2 candidate, and 06db installed-version source reference. The candidate is **32a2 plus three uncommitted tracked-file changes**, not a new Git commit. `snapshot_hash` describes only this seven-path overlay; it is not a full-repository Git tree.

Each patch was actually checked and applied to a fresh, isolated extraction of its stated Git baseline. The a43 full patch produced 7/7 exact candidate files; the 32a2 fixes produced 3/3 exact candidate files. The full patch also applied to the 06db source reference: 6/7 files matched the candidate exactly, while `data/lua/types/ccb_platform_v1.d.lua` retained the reference's independent SDL3 declaration changes and received both hook declarations. This is source-application evidence, not a rebuilt 06db executable or runtime acceptance.

| Relative source path | Candidate SHA-256 | Candidate Git blob SHA-1 |
| --- | --- | --- |
| data/lua/types/ccb_platform_v1.d.lua | 8e0560d5e3a003012e4c4b38e95c02a03da3741158c6dfcefccd2b7fa922007d | 459f4cfd953d8dbc30ed68c38aa008ed29f8751c |
| src/item_info.cpp | 5a8ccf0d1e352c7a981595dbd57ca8a5b66b1a443905e4837cc012c796d0c2b4 | 1c1dd88c87dafa56a3944b553b0303b82402d017 |
| src/lua_platform_disabled.cpp | d540a348714fb3cb47da92fa0cb7e6ed14af52c00a283ed514d255401d02ac8d | 280688aaeb80ec3fa12722e1a9d7c4e523481e31 |
| src/lua_platform_hooks.cpp | 130f28ef08ddbb31c55d9573222246845e6b20535b9a60b67579de2b8e7fd558 | 89197a67876f9a6361273f3a6aa45ea63380c142 |
| src/lua_platform_hooks.h | 7b9976694aa1b8cd774b34779cdf4e8bf80c0d6f9917e0936ee74b3154b56700 | a7a2398fd0801f77735ddad6f0eabc571c9838cc |
| src/lua_platform_runtime_hooks.cpp | 4310dd7a6383ef214c2a0d18791ab9ab2e15e8a294e93e45a90491e237f2b364 | 023c1057caf23073f8fc603661da09c9cc211094 |
| tests/lua_platform_test_01_contract.cpp | b73edd39f1d27bc5f65bd3b079d35582fc68aee86e5d06c386883a85ec59178d | c3a2bde561582a527a6b0648ab6af660b2de8ed4 |

Commands are recorded with relative patch placeholders. No personal checkout, user-data, build, or Nix-store paths are included. `source_file_sha256` in the license evidence fingerprints the upstream `LICENSE.txt`; the distributed `../LICENSE.txt` retains its primary license paragraph and the owner's same-license grant rather than irrelevant third-party font notices.
