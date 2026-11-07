# OpenTimestamps 存证记录

## 这次盖了什么

| 项 | 值 |
|---|---|
| 被存证文件 | `evidence/manifest.sha256`（25 个文件的 SHA-256 清单） |
| 该文件自身的 SHA-256 | `c42e95076da9172cb9018b17726d6a0c2c078e8ba388e1d3adc32bc043f7f826` |
| 存证时间（本地） | 2026-11-06 22:2x（Asia/Hong_Kong） |
| 对应提交 | `c6e428a`（本仓库初始提交） |
| 证明文件 | `evidence/manifest.sha256.ots` |
| 提交的日历 | opentimestamps 官方 pool（a/b.pool）、eternitywall、catallaxy（共 4 个） |
| 状态 | **已完成**：4 条比特币区块证明（block 974817 / 974819 / 974839 / 974847） |

## 它证明了什么

`manifest.sha256` 在提交给日历时就已经存在。任何人在之后修改仓库文件，都无法让这份清单的哈希与
未来某个比特币区块的时间戳对上——因为 Merkle 路径与区块头绑定。

## 完整证明（2026-11-07 完成）

`ots upgrade` 已成功执行，`.ots` 从 pending（1155 字节）升级为完整证明（5369 字节），包含 4 条独立区块证明：

```text
BitcoinBlockHeaderAttestation(974817)
BitcoinBlockHeaderAttestation(974819)
BitcoinBlockHeaderAttestation(974839)
BitcoinBlockHeaderAttestation(974847)
```

最早锚定在 block 974817。也就是说：`manifest.sha256` 的内容在 2026-11-06 提交后、
区块 974817 被打包之前，就已经存在。

验证需要能访问比特币区块链（本地节点或支持 OTS 的验证工具）：

```powershell
.venv\Scripts\ots.exe info evidence\manifest.sha256.ots     # 离线看结构
.venv\Scripts\ots.exe verify evidence\manifest.sha256.ots   # 需要比特币节点
```

第三方也能验证：`.ots` 文件本身包含到区块的 Merkle 路径，用任意 OTS 实现都能独立校验，不需要信任本仓库。

## 注意

- **不要**重新生成 `manifest.sha256` 之后继续拿这份 `.ots` 当证明——内容变了，哈希就对不上。
  想再存证就重新生成清单并 `ots stamp` 一次，旧证明保留为历史版本。
- 之后每次发版想再存证，重新生成清单并 `ots stamp` 一次，形成时间链。
- 本文件（`evidence/OTS.md`）不在 `c6e428a` 的清单里，属于存证记录本身，不影响验证。
