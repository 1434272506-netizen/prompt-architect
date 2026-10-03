# V0.4.6 · Priority Hint Language & Lifecycle Discovery（30 例破坏测试）

> **本轮只研究四件事**：自然语言 → **priority relation** → **scope** → **lifecycle / invalidation**。
> **不重新讨论**：Gap 状态／Action 类型／§11 问法／风险门／数值评分。
> **纪律**：**先破坏测试，暂不改 Priority Contract v1，不写新规则，不新增字段**。
> **O-3（scheduler starvation / fairness / 可见性）**：**不进本轮**，继续记观察。
> **上游**：[`priority-layer-contract.md`](priority-layer-contract.md)（`priority_hint{source, scope, relations}`）｜[`e2e-adaptive-replay.md`](e2e-adaptive-replay.md)（O-1／O-2）

**每个案例记录 11 项**：① 用户原话｜② 当前 active actions｜③ Layer 1 解析出的 priority relations｜④ `priority_hint.scope` 候选｜⑤ 是否含 `deprioritized`｜⑥ 是否同时含 delay／authorization／revision｜⑦ hard constraints｜⑧ effective scheduling｜⑨ 下一轮是否仍有效｜⑩ **Reason for expiry**｜⑪ 唯一／K4／K5。

**Reason for expiry 只允许五类**：`scope ended`｜`target removed`｜`superseded by newer hint`｜`Revision invalidated referent`｜`explicit cancellation`。**不得只写"失效了"。**

**五条不变量（Gate）**

```
H1  priority_hint 只表达偏序，不表达 gap 状态
H2  scope 生命周期不能泄漏到作用域外
H3  Revision 不应无脑删除所有旧 hint，只失效受影响的
H4  新 hint 可 supersede / shadow 旧 hint，但必须能解释哪个当前生效
H5  priority language 不得制造不存在的 dependency / blocker / risk
```

---

## 0. Layer 1 解析契约（本轮要验证的对象，**不新增机制**）

```
只产出「能确定的偏序边」，并集 ≤ 用户明确表达的边
不从"最重要"脑补完整排序（A ≻ {others} ≠ A ≻ B ≻ C）
不从顺序词生成 dependency（"A 做完再处理 B" ≠ A→B dependency）
不从"你判断"生成 relation（那是 authorization，不是 hint）
```

---

## A. 顺序表达解析（8 例）

**本组统一上下文**：`active actions = ASK(A)／ASK(B)／ASK(C)`（三项均合法、非阻塞、非 R6）；无其他反馈类型混入。

| # | ① 用户原话 | ③ 解析出的 relations | ④ scope 候选 | ⑦ hard | ⑧ effective scheduling | ⑨ 下轮有效 | ⑩ Reason | ⑪ 唯一 |
|---|---|---|---|---|---|---|---|---|
| **A-01** | `先 A 再 B。` | `A ≻ B` | `current_round` | 无 | A → B | 否 | `scope ended` | **唯一** |
| **A-02** | `A 比 B 重要。` | `A ≻ B` | `current_round` | 无 | A → B | 否 | `scope ended` | **唯一** |
| **A-03** | `优先做 A。` | `A ≻ {others}`（**不脑补 B 与 C 之间**） | `current_round` | 无 | A → (B、C 默认序) | 否 | `scope ended` | **唯一** |
| **A-04** | `B 放后面。` | `{others} ≻ B`（**不脑补 A 与 C 之间**） | `current_round` | 无 | (A、C 默认序) → B | 否 | `scope ended` | **唯一** |
| **A-05** | `A 和 B 都重要，但先 A。` | `A ≻ B` | `current_round` | 无 | A → B | 否 | `scope ended` | **唯一** |
| **A-06** | `A > B > C。` | `A ≻ B`、`B ≻ C`（＋传递闭包 `A ≻ C`） | `current_round` | 无 | A → B → C | 否 | `scope ended` | **唯一** |
| **A-07** | `A 做完再处理 B。` | `A ≻ B` —— **且明确不生成 `A → B` dependency** | `current_round` | 无 | A → B；**§11.6 依赖判定不参与** | 否 | `scope ended` | **唯一**（H5 ✓） |
| **A-08** | `A、C 优先，B 最后。` | `A ≻ B`、`C ≻ B`（**A 与 C 之间无序**） | `current_round` | 无 | (A、C 默认序) → B | 否 | `scope ended` | **唯一** |

**组 A 结论**：8/8 得到**明确偏序**，且**没有一例被脑补成完整全序**或**被误升级为 dependency**。

---

## B. scope 判定（8 例）—— 重点打 **O-1**

| # | ① 用户原话 | ④ scope 候选 | ② active actions | ⑦ hard | ⑧ effective scheduling | ⑨ 下轮有效 | ⑩ Reason | ⑪ 唯一 |
|---|---|---|---|---|---|---|---|---|
| **B-01** | `这轮先处理首页。` | `current_round` | ASK(首页)、ASK(页脚) | 无 | 首页 → 页脚 | 否 | `scope ended` | **唯一** |
| **B-02** | `现在先看性能。` | `current_round` | ASK(性能)、ASK(视觉) | 无 | 性能 → 视觉 | 否 | `scope ended` | **唯一** |
| **B-03** | `今天先做 A。` | **`current_round` 或 `whole_task`（时间窗）** | ASK(A)、ASK(B)、ASK(C) | 无 | A 先；**但"今天"跨越多个调度周期** | 是（若判 `whole_task`）／否（若判 `current_round`） | 取决于判定 | **K5 · scope 歧义** |
| **B-04** | `这个模块里先 A 后 B。` | `current_cluster` | ASK(A)、ASK(B)、ASK(模块外项 C) | 无 | A → B；**C 不受影响** | 是（cluster 内有效） | `scope ended`（cluster 完成） | **唯一** |
| **B-05** | `接下来都优先移动端。` | `whole_task` | ASK(移动端布局)、ASK(桌面端布局) | 无 | 移动 → 桌面（持续） | **是** | （未失效） | **唯一** |
| **B-06** | `整个项目性能优先视觉。` | `whole_task` | ASK(性能)、ASK(视觉) | 无 | 性能 → 视觉（持续） | **是** | （未失效） | **唯一** |
| **B-07** | `以后只要冲突就性能优先。` | `whole_task`（**条件型全局**） | ASK(性能)、ASK(视觉) | 无 | 仅当两者**同时为候选且冲突**时生效 | **是** | （未失效） | **唯一** |
| **B-08** | `先把这几个问题解决完。` ＋ **本轮一次调度两个 ASK（bundle）** | `current_cluster`（"这几个问题"＝该批） | ASK(q1)、ASK(q2) 同轮发出 | 无 | q1 → q2；**用户只答 q1 后，q2 的后续调度仍须由同一 hint 主导** | 是（bundle 未完成） | `scope ended`（bundle＋该批完成） | **唯一** |

### B 组特别结论 · O-1 的两种解释对照

| 解释 | 定义 | B-08 的结果 | 缺陷 |
|---|---|---|---|
| **Interpretation A** | `current_round` 在**用户下一次反馈后**失效 | 用户答 q1 → hint 立即失效 → **q2 的后续调度丢 hint**（同一 bundle 被作用一半） | ❌ 半作用 + 可能导致顺序回退 |
| **Interpretation B** | `current_round` 在**完成本次 assistant action bundle 后**失效 | hint 覆盖整个 bundle → q2 排序一致 | ✅ 无半作用、无泄漏 |

**本轮判定（仅作为测试结论，不落规则）**：**Interpretation B 胜出**——`round` 语义应**绑定一次调度周期**（bundle），而不是绑定"某条消息"。与用户倾向一致。

### B-03 的 K5 定位

- **歧义类型**：**scope 歧义**（时间窗表达 `今天` 在 `{current_round, current_cluster, whole_task}` 中没有对应项）。
- **两读法**：① 近似 `current_round`（今天这段时间内的本轮）；② 最近似 `whole_task`（今天整段会话持续生效）。
- **结论**：**现有 `source / scope / relations` 三字段不足**（缺"时间窗 scope"）；但按纪律 **本轮不新增字段、不补规则**，记为 **V0.4.7 输入**。
- **可选最小修法（不落盘）**：新增 `scope: timed{until}`，或规定"时间窗表达 → 取最近似 `whole_task` 并附到期时间"。**待裁决**。

---

## C. 生命周期 / Revision（6 例）

| # | ① 用户原话（上下文） | ③ relations | ④ scope | 旧 hint 处置 | ⑧ effective scheduling | ⑨ 下轮有效 | ⑩ Reason | ⑪ 唯一 |
|---|---|---|---|---|---|---|---|---|
| **C-01** | `整个项目性能优先视觉。` → 后来 `目标从手游改成企业后台。` | `性能 ≻ 视觉` | `whole_task` | **keep**（两个 referent 仍活跃，比较关系未被目标变化推翻） | 仍 性能 → 视觉 | **是** | （未失效） | **唯一**（H3 ✓） |
| **C-02** | `当前模块先 A 后 B。` → **该模块完成** | `A ≻ B` | `current_cluster` | **expire** | 不再参与 | 否 | **`scope ended`** | **唯一** |
| **C-03** | `A 优先 B。` → **A 已 `CLOSED`** | `A ≻ B` | `current_round`／`current_cluster` | **keep（no-op）**：A 不候选时该边无调度影响；A 若重开仍生效 | B 按默认序 | 是（保留） | （未失效） | **唯一** |
| **C-04** | `A 优先 B。` → **A 被 `INVALIDATED`** | `A ≻ B` | 同 C-03 | **keep**：hint 针对 **gap 的调度顺序**，不是值；A 的 gap 仍活跃（需重新消解） | A 重新消解 → 仍 A 先 | 是 | （未失效） | **唯一**（H3 ✓） |
| **C-05** | `首页优先动画。` → **用户把首页删掉** | `首页 ≻ 动画` | `current_cluster` | **expire** | 不再参与 | 否 | **`target removed`** | **唯一** |
| **C-06** | `全局移动端优先。` → 随后 `这个阶段桌面端先。` | 旧：`移动 ≻ 桌面`(whole_task)；新：`桌面 ≻ 移动`(current_cluster) | 旧 `whole_task` **保留**；新 `current_cluster` | **temporarily shadow**（**不是删除**） | 当前：桌面 → 移动；**cluster 结束后全局 hint 自动恢复** | 旧 hint 是 | `explicit cancellation`（仅当用户明确取消时）；本例为 **shadow**，无 expiry | **唯一**（H4 ✓） |

**组 C 结论**：三种结果（`keep`／`expire`／`temporarily shadow`）**互相可区分**；**Revision 未导致无脑删除**（C-01／C-04 均 keep）；**局部更强 hint 未被误处理成永久删除**（C-06）。

---

## D. 冲突 / 条件 / 复合表达（8 例）

| # | ① 用户原话 | ③ relations | ⑤ ⑥ 其他成分 | ⑦ hard | ⑧ effective scheduling | ⑨ 下轮有效 | ⑩ Reason | ⑪ 唯一 |
|---|---|---|---|---|---|---|---|---|
| **D-01** | `先 A，不过 B 更关键就你决定。` | `A ≻ B` | ＋**authorization（授权 scheduler 调整偏序）**；**不是** dependency、**不是** blocker | 无 | A → B；若现况显示 B 关键，授权允许改序 | 是（round 内） | （未失效） | **唯一**（H5 ✓） |
| **D-02** | `先 A，但如果 B 是阻塞项就先 B。`（同构：`先 A，但 B 如果风险更高就先 B`） | `A ≻ B` | ＋**条件**（B ∈ 硬约束时翻序） | 条件触发时 B 为 blocker | 条件不成立：A → B；成立：**B → A**（硬约束本来优先） | 是 | （未失效） | **唯一**（H5 ✓） |
| **D-03** | `A 和 B 都可以，你判断哪个更关键。` | **∅（不产出 relation）** | ＋**authorization（授权排序）** | 无 | 按默认序（§11.1 一级＋二级） | 否 | `scope ended` | **唯一**（H1 ✓） |
| **D-04** | `先性能，再视觉，不过别影响上线时间。` | `性能 ≻ 视觉` | ＋**硬约束（上线时间）** | 上线时间为硬约束 | 性能 → 视觉；**冲突时上线时间胜** | 是 | （未失效） | **唯一** |
| **D-05** | `A 最重要；等等，B 才是最重要。` | 新：`B ≻ {others}`；旧：`A ≻ {others}` | ＋**同轮自我修正** | 无 | B → (A、C 默认序) | 是（新 hint） | **`superseded by newer hint`**（**仅失效旧的一条**，不删其他 hint） | **唯一**（H4 ✓） |
| **D-06** | `先 A 再 B；不对，先 B 再 A。` | 新：`B ≻ A` | ＋反转 | 无 | B → A | 是（新） | **`superseded by newer hint`** | **唯一** |
| **D-07** | `颜色暂时不管，性能优先。` | `性能 ≻ 颜色` | ＋**`deprioritized`（颜色）**；**不是 delay** | 若颜色属 R6 → 降权**不生效** | 性能 → 颜色（排后但仍待决） | 是（hint）；降权按 scope 到期 | `scope ended` | **唯一** |
| **D-08** | `先 A，B 以后再说。` | `A ≻ B` | ＋**`delay`(B) —— 必须拆成两个事件** | 无 | A 先；B 转 `OPEN + deferred`（**由 Interface §3 承担，不进 hint**） | hint 是；B 的 defer 由 Interface 管 | `scope ended`（hint）／Interface 状态另行 | **唯一**（**O-2 收口** ✓） |

**组 D 结论**：8/8 唯一；**没有一例把 authorization／delay／deprioritized 塞进 `relations`**；**没有一例把"条件性授权"生成为 dependency 或 blocker**（H5 ✓）。

### D-07 的 `deprioritized` vs `delay` 边界（本轮确立的判定口径）

```
"不管 / 不处理 / 以后再决定"  → delay      （gap 状态：OPEN + deferred，可问、待拍板）
"排后面 / 不急 / 优先级低"    → deprioritized（纯调度；gap 状态不变）
```

（该口径属**判定契约**，不需要新字段。）

---

## 五条不变量验证

| 不变量 | 结果 | 取证 |
|---|---|---|
| **H1** `priority_hint` 只表达偏序，不表达状态 | ✅ | D-03（授权判定**不产出** relation）；全部 A 组只产出边，无状态写回 |
| **H2** scope 不泄漏到作用域外 | ✅ | B-01/02（round 内）／B-04（cluster 外项 C 不受影响）／B-05/06/07（whole_task 持续）；E2E-10 已验过期零泄漏 |
| **H3** Revision 不无脑删 hint，只失效受影响的 | ✅ | C-01（目标变更后 **keep**）／C-05（**target removed → expire**）／C-04（值失效但 gap 活跃 → **keep**） |
| **H4** 新 hint 可 supersede/shadow，且可解释哪个生效 | ✅ | D-05／D-06（**supersede**）／C-06（**shadow + cluster 结束自动恢复**） |
| **H5** priority language 不制造 dependency/blocker/risk | ✅ | A-07（顺序 ≠ 依赖）／D-01（条件性授权 ≠ dependency）／D-02（条件 ≠ 新 blocker） |

---

## 通过标准核对

| 项 | 结果 |
|---|---|
| 30/30 均有明确解析结果 | ✅ **30/30**（A 8／B 8／C 6／D 8） |
| 错误状态写回 | **0** |
| 错误 Action 改写 | **0** |
| 硬约束被 hint 越过 | **0** |
| scope 泄漏 | **0** |
| 把 delay／refused 当 priority | **0**（D-08 专项拆分） |
| 把 priority 当 dependency | **0**（A-07／D-01／D-02） |
| **K4** | **0** |
| **K5** | **1** —— **B-03**，定位到 **scope 歧义**（时间窗表达在 `{current_round, current_cluster, whole_task}` 无对应项） |

**K5 处置**：按纪律**不自动补字段**。核对现有 `source / scope / relations` 三字段——**结构足够**，缺的是**判定契约**（时间窗 → 最近似 scope 的映射 + 到期语义）。因此**不需要改 Contract 结构**，只需补一条判定口径（**待裁决**）。

---

## O-1 / O-2 收口

| # | 原观察 | 本轮结论 |
|---|---|---|
| **O-1** | `current_round` 的"一轮"边界未定义 | **Interpretation B 胜出**：绑定**一次调度周期（action bundle）**，而非"某条消息"；证据 = B-08（A 解释会让同一 bundle 后半段丢 hint） |
| **O-2** | "顺序偏好 + 延后决定"同句 | **必须拆两事件**：`priority_hint(A ≻ B)` ＋ `delay(B)`（gap 状态由 Interface §3 承担）；证据 = D-08 |
| O-3 | scheduler starvation 可见性 | **仍未进入本轮**，继续观察（属下一层：fairness / notification policy） |

---

## 边界与状态

| 项 | 状态 |
|---|---|
| Priority Contract v1 | **未修改** |
| §11／V0.3／Interface v1–v3／§10 | **未修改** |
| 新增规则／字段／Action／Type／Gap state | **无** |
| 数值评分 | **未设计** |
| 本轮产物 | 本文件（测试记录，仅测试） |
| 下一步（待裁决） | ① B-03 的判定契约（时间窗 → scope 映射）；② 是否把 O-1 结论（round = 调度周期）正式写入 Contract；③ `deprioritized` vs `delay` 的判定口径是否入册 |

---

## 封口（V0.4.6 收口，例外 #21 预登记后执行）

**裁决已落盘**：[`priority-layer-contract.md`](priority-layer-contract.md) **§9（L1–L3）**。

| # | 增量 | 内容 |
|---|---|---|
| **L1** | `scope` 与 temporal lifetime **正交** | `scope ∈ {current_round, current_cluster, whole_task}` ＋ 可附 **`valid_until`**／expiry condition；**不新增 `timed` scope**；结构作用域无更窄证据时取 `whole_task`，由 `valid_until` 限生命周期 |
| **L2** | `current_round` 正式定义 | = **一次 scheduler action bundle 的完整生命周期**（起于 bundle 生成，止于 bundle 全部完成／被取消／失效并触发重排）；**单条 user/assistant 消息不自动结束它** |
| **L3** | `deprioritized` vs `delay` | 按**效果**区分，**不按关键词**；机械判据＝"**还能不能在当前处理窗口里顺手处理？**"（能但别优先→`deprioritized`；现在不要处理→`delay`）；关键词仅作 cue，不足时一次最小澄清 |

### 收口后的重跑结果

| 项 | 结果 |
|---|---|
| **B-03（原 K5-1）** | **K5 消失** —— `今天先做 A` → `A ≻ {others}` ＋ `scope=whole_task` ＋ `valid_until=今天结束`（**唯一**） |
| 原 30/30（A／B／C／D） | **30/30 保持**（L1–L3 未改变任何一例既有结论） |
| **PHC-01～PHC-08** | **8/8 唯一** |
| K4 / K5 | **0 / 0** |
| scope leakage | **0** |
| delay / prioritization 混淆 | **0** |
| 未新增 | ❌ `timed` scope ❌ Gap 状态 ❌ Action ❌ Type ❌ 数值权重 |

**V0.4.6 Priority Hint Language & Lifecycle = ✅ 正式冻结（2026-10-02）。**

**O-3**（连续多轮 `deferred_by_capacity` 的 starvation / fairness / 可见性）**仍不进本轮**，单列下一阶段。
