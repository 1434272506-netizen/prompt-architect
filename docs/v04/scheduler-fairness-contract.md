# V0.4.8-A · Scheduler Fairness Contract（独立合同 · v1）

> **裁决落地（2026-10-02）**：① fairness **不自动压过仍有效的用户显式 soft hint**（可触发重新暴露，不可偷偷改序）② 批准 **Fairness Ledger**（scheduler-local 跨轮观测账，绑 `gap identity + resolution generation`，**计数是证据而非阈值**）③ `must_not_starve` 语义成立但**归 Notification Policy**，命名为 **`visibility_commitment`** ④ **Scheduler Fairness Contract 与 Notification Policy 正式拆为两个独立合同**。
> **O-3 关闭**：`Scheduler starvation visibility` → 正式分裂为 **A. Scheduler Fairness**（本合同）与 **B. Notification Policy**（V0.4.8-B）。
> **边界**：❌ 不改 Priority Contract v1.1／Interface／§11／V0.3 ❌ 不新增 Gap state／Action／Type／数值评分 ❌ 不产生用户可见通知（属 B）。

---

## 0. 架构位置（sibling contracts）

```
Gap Ledger
    ↓
V0.3 Resolution Engine
    ↓
Priority Layer（P1–P6 + §9 L1–L3）
    ↓
Scheduler Fairness（本合同）          ← 只改「调度机会」
    ↓
action bundle

旁路（不进主链）：
Fairness Ledger（scheduler-local 观测账）
    ↓
Notification Policy（V0.4.8-B）       ← 只改「用户可见性」
    ↓
是否需要向用户重新暴露长期未处理事项
```

**核心切口**：`promotion ≠ notification` —— 前者改变调度结果，后者只改变可见性，**两条链互相不能越权**。

---

## 1. 调度层次（**仅调度层，不是全系统优先级总表**）

```
Hard scheduling constraints
        >
explicit active user priority
        >
fairness adjustment
        >
ordinary soft scheduling preference
```

| 层 | 含义 | 谁可以覆盖它 |
|---|---|---|
| **Hard scheduling constraints** | R6 blocker／R14 high-risk C／R4 顺序与容量／§11.6 约束型依赖 | **任何人**（含 fairness）都不能覆盖 |
| **explicit active user priority** | 仍有效（scope 未到期、未被取消、覆盖该 gap）的 `priority_hint` 关系 | 只能被 **Hard constraints** 覆盖；**不能被 fairness 偷偷覆盖** |
| **fairness adjustment** | 本合同授予的调度机会修正 | 可被上面两层覆盖；可覆盖下面一层 |
| **ordinary soft scheduling preference** | 默认序（§11.1 一级＋二级）等普通软排序 | 可被 fairness 覆盖 |

> 用户明确偏好**可以被硬约束覆盖**，但**不应再被另一个内部软机制偷偷覆盖**。

---

## 2. 六条原则（F1–F6）

| # | 原则 |
|---|---|
| **F1** | 只有 **eligible-but-unscheduled** 且原因属于 `capacity`／`soft competition` 才累积 fairness debt |
| **F2** | **hard constraint 永不因 fairness 被越过** |
| **F3** | **仍有效的 explicit user priority 不被 fairness 自动覆盖**（可触发"重新暴露资格"，不改排序） |
| **F4** | **无显式用户排序约束时**，fairness 可以修正普通 soft scheduling |
| **F5** | debt 绑定 **`gap identity + resolution generation`**（**不绑 action 类型**） |
| **F6** | 失去 eligibility 的周期**不增加 debt**；`resolution generation` 变化时**旧 debt 终止** |

---

## 3. Fairness Ledger（scheduler-local 观测账）

**最小模型**

```yaml
fairness_entry:
  gap_id: G-17
  resolution_generation: 4
  eligible_unscheduled_cycles: 3
  last_skip_reason: capacity | soft_priority
  last_eligible_cycle: <cycle-id>
  starvation_candidate: true
```

**key = `gap identity + resolution generation`**（**不是** `ASK`／`SHOW` 或任何 action 类型）。

### 3.1 `resolution_generation` 的定义与禁止用途

```
当一个 gap 的「当前 resolution problem」被 Revision / invalidation / replacement 实质重建时，
generation 前进。
```

- 用途**只有一个**：**防止旧调度债污染新的问题**。
- **暂时不允许它影响**：`current_value`／`confidence`／`validity`／Action／§11。
- 它是 **Scheduler 可派生的 identity epoch**，**不塞进 Gap 生命周期正文**。

### 3.2 计数是证据，不是政策

```
eligible_unscheduled_cycles = 4      ← 可记录
≠  4 → 必须 promotion                ← 禁止
```

### 3.3 术语别名（N03 · 仅别名）

> **`cycle` 在本文中仅作为 `current_round` 的同义术语**，均指**一次 scheduler action bundle 的完整生命周期**（定义见 [`priority-layer-contract.md`](priority-layer-contract.md) §9.2）；**该术语统一不改变既有 debt accumulation semantics。**

**受保护不变式（本次未改）**：debt 何时 +1、一次 bundle 能否 +2、单条用户消息是否切 cycle、hard constraint 周期如何计——**全部维持原语义**。

```
eligible ∧ unscheduled ∧ reason ∈ {capacity, soft competition}  → 才可能累积 debt
hard constraint 周期            → 不增
deprioritized                   → 不增
```

**未落（HOLD · N04）**：`starvation_candidate ⟺ eligible_unscheduled_cycles ≥ 1` **不写入本合同**——现有证据只支持"存在符合既有 debt 观察条件的 eligible-but-unscheduled 事件"，**不支持一个正式的 0→false / 1→true 资格边界**；且引入字面阈值与"count 是证据不是政策"相冲突。**待 Fairness 正文取得明确证据后再裁。**

**本阶段：`count` 是证据，不是阈值。** 不引入任何数字评分系统。

---

## 4. 显式用户优先权的"有效性条件"

fairness **恢复**自动修正资格的三种情形（任一发生）：

```
① priority_hint scope expired        （含 §9 L1 的 valid_until 到期）
② 用户取消 / 修改该 hint             （explicit cancellation / supersede）
③ C 不再被该 relation 覆盖           （关系不再指向 C）
```

在三种情形**发生之前**：

```
保持 A ≻ C  ＋  把 C 交给 Notification Policy 判断
是否需要让用户重新审视该偏好
```

---

## 5. 职责边界

| ✅ 可以做 | ❌ 不可以做 |
|---|---|
| 识别 `starvation_candidate` | 越过 hard constraints |
| 修正**普通软排序**（无显式用户关系时） | 越过仍有效的用户显式排序 |
| 在没有有效用户 relation 时做 fairness promotion | 改 Gap 状态／`current_value`／`confidence`／`validity` |
| 向 Notification Policy **提供输入** | **发用户可见通知**（属 V0.4.8-B） |
| 维护 scheduler-local 观测账 | 影响 Action 类型或 §11 问题选择 |

---

## 6. Contract 证伪案例（18）

字段：`ID ｜ 场景 ｜ eligible? ｜ debt 变化 ｜ 显式用户优先级 ｜ hard ｜ fairness 结果 ｜ 通知? ｜ 唯一`

### 组 1 · 用户显式优先权 vs fairness（5）

| # | 场景 | eligible | debt | 显式用户优先级 | hard | fairness 结果 | 通知 | 唯一 |
|---|---|---|---|---|---|---|---|---|
| **SFC-01** | 用户 `A 一直比 C 优先`（`whole_task`，有效）；C 连续 **6** 周期 eligible-unscheduled | ✅ | **+6** | **有效（A ≻ C）** | 无 | **不 promotion**：保持 A ≻ C；`starvation_candidate=true`，**交给 Notification Policy** | 由 B 判 | **唯一**（**K5-1 关闭**） |
| **SFC-02** | 同 SFC-01，但该 hint **scope 到期** | ✅ | +6 | **已失效** | 无 | **fairness 立即恢复资格** → 可 promotion | 由 B 判 | **唯一** |
| **SFC-03** | 同 SFC-01，用户 `刚才那个顺序不算了`（**取消**） | ✅ | +6 | **已取消** | 无 | 立即恢复资格 → 可 promotion | 由 B 判 | **唯一** |
| **SFC-04** | 用户改为 `A ≻ B`，**C 未被提及** | ✅ | +5 | 无（**C 不被覆盖**） | 无 | 恢复资格 → 可 promotion | 由 B 判 | **唯一** |
| **SFC-05** | 有有效 hint，但 **A 已完成**，C 成唯一候选 | ✅ | 归零（被调度） | 有效但无对象 | 无 | 正常调度 C（**无需 promotion**） | 否 | **唯一** |

### 组 2 · debt 累积 / 暂停 / 终止（5）

| # | 场景 | eligible | debt 变化 | 依据 | 唯一 |
|---|---|---|---|---|---|
| **SFC-06** | 用户 `C 不急`（`deprioritized`），C 连续 10 周期排后 | ✅ | **不累积**（debt 恒为 0） | F1：真实原因＝用户偏好，**不是** capacity／soft competition；系统在忠实执行偏好 | **唯一** |
| **SFC-07** | C 进入 `SUSPENDED` 2 周期（ineligible），随后恢复 eligible，再被容量挤掉 2 周期 | ❌→✅ | **暂停（不增）**：仅后 2 周期计入 → `=2`；**不清零** | F6（失去 eligibility 的周期不增加债务；也不因暂时 ineligible 而丢弃已有证据） | **唯一** |
| **SFC-08** | 同 gap，Revision 实质重建 resolution problem | ✅ | **终止（清零）** | F5/F6：新 `generation` → 旧债终止 | **唯一** |
| **SFC-09** | **新 gap**（同主题、同 `ASK`；旧 gap 已 `CLOSED`） | ✅ | **从 0 计**（不继承） | F5：新 identity | **唯一** |
| **SFC-10** | 同 gap，动作由 `ASK` 被 V0.3 重算为 `SHOW`，`generation` 未变 | ✅ | **继承**（`=2`） | F5：**不绑 action 类型** | **唯一** |

### 组 3 · hard constraints 不可越（4）

| # | 场景 | debt | hard | fairness 结果 | 唯一 |
|---|---|---|---|---|---|
| **SFC-11** | C 等 5 周期 + 新 **R6 blocker** 出现 | 5 | R6 | **R6 先**；fairness 不越 | **唯一** |
| **SFC-12** | C 等 5 周期 + **R14 high-risk C** | 5 | R14 | **TEACH＋ASK 同轮并列** | **唯一** |
| **SFC-13** | C 等 5 周期 + **R4 强制顺序**（INSPECT 未做） | 5 | R4 | **INSPECT 先** | **唯一** |
| **SFC-14** | C 等 5 周期 + **§11.6 约束型依赖**（C 依赖未决 D） | 5（但 C 实际 ineligible） | §11.6 | **D 先**；C 本就不 eligible → 不计 debt | **唯一** |

### 组 4 · 普通软竞争 / 计数非阈值 / promotion 后归零（4）

| # | 场景 | debt | 显式用户优先级 | fairness 结果 | 唯一 |
|---|---|---|---|---|---|
| **SFC-15** | 对手均为普通候选，**无** hint；C 被软排序挤出 3 周期 | 3 | 无 | **fairness 可以改变排序**（promotion 生效） | **唯一** |
| **SFC-16** | `count = 4`，无 hint，且无其他约束 | 4 | 无 | 记录为**证据**；promotion 由 F4 条件（无显式用户排序约束）决定，**不因数字自动触发** | **唯一** |
| **SFC-17** | `count = 6` 且存在**有效**用户 hint | 6 | 有效 | **仍不 promotion**；`starvation_candidate=true` 作为 **Notification 输入** | **唯一** |
| **SFC-18** | fairness promotion 后 C 被调度 | **归零** | 无 | 下一周期从 0 重新计；`last_eligible_cycle` 更新 | **唯一** |

**结果：18/18 唯一；K4 = 0；K5 = 0（K5-1 由本合同裁决关闭）。**

---

## 7. 回归与验收

| 项 | 结果 |
|---|---|
| V0.4.7 Discovery **30/30** | **保持**（本合同未改变任何一例既有结论） |
| **K5-1（C-01／C-04）** | **关闭** —— `Hard > explicit active user priority > fairness > ordinary soft`（SFC-01 vs SFC-02/03/04 给出分界） |
| 新证伪集 **SFC-01～18** | **18/18 唯一** |
| fairness 越过 hard constraint | **0** |
| fairness 偷偷覆盖有效用户显式排序 | **0** |
| ineligible 周期累积 debt | **0**（SFC-07／SFC-14） |
| 失效／新 identity 继承旧债 | **0**（SFC-08／SFC-09） |
| 通知越权（fairness 直接发通知） | **0**（全部 case 的"通知"列均交给 B） |
| **K4 / K5** | **0 / 0** |

---

## 8. 非目标与下一步

**非目标（明确不做）**

- ❌ 任何"连续 N 轮必须提升"的阈值政策（count 只是证据）
- ❌ 用户可见通知（属 V0.4.8-B）
- ❌ 改 Gap 状态／有效集合／Action／§11
- ❌ 把 `visibility_commitment` 放进 Scheduler（那是 Notification Policy 的字段）

**V0.4.8-B · Notification Policy（待启动）** 将正式引入：

```yaml
visibility_commitment:
  required: true      # 例："不急，但别忘了" → deprioritized=true + visibility_commitment=true
```

并回答：什么情况必须提醒／一次提醒够不够／用户确认"知道了"后是否解除义务／如何防通知骚扰／`delay` 情况是否允许提醒。

---

## 9. 状态

| 项 | 状态 |
|---|---|
| Priority Contract v1.1／Interface／§11／V0.3 | **未修改** |
| 新增 | **Fairness Ledger（scheduler-local 观测账）**＋ `resolution_generation`（Scheduler 派生 identity epoch，**不进 Gap 生命周期**） |
| 未新增 | Gap state／Action／Type／数值评分／用户可见通知 |
| **O-3** | **正式关闭** → 分裂为 A（本合同）／B（V0.4.8-B） |
| 本合同状态 | **✅ Scheduler Fairness Contract v1 建立并冻结（2026-10-02）** |
