# 著作权证据包

本文件说明本仓库如何自证“这些东西是谁在什么时候写的”，以及别人怎么复核。

## 1. 证据由什么构成

| 证据 | 位置 | 说明 |
|---|---|---|
| Git 提交历史 | `.git` | 每次提交带作者、邮箱、时间戳（含时区）；Git 的提交哈希与父子链天然防篡改 |
| 文件哈希清单 | `evidence/manifest.sha256` | 对仓库内每个源文件计算 SHA-256；任何改动都会对不上 |
| 来源记录 | `evidence/provenance.json` | 作品与原始开发项目、原始提交的对应关系（机器可读） |
| 开发时间线 | `docs/timeline.md` | 按日期记录每个设计决策和对应提交 |
| 设计文档 | `docs/design.md` | 记录“思路”：为什么这样分层、为什么不用优先级 |
| 版权与许可声明 | `COPYRIGHT.md` / `NOTICE` / 各源文件头 | 明确权利人与许可条件 |

## 2. 怎么复核

```bash
# 1) 文件完整性：逐行核对哈希
sha256sum -c evidence/manifest.sha256

# 2) 作者与时间：每个提交是谁、何时、改了什么
git log --reverse --format="%H  %an  %ae  %ad  %s" --date=iso

# 3) 某个文件的历史
git log --follow -- src/avatar_feel/fusion.py

# 4) 来源对应关系
cat evidence/provenance.json
```

Windows 下 `sha256sum -c` 可用 Git Bash 或 `Get-FileHash` 逐个比对。

## 3. 时间线可交叉验证

`docs/timeline.md` 里记录的原始提交哈希，对应另一个本地仓库 `dsh-vts-avatar` 的真实提交。两份仓库的提交时间、作者、内容片段可以互相对照——独立开发痕迹比单一仓库更可信。

## 4. 更强的证据（可选，未包含）

如果需要对抗更极端的争抢场景，可以在此之上再做：

- **可信时间戳**：用 OpenTimestamps 把 `evidence/manifest.sha256` 锚定到比特币区块（免费）；
- **第三方存证**：公证或存证平台（有成本）；
- **软件著作权登记**：向版权局提交源代码与文档（官方登记证书）。

本仓库提供的是**技术性证据整理**，不构成法律意见；正式维权时请咨询律师。

## 5. 维护规则

- 每次发布新版本，重新生成 `evidence/manifest.sha256`；
- 不要在历史提交上 amend/rebase 已公开的提交（会破坏时间证据）；
- 设计与需求变更写进 `docs/timeline.md`，一条一记。
