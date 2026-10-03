# Priority Layer Contract v1（V0.4.4 · 独立成层）

> **版本**：**v1** = §1–§8（2026-10-02 建立并冻结）；**v1.1** = §9（V0.4.6 增量 L1–L3，2026-10-02，例外 #21 预登记）。

> **裁决（2026-10-02）**：**批准独立成层**。`priority_hint` 批准建立（**非数值、偏序、带作用域**）；`deprioritized` 正式确认为**纯调度属性**。
> **定位**：**Priority Layer 只对已经合法的 active actions 做调度；不产生动作、不改变 Gap 状态、不覆盖冻结规则。**
> **边界**：本层为**独立层文档**——❌ 不改 §11 ❌ 不改 V0.3 ❌ 不改 Interface v1／v2／v3／§10 ❌ 不新增 Action／Type／Gap state ❌ 不设计数值评分。
> **上游**：[`priority-model-discovery.md`](priority-model-discovery.md)（30 例破坏测试）｜Interface [`gap-ledger-interface.md`](gap-ledger-interface.md)（v1–v3 + §10）

---

## 1. 架构位置（四层职责分离）

```
Gap Ledger                「有什么 gap，什么值有效」
        ↓
V0.3 Resolution Engine    「每个 gap 用什么动作」（ASK／SHOW／INSPECT／TEACH／DISCOVER）
        ↓
Priority Layer            「这些合法动作现在先做哪个」        ← 本层
        ↓
§11 Question Selection    「若调度到 ASK，问什么、怎么问、是否合并」
```

**关键**：本层位于 **动作已选出之后**、**问题选择之前**。它**没有**动作选择权，也**没有**问题选择权。

---

## 2. 六条原则（P1–P6）

| # | 原则 |
|---|---|
| **P1** | **Hard scheduling constraints > user priority hints.** 硬调度约束优先于用户优先级提示 |
| **P2** | **User priority hints 只排序本来就合法的候选。** 提示不能使一个非法动作变合法 |
| **P3** | **`deprioritized` 只降低调度优先级**，不改变 gap 状态或 action eligibility |
| **P4** | **Priority 只能排序 V0.3 已选出的动作**，不得重选 ASK／SHOW／INSPECT／TEACH／DISCOVER |
| **P5** | **一旦 ASK 被调度，§11 独占问题选择、ASK 内部顺序与合并判断** |
| **P6** | **每轮派生排序不持久化**；只有用户显式 `priority_hint` 可在其 `scope` 内保留 |

**推论（本层禁止清单）**：不产出动作、不改变 gap 状态、不覆盖 R4／R6／R14／§11.6、不改 `effective_set`／`askable_set`、不做数值评分、不写回任何 gap 字段（唯一例外：`priority_hint` 按其 scope 保留）。

---

## 3. 硬调度约束（**收紧定义**）

**定义**：硬调度约束 = **既有冻结规则已经判定"必须前置"的约束**。本层**只读**它们，**不重新判定**。

| 白名单（仅此四类） | 来源 |
|---|---|
| **当前 blocker / R6 mandatory decision** | V0.3 契约 R6；Interface §1.2「阻塞且悬置」 |
| **R14 明确要求前置的 high-risk C** | V0.3 契约 R14（三闸门 + 与阻塞项同轮并列） |
| **§11.6 的约束型依赖** | §11.6 + §11.7 补充判据（约束型依赖 vs 共同决策） |
| **R4 等既有动作顺序／容量** | V0.3 契约 R4：`INSPECT → SHOW → TEACH → ASK`、同轮 ≤1 TEACH＋1 SHOW＋1 ASK |

**⛔ 明确不扩大**（反例，由 discovery 案例证明）：

- ❌ **不是"所有 Type C"**——只有 **R14 三闸门全过**的 high-risk C 才算硬约束（PCY-02）。
- ❌ **不是"所有 dependency"**——只有 **§11.6 界定的约束型依赖**（上游答案改变下游的可行取值／选项集／判断标准）才算；**共同决策型关系不强制上游先做**（PCY-03）。
- ❌ 不是"所有风险项"、不是"所有未决项"。

---

## 4. 输入／输出合同

```yaml
input:
  active_actions:                    # 已由 V0.3 §11.0 选出、且已通过 R6／R14 可执行性过滤
    - {gap_id, resolution, blocking, risk_class, provenance}
  hard_scheduling_constraints:       # §3 白名单，只读
  priority_hint:                     # §5，可为空
  deprioritized:                     # §6，可为空
  round_capacity: 3                  # 来自 R4／§2（1–3 问）

output:
  ordered_actions: [...]             # 本轮调度顺序
  same_round_group: [...]            # 允许同轮并列者（如 R14 的 TEACH＋ASK）
  deferred_by_capacity: [...]        # 本轮塞不下的动作
```

### 4.1 `deferred_by_capacity` ≠ Interface `deferred`

```
deferred_by_capacity  = 「本轮容量不足，顺延到下一轮执行」   → 纯调度事实，本轮一次性的
Interface §3 delay    = 「用户决定该缺口暂缓确认」          → gap 状态落点：OPEN + attempts≥1 + deferred=true
```

**铁律**：`deferred_by_capacity` **绝不写回** Interface 的 `deferred` 标志，**绝不改变任何 gap 状态**（PCY-04）。

---

## 5. `priority_hint` 规格（**非数值偏序**）

```yaml
priority_hint:
  source: user
  scope: current_cluster | current_round | whole_task
  relations:
    - before: [A, B]
    - before: [B, C]
```

**三条核心边界**

```
priority_hint ≠ gap state          # 不是状态，不写 gap.status／confidence／validity_state
priority_hint ≠ action selection   # 不产生动作、不改变 action eligibility
priority_hint ≠ hard dependency    # 不是依赖边；不得被当作 §11.6 的上游依据
```

**生命周期**

| 项 | 规则 |
|---|---|
| 用户显式表达的**顺序** | **可持久化到其 `scope` 失效为止**（`current_round` → 本轮末失效；`current_cluster` → 该决策簇结束时；`whole_task` → 任务结束） |
| **每轮最终排序结果** | **不持久化**（派生物） |
| 冲突的 hint（如 `A before B` ∧ `B before A`） | **不新增状态**：取一次澄清，或按硬约束处理（PCY-11） |
| hint 指向已 `CLOSED` 的 gap | **不复活 gap**（不改状态），仅忽略并记录（PCY-12） |
| 无显式 hint | 用默认序（§11.1 一级：排除下游最多；二级：可回答性），**不生成 hint**（PCY-10） |

---

## 6. `deprioritized` 规格（纯调度属性）

**语义**：

> "**在其他条件相同的情况下**，这个 gap 往后排。"

**它不能导致**：`CLOSED`／`INVALIDATED`／`assumed`／停止询问／改变 `effective_set`／改变 ASK-SHOW-INSPECT-TEACH-DISCOVER 的选择。

### 6.1 `expressed_priority` vs `effective_priority`（措辞修正）

```
expressed_priority   := 用户表达的偏好（始终记录，不丢）
effective_priority   := 本轮实际调度中生效的优先级
```

> **修正后的表述**：**用户可以表达降权，但硬调度约束可以使这个降权在当前轮不生效。**

- 不写成"blocker／R6／high-risk C 不能被 deprioritized"（那会被误读成**禁止记录偏好**）；
- 而写成：**偏好照记，当前轮调度以硬约束为准**。

### 6.2 例（PCY-01）

```
用户："预算先别管。"
→ expressed_priority：预算 = 降权（记录保留）
→ 但预算当前属 R6 blocker（硬约束）→ effective_priority：预算仍优先
→ 出口可向用户说明"这一项需要你先拍板"
→ gap 状态不变
```

---

## 7. 回归与 Canary

### 7.1 回归

| 套件 | 要求 | 结果 |
|---|---|---|
| **原 P1～P5（Discovery 30 例）** | 30/30 | **30/30 唯一**（本层未改变任何一例的结论） |
| **§11 Question Selection** | 35/35（23 + 12） | **35/35 唯一** |
| **V0.3 priority-sensitive 回归** | 全过 | **11/11**（`high-risk-c` HR-01～08 ＋ `unknown-known` UB-05 同轮顺序 ＋ `blind-spot` BS-07 同轮容量 ＋ `evidence-unknown` EU-10 先查后问） |

### 7.2 Priority Canary（12，含 4 个硬 canary）

| # | 场景 | 判定 | 唯一 |
|---|---|---|---|
| **PCY-01**（硬） | 用户降权 **R6 blocker** | 记录 `expressed_priority` 降权；`effective_priority` **不降权**；gap 状态不变 | **唯一** |
| **PCY-02**（硬） | **普通 Type C** vs 用户明确优先的普通 ASK | **不得把所有 Type C 当硬前置** → 用户的普通 ASK 可先行（Type C 仅在 R14 三闸门全过时才硬前置） | **唯一** |
| **PCY-03**（硬） | 存在 dependency edge 但**非约束型依赖**（共同决策型） | **不得自动强制上游先做**；可按 hint 排序 | **唯一** |
| **PCY-04**（硬） | 本轮容量不足 → action 顺延 | 记入 `deferred_by_capacity`；**不得写回 gap 的 `deferred` 状态** | **唯一** |
| PCY-05 | 硬约束 vs 用户显式序（blocker ＋ 用户点名先做非阻塞项） | 硬约束胜；出口向用户说明 | **唯一** |
| PCY-06 | R14 high-risk C ＋ 用户降权 | TEACH 仍前置（硬）；降权仅记录 | **唯一** |
| PCY-07 | R4 顺序 vs 用户序（用户要 ASK 先，同轮有未做 INSPECT） | **INSPECT 先** | **唯一** |
| PCY-08 | `priority_hint.scope = current_round` 到期 | 下一轮**不再生效**（scope 失效），不残留 | **唯一** |
| PCY-09 | `priority_hint.scope = whole_task` | 跨轮保留；遇硬约束仍不生效 | **唯一** |
| PCY-10 | 用户"你排"（无显式 hint） | 用默认序（§11.1 一级＋二级）；**不生成** `priority_hint` | **唯一** |
| PCY-11 | hint 自相矛盾（A before B ∧ B before A） | 一次澄清或按硬约束处理；**不新增状态** | **唯一** |
| PCY-12 | hint 指向已 `CLOSED` 的 gap | 不复活 gap（不改状态），仅忽略并记录 | **唯一** |

**Canary 结果：12/12 唯一。**

---

## 8. 边界与状态

| 项 | 状态 |
|---|---|
| §11／V0.3／Interface v1／v2／v3／§10 | **未修改** |
| 新增 Action／Type／Gap state | **无** |
| 数值评分 | **未设计**（明令禁止） |
| `priority_hint` | **新增字段（本层自有）**：非数值偏序 + scope；**不写入 gap 状态** |
| `deprioritized` | **本层消费的调度属性**；来源为 Phase 2.3-B 设计（未改其定义，只确认定位） |
| 本层状态 | **✅ Contract v1 建立并冻结（2026-10-02）** |

**本层一句话**：**它只回答"先做哪个"——不回答"做不做"（V0.3）、"状态变不变"（Interface）、"具体问什么"（§11）。**

---

# §9 V0.4.6 增量（L1–L3，例外 #21 预登记后落盘）

> **来源**：[`priority-hint-language-discovery.md`](priority-hint-language-discovery.md)（30 例破坏测试；**K5-1 = B-03 scope 歧义**）
> **裁决**：三项收口；**§1–§8 内容保持不动**（本节为纯增量）。
> **不新增**：`timed` scope／Gap 状态／Action／Type／数值权重。

## 9.1 L1 · `scope` 与 temporal lifetime **正交**

```
scope        回答「在哪里有效」    ∈ {current_round, current_cluster, whole_task}
valid_until  回答「有效到什么时候」 可缺省；可附 expiry condition
```

```yaml
priority_hint:
  source: user
  scope: whole_task            # 结构作用空间
  valid_until: end_of_today    # 生命周期时间边界（正交维度）
  relations:
    - before: [A, B]
```

| 规则 | 内容 |
|---|---|
| **L1-a** | **不把时间塞进 scope**：`今天／这一周／到周五／在上线前` 表达的是**生命周期边界**，写作 `valid_until`（或 expiry condition），**不新增 `timed` scope** |
| **L1-b** | **两条正交**："这个模块今天先 A 后 B" → `scope=current_cluster` ＋ `valid_until=end_of_today` |
| **L1-c** | **结构作用域无更窄证据时取 `whole_task`**，再由 `valid_until` 限制生命周期——**不是**"把时间窗近似成 whole_task" |
| **L1-d** | `valid_until` 到期 → `Reason for expiry = scope ended`（时间条件部分）；`scope` 的结构结束条件不变（见 9.2） |
| **L1-e** | 该字段是**调度属性**，**不写入任何 gap 状态** |

## 9.2 L2 · `current_round` 的正式定义

```
current_round :=

从 Priority Layer 基于某一状态快照生成本轮 action bundle 时开始，
直到该 bundle 中的动作：
  - 全部完成；
  - 被取消；或
  - 因需求状态变化而失效并触发重新调度
时结束。
```

**关键**：**单次用户消息本身不自动结束 `current_round`。**

- 因此 `ASK(q1) + ASK(q2)` 属同一 bundle 时，**即使中间用户先回应 q1，hint 不能突然从 q2 身上消失**；
- 只有真正发生"**旧 bundle 结束 → scheduler 重新生成新 bundle**"才算下一轮；
- 这比"assistant 一条消息"或"user 一次回答"都稳定（Discovery **O-1**：Interpretation B 胜出，证据 B-08）。

## 9.3 L3 · `deprioritized` vs `delay`：按**效果**区分，**不按关键词**

```
deprioritized
  用户仍允许该 gap 在当前处理窗口内被处理，只是要求相对调度优先级降低
  → 不改 gap 状态
  → 仍可进入 active candidates

delay
  用户要求该 gap 暂时不要被处理 / 不要现在决定，直到未来时间、条件或后续阶段
  → OPEN + deferred（Interface §3）
  → 当前不参与正常调度
```

**一句机械判据（正式判据）**：

> **还能不能在当前处理窗口里顺手处理？**
> 可以，只是别优先 → **`deprioritized`**；现在不要处理 → **`delay`**。

- 关键词只作 **cue**，**不作唯一判据**："不急／排后面／优先级低" 通常提示 `deprioritized`；"以后再说／等 X 后／先不决定" 通常提示 `delay`。
- 上下文仍不足时（例："这个先别管"）→ **一次最小澄清**，不得按词表硬判。
- **不得**把 `delay` 写进 `priority_hint.relations`；两者是**两个事件**（Discovery D-08）。

## 9.4 PHC Canary（8，V0.4.6 收口回归）

| # | 输入 | 判定 | 唯一 |
|---|---|---|---|
| **PHC-01** | `今天先 A。` | `relation A ≻ {others}` ＋ `scope=whole_task` ＋ **`valid_until=今天结束`**；到期 `Reason=scope ended` | **唯一**（**B-03 K5 由此消失**） |
| **PHC-02** | `这个模块今天先 A。` | `scope=current_cluster` ＋ `valid_until=今天结束` | **唯一** |
| **PHC-03** | 本轮 `ASK(q1)+ASK(q2)`，用户只答 q1 | **hint 对 q2 仍有效**（bundle 未完成 → `current_round` 未结束） | **唯一** |
| **PHC-04** | bundle 完成 → scheduler 重新调度 | `current_round` hint **失效**；`Reason=scope ended` | **唯一** |
| **PHC-05** | `B 不急，有空可以做。` | **`deprioritized`**（仍进 active candidates；**不改状态**） | **唯一** |
| **PHC-06** | `B 以后再说，现在别处理。` | **`delay`** → `OPEN + deferred`；当前不参与正常调度 | **唯一** |
| **PHC-07** | `先别管 B，顺手能做就做。` | **`deprioritized`**（机械判据：还能在当前窗口处理 → 是） | **唯一** |
| **PHC-08** | `先别管 B，等客户回复再处理。` | **`delay`**（现在不要处理，等到条件满足） | **唯一** |

### 9.5 收口验收

```
原 30/30（Discovery A/B/C/D）        保持
PHC-01～08                            8/8 唯一
B-03 K5                              消失
K4                                   0
K5                                   0
scope leakage                        0
delay / prioritization 混淆          0
```

**O-3（连续多轮 `deferred_by_capacity` 导致的 starvation / fairness / 可见性）**：**仍不在本轮**——属下一阶段问题："**一个合法但总排不上的 action，scheduler 什么时候必须主动照顾它？**"
