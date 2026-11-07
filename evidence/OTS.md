# OpenTimestamps 存证记录

本仓库所有源码与文档的哈希清单，按版本分别时间戳锚定到比特币。

## v0.1.0（已完成）

| 项 | 值 |
|---|---|
| 清单文件 | `evidence/manifest-v0.1.0.sha256` |
| 清单自身 SHA-256 | `c42e95076da9172cb9018b17726d6a0c2c078e8ba388e1d3adc32bc043f7f826` |
| 证明文件 | `evidence/manifest-v0.1.0.sha256.ots` |
| 提交 | `c6e428a`（初始提交） |
| 状态 | **完整**：4 条比特币区块证明 |
| 区块 | `974817` / `974819` / `974839` / `974847` |

## v0.2.0（pending）

| 项 | 值 |
|---|---|
| 清单文件 | `evidence/manifest.sha256`（28 个文件） |
| 证明文件 | `evidence/manifest.sha256.ots` |
| 存证时间 | 2026-11-07 09:35（Asia/Hong_Kong） |
| 状态 | **Pending**：已提交 4 个日历，等待聚合进比特币区块 |

v0.2.0 改了什么：`tool`（AI 自述）权重升到 1.0（全表最高，必须以它为主）；
`manual` 从投票权重表移出（它是用户指令，仍走硬覆盖）。其余为文档与测试。

## 等几小时后：升级 v0.2.0

```powershell
cd E:\avatar_feel
.venv\Scripts\ots.exe upgrade evidence\manifest.sha256.ots
```

成功输出 `Success! Timestamp complete` 后提交推送即可。

## 验证

```powershell
# 离线查看证明结构
.venv\Scripts\ots.exe info evidence\manifest-v0.1.0.sha256.ots
.venv\Scripts\ots.exe info evidence\manifest.sha256.ots

# 完整验证需要比特币节点
.venv\Scripts\ots.exe verify evidence\manifest-v0.1.0.sha256.ots
```

第三方验证不需要信任本仓库：`.ots` 文件自带到区块头的 Merkle 路径，任何 OTS 实现都能独立核对。

## 注意

- **每个版本单独存证**：清单变化就重新生成、重新 `ots stamp`，旧证明保留为历史。
- 不要在旧版本上 `ots upgrade`：`upgrade` 只补齐自己那份 `.ots`。
- 本机 `.venv` 里的 `python-bitcoinlib` 打过 Windows 兼容补丁（找不到 OpenSSL 时用 `MagicMock` 占位），只影响本机工具，不影响证明。
- 时间戳证明“内容在某时刻前已存在”，不证明“你是谁”；作者身份靠仓库提交、版权声明和软著登记补。
