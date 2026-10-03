# SHIP-02 · Protocol Pin（判定规则的版本锚）

> **作用**：证明 **Stable 晋升是按"预先写死的判定规则"执行的**，而不是 FAIL 之后调整过协议。
> **纪律**：本文件不改任何判定内容；它只**锚定**协议与模板的内容哈希。

---

## 1. Pin 记录

```
protocol_path      = docs/release-ship-02/protocol.md
protocol_sha256    = f102ff3cb6e9d05e934b81cf96c8ebcc771878e1544cfd603551081ddff57ab6
template_path      = docs/release-ship-02/record-template.md
template_sha256    = 38b664cff3e1ae982a2c4dcc0c0ec2697c6560dd1ae913c48bf1c7b47a45ea8a

protocol_commit    = 27aad93（本 pin 所锚定的协议内容所在 commit）
pinned_at          = 2026-10-03
runtime_base_tag   = v0.4.0-rc.2
runtime_base_commit= 7c0c9bd
```

**说明（无循环引用）**

```
① 内容哈希在 commit A（27aad93）提交前计算，且因仓库已 pin 行尾（.gitattributes: * -text），
   磁盘字节 == 入库字节 ⇒ 该 sha256 与 commit A 中的内容一致、可独立复核。
② 本 pin 文件在 commit B 中写入，故 pin 文件自身不参与上述哈希。
```

**独立复核命令**

```bash
git show 27aad93:docs/release-ship-02/protocol.md         | sha256sum
git show 27aad93:docs/release-ship-02/record-template.md  | sha256sum
# 期望分别等于上面的 protocol_sha256 / template_sha256
```

---

## 2. 规则

```
① 执行 SHIP-02 时，判定规则以本文件记录的 protocol_sha256 为准。
② 若协议在该 hash 之后被修改：
     - 必须在【本文件】新增一条 supersede 记录（含新 hash、原因、日期）；
     - 未登记而使用新版协议做出的 Stable 晋升 ⇒ 无效。
③ 协议本身不得因某组 FAIL 而被放宽；FAIL 走修复流程（新 commit → rc.3）。
```

---

## 3. Supersede 记录

（当前无。如发生协议修改，在此追加，格式：`新 hash / 原因 / 日期 / 谁批准`。）
