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
| 状态 | **Pending**：已进入日历，等待聚合进比特币区块（通常几小时内） |

## 它证明了什么

`manifest.sha256` 在提交给日历时就已经存在。任何人在之后修改仓库文件，都无法让这份清单的哈希与
未来某个比特币区块的时间戳对上——因为 Merkle 路径与区块头绑定。

## 怎么把它变成完整证明

等几个小时，让日历完成聚合，然后在仓库根目录执行：

```powershell
.venv\Scripts\ots.exe upgrade evidence\manifest.sha256.ots
```

看到 `Success! Bitcoin block <高度> attests existence as of <UTC 时间>` 就说明完整证明已写入 `.ots` 文件。
之后提交一次即可。

> 本机 `.venv` 里的 `python-bitcoinlib` 有一个 Windows 兼容补丁：`bitcoin/core/key.py` 在找不到
> OpenSSL DLL 时用 `unittest.mock.MagicMock()` 占位，避免 `ctypes` 崩溃。只影响本地工具，不影响本库。

## 怎么验证

```powershell
# 查看证明内容（不需要联网，也不需要比特币节点）
.venv\Scripts\ots.exe info evidence\manifest.sha256.ots

# 完整验证（升级完成后）
.venv\Scripts\ots.exe verify evidence\manifest.sha256.ots
# 或者用公开的比特币区块浏览器 API（各客户端参数不同，见 ots verify --help）
```

第三方也能验证：`.ots` 文件本身包含到区块的 Merkle 路径，用任意 OTS 实现都能独立校验，不需要信任本仓库。

## 注意

- **不要**在升级完成前重新生成 `manifest.sha256`——那会改变被存证的内容，旧 `.ots` 就对不上了。
- 之后每次发版想再存证，重新生成清单并 `ots stamp` 一次，形成时间链。
- 本文件（`evidence/OTS.md`）不在 `c6e428a` 的清单里，属于存证记录本身，不影响验证。
