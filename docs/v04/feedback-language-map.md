# V0.4.2 Phase 2.2 · Feedback Language Map（表达 → 意图槽位的最小映射契约）

> **目标（用户限定）**：建立**最小映射契约**，不是做 NLP 分类器。
> **禁止**：大模型分类／embedding／权重／机器学习／情感或性格判断。
> **边界**：❌ 不写 `SKILL.md` ❌ **不修改 Interface v2**（工程纪律：映射出问题时，先判定是**字段不足**还是**语义解析不足**，不回头改 v2） ❌ 不新增 Type／Action ❌ 不启用 Phase 2.3 字段。
> **上游**：[`feedback-transition-design.md`](feedback-transition-design.md)（T1/T2/T7 + TD-01～TD-20）、[`gap-ledger-interface.md`](gap-ledger-interface.md) §8（Interface v2 门）
> **本轮验收**：30 个边界案例（授权 10 / 否定 10 / 修正 10）+ **TD-01～TD-20 全部通过**。

---

## 1. 三层结构

```
Layer 1  表面表达族      → 候选槽位（candidate slot，不是最终 Intent）
Layer 2  上下文槽位解析   → target / scope（来自状态与最近动作，不来自词面）
Layer 3  契约输出         → (candidate_intent, target, scope, risk_check, effective, transition, unique?)
```

### 1.1 Layer 1 · 表面表达族（最小集）

| 族 | 表面表达（最小覆盖集） | 输出**候选槽位** | 明令禁止的直接判定 |
|---|---|---|---|
| **授权族** | 你决定／你看着办／随便／都可以／听你的／无所谓／默认吧／都行／不用问了／你定／不重要 | `authorization_candidate` | ❌ 直接判 `AUTHORIZED` 或 `CLOSED(assumed)`——必须先过 **T1 scope → T2 risk gate** |
| **否定族** | 这个不行／不要这个／换一个／不对／方向错了／不是这个意思／重新来／太丑了／都不行 | `feedback_target_resolution` | ❌ 直接判 `CHALLENGED` 或 `disagreed`——必须先定 **target** |
| **修正族** | 改成 X／换成 Y／还是原来的／回到之前／稍微调一下／微调 | `REVISION_CANDIDATE` | ❌ 直接判 `revised`——必须先分三形：**有新值／无新值／回退到历史值** |
| 无法回答族（**延期**） | 不知道／没想过／不清楚／说不出来 | `unresolved_candidate` | 本轮只做候选槽位，不做 `unable/evaded/refused` 分类（Phase 2.3） |

> **要点**：Layer 1 只做**收敛**（把表达收进三个候选槽位），不做判定。判定权全部交给 Interface v2 的门。

### 1.2 Layer 2 · 上下文槽位解析（关键：target/scope 不来自词面）

**target 解析顺序**（第一个能确定者胜出）：

1. **显式指代**（"这个／它／刚才那个"）→ 指向最近一次展示或提及的对象
2. **最近一次 resolution 的类型**：
   - `last_resolution = shown` → 默认 `proposal`
   - `last_resolution = asked` → 按该 gap 的维度：目标类槽位 → `goal`；约束类 → `constraint`；其余 → `confirmed_value`
3. **语义直指**（"不要做 X 了"直指产物目标；"不用黑色了"直指已确认约束）
4. 以上皆不能确定 → **`target_unresolved`**（禁止默认绑定）

**scope 解析**：

| 条件 | scope |
|---|---|
| 最近问句是 `§11.7` 合并问句 | `current_decision_cluster`（簇内全部子 gap） |
| 用户明确"整个／全部／都"**且**无未拍板阻塞项 | `whole_task` |
| 用户明确"整个／都"**但**存在未拍板阻塞项 | **降级** `current_decision_cluster` |
| 其余 | `current_gap` |

**risk_check 解析**：**与词面无关**，只读 gap 属性（R6 闭集／R14 高风险 C／不可逆／法律安全／费用／数据用途）。

---

## 2. 30 个边界案例

格式：`用户原话` ｜ 候选槽位 ｜ target ｜ scope ｜ risk gate ｜ state transition ｜ 是否唯一

### A · 授权歧义（10）

| # | 用户原话（← 上下文） | 候选槽位 | target | scope | risk gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **L-01** | `你决定吧，我不懂。` | `authorization_candidate` | — | `current_gap` | passed | `OPEN → CLOSED(assumed)` + 假设区 | **唯一**（真授权；"我不懂"不改变跃迁） |
| **L-02** | `都行，我懒得想。` | `authorization_candidate` | — | `current_gap` | passed | `CLOSED(assumed)` | **唯一**（"懒得想"属 Phase 2.3 的 `deprioritized`，不改变本轮跃迁） |
| **L-03** | `我不知道，你告诉我。` | `unresolved_candidate` | — | `current_gap` | — | **不是授权**：`UNABLE` → §11.2 降维／§2.5 动作层（INSPECT/DISCOVER） | **唯一** |
| **L-04** | `费用你决定。` | `authorization_candidate` | — | `current_gap` | **blocked（费用 ∈ R6）** | gap 保持 `OPEN` + `ASK`（必须拍板） | **唯一** |
| **L-05** | `随便。` ← 问图标样式 | `authorization_candidate` | — | `current_gap` | passed | `CLOSED(assumed)` | **唯一** |
| **L-06** | `都可以。` ← 问单页还是多页 | `authorization_candidate` | — | `current_gap` | passed（**口径**：R6「范围」指任务边界，不含页数） | `CLOSED(assumed)` + 出口标注 | **唯一**（依赖已声明口径） |
| **L-07** | `听你的。` ← 同轮 3 个待定项 | `authorization_candidate` | — | `current_decision_cluster` | 逐 gap：passed | 3 个 gap → `CLOSED(assumed)` | **唯一** |
| **L-08** | `整个都听你的。` ← 仍有费用项未拍板 | `authorization_candidate` | — | 声称 `whole_task` → **降级 cluster** | 费用项 **blocked**，其余 passed | 费用项保持 `OPEN`；其余 `CLOSED(assumed)` | **唯一** |
| **L-09** | `随便吧。` ← 问"是否允许自动给患者诊断" | `authorization_candidate` | — | `current_gap` | **blocked（法律安全 + R14 高风险 C）** | `OPEN` + `TEACH` 后 `ASK` | **唯一**（与 L-04 同构，证明与词面无关） |
| **L-10** | `你看着办。` ← 问品牌语气 | `authorization_candidate` | — | `current_gap` | passed | `CLOSED(assumed)` | **唯一**（**对照 L-04**：同句不同门结果） |

### B · 否定目标（10）

| # | 用户原话（← 上下文） | 候选槽位 | target | scope | risk gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **L-11** | `这个页面不好看。` ← 刚 SHOW | `feedback_target_resolution` | `proposal` | `current_decision_cluster` | — | `disagreed` → 换方向／提保真度 | **唯一** |
| **L-12** | `我不要做官网了。` | `feedback_target_resolution` | **`goal`**（语义直指产物） | `whole_task`（新目标待定） | — | `CHALLENGED(goal)` + `targets` 标记 + **必须 ASK 新目标** | **唯一** |
| **L-13** | `不用黑色了。` | `feedback_target_resolution` | **`constraint`** | `current_gap` | — | `CHALLENGED(constraint)`，其余不动 | **唯一** |
| **L-14** | `不要这个。` ← 面对 3 个 SHOW 方向 | `feedback_target_resolution` | `proposal` | `current_decision_cluster` | — | `disagreed` + 闸门计时 | **唯一** |
| **L-15** | `不要这个。` ← 面对已交付成稿 | `feedback_target_resolution` | **`artifact`** | `current_gap` | — | `disagreed` + `targets` + §4 澄清 | **唯一** |
| **L-16** | `不对。` ← 本会话只有一次 SHOW | `feedback_target_resolution` | `proposal`（最近 resolution = shown） | `current_decision_cluster` | — | `disagreed` | **唯一** |
| **L-17** | `不对。` ← 同轮既有 SHOW 又有已确认值被提及 | `feedback_target_resolution` | **`target_unresolved`** | — | — | **先一次定位**（ASK/INSPECT）→ 再分流 | **唯一（流程唯一）**：目标本身故意不定 |
| **L-18** | `方向错了。` ← "东方美学"已 CONFIRMED | `feedback_target_resolution` | `confirmed_value` | `current_gap` | — | `CHALLENGED` + `pending_resolution` + `supersedes` + **索取新值** | **唯一** |
| **L-19** | `换一个。` ← 已否掉一个方向（第 2 次） | `feedback_target_resolution` | `proposal` | `current_decision_cluster` | — | `consecutive_no_signal=2` → **禁止同保真度**，提保真度或转 ASK | **唯一** |
| **L-20** | `重新来。` | `feedback_target_resolution` | `target_unresolved` | **需 `reset_scope`（未批准字段）** | — | 本轮只做一次定位；**无法确定重开范围** | **不唯一（字段不足）** |

### C · Revision（10）

| # | 用户原话（← 上下文） | 候选槽位 | target | scope | risk gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **L-21** | `改成蓝色。` ← 主色已确认深色 | `REVISION_CANDIDATE`（有新值） | `confirmed_value` | `current_gap` | — | §6.5A：覆盖 + `supersedes` + 下游闭包 | **唯一** |
| **L-22** | `换成黑色。` | `REVISION_CANDIDATE`（有新值） | `confirmed_value` | `current_gap` | — | 同 L-21 | **唯一** |
| **L-23** | `还是原来的。` ← 前一轮刚改过 | `REVISION_CANDIDATE`（**回退型**） | `confirmed_value` | `current_gap` | — | 需要 `reverted_to`（未批准字段）；本轮只能用 `history` 回填，**无正式转换** | **不唯一（字段不足）** |
| **L-24** | `稍微调一下。` | `REVISION_CANDIDATE`（**无新值**） | `confirmed_value` | `current_gap` | — | 按 §6.5A 前置**必须索取新值**（一次 ASK）；`revision_scope=minor`（未批准字段）无法记录 | **不唯一（字段不足，但流程可走）** |
| **L-25** | `改成蓝色，另外页面重来。` | `REVISION_CANDIDATE` + `feedback_target_resolution`（**复合**） | 混合 | 混合 | — | 本轮：先处理有值的 Revision；`重来`部分转 `target_unresolved` → **需一次澄清** | **不唯一（复合语句，需一次澄清）** |
| **L-26** | `我想换目标。` | `REVISION_CANDIDATE`（**无新值**） | **`goal`** | `whole_task` | — | `CHALLENGED(goal)` + `targets` + **必须 ASK 新目标** | **唯一** |
| **L-27** | `我想换目标，改成面向企业客户。` | `REVISION_CANDIDATE`（有新值） | `goal` | `whole_task` | — | §6.5A Revision（锚点 + 下游闭包） | **唯一** |
| **L-28** | `不是这个意思。` | `feedback_target_resolution` | **`target_unresolved`** | — | — | 一次定位后再分流 | **唯一（流程唯一）** |
| **L-29** | `改成黑色。` ← 已确认"不用黑色"且**无修正声明** | `REVISION_CANDIDATE`（有新值） | `confirmed_value` | `current_gap` | — | §6.5B **Conflict**：暂停该组 + 只问一个最小澄清 | **唯一** |
| **L-30** | `回到最开始那版。` | `REVISION_CANDIDATE`（**回退到首版**） | `confirmed_value`（历史目标值） | `current_gap` | — | 同 L-23：需 `reverted_to` | **不唯一（字段不足）** |

---

## 3. 映射结果汇总

| 结果 | 案例数 | 案例 |
|---|---|---|
| **唯一（可直接进入门）** | **23** | L-01～L-19（除 L-17 标"流程唯一"）、L-21、L-22、L-26～L-29 |
| **唯一（流程唯一：先进 target 定位）** | **2** | L-17、L-28 |
| **不唯一 · 字段不足（Phase 2.3 已延期字段）** | **4** | L-20（`reset_scope`）、L-23／L-30（`reverted_to`）、L-24（`revision_scope`） |
| **不唯一 · 语句复合，需一次澄清** | **1** | L-25 |

**纪律判定（字段不足 vs 语义解析不足）**

| 归因 | 结论 |
|---|---|
| **字段不足** | 4 例（L-20／23／24／30）。所需字段（`reset_scope`／`reverted_to`／`revision_scope`）**你已明确延期到 Phase 2.3** → 本轮**不申请加字段**，不改 Interface v2 |
| **语义解析不足** | **0 例**。没有任何一例是因为 Layer 1／Layer 2 的映射契约不够而失败 |
| **语句复合** | 1 例（L-25）。属"一句话含两个独立反馈"——本轮按"分解 + 一次澄清"处理，**不新增规则**，也不改 v2 |

---

## 4. TD-01～TD-20 回归（必须全部通过）

用本映射重跑 Phase 2.1 的 20 例（语言层 → 门层是否与设计一致）：

| TD | 原话 | Layer 1 候选 | 解析 target / scope | 门结果 | 与设计一致 |
|---|---|---|---|---|---|
| TD-01 | 你决定吧 | `authorization_candidate` | —／`current_gap` | passed → `CLOSED(assumed)` | ✅ |
| TD-02 | 按默认来吧（3 缺口） | `authorization_candidate` | —／`current_decision_cluster` | 逐 gap passed | ✅ |
| TD-03 | 都可以 | `authorization_candidate` | —／`current_gap` | passed | ✅ |
| TD-04 | 这个不重要，随便 | `authorization_candidate` | —／`current_gap` | **blocked**（数据用途）→ `OPEN` + ASK | ✅ |
| TD-05 | 你看着办（费用） | `authorization_candidate` | —／`current_gap` | **blocked**（费用） | ✅ |
| TD-06 | 整个都听你的（含阻塞项） | `authorization_candidate` | —／`whole_task`→降级 | 阻塞项 `OPEN`，其余 assumed | ✅ |
| TD-07 | 都行，你定（合并问句） | `authorization_candidate` | —／`current_decision_cluster` | 3 子 gap 各自 assumed | ✅ |
| TD-08 | 这个不行（SHOW） | `feedback_target_resolution` | `proposal`／cluster | `disagreed` | ✅ |
| TD-09 | 换一个（第 2 次） | `feedback_target_resolution` | `proposal`／cluster | 闸门 → 提保真度/转 ASK | ✅ |
| TD-10 | 方向错了 | `feedback_target_resolution` | `confirmed_value`／gap | `CHALLENGED` + 索取新值 | ✅ |
| TD-11 | 重新来 | `feedback_target_resolution` | `target_unresolved`／需 `reset_scope` | 一次定位（范围待 Phase 2.3） | ✅（字段缺口同 L-20） |
| TD-12 | 不对（无指代） | `feedback_target_resolution` | `target_unresolved` | 一次定位 | ✅ |
| TD-13 | 太丑了 | `feedback_target_resolution` | `artifact`／gap | `disagreed` + `targets` + §4 | ✅ |
| TD-14 | 都不行（合并问句） | `feedback_target_resolution` | `proposal`（多目标） | `split_feedback` 分配 | ✅ |
| TD-15 | 改成蓝色 | `REVISION_CANDIDATE`（有值） | `confirmed_value`／gap | §6.5A | ✅ |
| TD-16 | 还是用原来的黑色 | `REVISION_CANDIDATE`（回退） | `confirmed_value`／gap | 同 L-23（字段缺口） | ✅（字段缺口） |
| TD-17 | 我想换个目标（无值） | `REVISION_CANDIDATE`（无值） | `goal`／whole_task | `CHALLENGED(goal)` + ASK | ✅ |
| TD-18 | 我想换目标，改成面向企业客户 | `REVISION_CANDIDATE`（有值） | `goal`／whole_task | §6.5A | ✅ |
| TD-19 | 稍微调一下，别大改 | `REVISION_CANDIDATE`（无值） | `confirmed_value`／gap | 索取新值（scope 字段缺口） | ✅ |
| TD-20 | 改成放真人照片（与旧值互斥） | `REVISION_CANDIDATE`（有值） | `confirmed_value`／gap | §6.5B Conflict | ✅ |

**结果：TD-01～TD-20 = 20/20 通过**（其中 TD-11／TD-16／TD-19 标注的是**已延期字段缺口**，跃迁与门结果与设计一致）。

---

## 5. 结论

1. **Layer 1 只收敛、不判定**：三个候选槽位（`authorization_candidate`／`feedback_target_resolution`／`REVISION_CANDIDATE`）承接全部表达，判定权在 Interface v2 的门。**"不要这个"不再可能被直接写成 `CHALLENGED`，"你决定"不再可能被直接写成 `AUTHORIZED`。**
2. **Layer 2 证明 target/scope 是状态量**：同一句"不要这个"落在 `proposal`（L-14）或 `artifact`（L-15）；同一句"你看着办"在语气项上 passed（L-10）、在费用项上 blocked（L-04）。**词面相同、跃迁相反**——这是本轮最重要的验证结果。
3. **唯一性**：30 例中 **25 例唯一**（23 直接 + 2 流程唯一）；**5 例不唯一全部归因于已延期字段（4）或语句复合（1）**，**无一例归因于语义解析不足**。
4. **Interface v2 未被修改**，也未申请修改：映射层不需要新字段；缺的字段全部是你已明确延期的 Phase 2.3 项。
5. **下一步建议**：进入 **Phase 2.3**——补 `reset_scope`／`reverted_to`／`revision_scope`／`deprioritized`／`pending_external`／`unaware` 六字段，并处理 `refused / unable / evaded` 分类；届时把 L-20／L-23／L-24／L-25／L-30 转为固定回归。
