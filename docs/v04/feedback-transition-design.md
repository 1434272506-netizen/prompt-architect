# V0.4.2 Phase 2.1 · Feedback Transition Design（只设计，不写 SKILL）

> **本轮性质**：**只设计，不改 `SKILL.md`**，不写规则文本、不新增 Type／Action。
> **范围**：只补 **T2 风险门（最高优先）→ T7 否定目标 → T1 授权作用域**；`refused / unable / evaded` 的语言分类**暂缓**（顺序原则：**先确定状态跃迁，再分类语言**）。
> **归属**：风险门与三个新字段落在 **Gap Ledger Interface / Feedback Interface**（用户裁决：**不解冻 §6.3**）——规范位置见 [`gap-ledger-interface.md`](gap-ledger-interface.md) **Interface v2**。
> **上游**：[`feedback-semantics-discovery.md`](feedback-semantics-discovery.md)（30 例，FS-03／06／10／15、FS-20／21／23、FS-25／27／29 是本轮的直接来源）。

**架构（用户裁决）**

```
Feedback Input → Feedback Intent（语义，不是语言分类）
              → State Transition Gate（T2 风险门 / T7 目标绑定 / T1 作用域）
              → Gap Update
```

**Feedback Intent 第一批（7）**：`AUTHORIZED` / `REJECTED_PROPOSAL` / `CHALLENGED_VALUE` / `REVISION_REQUEST` / `UNABLE` / `UNDECIDED` / `REFUSED`
—— 本轮只定义**它们各自的跃迁与门**；**如何从语言判出 intent = Phase 2.2，不做**。

---

## 1. T2 · 风险门（Effective Authorization）·最高优先

### 1.1 问题

```
现状：  用户"你看着办" → §6.3 authorized → AI 默认决定        ← 缺"AI 是否有资格接受"
目标：  authorized + permission boundary → effective authorization
```

§6.3 解决"用户是否把判断权交给 AI"；**风险门**解决"AI 是否有资格接受"。**两层分离，不改 §6.3。**

### 1.2 状态模型

```yaml
authorization:
  intent: AUTHORIZED            # 语义层判定（Phase 2.2 才做语言分类）
  candidate: true               # 用户把判断权交给 AI
  scope: current_gap            # T1：current_gap | current_decision_cluster | whole_task
  risk_check: pending | passed | blocked
  blocked_by: []                # R6_closed_set | high_risk_C | irreversible | legal_safety | cost | data_use
  effective: false              # effective ⟺ candidate ∧ risk_check = passed
```

### 1.3 判定规则（3 条）

| # | 规则 |
|---|---|
| **T2-a** | 只有 `effective = true` 才允许把 gap 落到 `CLOSED(assumed)`。`candidate = true` 且被 blocked → **gap 保持 `OPEN`**，反馈记为 `authorized_rejected_by_policy`。 |
| **T2-b** | 风险门输入：**契约 R6 闭集**（目标／范围／权限／费用／数据用途／不可逆操作）、**契约 R14 高风险 C**、以及"授权不得改写 `effective_set` 内的已确认值"（后者走 §6.5 兼容更新／§3.1 Conflict）。 |
| **T2-c** | 被 blocked 时的下一动作沿用 V0.3 动作层：阻塞项 → `ASK`（必须用户拍板）；高风险 C → `TEACH` 后 `ASK`；**不得静默取默认**。用户侧只说"这件事需要你定，因为……"，不出现机制词。 |

### 1.4 关键性质（与措辞无关）

> **同一句"你看着办"，在图标样式上可承接（TD-01），在费用/医疗/合规上不可（TD-05）。**
> 判定输入是**缺口性质**，不是语句本身——这正是 E2 唯一的正解。

---

## 2. T7 · 否定目标（feedback_target）·第二优先

### 2.1 问题

否定句**状态相关、而非词面相关**：同一句"不行"，否定的是**提案**还是**已确认值**，决定完全不同的跃迁。现状把两者都塞进 `disagreed`。

### 2.2 状态模型

```yaml
feedback_target: proposal | confirmed_value | goal | constraint | artifact
```

| target | 跃迁 | 记录 | 下一动作 |
|---|---|---|---|
| **proposal** | `disagreed` → 该提案作废，`consecutive_no_signal` 按闸门处理 | `last_resolution` 保留 | 换方向／提高保真度重发（≥2 次同保真度后闸门禁止） |
| **confirmed_value** | `CHALLENGED`（若影响当前交付 → `validity_state = pending_resolution`） | `supersedes` 边 | **必须索取新值**（一次 ASK），不得沿用旧值 |
| **goal**（P0 锚点） | 有值 → §6.5A Revision（重建锚点 + 下游闭包）；无值 → `CHALLENGED(goal)` | `targets` 标记已产出物 | 无值时必须 `ASK` 新目标；**禁止带着旧锚点继续产出** |
| **constraint** | `CHALLENGED(constraint)`，其余需求不动 | — | 一次 ASK 澄清约束 |
| **artifact**（已产出物） | `disagreed` + `targets` 标记 | 旧稿效力清单 | 走 §4 澄清"哪里不行" |

### 2.3 目标未绑定（`target_unresolved`）

"不对""不是这个意思""重新来"这类**没有指代对象**时：**不允许默认绑定**。

```
target_unresolved → 先做一次目标定位（ASK 或 INSPECT）→ 再进入上表
```

**禁止**：把 `target_unresolved` 直接记成 `disagreed`（→ 继续优化旧值，即 E3）或直接记成 `CHALLENGED`（→ 无谓重开）。

---

## 3. T1 · 授权作用域（authorization scope）·第三优先

### 3.1 状态模型

```yaml
authorization.scope: current_gap | current_decision_cluster | whole_task
```

| 取值 | 何时成立 | 生效范围 |
|---|---|---|
| `current_gap`（默认） | 用户只回应了当前一个问题 | 仅该 gap |
| `current_decision_cluster` | 当前问句是 `§11.7` 合并问句；或用户在同一决策簇内回应 | 该簇内**全部**活跃子 gap |
| `whole_task` | 用户**明确**说"整个都你定"**且**不存在未拍板的阻塞项 | 全部活跃 gap；否则降级为 cluster |

### 3.2 规则

1. **默认最保守**：无法判断时取 `current_decision_cluster`（比 `whole_task` 少假设，比 `current_gap` 少追问）。
2. **作用域内逐 gap 过风险门**：簇内某 gap 被 blocked → **该 gap 单独保持 OPEN**，同簇其他 gap 仍可 `CLOSED(assumed)`（避免"一条高风险否决全部授权"）。
3. 作用域外的 gap **一律不动**：既不取默认，也不因该授权而停止追问。
4. `whole_task` 若含未拍板阻塞项 → 降级 + 只对被明确点的 gap 生效。

---

## 4. 20 个破坏案例

字段：**语句 / 上下文 → Intent → target / scope → risk gate → 期望跃迁 → 当前 Gap 状态能否承接 → 需新增字段**。

### 授权族（7）

#### TD-01 · "你决定"（低风险单 gap）
- **语句 / 上下文**：`你决定吧。` ← 问"图标用线性还是填充"
- **Intent / target / scope**：`AUTHORIZED`／（无 target）／`current_gap`
- **风险门**：`passed`（非 R6 闭集、非高风险）
- **期望跃迁**：`OPEN → CLOSED(assumed)`；出口进「待确认假设」
- **当前能否承接**：❌ 缺 `authorization` 结构（现只有 §6.3 字面逻辑）
- **需新增字段**：`authorization{scope, risk_check, effective}`

#### TD-02 · "默认吧"（同轮 3 个待定项）
- **语句 / 上下文**：`按默认来吧。` ← 同轮存在配色／字号／动画 3 个非阻塞缺口
- **Intent / target / scope**：`AUTHORIZED`／—／`current_decision_cluster`
- **风险门**：逐一 `passed`
- **期望跃迁**：3 个 gap → `CLOSED(assumed)`；若其中一个属 R6 闭集 → 仅它保持 `OPEN`
- **当前能否承接**：❌ 作用域未定义（可能只作用于第一个，或过度作用于整任务）
- **需新增字段**：`authorization.scope`（+ 逐 gap 评估）

#### TD-03 · "都可以"（两个结构不同的选项）
- **语句 / 上下文**：`都可以。` ← 问"单页还是多页"
- **Intent / target / scope**：`AUTHORIZED`／—／`current_gap`
- **风险门**：`passed`
- **期望跃迁**：`CLOSED(assumed)` + 出口显式标注（结构性选择被默认）
- **当前能否承接**：⚠️ 字面清单不含"都可以"；**但这是 Phase 2.2 的语言问题**，跃迁本身可承接
- **需新增字段**：无（跃迁层已够）

#### TD-04 · "不重要"（落在合规项上）
- **语句 / 上下文**：`这个不重要，随便。` ← 问"数据保留策略"
- **Intent / target / scope**：`AUTHORIZED` + `DEPRIORITIZED`／—／`current_gap`
- **风险门**：**`blocked`（数据用途 ∈ R6 闭集）**
- **期望跃迁**：gap 保持 `OPEN`；记录 `authorized_rejected_by_policy`；下一动作 `ASK`/`TEACH`
- **当前能否承接**：❌ 无 `deprioritized`、无风险门 → 会被静默降权
- **需新增字段**：`authorization.blocked_by`、`deprioritized`（后续轮）

#### TD-05 · "你看着办"（费用）
- **语句 / 上下文**：`你看着办。` ← 问"这个功能要不要收费"
- **Intent / target / scope**：`AUTHORIZED`／—／`current_gap`
- **风险门**：**`blocked`（费用 ∈ R6 闭集）**
- **期望跃迁**：保持 `OPEN`；`ASK`（用户必须拍板）
- **当前能否承接**：❌（现行走 §6.3 字面 → 自动决定；例外块虽拦得住，但**不产生状态位**，后续无法复盘）
- **需新增字段**：`risk_check` / `blocked_by` / `effective`

#### TD-06 · "听你的"（声称整任务，但存在未拍板阻塞项）
- **语句 / 上下文**：`整个都听你的吧。` ← 仍有"要不要联网上传数据"未拍板
- **Intent / target / scope**：`AUTHORIZED`／—／声称 `whole_task` → **降级**
- **风险门**：其余 `passed`；数据用途项 `blocked`
- **期望跃迁**：降级为 `current_decision_cluster`；被阻塞项保持 `OPEN` + 必须拍板；其余可 `CLOSED(assumed)`
- **当前能否承接**：❌
- **需新增字段**：`scope` 降级规则 + 逐 gap 门

#### TD-07 · 授权落在 §11.7 合并问句上
- **语句 / 上下文**：`都行，你定。` ← 面对合并问句"发在哪、多长、看完做什么"
- **Intent / target / scope**：`AUTHORIZED`／—／`current_decision_cluster`（**三个子 gap**）
- **风险门**：全部 `passed`
- **期望跃迁**：3 个子 gap 各自 `CLOSED(assumed)`；出口逐条列出
- **当前能否承接**：❌ 合并问句的反馈**无法分配**（Discovery FS-23 同源）
- **需新增字段**：`split_feedback`（按子 gap 分配）

### 否定族（7）

#### TD-08 · "这个不行"（否定 SHOW 提案）
- **语句 / 上下文**：`这个不行。` ← 面对 3 个方向之一
- **Intent / target**：`REJECTED_PROPOSAL`／`proposal`
- **期望跃迁**：`disagreed`；提案作废；换方向或提高保真度重发；闸门计时
- **当前能否承接**：✅（`disagreed` + 闸门已有）
- **需新增字段**：`feedback_target`（用于与 TD-10 区分）

#### TD-09 · "换一个"（第二次否定提案）
- **语句 / 上下文**：`换一个。` ← 已否掉一个方向
- **Intent / target**：`REJECTED_PROPOSAL`／`proposal`
- **期望跃迁**：`consecutive_no_signal` 累加；**禁止同保真度第三次** → 提高保真度或转 ASK
- **当前能否承接**：✅（Interface v1 §5 闸门）
- **需新增字段**：无

#### TD-10 · "方向错了"（否定已确认值）
- **语句 / 上下文**：`方向错了。` ← "东方美学"已 `CONFIRMED`
- **Intent / target**：`CHALLENGED_VALUE`／`confirmed_value`（= 视觉方向 gap）
- **期望跃迁**：该 gap `CHALLENGED` → `validity_state = pending_resolution`（影响当前交付）；`supersedes` 边；**必须索取新方向**
- **当前能否承接**：❌ 现会被记成 `disagreed`（提案级）→ **E3**
- **需新增字段**：`feedback_target`

#### TD-11 · "重新来"（范围不明）
- **语句 / 上下文**：`重新来。`
- **Intent / target**：`REJECTED_ARTIFACT`（或 `RESET`）／`artifact`，`scope` 未定
- **期望跃迁**：`reset{scope: unresolved}` → **先确认范围**（局部重开？整任务？），确认前不动已确认值
- **当前能否承接**：❌ 现文与 §6.5C 局部重开**字面相反**，且无 `reset` 语义
- **需新增字段**：`reset_scope`（后续轮）

#### TD-12 · "不对"（target 未绑定）
- **语句 / 上下文**：`不对。` ← 刚出一版稿，未说明指哪
- **Intent / target**：`CHALLENGED_VALUE`（意图）／**`target_unresolved`**
- **期望跃迁**：**不默认绑定** → 一次定位（ASK/INSPECT）→ 再按 T7 表分流
- **当前能否承接**：❌ 现文按"明确否定旧值"直接 Revision
- **需新增字段**：`target_unresolved` 判定位

#### TD-13 · "太丑了"（产物级否定）
- **语句 / 上下文**：`太丑了。` ← 刚交付
- **Intent / target**：`REJECTED_ARTIFACT`／`artifact`
- **期望跃迁**：`disagreed` + `targets` 标记 + §4 澄清"丑指什么"（不直接改已确认值）
- **当前能否承接**：⚠️ 可记 `disagreed`，但 `targets` 与澄清链未绑定
- **需新增字段**：`feedback_target` + `targets.action`

#### TD-14 · "都不行"（合并问句整体否定）
- **语句 / 上下文**：`都不行。` ← 面对 3 子问题合并问句
- **Intent / target**：`REJECTED_PROPOSAL`／`proposal`（**多目标**）
- **期望跃迁**：`split_feedback` → 整体否定 vs 逐项否定需区分；整体否定不得误伤已确认项
- **当前能否承接**：❌
- **需新增字段**：`split_feedback`

### 修正族（6）

#### TD-15 · "改成蓝色"（标准 Revision）
- **语句 / 上下文**：`主色改成蓝色。`
- **Intent / target**：`REVISION_REQUEST`／`confirmed_value`（有新值）
- **期望跃迁**：§6.5A → 覆盖 + `supersedes` + 只重置受影响下游
- **当前能否承接**：✅
- **需新增字段**：无

#### TD-16 · "还是用原来的"（回退）
- **语句 / 上下文**：`还是用原来的黑色吧。`
- **Intent / target**：`REVISION_REQUEST`／`confirmed_value`（目标值 = 历史值）
- **期望跃迁**：`reverted{to: prior_confirmed}` → 旧值复活为 `CONFIRMED`；中间值 `INVALIDATED`
- **当前能否承接**：⚠️ 值可从 `history` 取回，但**无 `revert` 语义**，`supersedes` 单向
- **需新增字段**：`reverted_to`（后续轮）

#### TD-17 · "我想换目标"（P0 变更、无新值）
- **语句 / 上下文**：`我想换个目标。`
- **Intent / target**：`CHALLENGED_VALUE`／`goal`（无新值）
- **期望跃迁**：`CHALLENGED(goal)` + `targets` 标记旧产物；**必须 ASK 新目标**；禁止带旧锚点继续产出
- **当前能否承接**：❌ 无值时不落 §6.5A，且 §6.5C 只重开"受影响分支"，未规定锚点无值时的强制索取
- **需新增字段**：`feedback_target` + goal 级 CHALLENGED

#### TD-18 · "我想换目标" + 新值
- **语句 / 上下文**：`我想换个目标，改成面向企业客户。`
- **Intent / target**：`REVISION_REQUEST`／`goal`（有新值）
- **期望跃迁**：§6.5A Revision：锚点变更 → 下游闭包重开（受众／内容／视觉／验收）
- **当前能否承接**：✅（§6.5A + 接口层有效下游计数）
- **需新增字段**：无

#### TD-19 · "稍微调一下"（范围自限）
- **语句 / 上下文**：`稍微调一下就行，别大改。`
- **Intent / target**：`REVISION_REQUEST`／`confirmed_value`（**scope: minor**）
- **期望跃迁**：限制下游 `CHALLENGED` 闭包范围（只动直接受影响项）；记录 `revision_scope = minor`
- **当前能否承接**：❌ 接口层闭包默认取全传递闭包 → 会过度重开
- **需新增字段**：`revision_scope`

#### TD-20 · Revision 与已确认硬约束冲突
- **语句 / 上下文**：`改成放我的真人照片。` ← 已确认"不放真人照片"
- **Intent / target**：`REVISION_REQUEST`／`confirmed_value`（新值与旧值**互斥**且**无明确修正声明**）
- **期望跃迁**：§6.5B → **Conflict**：该组暂停、优先、只问一个最小澄清（不自动覆盖）
- **当前能否承接**：✅（§6.5B + §3.1）
- **需新增字段**：无

---

## 5. 汇总：当前 Gap 状态能否承接

| 结果 | 案例数 | 案例 |
|---|---|---|
| **可承接（现状即可）** | **6** | TD-08、TD-09、TD-15、TD-18、TD-20（+ TD-03 跃迁层可承接，语言层属 Phase 2.2） |
| **需新增字段（跃迁正确但无状态位）** | **6** | TD-13、TD-16、TD-10、TD-11、TD-12、TD-19 |
| **需新增字段 + 新转换** | **8** | TD-01、TD-02、TD-04、TD-05、TD-06、TD-07、TD-14、TD-17 |

**按优先级**：T2 风险门覆盖 **TD-01／02／04／05／06（+TD-07 部分）**；T7 否定目标覆盖 **TD-08／10／11／12／13／14／17**；T1 作用域覆盖 **TD-01／02／06／07**。

**三个验收错误的封口位置**

| 错误 | 封口 |
|---|---|
| E2 风险问题被默认 | **T2 风险门**（TD-04、TD-05、TD-06） |
| E3 Revision 被误认 | **T7 否定目标**（TD-10、TD-12、TD-17） |
| E1 授权被当未知 | **T1 作用域**（TD-02、TD-06、TD-07 不再反复追问同簇） |

---

## 6. 是否需要新增字段

**本轮需要（7 个，均落在 Interface v2，不进 `SKILL.md`）**

| # | 字段 | 值域 | 服务的转换 |
|---|---|---|---|
| F1 | `authorization.candidate` | bool | 授权候选 |
| F2 | `authorization.scope` | `current_gap｜current_decision_cluster｜whole_task` | T1 |
| F3 | `authorization.risk_check` | `pending｜passed｜blocked` | T2 |
| F4 | `authorization.blocked_by` | `[R6_closed_set｜high_risk_C｜irreversible｜legal_safety｜cost｜data_use]` | T2 |
| F5 | `authorization.effective` | bool | T2（`effective ⟺ candidate ∧ passed`） |
| F6 | `feedback_target` | `proposal｜confirmed_value｜goal｜constraint｜artifact｜target_unresolved` | T7 |
| F7 | `split_feedback` | 子 gap → intent 的映射 | TD-07、TD-14（§11.7 合并直接后果） |

**明确延期（本轮不设计）**：`deprioritized`（TD-04）、`reset_scope`（TD-11）、`reverted_to`（TD-16）、`revision_scope`（TD-19）、`pending_external`、`unaware`、`refused / unable / evaded` 分类（Phase 2.2）。

---

## 7. 是否触碰冻结区

**不触碰。零解冻。**

| 冻结对象 | 本轮处置 |
|---|---|
| **§6.3（授权默认字面清单）** | **不改**。用户裁决：授权逻辑正确，缺的是"AI 是否有资格接受"→ 由 **T2 风险门**在接口层补，§6.3 语义保持原样 |
| §2.1 / §3 / §6.4 / §6.5 | **不改**（§6.5A/B 被 TD-15／18／20 复用，未改一字） |
| **§11.1–§11.7（V0.2 冻结）** | **不改**（TD-07/TD-14 暴露的是**接口层缺 `split_feedback`**，不是 §11.7 写错） |
| V0.3 冻结规则（`core/`／`strategies/`） | **不改**（R6／R14 只被**读取**作为风险门输入） |
| Gap Model 正文 | **不改**（新字段写入 Interface v2，Model 只增不回改） |

> **唯一潜在触碰点**：若未来要求"§6.3 字面清单必须识别'都可以/无所谓'" → 那才是解冻申请。本轮**不需要**：跃迁层已足够，语言层属 Phase 2.2。

---

## 8. 下一轮建议（待裁决）

1. **Interface v2 落盘确认**：T2/T7/T1 三块已写入 [`gap-ledger-interface.md`](gap-ledger-interface.md)（v1 → v2 版本化扩展）。
2. **是否进入 Phase 2.2（语言分类）**：把 7 个 Intent 映射到**具体语句族**（含"都可以/无所谓/不重要"这类清单外表达），并复用本轮 TD 案例作为回归。
3. **继续延期**：`pending_resolution` 二次质疑计数、`refused/unable/evaded` 分类——两者都依赖 Phase 2.2 的意图判定。
