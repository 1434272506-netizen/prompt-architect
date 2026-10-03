# V0.4.8-B · Notification Policy Discovery（30 例破坏测试）

> **阶段性质**：**只做破坏测试，不写通知策略、不新增字段进入 Scheduler**（`visibility_commitment` 属本层，不入调度）。
> **职责（按裁决）**：Notification Policy **只回答**"有哪些长期未处理事项现在应该让用户知道？"
> **可以读取**：`starvation candidate`／`visibility_commitment`／用户显式 `delay`／`deprioritized`／当前交互负担。
> **不能**：改调度、promotion、改 Gap、改 Action。
> **架构边界**：`promotion ≠ notification`（与 [`scheduler-fairness-contract.md`](scheduler-fairness-contract.md) 为 sibling contracts）。
> **禁止**：❌ 改 Priority Contract v1.1／Fairness Contract v1／Interface／§11／V0.3 ❌ 新 Gap state／Action／Type ❌ 数值化通知频率评分。

**本轮要解决的五个问题**

```
Q1 什么情况【必须】提醒？
Q2 一次提醒够不够？
Q3 用户确认"知道了"后是否解除义务？
Q4 如何防通知骚扰？
Q5 delay 情况是否允许提醒？
```

---

## 0. 候选模型（**测试对象，非规则**）

```
输入： starvation_candidate ／ visibility_commitment ／ user delay ／ deprioritized ／ interaction_burden
输出： notify_now ｜ notify_later ｜ record_only ｜ never_notify
```

```yaml
visibility_commitment:            # 本层字段（不进 Scheduler、不改 Gap）
  required: true
  trigger: now | condition | time_window     # 候选
  discharged: false                          # 用户确认"知道了"后置 true（候选）
```

**五类必须打的表达（用户指定）**

```
N-01 不急，但别忘
N-02 这个以后提醒我
N-03 先不处理，但别漏掉
N-04 我知道它还在，不用一直提醒
N-05 如果今天还没排上再告诉我
```

**每例记录**：① 用户原话｜② 事项状态（eligible？debt？）｜③ `deprioritized`／`delay`｜④ `visibility_commitment` 判定｜⑤ 交互负担｜⑥ 输出（notify_now／later／record_only／never）｜⑦ 是否合并提醒｜⑧ 是否改变调度（**必须恒为否**）｜⑨ 是否改 Gap／Action（**必须恒为否**）｜⑩ 下一轮义务是否仍在｜⑪ K4／K5。

---

## A. `visibility_commitment` 的成立与强度（6）

| # | ① 用户原话 | ② 事项状态 | ③ delay／depri | ④ commitment | ⑤ burden | ⑥ 输出 | ⑦ 合并 | ⑧ 改调度 | ⑨ 改 Gap | ⑩ 下轮义务 | ⑪ K |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **NA-01** | `不急，但别忘。` | eligible，debt=3 | `deprioritized` | **required=true**，`trigger=now` | 低 | **notify_now**（一句话） | 可 | **否** | **否** | **在** | 唯一 |
| **NA-02** | `无所谓，你看着办。` | eligible，debt=2 | `deprioritized` | **无 commitment** | 低 | **record_only** | — | 否 | 否 | 否 | 唯一 |
| **NA-03** | `不重要。` | eligible，debt=4 | `deprioritized` | 无 | 低 | **record_only** | — | 否 | 否 | 否 | 唯一 |
| **NA-04** | `我知道它还在，不用一直提醒。` | eligible，debt=5 | — | **required=false（用户主动免除）** | 低 | **never_notify**（本世代内） | — | 否 | 否 | 否 | 唯一 |
| **NA-05** | `别漏掉它，其他都行。` | eligible，debt=3 | — | **required=true**，`trigger=now` | 低 | **notify_now** | 可 | 否 | 否 | 在 | 唯一 |
| **NA-06** | （无任何表达）纯 starvation candidate | eligible，debt=6 | — | **无** | 低 | **record_only**（候选） | — | 否 | 否 | 否 | **K5-1**（`notification boundary`） |

## B. 提醒时机与触发条件（6）

| # | ① 用户原话 | ④ commitment / 条件 | ⑥ 输出 | ⑩ 下轮义务 | ⑪ K |
|---|---|---|---|---|---|
| **NB-01** | `这个以后提醒我。` | `required=true`，`trigger=**condition 未指定**` | **notify_later**（等一个合适时机：下一轮有空位 or 该事项再次被提到） | 在 | **K5-2**（`timing`：未指定即需时机判定契约） |
| **NB-02** | `如果今天还没排上再告诉我。` | `required=true`，`trigger=time_window + condition` | 条件未满足 → record_only；满足 → **notify_now** | 在（条件解除后失效） | 唯一 |
| **NB-03** | `这轮结束前如果还没动它，说一声。` | `trigger=round-boundary` | 本轮结束且未调度 → **notify_now**（并入轮末输出） | 在 | 唯一 |
| **NB-04** | `以后再说，但别忘。` | `delay` + `commitment(required=true)` | **notify_now 一次**（延迟≠不可见） | 在 | 唯一（**Q5 关键**） |
| **NB-05** | `先做别的，这个回头处理。` | 仅 `deprioritized`（无 commitment） | **record_only** | 否 | 唯一 |
| **NB-06** | `这个以后提醒我` → 下一轮用户又主动提到该事项 | `commitment` 仍在，事项被重新提及 | **commitment 视为已满足** → `discharged=true`；不再单独提醒 | 否 | 唯一 |

## C. 一次够不够 / 义务解除（6）

| # | 场景 | ⑥ 输出 | 义务 | ⑪ K |
|---|---|---|---|---|
| **NC-01** | 已提醒过一次，用户**未回应**，事项仍 eligible | **不重复提醒**（等下一次成功调度或无更紧迫输出时再考虑；**不得每轮催**） | 在 | 唯一（**一次够**） |
| **NC-02** | 已提醒过一次，用户回 `知道了` | `discharged=true` → **never_notify**；历史保留该 commitment 痕迹 | **解除** | 唯一（**Q3**） |
| **NC-03** | 已提醒过，用户回 `先放着吧` | 义务**降级**为 `record_only`（不解除承诺，但不再主动提） | 弱化 | 唯一 |
| **NC-04** | 已提醒过，用户回 `那你现在做吧` | 承诺达成（事项进入调度）+ 义务解除 | 解除 | 唯一 |
| **NC-05** | 用户在同一轮说了两次 `别忘` | **去重**：仍只提醒一次（不叠加） | 在 | 唯一 |
| **NC-06** | `discharged=true` 之后，该 gap 进入**新 resolution generation** | 旧承诺随旧世代结束；新世代需重新表达才有义务 | 否（除非重述） | 唯一 |

## D. 防通知骚扰 / 交互负担（6）

| # | 场景 | ⑤ burden | ⑥ 输出 | ⑪ K |
|---|---|---|---|---|
| **ND-01** | 2 个事项同时需要可见，且同属一簇 | 中 | **合并为一句**（不占轮次、不单独输出） | 唯一 |
| **ND-02** | 当前轮已有 R6 拍板事项 | 高 | **延后**（本轮不加提醒）→ `notify_later` | 唯一 |
| **ND-03** | 用户连续快速回复、明显不耐烦 | 高 | **仅 record_only**（本轮不提） | 唯一 |
| **ND-04** | 用户明确 delay 且**未**要求可见 | 低 | **never_notify**（不催已说过"以后"的事） | 唯一（**Q5 默认**） |
| **ND-05** | 同一 commitment 在 3 个周期内已被提醒 2 次 | 中 | **静默**（进入冷静期，等条件/世代变化） | 唯一 |
| **ND-06** | 提醒内容可完全并入既有输出（如本轮已有 ASK） | 中 | **合并且不新开轮次** | 唯一 |

## E. delay / deprioritized / starvation candidate 与提醒的关系（6）

| # | 场景 | ③ 状态 | ④ commitment | ⑥ 输出 | ⑪ K |
|---|---|---|---|---|---|
| **NE-01** | 纯 starvation candidate，无任何用户表达 | debt=6 | 无 | `record_only`（**不得据此主动提醒**） | **K5-1** 同类 |
| **NE-02** | `deprioritized` + 无 commitment | — | 无 | `record_only` | 唯一 |
| **NE-03** | `delay`（`OPEN+deferred`）+ 无 commitment | — | 无 | `never_notify` | 唯一 |
| **NE-04** | `delay` + `别漏掉` | — | **required=true** | `notify_now`（一次） | 唯一 |
| **NE-05** | `starvation candidate` + `不急，但别忘` | debt=7 | **required=true** | `notify_now`（一次，合并） | 唯一 |
| **NE-06** | 事项已被 Revision 作废（ineligible） | — | commitment 仍在 | `never_notify`（**对象已消失**：提醒一个不存在的事项无意义） | 唯一 |

---

## 五个问题的结论

### Q1 · 什么情况**必须**提醒

**必须**提醒 ⟺ `visibility_commitment.required = true` **且**其触发条件成立（`now`／`condition`／`time_window`／轮次边界），**且**该事项**仍存在且属于合法待处理集合**。

- **`visible commitment` 是"必须"的唯一来源**；`starvation candidate` **单独不足以**触发主动提醒（NA-06／NE-01 → `record_only` 候选）。
- `delay` **本身**不产生提醒义务（NE-03）；只有叠加用户显式可见要求时才提醒（NE-04／NB-04）。

### Q2 · 一次提醒够不够

**一次足够。** 未回应**不得**逐轮复催（NC-01）；同一承诺在同一世代内**去重**（NC-05）；已提醒 2 次后进入静默，等条件或世代变化（ND-05）。

### Q3 · 用户确认"知道了"后是否解除

**解除**：`discharged=true` → `never_notify`；但**历史保留**该 commitment 的痕迹（可审计）。相关形态：`先放着吧` → **降级为 record_only**（不解除承诺）；`那你现在做吧` → 承诺达成、义务解除；**新 resolution generation** 后旧承诺自动结束（NC-06）。

### Q4 · 如何防通知骚扰

五条（本轮的实测收敛）：

1. **一承诺一次**（NC-01／NC-05）；
2. **合并**：能并入既有输出就并入，不新开轮次（ND-01／ND-06）；
3. **负担优先**：`burden 高`（已有 R6 拍板／用户不耐烦）→ 延后或仅记录（ND-02／ND-03）；
4. **冷静期**：同承诺短周期内已提醒 → 静默（ND-05）；
5. **不催已明确 delay 且未要求可见的事**（ND-04）。

### Q5 · `delay` 情况是否允许提醒

| 情形 | 允许提醒？ |
|---|---|
| `delay`，**无** commitment | **不允许**（NE-03／ND-04） |
| `delay` ＋ `别漏掉` / `但别忘` | **允许，且一次为限**（NE-04／NB-04） |

即：**delay 决定"现在不处理"，不决定"是否可以提"**；后者由 `visibility_commitment` 决定。**两个维度不互相推导。**

---

## 关键架构验证

| 边界 | 结果 |
|---|---|
| Notification **不得改调度** | ✅ 30/30 全部"⑧ 改调度 = 否" |
| Notification **不得改 Gap／Action** | ✅ 30/30 全部"⑨ 改 Gap = 否" |
| `promotion ≠ notification` | ✅ Fairness 侧只提供 `starvation candidate` 作为**输入**；是否提醒完全由本层决定（NA-01 vs NA-02／NE-01 vs NE-05） |
| 三维度分离（调度公平／用户优先权／用户可见性） | ✅ 同一事项可同时 `deprioritized=true`（不提升）＋ `visibility_commitment=true`（必须可见）＋ 调度序不变（NA-01／NE-05） |

---

## K4 / K5

| 项 | 结果 |
|---|---|
| **K4** | **0** |
| **K5** | **2，两类** |
| └ **K5-1** | **`notification boundary`**：**纯 `starvation candidate`、无任何用户表达**时，是否应当主动提醒？（NA-06／NE-01 取 `record_only` 为候选，但"零表达→零提醒"是否是欠拟合，未证） |
| └ **K5-2** | **`timing`**：`这个以后提醒我` 中"以后"**未指定时机** → 需一条时机判定契约（`notify_later` 的触发条件） |

**处置**：按纪律**不自动补字段**；现有 `visibility_commitment{required, trigger, discharged}` 结构**够用**，缺的是**判定契约**（时机 + 零表达边界）。**待裁决**。

---

## 状态

| 项 | 状态 |
|---|---|
| Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3 | **未修改** |
| 新增字段 | **`visibility_commitment`（本层，不进 Scheduler、不改 Gap）** |
| 未新增 | Gap state／Action／Type／数值化通知频率评分 |
| 本轮产物 | 本文件（测试记录，仅测试） |
| 下一步（待裁决） | ① K5-1 零表达边界；② K5-2 时机判定契约；③ 是否把 Notification Policy 立为正式 sibling contract（`v1`） |

---

## 封口（V0.4.8-B 收口，例外 #25 预登记后执行）

**裁决已落盘**：[`notification-policy-contract.md`](notification-policy-contract.md) **v1**（正式 sibling contract）。

| K5 | 裁决 | 落盘 |
|---|---|---|
| **K5-1 `notification boundary`** | **零表达的 `starvation_candidate` 默认不主动提醒** → `record_only`；钉成 **`fairness evidence ≠ notification obligation`**；并保住例外：**任务结束前披露未完成内容属既有交付完整性责任**，不是 starvation 触发 | 合同 **第 5 条** |
| **K5-2 `timing`** | `以后提醒我` → **`condition = next_relevant_checkpoint`**（**不是**"下一轮"、**不是**"有空位"）；含机械定义、典型/非 checkpoint 清单、时机解析顺序 **1–5**；**默认不立刻反问"什么时候"** | 合同 **第 6 条** |

**本轮另落三条**：`visibility_commitment` 的定位原则（**可见性义务 ≠ 需求状态 ≠ 调度优先级**）｜**one commitment → at most one proactive notification**（禁止"第 1 次／第 2 次／冷静期"式次数债）｜**delay 四象限**表。

**回归**：原 **30/30 保持**｜**NPC-01～10 = 10/10 唯一**｜**K4 = 0、K5 = 0**｜Notification 改调度 **0**｜Notification 改 Gap **0**｜starvation 自动生成通知义务 **0**｜delay 无授权被催 **0**｜重复主动提醒 **0**｜sibling boundary regression 通过。

**V0.4.8-B Notification Policy = ✅ Contract v1 建立并冻结（2026-10-03）。O-3 整条债完成。**

---

## 追加更正（append-only，N06／N08 裁决）

> **纪律**：**保留历史结果，不改写历史正文**；正式规范来源以 **Notification Policy Contract v1**（含本轮 N 系列裁决）为准。
> **治理依据**：本更正表是 [`historical-discovery-governance.md`](historical-discovery-governance.md)（**D10 治理条款**）的**应用实例**——`治理规则 → N06 实际应用 → 本表的 C-03／C-06`。

| 历史条目 | 历史结论（**保留**） | **规范解释（superseded）** |
|---|---|---|
| **NA-01** `不急，但别忘。` | `trigger=now` → `notify_now` | **改判**：无时机的可见请求 → `trigger=condition`，`condition=next_relevant_checkpoint`（**N08 裁决**，D02 冲突封口） |
| **C-03** `不急，但别忘了` | "应提醒"（未指明 trigger） | **补明**：`trigger=condition = next_relevant_checkpoint`（同上） |
| **C-06** `无所谓，但别漏` | "应提醒"（未指明 trigger） | **补明**：同上 |
| **NB-01** `这个以后提醒我` | `notify_later` | **不变**（已被合同 §6.2 规则 4 覆盖） |

**关于"30/30"的表述（对应原审计 D10）**：本文的 **30/30** 是**历史测试记录**，**不得**被读作"所有结论至今未变"。正确读法：

```
30/30 = 当时 30 例均有唯一分析结果（历史事实）
≠ 全部结论保持有效（NA-01／C-03／C-06 的 trigger 判定已被后续合同裁决 supersede）
```

---

## 跨文档更正（append-only，N10 关联）

| 关联文档 | 历史记录 | 更正 |
|---|---|---|
| `pending-resolution-second-challenge-discovery.md` **PR-17 行** | 该行本就把 `算了，还是你来定吧。` 的 intent 记为 **`Authorization`** | **原分类即正确**；后续 Contract 把它按 R-2 处理是**误归** → 已由 **N10** 更正（见 defect ledger §N10）。**本记录不改写历史表格** |
