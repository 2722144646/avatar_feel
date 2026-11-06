# 开发时间线

本库是 2026-11-06 从私有项目 `dsh-vts-avatar` 的情绪子系统中抽取出来的。下面两个时间线可以互相对照：本仓库的提交，与原始项目的提交哈希。

## 2026-11-06 · 原始项目 `dsh-vts-avatar`

| 时间（+08:00） | 提交 | 内容 |
|---|---|---|
| 13:40 | `30e56e1` | 情绪重构基线：备份 + tag `v0.5.0-emotion-baseline` |
| 13:46 | `0fddc58` | 增加 `[emotion] mode` 开关（legacy 默认） |
| 13:5x | `dcd6ffb` | affect 数据模型：AffectEvidence / AffectState / 锚点 / JSONL 日志 |
| 19:xx | `abe3501` | Expression Composer：多标签 → 五官目标；mixer 按模式分流 |
| 20:4x | `2e9f8bd` | `vts_avatar_feel` 工具 + 证据日志接线 |
| 20:5x | `36b0106` | 情绪保持 2 秒后衰减（修复“一直在笑”） |
| 21:0x | `5af86bf` | 多来源加权融合 Fusion（无优先级、manual 唯一硬覆盖） |
| 21:2x | `5ffcf50` | 记录两个缺口：系统提示引导、跨轮状态回灌 |
| 21:0x | `efb60e4` | 待机风格与表情强度参数（有存在感/活泼各半；自然 70% / 夸张 30%） |

## 2026-11-06 · 抽取为独立库 `avatar_feel`

- 抽取核心：`schema` / `presets` / `anchors` / `composer` / `fusion` / `log`，
  新增 `protocol`（协议无关校验）与 `engine`（一次调用的完整链路）。
- 去掉平台相关：VTube Studio 参数注入、DSH 插件工具、语音时钟，全部留在原项目。
- 新增文档：本文件、`docs/design.md`、`COPYRIGHT.md`、`EVIDENCE.md`、`COMMERCIAL.md`。
- 测试：29 项（schema 9 / composer 8 / fusion 7 / engine 5）。

## 为什么保留这两个时间线

- 原始项目的提交是**独立开发痕迹**：时间、作者、连续迭代，能说明这不是事后拼出来的；
- 本仓库的提交是**公开发布痕迹**：从哪一刻起对外可用；
- 两者互相印证，比单一仓库更难伪造。
