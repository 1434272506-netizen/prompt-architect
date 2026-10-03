# V0.4.7 · Scheduler Fairness & Starvation Discovery（30 例破坏测试）

> **本轮只做破坏测试**：不写公平策略、不新增 aging 字段、**不改 Priority Contract v1.1**。
> **核心问题不是"排队多久算久"，而是先确认：什么才算真正的 starvation。**
> **禁止**：❌ priority score ❌ "连续 3 轮必须提升" ❌ 新 Gap state ❌ 新 Action／Type ❌ 改 Priority Contract v1.1／Interface／§11／V0.3。
> **上游**：[`priority-layer-contract.md`](priority-layer-contract.md)（§9 L1–L3）｜[`e2e-adaptive-replay.md`](e2e-adaptive-replay.md)（O-3）

**第一条边界（本轮要检验的假设）**

```
合法且当前可执行（eligible）
+ 连续因 round_capacity / 其他软排序因素未被调度
= starvation candidate

以下都【不算】starvation：
  SUSPENDED ／ delay ／ dependency 尚未满足 ／ 被 R6·R14·R4 挡住 ／
  动作已失效 ／ gap 已 CLOSED
```

**每例记录 11 项**：① action／gap identity｜② 当前是否 eligible｜③ 未被调度的**真实原因**｜④ 连续几次 eligible-but-unscheduled（**观测数据，暂非规则**）｜⑤ hard constraints｜⑥ priority_hint／deprioritized｜⑦ round_capacity｜⑧ 本轮 effective scheduling｜⑨ 是否应获得 **fairness consideration**｜⑩ 是否应**用户可见提醒**｜⑪ K4／K5／是否需要新字段。

---

## A. 真 starvation（6）——纯容量／软排序竞争

| # | ① identity | ② elig | ③ 真实原因 | ④ 连续 | ⑤ hard | ⑥ hint／depri | ⑦ cap | ⑧ effective sched | ⑨ fairness | ⑩ 提醒 | ⑪ K／字段 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **A-01** | gap C（普通 ASK） | ✅ | **仅容量**：R1 {A,B}／R2 {A,D}／R3 {E,F} 各占满 2 席 | **3** | 无 | 无 | 2 | 三轮均未含 C | **应获**（候选） | 待 E 组判 | 唯一；debt 跨轮留证→**需证据** |
| **A-02** | gap C（普通 ASK） | ✅ | 仅容量（cap=1，每轮都有更强软序对手） | **2** | 无 | 守默认序 | 1 | 未含 C | **应获**（候选） | 待 E 组判 | 唯一（**不设阈值**） |
| **A-03** | gap C（唯一非阻塞非风险项） | ✅ | 仅容量：对手都是高价值但**非硬约束**项 | **3** | 无 | 无 | 2 | 未含 C | **应获** | 待 E 组判 | 唯一 |
| **A-04** | gap C，处于 `ASK(q1)+ASK(q2)` **同一 bundle** | ✅ | 同 bundle 内顺序未轮到（**bundle 未结束**） | **0**（跨轮计数） | R4（bundle 内顺序） | 无 | 2 | q1 先 | **否** | 否 | 唯一（**同 bundle 未完成 ≠ 跨轮 starvation**） |
| **A-05** | **同一 gap**，动作由 `ASK` 被 V0.3 重算为 `SHOW` | ✅ | 仅容量：两轮被更强软序对手挤出 | **继承 2** | 无 | 无 | 2 | 未含该 gap | **应获**（**继承等待史**） | 待 E 组判 | 唯一（**F5：debt 绑 gap identity + generation，不绑 action 类型**） |
| **A-06** | **全新 gap**（同主题、同 `resolution=ASK`；旧 gap 已 `CLOSED(assumed)`） | ✅ | 新 gap 首轮未排上（容量竞争） | **0**（从零计） | 无 | 无 | 2 | 未含 | 否（首轮） | 否 | 唯一（**F5：新 identity ⇒ 不继承旧债**） |

## B. 假 starvation（6）——"等得久"不能单独触发 fairness

| # | ① identity | ② elig | ③ 真实原因 | ④ 连续 | ⑤ hard／状态 | ⑧ effective sched | ⑨ fairness | ⑩ 提醒 | ⑪ K |
|---|---|---|---|---|---|---|---|---|---|
| **B-01** | gap C | ❌ | **dependency 未满足**（上游 D 未决） | 3（但**不 eligible**） | §11.6 约束型依赖 | 先 D | **否** | 否 | 唯一 |
| **B-02** | gap C | ❌ | **`SUSPENDED(external_owner)`** | 3 | Interface §9.5 | 不调度 | **否** | 否 | 唯一 |
| **B-03** | gap C | ❌ | **用户明确 delay**（"以后再说"） | 3 | `OPEN + deferred` | 不参与正常调度 | **否** | **否**（已 delay，不得催） | 唯一（**delay 误当 starvation = 0**） |
| **B-04** | gap C | ❌ | **R6 上游未拍板** | 3 | R6 mandatory | 先上游 | **否** | 否 | 唯一 |
| **B-05** | 旧 action（已被 Revision `INVALIDATED`） | ❌ | **动作已失效** | 3 | — | 不调度 | **否** | 否 | 唯一（**失效不继承等待债 = 0 违规**） |
| **B-06** | SHOW 待反应 | ❌ | **R4：SHOW 结果未处理完不得展开下一动作** | 2 | R4 | 先处理 SHOW | **否** | 否 | 唯一 |

## C. starvation × 用户 priority（6）——本轮最关键组

| # | ① identity | ③ 真实原因 | ④ 连续 | ⑥ hint／depri | ⑧ effective sched | ⑨ fairness | ⑩ 提醒 | ⑪ K |
|---|---|---|---|---|---|---|---|---|
| **C-01** | gap C（普通 ASK） | 用户多次 `A 最重要，C 放后面`（`whole_task` hint）＋容量 | 3 | **soft hint A ≻ C** | A 先，C 未排 | **三候选语义并列**：① 永远尊重用户排序 ② fairness 压过 soft hint ③ 不压但提醒 | ③ 需提醒 | **K5-1**（`fairness vs user preference`） |
| **C-02** | gap C | 用户 `C 不急`（`deprioritized`）＋容量 | **10** | **deprioritized** | C 始终排后 | **否**——**这是忠实执行用户偏好，不是系统不公平** | 否 | 唯一（**F3 核心**） |
| **C-03** | gap C | 用户 `C 不急，但别忘了` | 10 | `deprioritized` ＋**用户显式"别忘"** | C 仍排后 | **否**（不提升） | **应提醒**（用户已要求不遗忘） | 唯一；**`must_not_starve` 需求证据成立**（本轮**禁止新增字段**） |
| **C-04** | gap C（桌面端项） | 用户 `whole_task` hint `移动端优先` ＋容量 | 4 | **soft hint（全局）** | 移动端先 | **与 C-01 同类未决** | 待定 | **K5-1 同类实例** |
| **C-05** | gap C（**不在**任何 hint 中） | 同 A-01：纯容量，对手是不同项 | 3 | 用户 hint 只覆盖 `A ≻ B` | 未含 C | **应获**（C 未受用户偏好影响） | 待 E 组判 | 唯一 |
| **C-06** | gap C | 用户 `C 无所谓，但别漏` | 6 | `deprioritized` ＋"别漏" | 排后 | 否 | **应提醒** | 唯一（与 C-03 同族） |

## D. fairness × hard constraints（6）——公平**永远不能越过硬门**

| # | ① identity | ④ 连续 | ⑤ hard 竞争者 | ⑦ cap | ⑧ effective sched | ⑨ fairness | ⑪ K |
|---|---|---|---|---|---|---|---|
| **D-01** | 普通 ASK C（等久） | 4 | **新出现 R6 blocker** | 2 | **R6 先**，C 顺延 | 不能越过 | 唯一 |
| **D-02** | 普通 ASK C | 4 | **R14 high-risk C** | 2 | **TEACH＋ASK 同轮并列**（R14） | 不能越过 | 唯一 |
| **D-03** | 普通 ASK C | 5 | **R4 强制顺序**（同轮 INSPECT 未做） | 2 | **INSPECT 先** | 不能越过 | 唯一 |
| **D-04** | 普通 ASK C（依赖未决 D） | 3 | **§11.6 约束型依赖** | 2 | **D 先** | 不能越过 | 唯一 |
| **D-05** | 普通 ASK C | 5 | **R6 blocker** | **1** | **R6 先** | 不能越过 | 唯一 |
| **D-06** | gap 是**阻塞项**，但其 action 被算作 `DISCOVER` | 3 | **R6：阻塞项不可 DISCOVER** | 2 | 该 action **不合法** → 重新选动作 | **不适用**（问题在 eligibility，非 fairness） | 唯一 |

**D 组结论**：6/6 证明 **"C 等太久了所以先做 C" 永远打不穿 hard scheduling constraint**。

## E. notification / user visibility（6）——O-3 的另一半

| # | ① identity | ③ 状态 | ⑨ fairness | ⑩ 提醒 | 判据 | ⑪ K |
|---|---|---|---|---|---|---|
| **E-01** | 普通非阻塞 gap C，等 3 轮 | eligible，容量挤压 | 候选（待裁） | **应提醒一次**（可忽略、不占轮次） | 提醒 ≠ 提升：只给用户一个选择 | 唯一 |
| **E-02** | gap C | **用户已 delay**（"以后再说"） | 否 | **不得提醒** | 已明确不要处理 → 催办 = 打扰 | 唯一 |
| **E-03** | 普通 C | 容量**持续**被 R6／R14 占满 | 否（ineligible 于容量层面） | **只记录、不提醒** | 用户无行动空间，提醒无意义 | 唯一 |
| **E-04** | gap C | 用户 `别漏掉 C` | 否（不提升） | **必提醒**（义务升级） | 用户的显式要求改变的是**通知策略**，不是调度 | 唯一；`must_not_starve` 证据 |
| **E-05** | gap C | 已 `deprioritized`，用户说过"不急" | 否 | **不提醒** | 尊重偏好、避免打扰 | 唯一 |
| **E-06** | gap C（同簇内有更强上位项） | 容量挤压 | 候选 | **合并提醒**（同轮一句话带过，不单独占轮次） | 提醒可被"并入既有输出"而非新开轮次 | 唯一 |

---

## F1–F5 五个问题的结论

### F1 · starvation 的最小定义

**"连续没执行"太宽**（B 组 6 例全部证伪）。最小定义收敛为：

```
starvation candidate ⟺
  ① 当前 eligible（动作合法、gap 活跃、非 SUSPENDED／非 deferred）
  ∧ ② 未被调度的真实原因是 round_capacity 或软排序竞争
  ∧ ③ 无 hard constraint 阻断
  ∧ ④ 跨**调度周期**计数 > 0（同一 bundle 内未轮到不算 —— A-04）
```

**阈值不假定**：A-02（2 轮）与 A-01（3 轮）都只作**观测数据**；本轮**不规定**"几轮必须提升"。

### F2 · fairness 能覆盖什么

| 可被 fairness 修正 | **绝不能被覆盖** |
|---|---|
| 默认序竞争、纯容量挤压（A 组）、不在任何 hint 中的项（C-05） | **R6 blocker／R14 high-risk C／R4 顺序／§11.6 约束型依赖**（D 组 6/6） |
| 未决（K5）：**用户显式 soft hint**（C-01／C-04） | 用户显式 `delay`（B-03／E-02——本就不 eligible） |

### F3 · 用户明确降权后还存在 starvation 吗

- **`deprioritized`（"C 不急"）连续 10 轮未做 ⇒ 不是 starvation**（C-02）：这是**系统忠实执行用户偏好**，不是不公平。
- **但**"不急，**但别忘了**"产生一个**新需求证据**：`must_not_starve`（C-03／C-06／E-04）——其效果是**通知义务**，**不是**自动提升。
- **本轮禁止新增该字段**；证据已足够说明需求真实存在，字段设计留待下一轮（Fairness Contract 是否独立建层）。

### F4 · fairness promotion 与 notification 是否必须分开

**必须分开。** 证据：**应提醒但不应提升**（E-01／E-03／E-04）与**可提升但无需提醒**（A-02、C-05、D 组中的容量竞争）同时存在。

```
scheduler fairness   → 改变**调度结果**（可能挤压他人）
notification policy  → 只改变**用户可见性**（不改调度）
```

### F5 · starvation debt 跟谁绑定

**绑 `gap identity + 当前 resolution generation`，不绑 action 类型。**

| 情形 | 等待史 | 取证 |
|---|---|---|
| **同一 gap**，动作 `ASK → SHOW`（V0.3 重算） | **继承** | A-05 |
| **全新 gap**（同主题、同 `ASK`；旧 gap 已 `CLOSED`） | **不继承** | A-06 |
| 动作已被 Revision `INVALIDATED` | **不继承** | B-05 |

（`generation` = 该 gap 自上次值变更／重开以来的一代；仅作**假设**，不落字段。）

---

## 通过标准核对

| 项 | 结果 |
|---|---|
| 30/30 有明确分析结果 | ✅ **30/30**（A 6／B 6／C 6／D 6／E 6） |
| 把 **ineligible 误判成 starvation** | **0**（B 组 6/6、D-06） |
| **fairness 越过 hard constraint** | **0**（D 组 6/6） |
| **delay 被误当 starvation** | **0**（B-03、E-02） |
| **失效 action 继承等待债** | **0**（B-05、A-06） |
| **K4** | **0** |
| **K5** | **2 例，同一类** —— **C-01／C-04**，类别 = **`fairness vs user preference`**（fairness 能否压过用户显式 soft hint，三种候选语义未定） |

**K5 处置**：按纪律**不自动补字段、不补规则**。核对现有 `priority_hint` / `deprioritized` / `hard constraints` —— **表达力足够**，缺的是**判定契约**（用户 soft hint 与 fairness 的优先关系）。**待裁决**。

---

## 是否需要一个 fairness ledger（证据，不设计）

| 证据 | 指向 |
|---|---|
| A-01／A-02／A-03／A-05：需要**跨轮**知道"连续几次 eligible-but-unscheduled" | 单轮 `deferred_by_capacity` **不够**（它是每轮派生物）→ 需要**跨轮留存**的观测 |
| A-06／B-05：新 identity／失效 action **必须清零** | 观测需绑 **gap identity + generation**（F5） |
| C-03／C-06／E-04：`must_not_starve` 的**通知义务** | 属 notification policy，**不是**调度债 |
| E-04：用户要求改变的是**通知策略** | 进一步支持 F4（两层分离） |

**结论**：证据支持"可能需要一个 fairness 观测/账本"，但**本轮不设计、不新增字段**；下一轮再决定 **Fairness Contract** 与 **Notification Policy** 是否独立建层。

---

## 边界与状态

| 项 | 状态 |
|---|---|
| Priority Contract v1.1／Interface／§11／V0.3 | **未修改** |
| 新增字段／Gap state／Action／Type／priority score | **无** |
| "连续 3 轮必须提升" | **未规定**（④ 仅观测） |
| 本轮产物 | 本文件（测试记录，仅测试） |
| 下一步（待裁决） | ① C-01／C-04 的判定契约（fairness vs 用户显式 soft hint）；② 是否需要 **Fairness Ledger**（跨轮观测 + identity＋generation）；③ `must_not_starve` 是否成立为独立需求；④ **Fairness Contract / Notification Policy 是否独立建层** |
