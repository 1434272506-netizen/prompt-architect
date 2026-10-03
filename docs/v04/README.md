# Prompt Architect V0.4 · Adaptive Interview Architecture

> **Status**
> ```
> Architecture closure        complete
> Defect closure              complete   (D02–D12 CLOSED; D01 = this document)
> Evidence closure            complete
> Traceable release baseline  established
> ```
> **This README is the architecture index and release summary.**
> **Normative behavior remains owned by the underlying contracts** — this document never becomes a second contract layer.

> **Release baseline**
> ```
> baseline_id : v0.4.0-release-baseline-6     (REBASELINE; see manifest for supersedes chain)
> effective_at: see docs/v04/v0.4-release-baseline.json  (recorded value is authoritative)
> manifest    : docs/v04/v0.4-release-baseline.json   (machine source of truth)
> record      : docs/v04/v0.4-release-baseline.md     (human record)
> ```
> **Prospective-only**：本基线自所记录的生效时刻起具有冻结验证效力；**它不构成这些文件在此前历史时点始终保持相同内容的证明**。

> **Superseded**：本文件此前是 V0.4 的**早期章程**（"本轮只做破坏测试、不设计规则"阶段的导航页）。该阶段已结束；本文现为 **Final Architecture README（D01）**。历史章程内容**不再作为当前架构入口**（其原文可由 git 历史查回；本文件不静默改写历史，而是在此显式标注取代关系）。

---

## 1. System Purpose

Prompt Architect V0.4 的职责，是把**模糊、变化、不完整、会反复修改**的自然语言需求，维护为**可追踪的需求状态**，并在多轮交互中决定：

```
当前事实是什么        →  Gap / Feedback Interface
缺口是什么            →  Gap / Feedback Interface
该采取哪种已有 Action  →  V0.3 Resolution Engine
多个 Action 如何调度   →  Priority Layer
长期未处理如何保持公平  →  Scheduler Fairness
何时承担用户可见性义务  →  Notification Policy
ASK 真正执行时问什么   →  §11 Question Selection
```

它**不是**"更聪明的提问模板库"，而是一套**职责分离的交互架构**：每层只拥有一件事的写权限，其余层只能读。

---

## 2. Architecture at a Glance

```
User Feedback
      │
      ▼
Gap / Feedback Interface
      │  authoritative value · history · state transition
      ▼
V0.3 Resolution Engine
      │  chooses Action
      ▼
Priority Layer
      │  orders legal active actions
      ▼
Scheduler Fairness
      │  adjusts soft competition only
      ▼
Action Bundle
      │
      ├──────────── non-ASK ────────────► User-visible Response
      │
      └── ASK scheduled
              │
              ▼
       §11 Question Selection
              │
              ▼
       User-visible Response


Parallel visibility path:

Fairness / requirement context
      │
      ▼
Visibility Commitment
      │
      ▼
Trigger Resolution
      │
      ▼
Delivery Policy
      │
      ▼
Discharge / later evaluation
      │
      ▼
User-visible Reminder
```

> **第二条链是"理解用架构视图"，不是新状态机。**
> `Commitment → Trigger → Delivery → Discharge` 用于理解 V0.4 Notification 行为；**具体规范仍由 Notification Contract 所有**（[notification-policy-contract.md](notification-policy-contract.md)）。

---

## 3. Ownership Matrix

| Layer | 输入 | 输出 | 唯一写权限 | 明确禁止 |
|---|---|---|---|---|
| **Gap / Feedback Interface** | 用户反馈、现有 Gap/history | 合法状态跃迁、authoritative current value | **Gap state / history** | 不选 Action、不排序 |
| **V0.3 Resolution Engine** | 当前 Gap / context | `ASK / SHOW / INSPECT / TEACH / DISCOVER` | **Action type** | 不写 Gap、不负责优先级 |
| **Priority Layer** | 合法 active actions ＋ priority hint | ordered relation | **priority relation** | 不生成 Action、不改 eligibility |
| **Scheduler Fairness** | eligible actions、skip evidence、debt | fairness adjustment | **fairness ledger** | 不越 hard constraint、不翻有效用户序 |
| **Notification Policy** | visibility commitment ＋ trigger context | `notify_now / notify_later / record_only / never_notify` | **notification-local lifecycle** | 不调度、不改 Gap/Action |
| **§11 Question Selection** | 已被调度的 ASK | concrete question | **question selection** | 不决定 ASK 是否存在 |

**一句话**：**只有 Interface 改 Gap 状态；只有 V0.3 决定 Action 类型；只有 Priority 排序；只有 Fairness 调调度竞争；只有 Notification 决定可见性；只有 §11 决定问什么。**

---

## 4. Gap / Feedback Interface

（规范来源：[gap-ledger-interface.md](gap-ledger-interface.md) · [gap-ledger-proposal.md](gap-ledger-proposal.md)）

**必须记住的锚**

```
history = append-only
single authoritative current value
reset ≠ history deletion
local revision does not broaden propagation closure
effective_set = CONFIRMED ∩ valid
```

**集合成员资格**

```
askable_set includes:
  OPEN
  CHALLENGED + pending_resolution
  CLOSED(partial)

SUSPENDED:
  not askable
```

### 4.1 Clarified boundaries（D04 / D05 / D06 closure）

**Atomicity（D04 / CS-04）**

```
per-Gap complete gate-chain atomicity
≠ whole-feedback transaction
≠ whole-cluster transaction
```

"禁止部分执行"指**单个 Gap 在一次完整门链中不得部分提交**；同 cluster 其他 Gap **独立过各自门链**，不因一项 blocked 而整体回滚。

**External（D05 / CS-05）**

```
information_source ≠ external_owner
External dependency ≠ External decision ownership
```

`reason = information_source` → **保持 `OPEN`、用户仍为决策者**；仅 `reason = external_owner` → 既有 `SUSPENDED(external_owner)`。

**Delay（D06 / CS-06）**

```
OPEN + deferred
  askable_set       = YES
  normal scheduling = NO
```

`delay ≠ remove_from_askable_set`；`delay = suppress current normal scheduling`。

> 这三条是**最容易被误读的点**，也是本阶段唯一新增的 Interface 澄清。

---

## 5. Resolution & Value Semantics

（规范来源：[pending-resolution-transition-contract.md](pending-resolution-transition-contract.md)）

### 5.1 Authorization is not confirmation（N10）

```
Decision Authority  ≠  Value Acceptance
```

```
"你来定 / 还是你来定吧 / 你看着办"  → Authorization
                                    → 不确认具体值 · 不产生 CONFIRMED

"就按 X / 用线性"                   → acceptance of a concrete value
                                    → 可以满足既有的 R-2
```

> **R-2 本身没有被扩写成新规则**；N10 修复的是 **PR-17 的错误分类**（把"授权 AI 决定"误当成"用户确认了具体值"）。

### 5.2 与之同族的一条设计哲学

```
提供信息     ≠ 拥有决策权        （D05）
拥有决策权   ≠ 已确认具体值      （N10）
```

> **不要从"参与关系"推导"事实承诺"。**

### 5.3 重进入口（`CLOSED(assumed)`）

```
R-1 material          → 重开走正常处理
R-2 confirmatory      → 直接 CONFIRMED（不经 OPEN；仅当具体值被接受）
R-3 无决策意义        → 状态不变
R-4 原值已被 supersede → 走 revert / 现有状态规则
```

---

## 6. Priority Layer

（规范来源：[priority-layer-contract.md](priority-layer-contract.md)；**调度层次的规范落点在** [scheduler-fairness-contract.md](scheduler-fairness-contract.md) §1）

**调度层次（仅调度层，不是全系统优先级总表）**

```
Hard scheduling constraints
        >
explicit active user priority
        >
fairness adjustment
        >
ordinary soft scheduling preference
```

**Hard constraints 白名单（仅四类）**：当前 blocker / R6 · **R14 三闸门全过的** high-risk C · **§11.6 约束型依赖** · R4 既有顺序与容量。**不扩大**为"所有 Type C"或"所有 dependency"。

**两个常被混淆的软表达**

```
deprioritized  → 仍可处理，只是往后排（不改 gap 状态）
delay          → 当前不处理（OPEN + deferred）
```

**`current_round`**

```
= scheduler action bundle lifecycle
≠ one user message
```

**`cycle`** 只是 `current_round` 的**同义术语**，**无任何语义变化**。

---

## 7. Scheduler Fairness

（规范来源：[scheduler-fairness-contract.md](scheduler-fairness-contract.md)）

```
eligible ∧ unscheduled ∧ reason ∈ {capacity, soft competition}
        → may accumulate fairness debt
```

```
hard constraint  → no debt increment
deprioritized    → no debt increment
```

**O-5 的正式表述（由 ER-09 证明）**

```
deprioritized does not erase existing debt
deprioritized does not add new debt
```

> ⛔ 不是 `deprioritized → debt reset to 0`。

**计数不是政策**

```
debt = evidence
not an automatic promotion threshold
```

**Not defined in V0.4（N04 · deferred candidate）**

```
No numeric threshold such as
starvation_candidate ⇔ debt/count >= N
is part of the V0.4 normative contract.
```

状态：**deferred design candidate, not an open V0.4 defect.**

---

## 8. Notification Policy

（规范来源：[notification-policy-contract.md](notification-policy-contract.md)）

**四个正式出口**

```
notify_now  |  notify_later  |  record_only  |  never_notify
```

**Trigger 判定表（N08 / N09 闭合后）**

| 用户表达 | Trigger interpretation |
|---|---|
| "现在说 / 现在告诉我" | `now` |
| 明确时间窗口（"周五"） | `time_window` |
| 明确条件（"客户回复后"） | `condition` |
| external resume condition | **reuse existing condition** |
| "以后 / 之后 / 下次 / 到时候 提醒我" | `next_relevant_checkpoint` |
| **裸"别忘了 / 别漏掉 / 记着"** | `next_relevant_checkpoint` |

**B2（本层最值钱的一条）**

> **Burden-based delay only applies to system-selected timing. User-specified timing must not be silently rewritten by an internal soft mechanism.**

**条件已成立 ≠ 改触发类型**

```
checkpoint condition may already be true
  → delivery may occur immediately
  → but trigger remains condition
  → not reclassified as trigger=now
```

**一次足够**：`one active commitment → at most one proactive notification`；`discharge` 是 **Notification 层内部状态，不是 Gap 写回**。

**delay 四象限**

| delay | visibility commitment | 含义 |
|---|---|---|
| 否 | 否 | 正常处理，无通知义务 |
| 否 | 是 | 正常处理，但须满足可见承诺 |
| 是 | 否 | 延后，且**不主动催** |
| 是 | 是 | 延后处理，但 trigger 后**允许提醒一次** |

**fairness evidence ≠ notification obligation**

```
零表达的 starvation_candidate → record_only
（"长期没排上"不自动产生用户可见通知义务）
```

---

## 9. Notification vs Fairness

```
Fairness      answers: "系统调度是否长期不公平地没给它机会？"
                       → scheduling justice
                       → owned by Fairness Ledger

Notification  answers: "系统是否欠用户一次可见性的承诺？"
                       → user-visible obligation
                       → owned by visibility commitment
```

两者**都可能让某事项重新进入用户视野**，但 ownership 不同、**互不写权**：

```
Fairness → Notification : 只传证据
Notification → Fairness : 零写权
```

> **Notification is not a second Action Engine.**

---

## 10. ASK / §11 Boundary

```
V0.3 decides ASK
Scheduler decides whether ASK runs
§11 decides what ASK asks
```

顺序不能反：**§11 的 invocation condition = ASK has been scheduled**（证据见 [release-evidence-closure.md](release-evidence-closure.md) **E5-A / E5-B**）。

---

## 11. E1–E8 Invariants

```
E1  single authoritative current value
E2  only Interface changes Gap state
E3  only V0.3 decides Action type
E4  Priority only orders legal Actions
E5  §11 runs only after ASK is scheduled
E6  no internal machine terminology in user-visible response
E7  Fairness does not alter Gap/Action/effective user priority
E8  Notification does not alter scheduling/Gap/Action
```

| 状态 | 值 |
|---|---|
| Architecture definition | **CLOSED** |
| Evidence index | **repaired and verified**（[release-evidence-closure.md](release-evidence-closure.md)：E3/E5 的 4 条错引用已改，E3-A/B ＋ E5-A/B 重建） |

---

## 12. Historical / Discovery Governance

（规范来源：[historical-discovery-governance.md](historical-discovery-governance.md)）

```
Discovery  = historical candidate evidence
Contract   = current normative authority

30/30
  = historical execution / coverage
  ≠ all historical conclusions remain normative
```

**取代处理**

```
superseded result:
  preserve
  label
  link to superseding contract
  never silently rewrite
```

---

## 13. Release Evidence

**只做索引，不复制历史测试结果。**

| 证据类别 | 位置 |
|---|---|
| Behavior / migration | [interface-v3-migration-test.md](interface-v3-migration-test.md) · [interface-v3-migration-manifest.md](interface-v3-migration-manifest.md) |
| Ownership / invariants | [release-evidence-closure.md](release-evidence-closure.md)（ER-07 / ER-08 / ER-09；EV-07/08/09） |
| Multi-turn behavior | [e2e-adaptive-replay.md](e2e-adaptive-replay.md) · [full-adaptive-e2e-replay.md](full-adaptive-e2e-replay.md) |
| Historical governance | [historical-discovery-governance.md](historical-discovery-governance.md)（HG-10） |
| Defect closure | [v04-defect-ledger.md](v04-defect-ledger.md)（D02–D12） |
| Release baseline | [v0.4-release-baseline.json](v0.4-release-baseline.json) · [v0.4-release-baseline.md](v0.4-release-baseline.md) |

**最终状态**

```
D02–D12   CLOSED
K4        0
K5        0
```

> **K5 说明**：当前值来自 **N10 之后的重新分类与重确认**；V0.4.3 的早期 `K5=0` **仅作历史记录保留，不作为最终证据**。

---

## 14. Freeze & Release Governance

```
Machine source of truth : docs/v04/v0.4-release-baseline.json
Human record            : docs/v04/v0.4-release-baseline.md

File hash    : SHA-256 raw bytes    → authoritative
Section hash : per-`##` diagnostic  → localization only
               (file DIFF + section MATCH never means pass)

Verifier     : .gh-search/verify_v04_release_baseline.py   (READ-ONLY; no write flag)
Initializer  : .gh-search/generate_v04_baseline.py         (--init / --rebaseline --reason)
Drift probe  : .gh-search/probe_baseline_drift.py          (BL-08)
V0.3 baseline: docs/freeze-v0.3.md + .gh-search/freeze_v03.py   (referenced, NOT copied)
```

**退出码语义**：`0 PASS`｜`1 DRIFT（DIFF·MISSING·UNREGISTERED）`｜`2 manifest 不可读`｜`3 V0.3 校验失败`。

> 当前 baseline（`v0.4.0-release-baseline-6`）**自其 `effective_at` 起**生效，是 V0.4 首个可追溯 release baseline；**不证明此前历史内容恒定**。基线版本的唯一权威来源是 manifest 的 `baseline_id`。

---

## 15. Known Non-goals / Deferred Work

**N04 · starvation threshold**

```
V0.4 does not define a numeric starvation_candidate threshold.
No ≥1 / ≥N threshold is normative.
```
状态：**deferred design candidate, not an open V0.4 defect.**

**N07 · "user mentions it again = discharge"**

```
V0.4 does not generalize
"user mentions item again"
into an automatic universal discharge rule.
```
若 NB-06 有局部行为，**照现有合同执行**。状态：**unresolved generalization deliberately excluded from V0.4.**

**D12 residual · legacy tooling debt**

```
freeze_v03.py --write  → sentinel duplication bug still present
```
定位：**legacy tooling debt, mitigated and outside the V0.4 runtime architecture.**
护栏：

```
docs/freeze-v0.3.md is itself covered by the V0.4 baseline
  → corruption of its sentinel region becomes a V0.4 DIFF
  → detected by the read-only verifier
```

**其他非目标**：不新增数值评分／不新增 Gap state／不把 Notification 变成 Action Engine／不让 README 成为合同层。

---

## 16. Future Architecture Candidates

```
C1  Authority / Value Separation
    Decision Authority ≠ Value Commitment

C2  Notification lifecycle decomposition
    Commitment → Trigger → Delivery → Discharge
```

> These are **V0.5 candidates, not V0.4 normative extensions.** 完整清单（含未成熟观察）见 [v05-architecture-candidates.md](v05-architecture-candidates.md)。

---

## 17. Final Release Gate

README 落盘后由**独立 Gate** 判定，不手写 `RELEASE READY`：

| # | Gate | 判定方式 |
|---|---|---|
| **FRG-01** | V0.3 freeze verification | `freeze_v03.py` → MATCH 24 / DIFF 0 / UNREGISTERED 0 |
| **FRG-02** | V0.4 baseline verification | verifier → MATCH / DIFF 0 / MISSING 0 / UNREGISTERED 0（exit 0） |
| **FRG-03** | Release evidence | EV-07 / EV-08 / EV-09 PASS |
| **FRG-04** | Historical governance | HG-10 PASS |
| **FRG-05** | D02 closure linkage | EL-02 PASS |
| **FRG-06** | Defect ledger | D02–D12 CLOSED；D01 complete |
| **FRG-07** | README reverse-reference audit | 每条 README 规范主张指向下层权威来源；**不存在 README-only rule** |
| **FRG-08** | Baseline integrity after README addition | README 纳入 baseline scope → 经批准 rebaseline → 最终 verifier PASS |

---

## Appendix A · README Claim Index（FRG-07 机器可校验）

> 每条 claim 必须能落到一个**下层权威来源**；本表由 `.gh-search/verify_readme_reverse_refs.py` 逐条校验（来源文件必须存在 ＋ anchor 必须出现）。**README 不创造任何规则。**

| claim | 主张 | source | anchor |
|---|---|---|---|
| CL-01 | `effective_set = CONFIRMED ∩ valid` | docs/v04/gap-ledger-interface.md | `effective_set := CONFIRMED ∩ valid` |
| CL-02 | history 只追加、不可覆写 | docs/v04/gap-ledger-interface.md | `历史不可覆写` |
| CL-03 | reset 不删除历史 | docs/v04/gap-ledger-interface.md | `reset ≠ 删除历史` |
| CL-04 | local revision 不扩大闭包 | docs/v04/gap-ledger-interface.md | `local 不扩大闭包` |
| CL-05 | 原子性 = per-Gap 完整门链 | docs/v04/gap-ledger-interface.md | `atomicity = per-Gap transition atomicity` |
| CL-06 | `information_source ≠ external_owner` | docs/v04/gap-ledger-interface.md | `External dependency  ≠  External decision ownership` |
| CL-07 | delay 仍属 askable 但不参与调度 | docs/v04/gap-ledger-interface.md | `delay ≠ remove_from_askable_set` |
| CL-08 | N10：授权 ≠ 值接受 | docs/v04/pending-resolution-transition-contract.md | `Authority transfer is not value confirmation` |
| CL-09 | R-2 定义未被扩写 | docs/v04/pending-resolution-transition-contract.md | `R-2 confirmatory` |
| CL-10 | 调度层次四层 | docs/v04/scheduler-fairness-contract.md | `explicit active user priority` |
| CL-11 | `current_round` = action bundle 生命周期 | docs/v04/priority-layer-contract.md | `current_round :=` |
| CL-12 | `cycle` 只是同义术语 | docs/v04/scheduler-fairness-contract.md | `同义术语` |
| CL-13 | debt 累积条件 | docs/v04/scheduler-fairness-contract.md | `才累积 fairness debt` |
| CL-14 | 计数是证据不是政策 | docs/v04/scheduler-fairness-contract.md | `计数是证据，不是政策` |
| CL-15 | N04 未定义数值阈值 | docs/v04/scheduler-fairness-contract.md | `未落（HOLD · N04）` |
| CL-16 | deprioritized 不清零、不新增债 | docs/v04/release-evidence-closure.md | `deprioritized does not erase existing debt` |
| CL-17 | 四个通知出口 | docs/v04/notification-policy-contract.md | `record_only` |
| CL-18 | trigger 判定表（含规则 6） | docs/v04/notification-policy-contract.md | `6. 用户明确要求当场` |
| CL-19 | B2：burden 不改写用户指定时机 | docs/v04/notification-policy-contract.md | `burden 不得偷偷改写用户时机` |
| CL-20 | N07 未泛化（HOLD） | docs/v04/notification-policy-contract.md | `N07 · HOLD` |
| CL-21 | E1–E8 不变式表 | docs/v04/full-adaptive-e2e-replay.md | `E1–E8 验证汇总` |
| CL-22 | ER-07 ownership trace（M-01～M-11） | docs/v04/release-evidence-closure.md | `M-01` |
| CL-23 | E3-A / E3-B / E5-A / E5-B 证据索引 | docs/v04/release-evidence-closure.md | `E3-A` |
| CL-24 | HG-10 PASS | docs/v04/historical-discovery-governance.md | `HG-10 = PASS` |
| CL-25 | EL-02 PASS | docs/v04/v04-defect-ledger.md | `EL-02 = PASS` |
| CL-26 | Discovery 治理五条 | docs/v04/historical-discovery-governance.md | `append-only historical evidence` |
| CL-27 | prospective-only 基线声明 | docs/v04/v0.4-release-baseline.json | `prospective_only` |
| CL-28 | 基线协议步骤 BL-01～BL-10 | docs/v04/v04-defect-ledger.md | `V0.4 Release Baseline Protocol` |
