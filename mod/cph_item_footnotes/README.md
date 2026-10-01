# 末日脚注 / Apocalypse Footnotes 0.1.0

为原有物品描述追加中英双语脚注；中文游戏语言显示中文，其他语言显示英文。原生字符画优先，适用物品可使用补充 ASCII 图。

## 安装

1. 使用提供 `on_item_description_append` 和 `on_item_ascii_art_fallback` 的 CPH 引擎，并启用 Lua Platform 与基础模组 `ccb`。
2. 解压后，将完整 `cph_item_footnotes` 文件夹放入游戏的 `data/mods/`。
3. 创建世界时，在模组选项中启用“末日脚注 / Apocalypse Footnotes”。

本压缩包包含 MOD，不包含引擎。没有上述接口的 CPH 版本无法加载此 MOD；引擎兼容说明见 `COMPATIBILITY.md`。

本版包含 10332 个静态基础物品、4 个运行时基础物品、2 个专属变体脚注及 1 幅补充字符画。未覆盖的物品继续显示原生内容。
发行策略是 `integration_only_user_accepted_content`：本版以加载和显示整合为目标，未完成的文案审稿不作为发行门禁；不宣称全体物品覆盖或全部文案已批准。当前已退回的稿件、未验证的可靠性声明及技术校验失败内容会被排除。

## Installation

Use a CPH engine providing both native hooks named above, Lua Platform, and core mod `ccb`. Extract the ZIP, copy the complete `cph_item_footnotes` directory into `data/mods/`, and enable Apocalypse Footnotes when creating a world. Chinese locales select Chinese footnotes; other locales select English. Native descriptions and artwork retain priority.

This integration release contains 10338 text entries and 1 artwork entries. It does not claim complete item coverage, universal CPH compatibility, verified trivia, or completed editorial approval.

许可 / License: CC-BY-SA 3.0；署名与许可说明见 `LICENSE.txt` 和 `NOTICE.md`。
