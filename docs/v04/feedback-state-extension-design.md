# V0.4.2 Phase 2.3 · Feedback State Extension（设计 + 30 例）

> **本轮性质**：**只设计，不写 `SKILL.md`**。
> **不修改**：`SKILL.md`／§11／§6.3／**Interface v2 冻结正文**（`gap-ledger-interface.md` 一字不动）。
> **落盘形态**：本文件即 **Interface v3 候选**（v2 之上**纯增量**的字段扩展层）；v3 待批准后才并入接口正文。
> **上游**：[`feedback-language-map.md`](feedback-language-map.md)（L-01～L-30）、[`feedback-transition-design.md`](feedback-transition-design.md)（T1/T2/T7）、[`gap-ledger-interface.md`](gap-ledger-interface.md)（**v2，已冻结**）
> **纪律**：每新增一个字段，必须证明它解决的是**"状态不可表达"**，而不是**"规则不够细"**。

**分组（按你的优先级）**

| 组 | 内容 | 状态 |
|---|---|---|
| **2.3-A（先做）** | `reset_scope` · `revision_scope` · `reverted_to` | 状态缺口补全 |
| **2.3-B（设计批准、暂缓）** | `deprioritized` · `pending_external` · `unaware` ＋ `feedback.intent` 分类（`refused`／`unable`／`evaded`） | 优先级与反馈方式语义 |

---

## 1. 六字段设计

### A-1 `reset_scope`

```yaml
reset_scope: artifact | decision_cluster | goal | whole_task | unresolved
```

| 取值 | 含义 | 跃迁 | 出口要求 |
|---|---|---|---|
| `artifact` | 删当前方案，**目标保持** | 受影响 `targets` 作废；目标 `CONFIRMED` 不动；重新产出 | 旧稿效力清单 |
| `decision_cluster` | 重开当前决策簇 | 簇内 gap → `CHALLENGED`／重新消解；其余保留 | 列出重开项 |
| `goal` | 目标变了但**无新值** | `CHALLENGED(goal)` + `targets` 标记 + **必须 ASK 新目标** | 禁止带旧锚点继续 |
| `whole_task` | 全部重来 | 仅当**无未拍板阻塞项**时成立；否则**降级** `decision_cluster`（与 T1 降级一致） | 重新走 P0 |
| `unresolved` | 范围不明 | **先一次定位**，不得默认取 `artifact` | 一次 ASK |

**判定顺序**：显式保留目标（"重新来，但还是做官网"）→ `artifact`；显式"全部／推倒重做"→ `whole_task`（过阻塞检查）；指同时多版产出物 → `unresolved`。

### A-2 `revision_scope`

```yaml
revision_scope: local | cluster | global | unresolved
```

| 取值 | 含义 | 下游闭包 |
|---|---|---|
| `local` | 只改值本身 | **不扩张**（默认拒绝传递闭包） |
| `cluster` | 同簇调整 | 簇内传播 |
| `global` | 大改 | 全传递闭包 |
| `unresolved` | 范围说不出 | 一次澄清（可给局部示例），**不得默认取 global** |

> 无此字段时的失效：任何 Revision 都按全闭包处理 → "稍微调一下"把整个下游作废（L-24 的成因）。

### A-3 `reverted_to`（状态图**反向边**）

```yaml
reverted_to: target_snapshot | target_value | previous_state
```

| 取值 | 目标 | 记录 |
|---|---|---|
| `target_snapshot` | 指定版本/快照 | 新增 `reverts` **反向边**；中间值 → `INVALIDATED` |
| `target_value` | 指定历史值 | 同上（值级回退） |
| `previous_state` | 上一个确认态 | 同上（一步回退） |
| `unresolved` | 指代不明 | 一次定位 |

**三条硬约束**：① `history` 只追加、不改写（回退靠边，不靠删除）；② 回退**必须**产生反向边，否则图无法表达"值复活"；③ 回退目标必须能在 `history` 中定位，否则转 `unresolved`。

### B-1 `pending_external`（Phase 2.3-B）

> **本小节已被 [`feedback-responsibility-extension-design.md`](feedback-responsibility-extension-design.md) §1 **细化并取代**（按 2026-10-02 裁决：**不新增 Gap 状态**，继续用 `SUSPENDED` + `suspension_reason: external_owner`；字段为 `owner / reason / resume_condition`）。此处仅留索引。

```yaml
pending_external:
  owner: <角色/人>            # 老板 / 客户 / 市场部 / 法务 / 合伙人
  reason: decision_owner | approval_required | information_source
  resume_condition: <什么事件发生即复位>
suspension_reason: external_owner     # 挂在既有 SUSPENDED 上
```

- **不进 `askable_set`**（不对用户本人反复追问）；出口渲染"待 X 确认"。
- **不是** `unable`、**不是** `refused`：缺的是**决策权不在场**。
- 边界：`reason = information_source` 时用户仍是拍板人 → **保持 `OPEN`**，不落 `SUSPENDED`；外部方授权**不替代**用户授权。

### B-2 `unaware`（Phase 2.3-B · **属于 `feedback.intent`，不是 gap 状态位**）

| intent | 含义 | 动作 |
|---|---|---|
| `unable` | 知道问题，答不出 | §11.2 降维 → 再问一次 |
| `unaware` | **不知道自己需要决定**（岔路口未被呈现过） | **TEACH**（≤3 条、讲后果）→ 再 ASK |

**判定依据是状态量，不是措辞**：该岔路口**是否曾被呈现/教学过**（`topic_presented := attempts ≥ 1 ∨ history 含该 gap 的 TEACH／SHOW 记录`，**由既有字段派生、不新增字段**）。

**V3-C4 修订（2026-10-02，预登记 #13）**——`topic_presented` 是重要证据，但**不是唯一来源**：

```
unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness

user_evidences_awareness := 用户在当前或已有对话中
                           ① 明确承认该决策存在，或
                           ② 能主动描述该决策的选项 / 取舍 / 后果
```

- 两者均为**派生证据**，**不新增 Gap 状态、不新增持久字段**。
- 例："我知道这个问题，但一直没想清楚"、"预算我考虑过，还没定上限"、"性能和画质我知道要取舍，只是还没选" → **NOT `unaware`** → `unable`／`undecided`（§11.2 降维）。
- 完整契约与 20 例见 [`feedback-responsibility-extension-design.md`](feedback-responsibility-extension-design.md) §2。

### B-3 `deprioritized`（Phase 2.3-B · 影响 **priority**，不影响状态）

```yaml
deprioritized: true | false
```

- 只降低该 gap 的**问询优先级**；**不产生** `CLOSED(assumed)`。
- **不得**作用于 R6 闭集／高风险 C 项（风险门优先级更高）。
- 因此它不是状态转换字段 —— 归 2.3-B 的理由与你的判断一致。

### B-4 `feedback.intent` 属性（`refused` / `unable` / `evaded`）

```yaml
feedback:
  intent: refused | unable | evaded | unaware | ...
```

- 描述的是**用户反馈方式**，不是需求状态 → 作为**反馈属性**承载，不新开 gap 状态。
- `refused` + `blocking` → 不再重复请拍板，`CLOSED(assumed)` + 显式标注"用户拒绝提供"（沿用 F3-06/S-03 迁移规则）；
- `refused` + **R6 闭集** → 风险门优先：保持 `OPEN` + 部分稿 + 最小关键决定；
- `evaded` → 计 `consecutive_no_signal`，**不得**视为授权。

---

## 2. 30 个案例

链式字段：`原话 | Intent | target | 新字段值 | risk gate | transition | 唯一`

### reset（8）

| # | 用户原话（← 上下文） | Intent | target | `reset_scope` | gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **RST-01** | `重新来。` ← 刚出一版稿，目标未变 | `RESET_REQUEST` | `artifact` | `artifact` | — | 旧稿作废（`targets`）+ 目标保留 + 重新产出 | **唯一** |
| **RST-02** | `推倒重做。` ← 对结构不满 | `RESET_REQUEST` | `confirmed_value` | `decision_cluster` | — | 簇内重开，其余保留 | **唯一** |
| **RST-03** | `不要这个方向。` ← 方向已确认 | `CHALLENGED_VALUE` | `confirmed_value` | **不适用**（不是 reset） | — | 走 T7：`CHALLENGED` + 索取新值 | **唯一**（边界：否定≠重开） |
| **RST-04** | `换个方案。` ← 方案稿已出 | `RESET_REQUEST` | `artifact` | `artifact` | — | 方案作废，目标不动 | **唯一** |
| **RST-05** | `从头再来。` ← 无未拍板阻塞项 | `RESET_REQUEST` | `goal` | `whole_task` | — | 全量重开 + 重新走 P0 | **唯一** |
| **RST-06** | `重新来，但还是做官网。` | `RESET_REQUEST` | `artifact` | `artifact`（**显式保留目标**） | — | 只作废稿，目标保留 | **唯一** |
| **RST-07** | `重新来。` ← 同时存在方向稿与成稿 | `RESET_REQUEST` | `target_unresolved` | `unresolved` | — | **先一次定位** | **唯一（流程唯一）** |
| **RST-08** | `别改了，全部重来。` ← 仍有费用项未拍板 | `RESET_REQUEST` | `goal` | 声称 `whole_task` → **降级** `decision_cluster` | 费用项 **blocked** | 降级重开；费用项保持 `OPEN` | **唯一** |

### revert（5）

| # | 用户原话（← 上下文） | Intent | target | `reverted_to` | gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **REV-01** | `还是原来的。` ← 上一轮刚改过 | `REVERT_REQUEST` | `confirmed_value` | `previous_state` | — | `reverts` 反向边 + 中间值 `INVALIDATED` | **唯一** |
| **REV-02** | `回到最开始那版。` | `REVERT_REQUEST` | `confirmed_value` | `target_snapshot` | — | 反向边 + 快照定位 | **唯一** |
| **REV-03** | `用刚才那个版本。` | `REVERT_REQUEST` | `confirmed_value` | `target_snapshot`（上一版） | — | 反向边 | **唯一** |
| **REV-04** | `还是用黑色吧。` | `REVERT_REQUEST` | `confirmed_value` | `target_value`（历史值） | — | 值级回退 + 当前值 `INVALIDATED` | **唯一** |
| **REV-05** | `改回我最初说的那个。` ← 值/版不明 | `REVERT_REQUEST` | `target_unresolved` | `unresolved` | — | **先一次定位** | **唯一（流程唯一）** |

### revision scope（5）

| # | 用户原话（← 上下文） | Intent | target | `revision_scope` | gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **RSC-01** | `稍微调一下。`（无新值） | `REVISION_CANDIDATE` | `confirmed_value` | `local` | — | 索取新值（一次 ASK）；闭包**不扩张** | **唯一** |
| **RSC-02** | `改一点，别动别的。` | `REVISION_CANDIDATE` | `confirmed_value` | `local`（显式） | — | 仅改该值 | **唯一** |
| **RSC-03** | `整体优化一下。` | `REVISION_CANDIDATE` | `confirmed_value` | `cluster` | — | 簇内传播 | **唯一** |
| **RSC-04** | `大改一版。` | `REVISION_CANDIDATE` | `confirmed_value` | `global` | — | 全传递闭包 | **唯一** |
| **RSC-05** | `调一下，具体哪我也说不好。` | `REVISION_CANDIDATE` | `confirmed_value` | `unresolved` | — | 一次澄清（可给局部示例）；**不得默认 global** | **唯一（流程唯一）** |

### external owner（4）

| # | 用户原话 | Intent | target | `pending_external` | gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **EXT-01** | `我得问老板。` | `EXTERNAL_DEPENDENCY` | — | `owner=老板` | — | `SUSPENDED(deferred_external)`；不进 `askable`；出口"待老板确认" | **唯一** |
| **EXT-02** | `等客户确认后再定。` | `EXTERNAL_DEPENDENCY` | — | `owner=客户` | — | 同上 | **唯一** |
| **EXT-03** | `这块归市场部管。` | `EXTERNAL_DEPENDENCY` | — | `owner=市场部` | — | 同上 | **唯一** |
| **EXT-04** | `问老板，但他这周不在。` | `EXTERNAL_DEPENDENCY` | — | `owner=老板` + 时间窗 | — | 暂缓确认项；**不反复追问本人** | **唯一** |

### unaware（4）

| # | 用户原话（← 上下文） | Intent | target | 判据（状态量） | gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **UNW-01** | `原来还有这个问题？` | `unaware` | 该 gap | 岔路口**未呈现过** | — | `TEACH`（≤3 条、讲后果）→ 再 ASK | **唯一** |
| **UNW-02** | `不知道。` ← AI 首次提出数据合规项 | `unaware` | `constraint` | 未呈现过 | — | `TEACH` → ASK | **唯一** |
| **UNW-03** | `不知道。` ← 用户已被告知该岔路 | `unable` | 该 gap | **已呈现过** | — | §11.2 降维 → 再问一次 | **唯一**（对照 UNW-02） |
| **UNW-04** | `这还需要我决定吗？` | `unaware` | 该 gap | 未呈现过 | — | `TEACH` + 说明为何必须由他拍板 | **唯一** |

### refused / unable / evaded（4）

| # | 用户原话（← 上下文） | Intent | target | 属性 | gate | transition | 唯一 |
|---|---|---|---|---|---|---|---|
| **FBC-01** | `不想说。` ← 非阻塞细节 | `refused` | 该 gap | 反馈方式 | passed | `CLOSED(assumed)` + 标注"用户拒绝提供" | **唯一** |
| **FBC-02** | `不想说。` ← **费用**（阻塞项） | `refused` | 该 gap | 反馈方式 | **blocked** | **风险门优先**：保持 `OPEN` + 部分稿 + 最小关键决定 | **唯一** |
| **FBC-03** | `我不太清楚。` ← 已呈现过 | `unable` | 该 gap | 反馈方式 | — | 降维 → 延后 → 或默认（按 §11.2 分流） | **唯一** |
| **FBC-04** | 用户只回一个表情 | `evaded` | — | 反馈方式 | — | 计 `consecutive_no_signal`；**不得视为授权** | **唯一** |

---

## 3. 结果

| 组 | 案例 | 唯一 | 流程唯一 |
|---|---|---|---|
| reset | 8 | 7 | 1（RST-07） |
| revert | 5 | 4 | 1（REV-05） |
| revision scope | 5 | 4 | 1（RSC-05） |
| external owner | 4 | 4 | 0 |
| unaware | 4 | 4 | 0 |
| refused/unable/evaded | 4 | 4 | 0 |
| **合计** | **30** | **27** | **3** |

**30/30 均有唯一裁定路径**（27 直接 + 3 流程唯一 = 先在状态量上定位一次）。**Phase 2.2 遗留的 5 个不唯一案例全部关闭**（见下）。

---

## 4. 固定回归：L-20 / L-23 / L-24 / L-25 / L-30

| 案例 | 原缺口 | 本轮的关闭方式 | 对应新案例 | 结果 |
|---|---|---|---|---|
| **L-20** | reset | `reset_scope` 五值分流（artifact／cluster／goal／whole_task／unresolved） | RST-01／02／05／07 | **唯一** |
| **L-23** | revert | `reverted_to = previous_state` + `reverts` 反向边 | REV-01 | **唯一** |
| **L-24** | revision scope | `revision_scope = local` + 索取新值（一次 ASK） | RSC-01 | **唯一** |
| **L-25** | split feedback | **复合语句分解契约**（见 §5）：分解为 `REVISION(有值, local)` + `RESET(artifact)` 两条独立链 | RST-04 + RSC-01 | **唯一** |
| **L-30** | revision + conflict（回退到首版） | `reverted_to = target_snapshot` | REV-02 | **唯一** |

**这 5 例转入固定回归**：今后任何字段改动必须让它们继续通过。同时 **TD-01～TD-20 与 L-01～L-19、L-21、L-22、L-26～L-29 不得回归**（新字段为纯增量，不改变既有跃迁）。

---

## 5. 一处解析契约补充（不是新字段）

**复合语句分解**（服务于 L-25）：

> 一句话含**两个及以上独立反馈**时（"改成蓝色，另外页面重来"）：**先分解**为 n 条独立反馈，**各自走 T1→T7→T2 门**；无法分解或相互依赖 → **一次澄清**，不得只执行其中一条。

- 归属：Layer 1 之后的**分解步**（语言映射层），**不是** Interface v2 的改动，也不新增 gap 状态。
- 禁止：把复合语句压成单条 intent（会静默丢掉其中一半反馈）。

---

## 6. 纪律检查：每个字段解决的是"状态不可表达"，不是"规则不够细"

| 字段 | 若无此字段会出现什么 | 归因 | 判定 |
|---|---|---|---|
| `reset_scope` | "重新来"无法区分"删稿保目标"与"目标变了"→ 状态**无法表达** | 状态不可表达 | ✅ 通过 |
| `revision_scope` | 任何 Revision 都按全闭包 → "稍微调一下"把整个下游作废 | 状态不可表达 | ✅ 通过 |
| `reverted_to` | 图里只有单向 `supersedes` → "值复活"**无法表达** | 状态不可表达 | ✅ 通过 |
| `pending_external` | 只能记 `unable` → 把"决策权不在场"误表为"用户答不出" | 状态不可表达 | ✅ 通过 |
| `unaware` | 只能记 `unable` → 对未呈现过的岔路口继续追问（用户仍答不出） | 状态不可表达 | ✅ 通过（作为 `feedback.intent` 属性，不新开 gap 状态） |
| `deprioritized` | 影响的是**优先级**，不影响状态可表达性 | **不是**状态字段 | ✅ 归 2.3-B（与你的判断一致） |
| `refused／unable／evaded` | 描述**反馈方式**，不是需求状态 | **不是**状态字段 | ✅ 作为 `feedback.intent` 承载 |

---

## 7. 冻结影响

| 对象 | 处置 |
|---|---|
| `SKILL.md`（含 §11、§6.3） | **未修改** |
| **Interface v2 冻结正文**（`gap-ledger-interface.md`） | **未修改**（本文件是 v3 候选，纯增量；v3 待批准后才并入） |
| V0.3 冻结规则（`core/`／`strategies/`） | **未修改** |
| Gap Model 正文 | **未修改** |
| 新增 Type / Action | **无**（现有 A–E 与五动作不变） |

---

## 8. 下一步（待裁决）

1. **Interface v3 是否落盘**：把 §1 六字段 + §5 分解契约并入接口正文（届时走"登记 → 落盘 → 全量回归 → 重新冻结"）。
2. **2.3-B 是否开工**：`pending_external` / `unaware` / `deprioritized` + `feedback.intent` 分类（3 例 `refused`／`unable`／`evaded` 已在本轮给出回归位）。
3. **延期不变**：`pending_resolution` 二次质疑计数（依赖 `feedback.intent` 分类）。
