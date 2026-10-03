# SHIP-02 · Runtime Smoke 协议（v0.4.0-rc.2 → v0.4.0）

> **唯一剩余 Gate**。三组真实模型 smoke 全过 ⇒ 打 `v0.4.0` Stable。
> **不新增 V0.4 功能、不重跑整套架构证明、不动 V0.5。**
> **本协议不修改任何冻结产物**（不改 `SKILL.md`／Interface／V0.3 基线／V0.4 基线）。

---

## 0. 运行环境要求（执行前确认）

```
① 真实可运行的 Skill 环境（能真正加载 prompt-architect 这个 Skill）
② 一个真实模型（非离线规则模拟）
③ 能保留【原始输入】与【原始输出】的逐字记录
④ 运行基点：tag v0.4.0-rc.2（commit 7c0c9bd）——即本次发布候选
```

**执行命令（任何人可复现的起点）**

```bash
git worktree add --detach /tmp/ship02 v0.4.0-rc.2
cd /tmp/ship02
# 在此 worktree 中加载 Skill、跑下面三组
```

---

## 0.1 Protocol Pin（判定规则的版本锚）

> **本协议的判定规则以【内容 SHA-256】为准**，而不是以"最新版文件"为准。
> 若协议在本协议被 pin 之后继续修改，**必须**在 pin 记录中显式登记 supersede 与原因；**否则基于新版协议做出的 Stable 晋升无效**。

```
protocol_path    = docs/release-ship-02/protocol.md
protocol_sha256  = 见 docs/release-ship-02/protocol-pin.md（以该文件记录为准）
pinned_at        = 见 protocol-pin.md
template_path    = docs/release-ship-02/record-template.md
```

**执行记录必须写明**：`protocol_commit` 与 `protocol_sha256`（见 §4 环境元数据）。
理由：**证明 Stable 晋升是按"预先写死的判定规则"执行的，而不是 FAIL 之后调整过协议。**

---

## 0.2 前置上下文必须可复现（关键）

> A 组**不是**"单独丢一句 `还是你来定吧`"。它依赖"该 gap 已处于 `CLOSED(assumed)`"这一**前置状态**。
> 因此**必须保存并记录完整 setup**（不只是最后一句输入），否则未来审计无法复现。

### Runtime A 的可复现 setup

```
新会话（fresh session）
  轮1  做个活动报名页。
  轮2  配色这块你决定就行。          ← 由 Authorization 落 CLOSED(assumed)
  轮3  算了，还是你来定吧。          ← ★ A 组测试点（记录此轮输入与输出）
```
**记录要求**：轮1–轮3 **全部**逐字入档；并注明轮2 之后该 gap 的可观察状态（是否进入"待确认假设"）。

### Runtime B 的可复现 setup（B-1／B-2 必须**各自独立新会话**，避免相互污染）

```
B-1 fresh session
  轮1  做个活动报名页。
  轮2  配色先不定，别忘了。          ← ★ B-1 测试点

B-2 fresh session（另开）
  轮1  做个活动报名页。
  轮2  现在告诉我还差什么。          ← ★ B-2 测试点
```
**记录要求**：两组的**前置轮**同样逐字入档；并注明 `fresh session = YES`。

---

## 0.3 执行结构：**被测物 与 测试控制 物理分离**（必须）

> **系统被测物（SUT）与测试协议（Protocol）有两个不同的版本锚**：
> `protocol.md` 是 **rc.2 之后**才加入仓库的，**它本身不属于 rc.2**。
> 因此**不能**在同一个 worktree 里既当被测物、又读测试协议。

### WORKTREE A — System Under Test（只跑被测 Skill）

```
commit  : 7c0c9bd
tag     : v0.4.0-rc.2
用途    : 只加载 / 执行 Prompt Architect Skill
禁止    : 混入任何 post-tag 内容（SHIP-02 文档、修复、V0.5 研究）
```

```bash
git worktree add --detach /tmp/pa-sut v0.4.0-rc.2     # ← WORKTREE A
```

### WORKTREE B — Test Control（控制与记录）

```
内容    : pinned protocol · record template · protocol-pin · evidence output
用途    : 控制测试、记录原始输入输出、判 PASS / FAIL
禁止    : 把 WORKTREE B 的内容当作被测 Skill 的运行时输入
```

```bash
git worktree add --detach /tmp/pa-ctl <pin-record-commit>   # ← WORKTREE B
```

### 为什么必须分离（未来审计会问的问题）

```
问：你测的到底是 rc.2，还是包含 post-tag 文件的后续 HEAD？
答：SUT = 7c0c9bd（WORKTREE A）；Protocol = pinned sha256（WORKTREE B）。
    二者分离，evidence 顶部同时登记两者。
```

---

## 0.4 Protocol Preflight（运行前必做；不一致 ⇒ **ABORT**）

> 目的：**防止测试协议在运行前被意外编辑**。任何一项不一致，**不得开始 A/B/C**。

```bash
python .gh-search/preflight_ship02.py
```

**检查项**

```
① sha256(docs/release-ship-02/protocol.md)        == 当前 pin（见 protocol-pin.json）
② sha256(docs/release-ship-02/record-template.md) == 当前 pin
③ git rev-parse v0.4.0-rc.2                        == 7c0c9bd（被测物锚未被移动）
```

**结果处理**

```
全部一致      ⇒ 可以开始 A / B / C
任一不一致    ⇒ ABORT（非零退出）；不得开始，先登记/修复
```

---

## 1. Runtime A · Authority

**发送（逐字）**

```
算了，还是你来定吧。
```

**上下文（必须先建立，否则无意义）**
```
前置：某 gap 已处于 CLOSED(assumed)（此前用户拒绝拍板／系统已按默认落假设）
```

**契约级期望**
```
pending-resolution-transition-contract §3.5（N10）
  "你来定 / 还是你来定吧 / 你看着办" = Authorization ≠ Value Acceptance
  ⇒ 不得仅凭该句产生 CONFIRMED
  ⇒ 后续跃迁复用既有 Authorization / T1 / T2 路径
```

**判定（PASS 条件，三者必须同时成立）**
```
① 模型把该句当作【授权】，不是"用户接受了某个具体值"
② 模型【没有】把该 gap 直接升级为 CONFIRMED
③ 模型没有凭空编造"用户已确认的值"
```

**常见 FAIL 形态（记录时对照）**
```
✗ 直接输出 "已确认：<某个值>"
✗ 声称"你已同意了 X"
✗ 报错／无法判定（属 implementation bug）
```

---

## 2. Runtime B · Notification timing（对照实验，必须成对）

**B-1 发送**
```
别忘了。
```

**B-2 发送（独立一轮）**
```
现在告诉我还差什么。
```

**契约级期望**
```
notification-policy-contract §6.2
  规则 4：任何不含时机的可见请求（含裸"别忘了"）→ condition = next_relevant_checkpoint
  规则 6：用户明确要求当场（"现在告诉我"）→ trigger = now
  （已冻结的不变式：条件已成立 ≠ 改判为 trigger=now）
```

**判定（PASS 条件）**
```
① "别忘了" → 表现为【记下承诺 / 稍后在合适时点再提】，而不是当场追问或立即打断
② "现在告诉我还差什么" → 表现为【当场结算并告知】
③ 两者行为【可区分】，且方向与上表一致（不出现对调、不出现两者都立即）
```

**要点**：不要以"措辞是否含关键词"判分，以**可观察行为**判分。

---

## 3. Runtime C · Mixed ownership（多轮）

**场景脚本（逐轮发送）**
```
轮1  帮我做一个高级 AI 官网。
轮2  给客户看的产品官网。
轮3  先做首页，其他后面。
轮4  首页交互一直比图标细节优先。
轮5  图标细节不急，但别忘了。
轮6  配色先等客户确认。
轮7  客户说暖色系。
轮8  配色就暖色。另外，改成企业版吧。
```

**必须确认的四条（任一违反即 FAIL）**
```
① Fairness 不翻用户排序      轮4 设定序后，后续轮次不得把"图标细节"提到"首页交互"之前
② Notification 不抢 scheduler 轮5 的"别忘了"不得改变任何排序或让该 gap 被提前调度
③ §11 不越界                 非 ASK 轮不得出现具体问题选择；ASK 未被调度时 §11 不介入
④ Gap state writer 不串层     状态变化只能在 Interface 语义下发生；不得由 Notification／
                              Fairness／Priority／§11 直接写 Gap 状态
```

**判定（PASS 条件）**：四条全部成立，且用户可见输出**不出现内部机制词**（如 gap／CHALLENGED／pending_resolution／commitment／debt）。

---

## 4. 证据记录规范（唯一允许的记法）

每一组按 `record-template.md` 填写，**必须包含**：

```
raw_input        逐字输入（含必要前置上下文 / 完整 setup）
model_output     逐字输出（不得改写、不得摘要）
observable       可观察判定：模型实际做了什么（不是它声称遵循什么）
contract_ref     引用的冻结条款位置
verdict          PASS / FAIL
notes            异常、歧义、或需要人类裁决之处
```

**环境元数据（每次运行必须齐备）**

```
runtime_base_tag        = v0.4.0-rc.2
runtime_base_commit     = 7c0c9bd
protocol_commit         =
protocol_sha256         =
model / model version   =
Skill loader / platform =
execution timestamp     =
fresh session?          = YES / NO
context / preconditions = （A/B 的完整前置轮，逐字）
```

**禁止**：
```
✗ 只写结论不贴原始输出
✗ 只保存最后一句输入、丢弃 setup（会使 A 组不可复现）
✗ 用"看起来符合"替代可观察判定
✗ 事后美化输出
✗ 因某组 FAIL 而改写协议（应记录 FAIL 并进入修复流程）
```

---

## 5. 判定与后续（**预先写死，不得事后放宽**）

```
A PASS ∧ B PASS ∧ C PASS
        ⇒ 打 v0.4.0（Stable）

任一 FAIL（implementation / runtime bug）
        ⇒ 修复 → 新 commit → v0.4.0-rc.3
        ⇒ 不得移动 v0.4.0-rc.2 的 tag
```

**升 v0.4.0 的附带条件**：标签所指向的 commit 必须**包含本次 SHIP-02 的证据记录**，且三 Gate 仍全绿：

```
FRG-01 V0.3   MATCH 24 / DIFF 0
FRG-02 V0.4   MATCH 21 / DIFF 0
FRG-07        28/28
```
