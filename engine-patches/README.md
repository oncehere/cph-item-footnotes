# CPH item-footnotes engine patches

本包提供“末日脚注 / Apocalypse Footnotes”所需的原生显示接口。MOD 保留游戏已解析的主描述与现有字符画，在主描述后增加单独的脚注段落；缺失原生字符画时才查询 MOD 回退图。脚注使用当前游戏语言：中文使用中文，其他语言使用英文。必须启用 CPH Lua-first Platform，中文切换还需要本地化支持。

This source-only package adds the native display hooks required by Apocalypse Footnotes. Existing resolved descriptions and native art retain priority. The MOD needs a Lua-first CPH build exposing `on_item_description_append` and `on_item_ascii_art_fallback`; the hook payload contains `item_id`, optional `variant_id`, and the current `language`.

## Patch selection

| Patch | Exact starting point | Result |
| --- | --- | --- |
| `cph-item-footnotes-hooks-a43a8f2-to-candidate.patch` | `a43a8f2f270994dad716ab067c48aad7c2eeaee3` | Complete seven-path hook implementation and fixes |
| `cph-item-footnotes-fixes-32a2a03-to-candidate.patch` | `32a2a03425aed2de13d1aa38c698f843d29f3ba2` | Three tracked-file fixes for an existing early hook candidate |

Choose one patch. Do not apply both. The target is the recorded 32a2 candidate plus three uncommitted changes; it is not a new upstream commit. The full patch is readable text. The incremental patch uses Git's **forward-only binary literal** format so it does not distribute the earlier test's deleted personal path or any reverse-source data. Its decoded new source files are byte-identical to the same candidate; `git apply --reverse` is not supported for that incremental patch. The full patch remains available for code review.

The source reference `06db38942be4ba0647005c40e59c96c7dc8e67b8` has the Lua-first Platform but lacks both item-display hooks. The full patch was mechanically applied to that reference in isolation: six implementation/test paths match the candidate exactly and its separate SDL3 type-declaration changes are retained. That check does not claim a rebuilt or installed 06db game. Later CPH commits require their own application, build, and runtime checks.

## Applying and checking

Use a separate checkout of the selected baseline, with this directory available as `engine-patches`. For example, from the CPH source root with `engine-patches` beside that root:

```sh
git apply --check ../engine-patches/cph-item-footnotes-hooks-a43a8f2-to-candidate.patch
git apply ../engine-patches/cph-item-footnotes-hooks-a43a8f2-to-candidate.patch
cmake -S . -B build -DCATA_ENABLE_LUA_PLATFORM=ON -DLOCALIZE=ON -DTILES=ON
cmake --build build -j2
build/tests/cata_test-tiles '[lua][platform][hooks]'
```

These are generalized reproduction commands, not a claim that this packaging task performed a fresh engine build. Use the baseline's documented toolchain and dependencies. The native regression tests create their own temporary MOD fixture; they do not replace loading the exact distributed MOD assets. Actual release-asset integration results belong to the MOD release's validation manifest.

## Why a JSON-only replacement is not equivalent

The native item loader treats `description` as a complete translation value. It does not expose an item-wide JSON append field or an inline `{zh, en}` language map. Cosmetic-variant `append` appends that variant's fragment to the base description; turning it into a universal footnote would change variant selection and would miss instance-generated/snippet descriptions. Runtime overmap/blueprint proxy types are generated after the static item definitions. ASCII JSON registers pictures, while `ascii_picture` chooses an item or variant picture; registration alone does not supply a missing-art fallback. Replacing descriptions or system locale catalogs would break the requested preservation and language behavior. This MOD therefore declares a native-hook dependency rather than offering a misleading JSON-only alternative.

Source references: `src/item_factory.cpp` (item and runtime-proxy loading), `src/translation.cpp` (translation deserialization), `src/item.cpp` (variant descriptions), `src/item_info.cpp` (resolved display and art priority), and `doc/JSON/ITEM.md` (variant append semantics).

## Delivery scope

`source-hashes/manifest.json` records actual patch checks, exit codes, all baseline and target hashes, and preservation of the independent 06db declarations. Both a43 and 32a2 patch applications passed exact-source hash comparison. This package contains no Nix-store-dependent executable, no game data, no fonts, no vendored libraries, and no personal paths. It neither updates an installed game nor claims GUI, old-save, all-platform, or complete-universe content acceptance. The native `null` sentinel does not reach normal item information display; this patch does not change that boundary or gameplay.

The owner selected [CC BY-SA 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/) for these contributions. See `LICENSE.txt` and `NOTICE.md` for attribution to oncehere and CPH/Cataclysm contributors and the AI-assistance disclosure.
