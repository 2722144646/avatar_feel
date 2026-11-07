# avatar_feel

**让 AI 把自己对语气和语境的理解，变成一张会动的脸。**

这是一个独立、可复用的情绪能力库：调用方（通常是主模型/LLM）用加权标签描述当下心情，本库把它融合成一个连续状态，再合成到**眉眼、眼神、嘴角、脸颊、头部**这五个面向上，输出一组目标值。它不绑定任何渲染器，也不依赖额外模型。

- 作者：2722144646
- 首次提交：2026-11-06
- 许可：AGPL-3.0；商业闭源使用需另行购买授权（见 [COMMERCIAL.md](COMMERCIAL.md)）

---

## 它解决什么

关键词表能识别“开心”，但识别不了“我才不生气”；固定预设能演“难过”，但演不了“有点难过但还在笑”。这套能力换了个思路：

> **让真正读过这段对话的模型，自己写下它现在是什么心情；库只负责相信这份自述、把它融合、翻译成五官。**

没有额外的情绪分类模型，没有优先级阶梯，没有“某种来源说了算”。

---

## 能力对照

| 要求 | 本库怎么做到 |
|---|---|
| **理解** | 判断来自调用方（读完整上下文的模型）。本库不做字面匹配，不猜；它只接收结构化自述并保持其语义。 |
| **自由** | `labels` 是权重字典：`{happy: 0.6, tired: 0.4}`；允许混合、低置信度、`neutral`、空。`fusion` 不做排序、不做硬优先级。 |
| **真实** | 证据权重 = 置信度 × 来源可靠性 × 新鲜度；证据会过期，状态有保持与衰减；同一句话里的变化可以跟着句子走。 |
| **五官配合** | 同一个标签混合结果，同时生成眉、眼、嘴、脸颊与头部偏置（composer.py），不是单参数独立拉扯。 |
| **不硬压** | 唯一允许硬覆盖的来源是 `manual`（用户指令），且 6 秒后过期；其余来源都只是加权票，冲突保留为混合状态。 |

---

## 架构

```text
调用方（LLM 工具调用 / HTTP / 本地脚本）
        │  FeelRequest { labels, intensity, confidence, note }
        ▼
   AffectFusion          多来源加权，无优先级；manual 唯一硬覆盖
        │  AffectState { labels, intensity, confidence, valence, arousal }
        ▼
   Expression Composer   标签 -> smile / eye / brow / angry / inner_brow / gaze / head
        │  face targets, head targets
        ▼
   你的适配器（VTube Studio / Live2D / 3D 骨骼 / 别的什么）
```

本库**只输出目标值**，不写任何渲染器。这是故意的：核心能力要能独立于平台存在。

---

## 快速开始

```python
from avatar_feel import FeelEngine, FeelRequest

engine = FeelEngine()  # 可传 FusionSettings / AffectLog

result = engine.feel(
    FeelRequest.from_message(
        {"labels": {"happy": 0.6, "tired": 0.4}, "intensity": 0.8, "confidence": 0.9}
    )
)

result.state.labels      # {"happy": 0.6, "tired": 0.4}
result.state.valence     # 0.33（加权推导，不要求调用方填）
result.face["smile"]     # 0.81...
result.head["pitch"]     # -0.4...
```

多来源（可选）：任何来源都可以投票，冲突不会被抹掉。

```python
from avatar_feel import AffectEvidence

engine.add(AffectEvidence(source="keyword", labels={"sad": 1.0}, intensity=0.5, confidence=0.5))
```

来源可靠性（可在 `FusionSettings` 覆盖）：

```text
tool 1.0（AI 自述，权重最高，必须以它为主）
tag 0.85 / context 0.75 / classifier 0.7 / manual 0.5 / keyword 0.45 / ndi 0.0（只修正，不投票）
```

`manual` 是用户显式指令，但仍只是 0.5 权重的普通票：**没有任何来源可以硬覆盖**，
用户命令也参与混合。这是为了“自由”——强制表达本身就是一种不真实。

---

## 目录

```text
src/avatar_feel/
  schema.py      AffectEvidence / AffectState，标签归一化与 valence/arousal 推导
  presets.py     标签锚点与中文别名
  anchors.py     五官目标词汇表（同 rig 校准得到的具体数值）
  composer.py    多标签 -> 五官目标（含中性基线与强度插值）
  fusion.py      多来源加权融合、证据过期、manual 硬覆盖、防抖
  log.py         JSONL 证据/状态日志（可回放、可审计）
  protocol.py    FeelRequest / FeelResult，协议无关校验
  engine.py      FeelEngine：一次叫用的完整链路
tests/           29 项单元测试
docs/design.md   设计思路与取舍
docs/timeline.md 开发时间线与来源
evidence/        著作权证据包（哈希清单、来源记录）
```

---

## 许可

本库以 **GNU AGPL-3.0** 发布。它允许商业使用，但**如果以网络服务形式提供**，AGPL 要求你向使用者提供对应源代码。

如果你希望**闭源商用**（不承担 AGPL 的强制开源义务），需要另行购买商业授权，详见 [COMMERCIAL.md](COMMERCIAL.md)。

商业授权不会改变本库对非商业/开源使用者的授权条件。
