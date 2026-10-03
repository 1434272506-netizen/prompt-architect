# Gap Ledger Interface Layer（V0.4 · Patch v1 → **v2** → **v3** → **v3 + Contract §10**）

> **版本**：**v1** = §1–§7（Phase 1，M1–M4 接口）；**v2** = §8（Phase 2.1 反馈跃迁门）；**v3** = §9（Phase 2.3 历史一致性 + 责任/认知边界）；**§10** = Pending Resolution Transition Contract（V0.4.3）。
> **定位**：本文件**不是** Question Selection 规则，也**不是**对 Gap Model 的修改。它是 **Gap Ledger → Question Selection（§11）** 之间的**接口层**。
> **归属裁决（2026-10-02）**：M1–M4 全部批准，但**写入接口层而非 §11**——测试已证明 **§11 的判据没错**，缺的是账本到问题选择之间的数据接口与优先级声明。
> **边界**：❌ 不修改 §11 ❌ 不修改 V0.3 冻结规则 ❌ 不重新定义 Type ❌ 不新增 Action ❌ 不修改 `docs/v04/gap-ledger-proposal.md`（Gap Model 正文）❌ **不解冻 §6.3**（风险门放本层，不放 §6.3）。**v2 章节逐字保留**（v3 为纯增量）。

**上游**：`docs/v04/gap-ledger-proposal.md`（Gap Entity · 七态 · §2.1 谓词 · §4 传播 · §4.2 值效力 · §5 反馈账）
**下游**：`SKILL.md` §11.1–§11.7（Question Selection，**已冻结**）
**验证**：`docs/v04/gap-ledger-x-v11-compat.md`（C-01～C-15 重跑 + I-01～I-12 新增回归）；`docs/v04/feedback-transition-design.md`（Phase 2.1 设计 + TD-01～TD-20）

---

## 1. 集合谓词（供 §11 直接消费）

### 1.1 有效集合（effective set）

```
valid         := validity_state = stable
effective_set := CONFIRMED ∩ valid
              = { g | g.status = CONFIRMED ∧ g.confidence = confirmed ∧ g.validity_state = stable }
```

- 只有 `effective_set` 内的值可以**作为已确认事实**进入出口、参与裁界、支持"进一步确认扩散"。
- `effective_set` 是 §6.4「禁止重复询问」的**唯一判据来源**（见 §4）。

### 1.2 可问集合（askable set）

```
askable_set := { g | g.status = OPEN }
             ∪ { g | g.status = CHALLENGED ∧ g.validity_state = pending_resolution }
             ∪ { g | g.status = CLOSED ∧ g.confidence = partial }
```

- §11 的**候选问题集合 = askable_set**（不是"所有历史 gap"，也不是"所有已知槽位"）。
- 合并提问（§11.7）的**子问题也必须取自 `askable_set`**——已确认项不得进入合并问句。
- `SUSPENDED`（冲突组已挂起）**不进 `askable_set`**：它只接受"用户回到该话题"或"上游变化解除冲突"两种入口。
- `CLOSED(assumed)`（授权默认落点）**不进 `askable_set`**：它是终态，除非用户主动回到该话题。
- **`OPEN + deferred`（用户 `delay`）仍 ∈ `askable_set`** —— 因为 `status` 仍是 `OPEN`；`delay` **只关闭"当前正常调度"**，**不改变集合成员资格**。
  ```
  OPEN + deferred
    askable_set       = YES      （status = OPEN）
    normal scheduling = NO       （delay 生效期间）
  delay ≠ remove_from_askable_set
  ```
  > **D06 / CS-06 澄清（normative home）**：`askable` 描述"该类 Gap 是否属于 ASK 可处理的需求类别"；调度资格描述"当前执行窗口是否允许正常调度它"。**两个维度不同**，勿把 `askable_set` 当作 scheduler queue。

### 1.3 下游计数基数（供 §11.1 一级/二级裁界）

```
下游计数基数 := { g | g.status ∈ {OPEN, PROPOSED, SUSPENDED, CHALLENGED} }
                  ∪ { g | g.status = CONFIRMED ∧ g.confidence = confirmed ∧ g.validity_state = stable }
有效下游     := affected ∩ 下游计数基数        ← 仅统计可被本次变化真实影响的分支
```

- 历史 `CLOSED` 记录**不参与计数**（仅作审计与"旧稿效力清单"）。
- §11.1 的一级裁界（"排除更多下游分支"）与二级裁界（可回答性／回答成本）都以**有效下游**为基数，避免用 `CHALLENGED` 的不可用值算排序。

### 1.4 `partial` 状态说明

```
partial: 可继续询问（∈ askable_set）
         不可作为已确认依据（∉ effective_set，不参与裁界、不作为交付事实）
```

即：`CLOSED(partial)` 既不是"已完成"，也不是"要重来"——它是**待重新评估**的可问项，出口必须显式列出。

---

## 2. `validity_state`（Pending Validity Change）

**问题本质**（M5 裁决）：`CHALLENGED 必须处理` × `信息足够立即出稿` **不是普通优先级冲突**，而是
> **需求稳定性状态 × 当前交付动作停止条件** 的冲突。

二选一都会坏：写"CHALLENGED 永远优先" → 系统永远无法结束；写"停止条件永远优先" → 用户已改目标而系统继续用旧需求。

### 2.1 新增字段（接口层扩展，七态不变）

```yaml
validity_state: stable | challenged | pending_resolution
```

| 取值 | 含义 | 能否进出口 |
|---|---|---|
| `stable` | 值未被质疑 | ✅ 可直接使用、可扩散确认 |
| `challenged` | 值受质疑，但**不影响当前交付** | ⚠️ 可继续输出，但**必须标注受质疑、待重新评估**；**不得作为"进一步确认扩散"的依据** |
| `pending_resolution` | 变化**影响当前交付目标 / 已确认上游 / 关键约束** | ❌ **阻断基于该值的交付**，进入待确认（可问） |

### 2.2 判定流程

```
CONFIRMED ──用户新信息──▶ CHALLENGED
                             │
                        判断影响范围
                             │
        ┌────────────────────┴────────────────────┐
        │                                          │
   局部不影响                                  影响当前交付
        │                                          │
   validity_state = challenged              validity_state = pending_resolution
   → 继续输出（标注受质疑）                    → 阻断该值，进 askable_set
```

### 2.3 裁决原文（口径）

> **CHALLENGED 的处理优先于"基于该值的进一步确认扩散"，但不必阻断所有交付；只有当变化影响当前交付目标、已确认上游或关键约束时，才进入待确认状态。**

### 2.4 与 §4.2「值效力」的关系（接口层解释，不改 Model 正文）

Gap Model §4.2 写"`CHALLENGED` 值不得直接使用"。接口层把它**细化为两档**（原文不动）：

- `challenged`：值**不得作为已确认事实**使用，但允许在"不依赖它的部分"继续输出，且该值在出口**必须标注受质疑**；
- `pending_resolution`：**完全不得进入出口**，先重新评估。

### 2.5 停止判据的适用范围（解 C-11）

- `validity_state = pending_resolution` 的缺口，**允许且仅允许**在 §6.1 判"信息足够"时仍发起**一次**确认动作。
- `challenged` / `stable` 不享有该例外——不得因此让系统无法结束。
- 该例外是**点例外**：确认后必须回到 `stable` 或转 `INVALIDATED`，不得连续发起第二次同口径确认。

---

## 3. §11.2 三出口 → 账本状态映射

| §11.2 出口 | 账本落点 | 出口渲染要求 |
|---|---|---|
| **default**（取合理默认） | `CLOSED(assumed)` | 进「待确认假设」区 |
| **delay**（延后到有上下文时再问） | `OPEN` + `attempts ≥ 1` + `deferred=true` | 出口列出"暂缓确认项" |
| **skip**（跳过该缺口） | `CLOSED(partial)` | 出口显式列出"待重新评估" |

> 三出口都必须**可见**：`assumed → 假设区`；`partial → 待重新评估清单`；`OPEN+deferred → 暂缓确认项`。

---

## 4. 重复询问的定义（M6）

```
重复询问 := 对 current effective_set 内已确认且未失效的信息再次索取
```

**不是**：曾经出现过同类问题。

- 判定只读 `effective_set`（§1.1），**不读历史提问记录**。
- 推论：`INVALIDATED → OPEN` 后重新消解**不算重复询问**（旧值已不在 `effective_set`）。
- 推论：`supersedes` 后被替代的旧值**不得**作为候选或合并子问题；只有新值可被确认。
- 与冻结 §6.4 的关系：§6.4 原文不动；本定义是**接口层的判定口径**（§6.4 的"已经答过的问题"= 当前有效且未失效的已确认信息）。

---

## 5. 优先级声明

```
Gap state constraint  >  Question form selection
```

- **动作闸门优先于 §11.5 形式选择**：`consecutive_no_signal ≥ 2 ∧ last_resolution 连续两次相同` → 禁止再用同一动作；此时 §11.5 的"开放问／选择题"判据**只在允许发出的动作集合内**生效，不得据 §11.5 再发第三次同口径动作。
- **上游依赖优先于形式与合并**：账本已声明依赖边时，§11.6 上游优先决定顺序；§11.7 补充判据决定能否合并（约束型依赖 → 不合并）。
- **停止判据的例外仅限 §2.5**：只有 `pending_resolution` 能触发"仍发一次确认"。

---

## 6. 消费契约（§11 侧如何读，不改 §11 正文）

| 场景 | 接口读法 |
|---|---|
| 构造候选问题（§11.1／§11.5） | `askable_set` |
| 合并判断（§11.7） | 子问题 ⊆ `askable_set`；且若 `unmodeled_dependencies ≠ []`，合并出口**必须渲染**"未建模的潜在依赖：X（建议你确认）" |
| 上游顺序（§11.6） | 已声明依赖边；`challenged` / `pending_resolution` 的上游一律先于下游 |
| 裁界基数（§11.1） | 有效下游（§1.3） |
| 是否重复询问（§6.4） | `effective_set`（§4） |
| 形式选择（§11.5） | 受动作闸门约束（§5） |

**禁止**：接口层不得新增 Type、不得新增 Action、不得改写 §11 判据、不得把账本字段作为用户可见文本输出。

---

## 7. 本层不做什么

- 不判定"新值是否与旧值兼容"（属 §3.1）；
- 不重算下游值（Phase 3）；
- 不做反馈语义分类器（Phase 2.2 语言层）；
- 不把账本变成持久化存储（沿用 Model §1.3）。

---

# Interface v2（Phase 2.1）：反馈跃迁门

> **依据**：用户裁决 2026-10-02——**暂不触碰 §6.3**；§6.3 负责"用户是否交出判断权"，**本层负责"AI 是否有资格接受"**。
> **设计全文与 20 个破坏案例**：[`feedback-transition-design.md`](feedback-transition-design.md)。
> **架构**：`Feedback Input → Feedback Intent（语义）→ State Transition Gate（本节）→ Gap Update`。

## 8. 反馈跃迁门（State Transition Gate）

### 8.1 流程（三段门，顺序不可换）

```
feedback
  → [T1 作用域门]  确定这次反馈作用于哪些 gap        （G-8.3）
  → [T7 目标门]    确定它否定/修正的是哪个对象        （G-8.4）
  → [T2 风险门]    确定这个跃迁是否被允许执行         （G-8.2）
  → 写回 gap
```

**门必须先于写回**：任何一关未通过，gap 状态**不变**（保持原状并在出口说明），禁止"部分执行"。

> **原子性作用域（normative clarification · CS-04，2026-10-03）**
> “禁止部分执行”指**单个 Gap 在一次完整反馈门链中的状态跃迁不得部分提交**；同一 feedback／cluster 中**其他 Gap 独立经过各自门链**，**不因某一 Gap 被 blocked 而整体回滚**。
> ```
> feedback
>   └─ cluster
>       ├─ Gap A → gate1 → gate2 → gate3   ✕  ⇒ A 全链不部分提交，保持进入该链前的合法状态
>       └─ Gap B → gate1 → gate2 → gate3   ✓  ⇒ B 正常提交自己的合法跃迁
> ```
> ```
> atomicity = per-Gap transition atomicity
> ≠ whole-feedback transaction
> ≠ whole-cluster transaction
> ```
> 因此下方 **G-8.3c（逐 gap 过 T2 门）是该原则的正例，不是例外**；不需要 rollback 机制，也不需要 cluster transaction，且**不新增任何状态**。

### 8.2 T2 · 风险门 / Effective Authorization（最高优先）

```yaml
authorization:
  intent: AUTHORIZED
  candidate: true               # 用户把判断权交给 AI（语义判定）
  scope: current_gap            # T1
  risk_check: pending | passed | blocked
  blocked_by: []                # R6_closed_set | high_risk_C | irreversible | legal_safety | cost | data_use
  effective: false              # effective ⟺ candidate ∧ risk_check = passed
```

| 编号 | 规则 |
|---|---|
| **G-8.2a** | 只有 `effective = true` 才允许 `CLOSED(assumed)`；`blocked` → gap 保持 `OPEN`，记 `authorized_rejected_by_policy` |
| **G-8.2b** | 风险门输入：契约 **R6 闭集**（目标／范围／权限／费用／数据用途／不可逆操作）、契约 **R14 高风险 C**、以及"授权不得改写 `effective_set` 内的已确认值"（后者走 §6.5／§3.1，不在本门处理） |
| **G-8.2c** | 被 blocked 的下一动作沿用 V0.3 动作层：阻塞项 → `ASK`；高风险 C → `TEACH` 后 `ASK`。**禁止静默取默认**；用户侧只说"这件事需要你定"，不出现机制词 |
| **G-8.2d** | 本门**不修改 §6.3**：§6.3 的"用户授权"照旧成立；本门只决定该授权**能否生效** |

> **性质**：判定输入是**缺口性质**（是否 ∈ R6 闭集／高风险），不是语句本身。同一句"你看着办"，细节项可生效、费用/医疗/合规项不可生效。

### 8.3 T1 · 授权作用域门

```yaml
authorization.scope: current_gap | current_decision_cluster | whole_task
```

| 编号 | 规则 |
|---|---|
| **G-8.3a** | 默认最保守：能确定是合并问句或同簇回应 → `current_decision_cluster`；否则 `current_gap` |
| **G-8.3b** | `whole_task` 需用户**明确**表示，**且**不存在未拍板阻塞项；否则**降级**为 cluster |
| **G-8.3c** | 作用域内**逐 gap** 过 T2 门：某项 blocked → **仅该项**保持 `OPEN`，同簇其余仍可 `CLOSED(assumed)`（**＝ §8.1「原子性作用域」的正例**：per-Gap 全链原子，非 cluster 事务） |
| **G-8.3d** | 作用域外的 gap **一律不动**（不取默认、也不因该授权而停止追问） |

### 8.4 T7 · 否定/修正目标门

```yaml
feedback_target: proposal | confirmed_value | goal | constraint | artifact | target_unresolved
```

| 编号 | 规则 |
|---|---|
| **G-8.4a** | `proposal` → `disagreed`；提案作废；换方向或提高保真度重发（受 §5 动作闸门约束） |
| **G-8.4b** | `confirmed_value` → `CHALLENGED`（影响当前交付时 `validity_state = pending_resolution`）+ `supersedes` 边 + **必须索取新值**（一次 ASK），**不得沿用旧值** |
| **G-8.4c** | `goal` → 有新值：走 §6.5A Revision（锚点 + 下游闭包重开）；**无新值**：`CHALLENGED(goal)` + `targets` 标记旧产物 + **必须 ASK 新目标**，禁止带旧锚点继续产出 |
| **G-8.4d** | `constraint` → `CHALLENGED(constraint)`，其余需求不动 |
| **G-8.4e** | `artifact` → `disagreed` + `targets` 标记 + 走 §4 澄清"哪里不行"（不直接改写已确认值） |
| **G-8.4f** | `target_unresolved` → **不允许默认绑定**；先做一次目标定位（ASK 或 INSPECT）再回落上表 |
| **G-8.4g** | **禁止**把 `target_unresolved` 记成 `disagreed`（→ 继续优化旧值，即 E3）或直接记成 `CHALLENGED`（→ 无谓重开） |

### 8.5 合并问句的反馈分配

| 编号 | 规则 |
|---|---|
| **G-8.5a** | 反馈作用于 §11.7 合并问句时，必须用 `split_feedback` 逐子 gap 分配 intent |
| **G-8.5b** | 整体否定（"都不行"）**不得**误伤 `effective_set` 内的已确认项；未绑定的子项转 `target_unresolved` |
| **G-8.5c** | 分配不能确定时，只问**一次**澄清，不得逐项重复询问（§6.4 与 Interface §4 的重复询问口径） |

### 8.6 本轮新增字段（7）

`authorization.candidate` / `authorization.scope` / `authorization.risk_check` / `authorization.blocked_by` / `authorization.effective` / `feedback_target` / `split_feedback`

### 8.7 v2 与 v1 的关系

- v1（§1–§7）**不变**：集合谓词、`validity_state`、§11.2 映射、重复询问口径、优先级声明继续有效；
- v2 只**新增前置门**：反馈先过 T1/T7/T2，再按 v1 的谓词写回；
- v2 **不新增 Type、不新增 Action、不改 §11、不解冻 §6.3**。

### 8.8 延期项（本轮不设计）

`deprioritized`、`reset_scope`、`reverted_to`、`revision_scope`、`pending_external`、`unaware`、`refused / unable / evaded` 的语言分类（Phase 2.2）、`pending_resolution` 二次质疑计数。

> **注（v3 起）**：上列前六项中除 `deprioritized` 外，均已在 **§9（Interface v3）** 设计并落盘；`deprioritized` 移交 Priority Layer；`pending_resolution` 二次质疑仍延期。

---

# Interface v3（Phase 2.3）：历史一致性与责任 / 认知边界

> **增量定位**：v2 解决"反馈如何进入状态门"；**v3 解决"状态变化后如何保持历史一致性"**。v2（§1–§8）**逐字未改**。
> **设计全文**：[`feedback-state-extension-design.md`](feedback-state-extension-design.md)、[`feedback-responsibility-extension-design.md`](feedback-responsibility-extension-design.md)
> **验证**：[`interface-v3-migration-manifest.md`](interface-v3-migration-manifest.md)（Raw 167 / 唯一 136 / 固定回归 5 / canary 4）＋ [`interface-v3-migration-test.md`](interface-v3-migration-test.md)（K1 48 / K2 48 / K3 71 / **K4 0** / **K5 0**）

## 9.1 四条历史一致性不变量（规范性）

| # | 不变量 | 规则 |
|---|---|---|
| **I-1** | **历史不可覆写** | `history` 只追加；回退/重开**以边表达**，不得改造成"只剩目标态"。审计必须仍能解释"为什么曾经到过 B/C" |
| **I-2** | **当前值唯一** | 任意 gap 同一时刻只能有一个 `authoritative current_value`：历史节点可多，真值唯一 |
| **I-3** | **reset ≠ 删除历史** | `whole_task reset` 只改**当前有效集**与**分支起点**；旧结论转失效，记录保留 |
| **I-4** | **local 不扩大闭包** | `revision_scope = local` 处**硬停**：不得因 `affected` 图很大而扩大传播 |

**唯一性谓词**

```
authoritative(g) := ∃! v ∈ history(g) :
        v.status = CONFIRMED ∧ v.confidence = confirmed ∧ g.validity_state = stable
```

## 9.2 回退：`reverted_to` + `reverts` 反向边

```yaml
reverted_to: target_snapshot | target_value | previous_state | unresolved
```

| # | 规则 |
|---|---|
| **V-1** | `supersedes` = 正向演化；**`reverts` = 历史恢复**——两者**必须并存** |
| **V-2** | 回退产生 **`reverts` 边**，中间值转 `INVALIDATED`（历史可读、不再 authoritative） |
| **V-3** | 回退目标必须能在 `history` 中定位；定位不了 → `unresolved` → 一次定位 |

## 9.3 重开：`reset_scope`

```yaml
reset_scope: artifact | decision_cluster | goal | whole_task | unresolved
```

| # | 规则 |
|---|---|
| **R-1** | `artifact` = 作废当前产出、**目标保留**；`decision_cluster` = 簇内重开；`goal` = 目标变但无新值 → **必须 ASK 新目标**且禁止带旧锚点继续产出；`whole_task` = 全部重来 |
| **R-2** | `whole_task` 仅在**无未拍板阻塞项**时成立，否则**降级** `decision_cluster`（与 T1 降级一致） |
| **R-3** | 显式保留目标优先（"重新来，但还是做官网" → `artifact`）；范围不明 → `unresolved`，**不得默认取 `artifact`** |

## 9.4 修改范围：`revision_scope`

```yaml
revision_scope: local | cluster | global | unresolved
```

| # | 规则 |
|---|---|
| **S-1** | `local` **默认拒绝扩张**传递闭包；`cluster` 簇内传播；`global` 全闭包 |
| **S-2** | `unresolved` → 一次澄清（可给局部示例）；**不得默认取 `global`** |

## 9.5 责任边界：`pending_external`

```yaml
pending_external:
  owner: <角色/人>
  reason: decision_owner | approval_required | information_source
  resume_condition: <什么事件发生即复位>
suspension_reason: external_owner        # 挂在既有 SUSPENDED 上，不新增 Gap 状态
```

| # | 规则 |
|---|---|
| **X-1** | **不新增 Gap 状态**：复用 `SUSPENDED` + `suspension_reason` |
| **X-2** | 进入后**不进 `askable_set`**；出口渲染"待 X 确认" |
| **X-3** | **恢复路径唯一**：`SUSPENDED → OPEN`（外部意见 = input/proposal，**不等于** `confirmed_value`）；`attempts`／`unresolved` **保留**；解除后重回 `askable_set`；**仍需用户本人确认** |
| **X-4** | **外部方授权不替代用户授权**；风险门不受外部方影响；`reason = information_source` 时用户仍是拍板人 → **保持 `OPEN`** |

## 9.6 认知边界：`feedback.intent`

```yaml
feedback:
  intent: unaware | unable | refused | evaded      # 事件属性，不是 Gap 状态、不是用户标签
```

```
topic_presented          := attempts ≥ 1 ∨ history 含该 gap 的 TEACH／SHOW 记录
user_evidences_awareness := 用户在当前或已有对话中
                            ① 明确承认该决策存在，或
                            ② 能主动描述该决策的选项 / 取舍 / 后果

unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness
unable  ⟺ (topic_presented ∨ user_evidences_awareness) ∧ 承认要决定 ∧ 无可用答案
refused ⟺ (topic_presented ∨ user_evidences_awareness) ∧ 明确不承担
evaded  ⟺ (topic_presented ∨ user_evidences_awareness) ∧ 无产出 ∧ 绕开
```

| # | 规则 |
|---|---|
| **N-1** | 两者均为**派生证据**，**不新增 Gap 状态或持久字段**；认知证据**优先于**呈现证据 |
| **N-2** | `unaware` → TEACH（≤3 条、讲后果）→ ASK；`unable` → §11.2 降维；`refused` → 非阻塞 assumed／**阻塞或 R6 → 保持 OPEN**；`evaded` → 计 `consecutive_no_signal`，**不得视为授权** |
| **N-3** | `intent` 是**事件属性**：同一 gap 可跨轮变化（`unable → refused` 及反向），历史只追加；**不得**据此建立用户永久标签 |

## 9.7 v3 验证与状态

| 项 | 结果 |
|---|---|
| 迁移测试 | **K1 48 / K2 48 / K3 71 / K4 0 / K5 0**（167 raw） |
| UA 证伪集 | UA-01～UA-04 **4/4 唯一**（V3-C4 修订后） |
| canary | L-20／23／24／25／30 **5/5**；V3-C1／C2／C3／C4 **4/4** |
| Release regression | **201/201 raw** |
| 冻结影响 | §11／§6.3／V0.3／Gap Model 正文**均未改动**；v2 章节逐字保留 |
| 状态 | **✅ 已并入并冻结（2026-10-02）** |

## 9.8 v3 与 v2 的关系

- v2（§1–§8）**逐字不变**：集合谓词、`validity_state`、跃迁门、§11.2 映射、重复询问口径、优先级声明继续有效；
- v3 只**新增**：历史一致性不变量（§9.1）、回退边（§9.2）、重开与修改范围（§9.3／§9.4）、责任边界（§9.5）、认知边界（§9.6）；
- v3 **不新增 Type／Action／Gap 状态**，**不改 §11／§6.3**，**不解冻任何冻结章节**。

---

# §10 Pending Resolution Transition Contract（V0.4.3，2026-10-02）

> **设计全文**：[`pending-resolution-transition-contract.md`](pending-resolution-transition-contract.md)
> **破坏测试**：[`pending-resolution-second-challenge-discovery.md`](pending-resolution-second-challenge-discovery.md)（PR-01～36）
> **本轮修正（预登记 #16）**：R-2 由"保持 `CLOSED` 只升 `confidence`" → **直接确认跃迁** `CLOSED(assumed) → CONFIRMED`（不经 OPEN）。

## 10.1 两段式模型（**不是 `intent → state` 一跳映射**）

```
pending_resolution → 第二次反馈
   ↓ ① intent dispatch            （决定进入哪一类跃迁分支）
   ↓ ② target / scope / risk / blocking / provenance / resume_condition（决定该分支的具体出口）
   ↓ 具体跃迁
```

**废弃**：`pending_resolution → 剩余确认次数 → 是否还能再问`。
**计数声明**：本 Contract **不自带计数器**；`pending_resolution` **不新增独立额度**；既有 `unable`／`evaded`／`no_signal` 计数**仍归其原冻结规则**（未改写归属与语义）。

## 10.2 六分支骨架

| intent | 出口（经 ② 判定） |
|---|---|
| **Revision** | 有新值 → 正常 Revision（`supersedes`／`reverts`）；无新值 → 保持待解决 + 索取最小必要新值；**不受"已确认过一次"限制** |
| **Unable** | 降维／`defer`／`default`；**`blocking = true` 不得静默默认** |
| **Refused** | 非阻塞 → 允许 `CLOSED(assumed)`；blocking／R6 → 保持 `OPEN` |
| **Authorization** | **必须重过 T1 scope + T2 risk gate**；`effective` 才 assumed；blocked → 未决 |
| **Challenge** | 新质疑 → 继续 `pending_resolution`；**撤回 → 恢复原有效值**；target 不明 → 先定位 |
| **External** | **按既有 `external reason` 分派**（**不新增子类型、不新增第七分支**）：<br>• `reason = information_source` → **依 §9.5 X-4 保持 `OPEN`**，**用户仍为决策者**（外部方只提供信息）<br>• `reason = external_owner` → 才进入既有 **`SUSPENDED(suspension_reason=external_owner)`**，`resume_condition` 满足后重新进入正常处理 |

> **CS-05 澄清（D05，2026-10-03）**：**External 描述依赖来源；`SUSPENDED(external_owner)` 描述决策权／可继续处理能力是否真的离开了"用户—系统"闭环。**
> ```
> External dependency  ≠  External decision ownership
> information source   ≠  decision authority
> ```
> 本摘要**引用既有 X-4**，**不重新定义合同**。

## 10.3 `CLOSED(assumed)` 重进入口（R-1～R-4）

| 类 | 条件 | 跃迁 | 经 OPEN |
|---|---|---|---|
| **R-1 material** | 改变 assumed 值／产生新决策 | `CLOSED(assumed)` → `OPEN` → intent dispatch | **经** |
| **R-2 confirmatory** | 用户**明确追认**当前 assumed 值，且未被 supersede／invalidated | `CLOSED(assumed)` → **`CONFIRMED`**；`confidence := confirmed`；`provenance += user_confirmed_after_assumed` | **不经** |
| **R-3 无决策意义** | 闲聊／无关提及 | 状态不变 | — |
| **R-4 原值已被 supersede** | 用户又确认已被替代的旧值 | **不得直接 CONFIRMED** → 走 `revert`（`reverted_to`）或当前状态规则 | 视路径 |

**R-2 为何必须是状态跃迁**：v1 冻结谓词 `effective_set = CONFIRMED ∩ valid`；若只升 `confidence` 而保持 `CLOSED`，gap **进不了生效集合**，且 `status` 与 `confidence` 会**争夺 authoritative truth**（双重事实源）。改为直接跃迁后**自然满足谓词**，且仍禁止无意义的 `OPEN → CLOSED` 抖动。

**原则（本次确立）**：**`status` 决定需求生命周期；`confidence`／`provenance` 只描述"这个状态为什么成立"**——不允许 `confidence` 反向改写生命周期意义。

## 10.4 G-1 质疑撤回 / G-2 meta feedback

- **G-1 `Challenge withdrawal`**：三条件（无新值 ∧ 明确撤回 ∧ 原值仍存在且未被 invalidated）→ 原 `authoritative value` 恢复有效；历史**必须保留** `challenged → withdrawal`。
- **G-2 meta feedback**：`target = interaction_process` → 解释原因、**gap 状态不变**、pending 保留、继续原流程；**不是第七种业务 Intent**，不新增 Gap 状态。

## 10.5 验证与 Release Gate（分栏）

```
Base raw regression      201/201      # B0 34 + B1 27 + B2 80 + B3 60
Pending Contract          18/18       # PC-01～PC-18
R-2 confirmation probes    4/4        # RC-01～RC-04
V3 canaries               PASS        # V3-C1/C2/C3/C4 + UA-01～04
K4                           0
K5                           0
```

- **PR-17 的 K5 已消失**（**归因已由 N10 更正，2026-10-03**）：
  - **原归因（已更正）**："判为 R-2：直接 `CONFIRMED`，不经 OPEN" —— 该读法**超出 R-2 的字面条件**。
  - **现归因**：`算了，还是你来定吧。` = **Authorization（决定权转移 ≠ 值接受）**，**该句不确认具体值、不产生 `CONFIRMED`**；后续状态迁移复用既有 Authorization／T1／T2 路径。R-2 定义不变。
  - 详见 [`pending-resolution-transition-contract.md`](pending-resolution-transition-contract.md) **§3.4 更正框／§3.5 N10 边界／§8.1 重确认**。
- 依赖面重跑唯一：`effective_set`／`CLOSED(assumed)`／`CLOSED(partial)`／Revision + `reverts`／§11 消费契约。
- **v2（§1–§8）与 v3（§9）章节逐字保留**，§10 为纯增量。
