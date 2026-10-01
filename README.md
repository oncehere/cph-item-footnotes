# 末日脚注 / Apocalypse Footnotes

为 CPH 物品原有描述追加一段俏皮、带黑色幽默的笑话、冷知识或短诗。游戏语言为中文时显示中文，其他语言显示英文；原生描述与字符画保留，缺图物品可使用补充 ASCII 图。

**[下载 v0.1.0](https://github.com/oncehere/cph-item-footnotes/releases/tag/v0.1.0)** · [CPH 引擎](https://github.com/oncehere/Cataclysm-Phantom-Hope)

## 安装

1. 使用已提供 `on_item_description_append` 和 `on_item_ascii_art_fallback` 的 CPH 引擎，并启用 Lua Platform。
2. 下载 `cph_item_footnotes-v0.1.0.zip`，解压后将整个 `cph_item_footnotes` 文件夹放入游戏 `data/mods/`。
3. 创建世界时保留核心模组 `ccb`，加入“末日脚注 / Apocalypse Footnotes”。

安装包只包含 MOD。缺少这两个接口的 CPH 版本需要先使用 Release 附带的引擎补丁；完整补丁以 CPH `a43a8f2f270994dad716ab067c48aad7c2eeaee3` 为基线，增量补丁以 `32a2a03425aed2de13d1aa38c698f843d29f3ba2` 为基线。应用、版本边界和编译说明见 [引擎兼容说明](engine-patches/README.md)。

## 当前收录

| 内容 | 数量 |
|---|---:|
| 静态基础物品脚注 | 10,332 |
| 运行时 UI 代理脚注 | 4 |
| 专属变体脚注 | 2 |
| 双语脚注合计 | 10,338 |
| 补充字符画 | 1 |

有专属变体脚注时优先使用，否则回退到基础脚注；未收录目标保留游戏原有内容。`null` 等原生空物品哨兵继续遵守引擎显示规则，不强行显示脚注。

本版按作者接受现有文字的整合策略发行，待审稿件保持原状态，不宣称全部文字完成独立审核或所有冷知识可靠。没有宣称可靠的条目不强制外部来源。长期基础目标为 35,805 项；当前尚未覆盖全部运行时目标与必要变体。

## 验证与源码

真实引擎验收检查原生物品信息、中文/英文动态切换、专属变体与基础回退、原生字符画优先、MOD 开关以及 RNG/序列化一致性。最终结果和边界见 [验证记录](VALIDATION.md)。

`mod/cph_item_footnotes/` 是可安装 MOD 源码，`engine-patches/` 是对应本体接口修改。`exports/` 的 JSON 仅供工具读取，不能放入游戏 MOD 目录。

使用 Python 3 校验公开文件和安装包：

```sh
python3 scripts/verify_release.py
```

`manifest.json` 是冻结构建清单，记录来源、收录键和逐文件 SHA-256；运行验收与发布状态单独记录。

## English

Apocalypse Footnotes appends bilingual dark humor to existing CPH item descriptions. Chinese locales use Chinese; every other locale uses English. Native descriptions and artwork remain intact.

Download the MOD ZIP from Releases, extract the complete `cph_item_footnotes` directory into `data/mods/`, and enable it alongside core mod `ccb` when creating a world. The engine must provide Lua Platform and both item hooks listed above. If your engine lacks them, see the supplied engine patches and their exact revision requirements.

Version 0.1.0 contains 10,338 bilingual text entries and one ASCII picture. This is an integration release with partial runtime/variant coverage; it does not certify all editorial content or trivia. Python 3 can verify the frozen package using the command above.

## 许可与署名

采用与 CPH 一致的 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。维护者：oncehere。游戏与引擎衍生部分署名 CPH / Cataclysm contributors；文字由 Gemini 辅助创作，集成和验证由 Codex 辅助完成。详见 [LICENSE.txt](LICENSE.txt) 与 [NOTICE.md](NOTICE.md)。
