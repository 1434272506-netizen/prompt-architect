# V0.4.2 Phase 2.3-B · Feedback Responsibility Extension

> **本轮性质**：**只设计，不写 `SKILL.md`**。
> **不修改**：`SKILL.md`／§11／§6.3／**Interface v2 冻结正文**／V0.3 规则／Gap Model 正文。
> **落盘形态**：并入 **Interface v3 候选**（与 [`feedback-state-extension-design.md`](feedback-state-extension-design.md) 的 A 类三字段共同构成 v3；**v3 目前只批准进入落盘候选，不冻结**）。
> **本轮顺序（用户裁决）**：`pending_external` → `unaware / unable / refused / evaded` →（后续）`pending_resolution` 二次质疑。
> **暂不做**：❌ `deprioritized`（属 Priority Layer，不进状态接口）❌ `pending_resolution` 二次计数（依赖 `feedback.intent` 落地）。

**本阶段的问题层次**：前面解决"AI 如何理解用户**想要什么**"；本轮解决"AI 如何理解用户**为什么这样反馈**，以及**谁拥有最终决策权**"。

---

## 1. 第一组 · 责任边界：`pending_external`

### 1.1 字段

```yaml
pending_external:
  owner: <角色/人>              # 老板 / 客户 / 市场部 / 法务 / 合伙人
  reason: decision_owner | approval_required | information_source
  resume_condition: <什么事件发生即复位>
suspension_reason: external_owner     # 挂在既有 SUSPENDED 上，不新增 Gap 状态
```

### 1.2 规则

| # | 规则 |
|---|---|
| **E-1** | **不新增 Gap 状态**：继续用 `SUSPENDED`，只加 `suspension_reason = external_owner`（与 `conflict_group`／`evaded` 并列区分原因） |
| **E-2** | 进入后**不进 `askable_set`**：不得对**用户本人**反复追问同一缺口 |
| **E-3** | `resume_condition` 必须明确；无法明确时取默认 `user_returns_with_decision`，并在出口写明"待 X 确认" |
| **E-4** | 出口渲染"待 X 确认"；已产出物按 `targets` 生成旧稿效力清单 |
| **E-5** | **风险门不受外部方影响**：若该缺口属 R6 闭集／高风险，**用户本人的拍板义务不因"要问老板"而转移**——若外部方也无权拍板，保持 `OPEN`（不得用 external 绕过风险门） |
| **E-6** | `reason` 区分两种不同处境：`decision_owner`（决策权不在场 → `SUSPENDED`）；`information_source`（只需补信息、用户仍是拍板人 → **保持 `OPEN`**，可继续推进其他分支） |

### 1.3 十个案例

| # | 用户原话 | owner | reason | resume_condition | 状态 | 唯一 |
|---|---|---|---|---|---|---|
| **EXT-01** | `我得问老板。` | 老板 | `decision_owner` | 用户带回老板意见 | `SUSPENDED(external_owner)` | **唯一** |
| **EXT-02** | `等客户确认后再定。` | 客户 | `decision_owner` | 客户确认到达 | `SUSPENDED(external_owner)` | **唯一** |
| **EXT-03** | `这块归市场部管。` | 市场部 | `decision_owner` | 市场部给出结论 | `SUSPENDED(external_owner)` | **唯一** |
| **EXT-04** | `问老板，但他这周不在。` | 老板 | `decision_owner` | 下周带回意见 | `SUSPENDED` + 出口标注时间窗 | **唯一** |
| **EXT-05** | `我先跟法务确认下合规要求。` | 法务 | **`information_source`** | 拿到合规要求 | **保持 `OPEN`**（用户仍是拍板人；可继续推进其他分支） | **唯一**（边界：不等于决策权转移） |
| **EXT-06** | `客户说下个月才给答复。` | 客户 | `decision_owner` | 下月答复到达 | `SUSPENDED` | **唯一** |
| **EXT-07** | `老板说随便，你们定。` | 老板 | `decision_owner`（但外部方把决定权交回） | — | **外部方授权 ≠ 用户授权** → 用户本人未授权时**保持 `OPEN`**；风险门不因第三方"随便"而放行 | **唯一** |
| **EXT-08** | `这得我们合伙人一起定。` | 合伙人（多人） | `decision_owner` | 集体结论 | `SUSPENDED` | **唯一** |
| **EXT-09** | `我问过老板了，他说用蓝色。` | — | — | **已带回结论** | 不进入 `SUSPENDED`；按内容走正常跃迁（Revision／CONFIRMED） | **唯一** |
| **EXT-10** | `没人管这块。` | 无 | — | — | **不是** `pending_external`（无 owner）：R6 闭集 → 保持 `OPEN` + 必须拍板；非 R6 → `CLOSED(assumed)` + 出口标注"责任真空" | **唯一** |

> **边界价值**：EXT-05（只需信息，拍板权仍在用户）与 EXT-01（决策权不在场）必须走不同路径；EXT-07 证明**第三方授权不能替代用户授权**；EXT-10 证明"无 owner"不是 `pending_external`。

---

## 2. 第二组 · 认知边界：`feedback.intent`

### 2.1 属性（不是 Gap 状态）

```yaml
feedback:
  intent: unaware | unable | refused | evaded
```

**为何与 gap 分离**：同一个 gap 的两次反馈可以是不同 intent（第一次 `unable`、第二次 `refused`）——它描述**用户如何回应**，不描述"需求是什么"。

### 2.2 四态定义与路径

| intent | 含义 | 路径 | 计数 |
|---|---|---|---|
| **`unaware`** | **不知道存在这个决策**（岔路口从未被呈现/教学过） | `TEACH`（≤3 条、讲后果）→ `ASK` | 不计 unresolved |
| **`unable`** | 知道问题、承认要决定，但**答不出** | §11.2 **降维问法** → 再问一次 | 计 `unresolved`／`consecutive_no_signal` |
| **`refused`** | 明确**不承担/不投入**该决定 | 非阻塞 → `CLOSED(assumed)` + 出口标注"用户拒绝提供"；**阻塞/R6 → 保持 `OPEN` + 最小关键决定**（风险门优先） | 不计 unresolved |
| **`evaded`** | **刻意绕开**（答别的／只回表情／沉默／转话题） | 计 `consecutive_no_signal`；**不得视为授权**；达 2 次按闸门换动作或落 `assumed` | 计入 |

### 2.3 判定契约（**依据状态量，不依据措辞**）

```
unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness
unable  ⟺ (topic_presented ∨ user_evidences_awareness)
          ∧ 用户承认要决定 ∧ 无可用答案
refused ⟺ (topic_presented ∨ user_evidences_awareness)
          ∧ 明确不承担（"你定／别问我／不想管"）
evaded  ⟺ (topic_presented ∨ user_evidences_awareness)
          ∧ 无产出 ∧ 绕开（答别的／表情／沉默／转话题）
```

**`topic_presented` 与 `user_evidences_awareness` 均为派生证据，不新增 Gap 状态或持久字段**：

```
topic_presented            := attempts ≥ 1
                            ∨ history 中存在该 gap 的 TEACH／SHOW 记录

user_evidences_awareness   := 用户在当前或已有对话中
                              ① 明确承认该决策存在，或
                              ② 能主动描述该决策的选项 / 取舍 / 后果
```

（`attempts`／`history`／`last_resolution` 均为 Gap Model §5 与 v1 已有字段；② 从对话文本判定，属解析层。）

> **修订缘由（V3-C4，预登记 #13）**：原判据 `unaware ⟺ ¬topic_presented` 会把"系统从未呈现、但用户明显知道该决策"的人误判为 `unaware`（→ 多教一遍）。补 `¬user_evidences_awareness` 后，认知证据优先于呈现证据。

### 2.4 核心测试：同一句"不知道"的四种上下文

| 上下文 | 判定 | 依据（状态量） | 路径 |
|---|---|---|---|
| 未展示过选项（AI 首次提出该岔路） | **`unaware`** | `topic_presented = false` | TEACH → ASK |
| 展示过选项，但选不出 | **`unable`** | `topic_presented = true` ∧ 承认要决定 | §11.2 降维 → 再问一次 |
| 展示过，且说"你定吧，我不想管" | **`refused`** | 明确不承担 | 非阻塞 assumed／阻塞保持 OPEN |
| 展示过，答"不知道"但随后答别的或沉默 | **`evaded`** | 无产出 ∧ 绕开 | 计 `consecutive_no_signal`；不视为授权 |

### 2.5 二十个案例

#### `unaware`（5）

| # | 用户原话（← 上下文） | 判定 | 路径 | 唯一 |
|---|---|---|---|---|
| **INT-01** | `原来还有这个问题？` | `unaware` | TEACH → ASK | **唯一** |
| **INT-02** | `不知道。` ← AI **首次**提出数据合规项 | `unaware`（`topic_presented=false`） | TEACH → ASK | **唯一** |
| **INT-03** | `这个还需要我定吗？` | `unaware` | TEACH + 说明为何必须由他拍板 | **唯一** |
| **INT-04** | `你说的这个我完全没概念。` ← 术语首现 | `unaware` | TEACH → ASK | **唯一** |
| **INT-05** | `等一下，这是什么意思？` | `unaware` | TEACH → ASK | **唯一** |

#### `unable`（5）

| # | 用户原话（← 上下文） | 判定 | 路径 | 唯一 |
|---|---|---|---|---|
| **INT-06** | `我不知道选哪个。` ← 三方向已展示 | `unable` | §11.2 降维 → 再问一次 | **唯一** |
| **INT-07** | `不知道。` ← 已展示方向但选不出 | `unable` | 同 INT-06 | **唯一**（**对照 INT-02**） |
| **INT-08** | `两个都差不多，我分不出。` | `unable` | 降维 + 更保真的 SHOW | **唯一** |
| **INT-09** | `选项我都理解，但定不了。` | `unable` | 降维；两次后按 §3.2 分流 | **唯一** |
| **INT-10** | `这超出我能力范围了。` ← 已呈现且承认要决定 | `unable` | 降维 → 延后／默认 | **唯一** |

#### `refused`（5）

| # | 用户原话（← 上下文） | 判定 | 路径 | 唯一 |
|---|---|---|---|---|
| **INT-11** | `不想管，你定。` ← 非阻塞细节 | `refused` | `CLOSED(assumed)` + 标注"用户拒绝提供" | **唯一** |
| **INT-12** | `这个你随便吧，别问我。` ← 非 R6 | `refused` | 同上 | **唯一** |
| **INT-13** | `我没精力想这个。` ← 非阻塞 | `refused` | 同上 | **唯一** |
| **INT-14** | `不想说。` ← **费用**（R6 闭集） | `refused` + 风险门 **blocked** | **保持 `OPEN`** + 部分稿 + 最小关键决定 | **唯一**（风险门优先） |
| **INT-15** | `你们看着办，出事别找我。` | `refused`（授权 + 免责双记） | 非阻塞 → assumed + 标注；R6 → 保持 OPEN | **唯一** |

#### `evaded`（5）

| # | 用户原话（← 上下文） | 判定 | 路径 | 唯一 |
|---|---|---|---|---|
| **INT-16** | 只回一个表情 | `evaded` | 计 `consecutive_no_signal`；不视为授权 | **唯一** |
| **INT-17** | 回答了**另一个**缺口（答非所问） | `evaded` | 吸收旁支信息 + 计未解决；继续当前缺口 | **唯一** |
| **INT-18** | 连续两轮沉默 | `evaded`×2 | 闸门：禁止同保真度第三次 → 换动作或落 `assumed` | **唯一** |
| **INT-19** | `先不说这个，先做别的。` | `evaded`（转话题） | 该缺口计一次回避；不视为授权 | **唯一** |
| **INT-20** | `嗯。`（无信息量） | `evaded` | 同 INT-16 | **唯一** |

---

## 3. 结果

| 组 | 案例 | 唯一 |
|---|---|---|
| 责任边界 `pending_external` | 10 | **10** |
| 认知边界 `unaware` | 5 | **5** |
| 认知边界 `unable` | 5 | **5** |
| 认知边界 `refused` | 5 | **5** |
| 认知边界 `evaded` | 5 | **5** |
| **合计** | **30** | **30/30 唯一** |

**关键对照（本轮的核心证明）**：`不知道` 判定为四种不同 intent，靠的是**状态量**（`topic_presented`／承认要决定／是否不承担／是否绕开），**不靠措辞**——INT-02（`unaware`）与 INT-07（`unable`）措辞相同、跃迁相反。

---

## 4. Interface v3 候选范围（落盘候选，**不冻结**）

| 来源 | 内容 | 状态 |
|---|---|---|
| Phase 2.3-A | `reset_scope`（5 值）／`revision_scope`（4 值）／`reverted_to`（3 值）+ **`reverts` 反向边** | ✅ 批准并入 v3 候选 |
| Phase 2.3-B（本轮） | `pending_external{owner, reason, resume_condition}` + `suspension_reason: external_owner` | ✅ 批准并入 v3 候选 |
| Phase 2.3-B（本轮） | `feedback.intent: unaware`（+ 既有 `unable`／`refused`／`evaded` 的路由契约） | ✅ 批准并入 v3 候选 |
| 解析层补充 | 复合语句分解契约（L-25） | 已入 A 文档 §5 |
| **暂不入 v3** | `deprioritized`（Priority Layer）、`pending_resolution` 二次计数 | ⏸ 暂缓 |

**v3 与 v2 的关系**：v2 = "反馈如何进入状态门"；**v3 = "状态变化后如何保持历史一致性"**（反向边、局部重构、责任与认知边界）。因涉及**状态图反向边与局部重构**，v3 **必须经过一次完整迁移测试**后才可冻结。

---

## 5. 冻结影响

| 对象 | 处置 |
|---|---|
| `SKILL.md`（含 §11、§6.3） | **未修改** |
| **Interface v2 冻结正文** | **未修改**（本轮为 v3 候选的增量设计） |
| V0.3 规则（`core/`／`strategies/`） | **未修改** |
| Gap Model 正文 | **未修改**（`suspension_reason`／`pending_external` 写在 v3 候选，不开新 Gap 状态） |
| 新增 Type / Action | **无** |

---

## 6. 下一步（待裁决）

1. **Interface v3 落盘前的迁移测试**：用 v3 候选重跑 **v2 全量回归**（C-01～C-15、I-01～I-12）＋ **Phase 2 全部案例**（L-01～L-30、TD-01～TD-20）＋ **2.3-A/B 共 60 例**（含 L-20/23/24/25/30 五例固定回归），验证"反向边与局部重构"不破坏既有跃迁。
2. **`pending_resolution` 二次质疑**：待 `feedback.intent` 落地后开工（四种第二次质疑：Revision／unable／authorization／challenge）。
3. **`deprioritized`**：移交后续 **Priority Model**，不进状态接口。
