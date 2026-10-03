# V0.4 Release Evidence Closure（ER-07 / ER-08 / ER-09）

> **阶段性质**：**只修证据链，不裁任何行为**（D07–D09 evidence repair）。
> **目标**：让"E2/E3/E5/Fairness 都成立"从**一句结论**变成**可逐轮复核的证据链**。
> **编号**：`ER-07` E2 ownership trace｜`ER-08` E3/E5 corrected evidence index｜`ER-09` scenario-12 debt provenance trace。
> **纪律**：**不为保住 PASS 去找"差不多"的轮次**；找不到就标 `NOT EVIDENCED`，**不补造**。

---

## ER-07 · D07 · E2 ownership trace

### 0. 要证明什么（不是"Interface 理论上有写权限"）

> **每一次实际 Gap-state mutation，最终 write owner 都能追到 Interface。**

### 1. 最小 ownership trace（六行表）

| 阶段 | owner | 允许做什么 | 不允许做什么 |
|---|---|---|---|
| V0.3 | Resolution Engine | **选择 Action** | **不直接写 Gap state** |
| §11 | Question Selection | ASK 已调度后**选择具体问题** | 不写 Gap state |
| Priority | Priority Layer | **排序合法 Action** | 不写 Gap state |
| Fairness | Scheduler Fairness | 调整**合法调度竞争** | 不写 Gap state |
| Notification | Notification Policy | `visibility`／`discharged` 等**本层内部状态** | **不写 Gap state** |
| **Gap state commit** | **Interface** | **执行合法状态跃迁** | — |

### 2. 逐 mutation 完整链（自 V0.4.9 十二剧本抽取）

| # | 剧本·轮 | Gap-state mutation | 完整链（V0.3 → §11 → Priority／Fairness → **Interface commit**） |
|---|---|---|---|
| **M-01** | 剧本 1 轮1 | 受众 `→ PROPOSED` | V0.3：P0 锚点缺失 → 决定 **ASK**；§11：选"核心用户"问法；Priority：该 ASK 被调度执行；**Interface：接收合法 transition result → commit 受众 = `PROPOSED`** |
| **M-02** | 剧本 1 轮2 | 布局 `→ PROPOSED` | V0.3：**SHOW**（首页布局 3 方向）；Priority：R4 使 SHOW 先行（ASK 顺延）；§11：**不参与**；**Interface：commit 布局 = `PROPOSED`** |
| **M-03** | 剧本 1 轮3 | 布局 `→ CONFIRMED`（进 `effective_set`） | V0.3：选择型反馈 → 无需新动作；Priority：重排至 ASK(表格交互)；**Interface：commit 布局 = `CONFIRMED`** |
| **M-04** | 剧本 1 轮4 | 表格交互 `→ CONFIRMED` | V0.3：Revision(有值)；Priority：`[ASK(权限范围)]`；**Interface：commit** |
| **M-05** | 剧本 1 轮6 | 费用 `→ CONFIRMED` | V0.3：Revision；Priority：`[ASK(导出格式)]`；**Interface：commit** |
| **M-06** | 剧本 8 轮2 | B `→ OPEN + deferred` | V0.3：**delay**（非动作变化）；Priority：B 不再参与正常调度；**Interface：commit `deferred`**（Notification 只持有 commitment；见 M-10） |
| **M-07** | 剧本 8 轮6 | B `→ CONFIRMED` | 用户解除 delay → V0.3 重算 → ASK；Priority：调度；**Interface：commit** |
| **M-08** | 剧本 9 轮5 | 主视觉 `SUSPENDED → OPEN` | V0.3：外部输入到达 → **resume**；Priority：不调度 suspended gap（解除后可调度）；**Interface：commit `OPEN`**（**不自动 `CONFIRMED`**） |
| **M-09** | 剧本 10 轮4 | 锚点 `→ CONFIRMED(新值)` ＋ `supersedes`；下游 `→ CHALLENGED` | V0.3：Revision(target=goal)；Interface §9：传播 + generation 前进；**Interface：commit** |
| **M-10** | 剧本 3 轮5 | **无 Gap 写回**（`discharged` 仅 Notification 内部） | V0.3：无动作；Priority：配色仍排后；Notification：**本层状态 `discharged`**；**Interface：无 mutation → 不写入** |
| **M-11** | 剧本 12 轮8 | 配色 `→ CONFIRMED`；下游 `→ CHALLENGED`；新 generation | V0.3：Revision(goal)+用户值；Priority：重排；**Interface：commit** |

### 3. 负向核对（没有任何"越权 writer"）

| 检查 | 结果 |
|---|---|
| Action 层（V0.3）被写成 Gap-state writer？ | **否**（M-01～M-11 中 V0.3 仅"选动作"） |
| §11 被写成 Gap-state writer？ | **否** |
| Priority 被写成 Gap-state writer？ | **否**（仅排序；M-04 的 owner 行原文"Fairness 记证据"不构成写回） |
| Fairness 被写成 Gap-state writer？ | **否**（`debt` 是其**自有观测账**，非 Gap 字段） |
| Notification 被写成 Gap-state writer？ | **否**（`discharged` ＝ **本层内部状态**，N01；M-10 就是该边界的正例） |

**D07 closure 条件达成**：所有被 E2 引用的状态变化轮，**最后 state commit owner = Interface**；无任何 Action／Priority／Fairness／Notification 被写成 Gap-state writer。

---

## ER-08 · D08 · E3/E5 corrected evidence index

### 0. 要证明什么

```
E3：最终 Action 类型【始终由 V0.3 决定】——没有 Priority／Fairness／Notification 改选 Action
E5：§11 的 invocation condition = 【ASK has been scheduled】
```

### 1. 旧汇总的索引损坏（**逐条打开后确认**）

| 旧引用 | 汇总声称 | **实际轮次内容** | 判定 |
|---|---|---|---|
| `剧本 2 轮2` | "R4 让 **SHOW** 先行" | 剧本 2 轮2＝用户"给客户看" → **`ASK(主视觉方向)`**（**不是 SHOW**） | ❌ **引用错误** → 改为 **剧本 1 轮2** |
| `剧本 9 轮2` | "**不落** SUSPENDED（information_source）" | 剧本 9 轮2＝用户"主视觉方向等客户回复" → **正是 `SUSPENDED(external_owner)`** | ❌ **引用错误** → 改为 **V0.4.5 `E2E-08` 轮2**（法务＝`information_source` → **保持 `OPEN`、不落 SUSPENDED**） |
| `剧本 3 轮2` | "SHOW 轮，§11 未介入" | 剧本 3 轮2＝"配色不急，但别忘了" → **deprioritized ＋ commitment 轮**（**不是 SHOW**） | ❌ **引用错误** → 移出 E5 |
| `剧本 5 轮2` | 同上 | 剧本 5 轮2＝"图表交互（A）一直比导出格式（C）优先" → **`priority_hint` 轮**（**不是 SHOW**） | ❌ **引用错误** → 移出 E5 |

### 2. 修正后的 E3 / E5 evidence index（`E3-A`／`E3-B`／`E5-A`／`E5-B`）

| 项 | 证据轮 | 逐轮事实 | 结论 |
|---|---|---|---|
| **E3-A**（SHOW case） | **剧本 1 轮2** | V0.3 → **SHOW(首页布局 3 方向)**；Priority → 仅调整位置（R4：SHOW 先行，ASK 顺延）；Fairness → 本轮无债务，不介入；Notification → 本轮无 commitment，不介入；**最终仍 SHOW** | ✅ **Action 类型未被他层改选** |
| **E3-B**（ASK case） | **剧本 1 轮1** | V0.3 → **ASK(核心用户)**；§11 在 **ASK 被调度后**才选具体问法；Priority → 单动作、无排序争议；**最终仍 ASK** | ✅ 同上 |
| **E3-补充**（information_source） | **V0.4.5 `E2E-08` 轮2** | 用户"合规这块我去问法务" → `reason = information_source` → **保持 `OPEN`，不落 `SUSPENDED`**；动作仍由 V0.3 决定 | ✅ 与 **CS-05／X-4** 一致 |
| **E5-A**（non-ASK negative control） | **剧本 1 轮2**（SHOW）／**剧本 12 轮2**（SHOW） | 两轮 §11 记录均为 **不参与（非 ASK 轮）**；§11 未产生任何问题选择 | ✅ **§11 未被唤醒** |
| **E5-B**（ASK positive control） | **剧本 1 轮1** ＋ **剧本 1 轮3** | 两轮 ASK 被 scheduler 接纳 → §11 **才**选择具体 question（"核心用户"问法／"表格批量操作"问法） | ✅ **invocation condition 成立** |

**未发现 `NOT EVIDENCED` 项**（E3-A／B、E5-A／B 均有真实轮次支撑）；**未补造任何轮次**。

> 说明：V0.4.9 的 SHOW 轮共 **2 个**（剧本 1 轮2、剧本 12 轮2）；旧汇总中另两个"SHOW 证据"实为误引，已按上表移除。

---

## ER-09 · D09 · scenario-12 debt provenance trace

### 0. 要证明什么（不是"debt=2 是对的"）

> **这 2 是什么时候来的？** 若没有记录 skip reason 与 increment，就无法证明它是**先前的 capacity／soft-competition debt**，而不是 `deprioritized` 之后**新长出来的**。

### 1. 逐轮 provenance（剧本 12）

| 轮 | eligible | scheduled | skip_reason | debt 变化 | 依据 |
|---|---|---|---|---|---|
| **轮3** | ✅ | ❌ | **`soft_competition`**（用户 `priority_hint{scope:current_round}`：首页 ≻ 其他 → C 不在本 bundle） | **0 → 1** | F1 |
| **轮4** | ✅ | ❌ | **`soft_competition`**（显式 hint `A ≻ C`，scope=whole_task） | **1 → 2** | F1（**显式用户排序属软竞争，仍计债**；SFC-01 同理） |
| **轮5** | ✅ | ❌ | **`user_deprioritization`**（用户"C 不急，但别忘"） | **2 → 2（increment = 0）** | F1：`deprioritized` **不是** capacity／soft competition → **不增债** |
| 轮6–7 | ✅ | ❌ | `user_deprioritization` | **2 → 2** | 同上 |
| **轮8** | — | — | **generation replacement**（goal 变 → 新 generation） | **旧债终止** | F5／F6 |

**结算**：`debt=2` **可由前序完整推出**（轮3 +1、轮4 +1）；**每次 +1 都有合法 skip reason**；**轮5 起 increment = 0**。

### 2. 两个必须分开的命题（本轮明确写出）

```
deprioritized does not erase existing debt     ← 已有债不清零
deprioritized does not add new debt            ← 不新增债
```

**⛔ 明确不是**：`deprioritized → debt reset to 0`（那会改语义，**未采用**）。

### 3. 同源核对（剧本 10，同一缺陷类）

| 轮 | eligible | scheduled | skip_reason | debt 变化 |
|---|---|---|---|---|
| 轮2 | ✅ | ❌ | `soft_competition`（A 的 `deprioritized`＋commitment 使 A 排后，C 与其余项竞争） | 0 → 1 |
| 轮3 | ✅ | ❌ | `soft_competition` | 1 → 2 |
| 轮4 | — | — | **generation replacement** | **旧债终止** |
| 轮5 | — | — | 旧 commitment 不继承（Notification 层） | — |

> 原文档仅写"C 开始累积／C 又未排上"而**未记 skip reason 与 increment** —— **这正是 D09 所指的证据透明性问题**；本表即为最小补证。

---

## 证据一致性探针（EV-07／EV-08／EV-09）

| # | 探针 | 结果 |
|---|---|---|
| **EV-07** | 抽取所有被 E2 引用的 state mutation（M-01～M-11）→ **final writer 是否全部 = Interface** | ✅ **11/11 = Interface**；**无越权 writer**（Action／§11／Priority／Fairness／Notification 均未被写成 Gap-state writer） |
| **EV-08** | 逐条打开 E3/E5 citation → cited round 的**实际 Action / §11 involvement** 与汇总描述是否一致 | ✅ **修正后 4/4 一致**（E3-A／E3-B／E5-A／E5-B）；**旧 4 条错误引用已登记并替换**；**无 `NOT EVIDENCED`** |
| **EV-09** | 逐轮重建 scenario 12 debt → 每次 +1 是否都有合法 skip reason；`deprioritized` 后 increment 是否为 0；最终 debt=2 是否可由前序完整推出 | ✅ 全部成立（轮3 +1／轮4 +1／轮5 起 0）；**O-5 未被混合场景违反** |

## 回填

```
D07  ✅ CLOSED BY ER-07   E2 ownership trace（每次 mutation 的 commit owner = Interface）
D08  ✅ CLOSED BY ER-08   E3/E5 corrected index（4/4 一致；旧 4 条错引用已改）
D09  ✅ CLOSED BY ER-09   scenario-12 debt provenance（+1 有据、deprioritized 后 increment=0）
```

**本阶段门槛**：**EV 3/3 通过**｜**D07–D09 全部 CLOSED**｜**未新增行为规则／字段／状态**｜**未补造证据**。
