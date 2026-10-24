# Engine compatibility

Requires Lua Platform, core mod `ccb`, `on_item_description_append`, and `on_item_ascii_art_fallback`. These are CPH native display capabilities. A build that already exposes both hooks needs no additional footnotes-specific engine patch. Lua Platform or the core ID `ccb` alone does not establish compatibility with arbitrary CCB or CDDA builds.

CPH owns preservation of the resolved native description and priority of native artwork. This MOD owns bilingual text, language fallback, item/variant selection and missing-art mappings. The hook payload supplies `item_id`, optional `variant_id`, and current `language`.

Historical v0.1.0 validation used engine base `32a2a03425aed2de13d1aa38c698f843d29f3ba2` plus the separately supplied hook patch. The release patches target their recorded baselines; they are not patches for arbitrary later revisions. The MOD ZIP does not contain the engine. Runtime acceptance is recorded separately against exact package and engine bytes.

本 MOD 依赖启用 Lua Platform 的 CPH 通用展示接口。已提供两个接口的引擎可直接加载；内容和语言/补图规则由 MOD 维护。历史补丁与 v0.1.0 验收保留原有版本边界，不代表所有 CPH、CCB 或 CDDA 版本均兼容。
