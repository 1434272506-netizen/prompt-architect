# V0.5 Architecture Candidates（只记录，不改 V0.4）

> **用途**：把 V0.4 closure 过程中**发现的架构级认识**留下，避免"封版即掩埋"。
> **纪律**：**只记录发现**；**不改 V0.4 任何冻结正文**；是否建模留待 V0.5。

---

## C1 · Authority / Value Separation

**来源**：N10（原审计 D03 / PR-17）

```
Decision Authority        ≠   Value Commitment
（"你来定 / 你看着办"）        （"就按 X"）
        ↓                            ↓
   Authorization                 R-2 confirmatory
        ↓                            ↓
 不产生 CONFIRMED               → CONFIRMED
```

**V0.4 内的最小形态**：只是一条**分类边界**（`pending-resolution-transition-contract.md` §3.5），不新增字段、不新增状态。

**V0.5 可选方向**：是否把"决定权"与"值承诺"显式建模为两个可独立追踪的对象（例如：授权本身可被撤销而不影响已承诺的值；或值承诺可独立于授权来源审计）。

**价值判断**：这是**语义所有权**问题——谁来承担"值是对的"这一责任。V0.4 只做到"不把两者混为一谈"。

---

## C2 · Notification lifecycle decomposition

**来源**：N08 / N09（Notification Policy Contract v1）

```
Commitment  →  Trigger  →  Delivery  →  Discharge
（可见性义务）  （时机解析）  （兑现/延后）  （解除）
```

| 阶段 | V0.4 已有表达 |
|---|---|
| Commitment | `visibility_commitment{required, trigger, discharged}` |
| Trigger | 判定表 7 行（`now`／`time_window`／`condition`／复用恢复条件／"以后"→checkpoint／裸"别忘了"→checkpoint／最小澄清） |
| Delivery | `notify_now`／`notify_later`／`record_only`／`never_notify` |
| Discharge | `discharged`（本层内部状态，非 Gap 写回） |

**V0.5 可选方向**：这四段是否应成为**独立的可观测状态机**（而非合同内的判定表），尤其是：
- Trigger 与 Delivery 分离后，`burden` 只作用于 Delivery（系统自选时机的兑现时刻）——已在 V0.4 确立，是否显式化；
- 是否需要一个**跨会话/跨任务**的可见性承诺载体（V0.4 明确不含）。

**价值判断**：这一切分的核心收益是**不发明计数器**——用"阶段化"替代"次数化"。

---

## 待观察（尚未成熟，暂不编号）

| 候选 | 来源 | 状态 |
|---|---|---|
| **Participation / Information provision / Decision authority 是三个不同维度** | **D05（CS-05）** | 只记录：**不要从"谁参与"推导"谁拥有决定权"**；与 C1（`authority transfer ≠ value acceptance`）同属一族纪律：`information source ≠ decision authority`。**不改 V0.4 ontology** |
| Fairness evidence 的**跨会话持久化** | N04 HOLD（`≥1` 门槛未落） | 证据不足，不建模 |
| `scheduler fairness` 与 `notification` 的**共享证据账本边界** | Fairness §3 ／ Notification 第 2 条 | 已确立"共享证据、互不写权"；更细的账本 schema 留待 V0.5 |
| 用户可见性承诺的**跨任务迁移**（任务结束时未兑现的 commitment 何去何从） | V0.4.9 剧本 3（任务收尾处仅披露未完成项，非 Notification） | 已明确"由交付完整性负责"，是否合并入 Notification 留待 V0.5 |
| **askable 成员资格 vs 当前调度资格**（两个维度） | **D06（CS-06）** | 只记录：`askable` 描述"该类 Gap 是否属于 ASK 可处理的需求类别"；`eligibility/scheduling` 描述"当前执行窗口" |
