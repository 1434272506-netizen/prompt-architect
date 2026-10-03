# SHIP-02 · Protocol Pin（判定规则的版本锚）

> **作用**：证明 **Stable 晋升是按"预先写死的判定规则"执行的**，而不是 FAIL 之后调整过协议。
> **机器可读权威**：[protocol-pin.json](protocol-pin.json)（preflight 读它）｜**本文件为人读记录**。
> **纪律**：pin 只锚定**内容哈希**；协议若修改，**必须**在此登记 supersede，未登记即使用新版协议 ⇒ 晋升无效。

---

## 1. 当前有效 pin（**pin-2**）

```
protocol_path      = docs/release-ship-02/protocol.md
protocol_sha256    = 51bbf0fae930b08889e39979ac569d41cdbe6d0e430f98895c3fc9e36ee29268
template_path      = docs/release-ship-02/record-template.md
template_sha256    = 650ff796e9b2583abcf01aa642513233f38a8b8fc8ee184b6f0dad70ca1cf67b

protocol_commit    = （见 §3 pin-2 行）
pin_commit         = （见 §3 pin-2 行）
pinned_at          = 2026-10-03
runtime_base_tag   = v0.4.0-rc.2
runtime_base_commit= 7c0c9bd（7c0c9bd1db02c5baf6b3268a3c43827b7370c609）
```

**执行 SHIP-02 前必须先跑 preflight**

```bash
python .gh-search/preflight_ship02.py      # 不一致 ⇒ ABORT，不得开始 A/B/C
```

---

## 2. 规则

```
① 执行 SHIP-02 时，判定规则以【当前有效 pin 的内容哈希】为准（protocol-pin.json → current_pin）。
② 协议在该 hash 之后被修改：
     - 必须在 protocol-pin.json 与 本文件的 §3 追加 supersede 记录（新 hash / 原因 / 日期）；
     - 未登记而使用新版协议做出的 Stable 晋升 ⇒ 无效。
③ 协议本身不得因某组 FAIL 而被放宽；FAIL 走修复流程（新 commit → rc.3）。
④ 被测物锚（runtime_base_tag / commit）若被移动 ⇒ preflight ABORT，运行无效。
```

---

## 3. Pin 历史（append-only）

| pin | protocol_sha256 | template_sha256 | protocol_commit | pin_commit | 状态 | 原因 / 日期 |
|---|---|---|---|---|---|---|
| **pin-1** | `f102ff3c…57ab6` | `38b664cf…45ea8a` | `27aad93` | `2465271` | superseded | 首次 pin（判定规则原文）／2026-10-03 |
| **pin-2** | `51bbf0fa…e29268` | `650ff796…1cf67b` | _见下行更新_ | _见下行更新_ | **CURRENT** | **新增执行结构（被测物/控制物理分离）＋ protocol preflight 要求；判定规则未变**／2026-10-03 |

**supersede 说明（pin-1 → pin-2）**

```
变更内容：protocol.md §0.3（两 worktree 分离）＋ §0.4（preflight，ABORT 规则）
          record-template.md（四点分离的 evidence 顶部）
未变更：  §1 Runtime A / §2 Runtime B / §3 Runtime C 的判定条件
          §5 判定与后续（A∧B∧C ⇒ v0.4.0；任一 FAIL ⇒ rc.3）
性质：    执行层细节补充，不是判定规则放宽
```

**独立复核（无循环引用）**

```bash
# 内容哈希在提交前计算；仓库已 pin 行尾（.gitattributes: * -text）⇒ 磁盘字节 == 入库字节
sha256sum docs/release-ship-02/protocol.md
sha256sum docs/release-ship-02/record-template.md
git rev-parse v0.4.0-rc.2        # 期望 7c0c9bd1db02c5baf6b3268a3c43827b7370c609
```
