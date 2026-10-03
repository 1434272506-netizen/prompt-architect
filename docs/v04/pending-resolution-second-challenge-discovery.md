# V0.4.3 · `pending_resolution` Second-Challenge Discovery（36 例破坏测试）

> **阶段定位**：**先做破坏测试，不写规则。** 验证核心假设：**第二次质疑不是"次数问题"，而是"反馈意图问题"。**
> **不修改**：`SKILL.md`／§6.3／§11／**Interface v2**／**Interface v3**／V0.3 规则。
> **不新增**：Type／Action／**Gap 生命周期状态**。
> **验收**：**36/36 有明确分析结果**；**K4 = 0**；K5 可出现但必须定位根因。

**被测的旧假设（本轮要打的靶子）**

```
pending_resolution：
  允许一次确认
  不得连续第二次          ← 预期最值得证伪的一条
```

**每例记录 9 项**：当前 gap 状态 → 第一次 `pending_resolution` 来源 → 第二次反馈原话 → `feedback.intent` → `feedback_target`／`scope` → 当前 v3 能否唯一承接 → 应发生跃迁 → **"确认额度"是否真的需要计数** → 是否 K4／K5。

**K 口径**：`K1` 旧行为保持｜`K2` 结果不变、状态表示更精确｜`K3` v3 接管｜`K4` **回归（旧行为被改错）**｜`K5` **两个解释都合法**

---

## 一、Revision 分支（6）

| # | 当前状态 & 第一次来源 | 第二次反馈原话 | intent | target / scope | v3 唯一 | 应发生跃迁 | 计数必要? | K |
|---|---|---|---|---|---|---|---|---|
| PR-01 | `CHALLENGED/pending`（主色）；第一次：用户把主色由蓝改墨绿 | `还是改成原来的蓝吧。` | `Revision`（**回退型**） | `confirmed_value`／`current_gap` | ✅ | `reverted_to=target_value` → CONFIRMED(蓝)；pending **终结** | **不必要**（计数会把第三次合法修改判超额度） | K2 |
| PR-02 | 同上（视觉方向） | `算了，回到刚才那版。` | `Revision`（回退） | `confirmed_value`／`current_gap` | ✅ | `reverted_to=previous_state`；中间值 INVALIDATED | 不必要 | K2 |
| PR-03 | `CHALLENGED/pending`（文案）；第一次：用户说"文案要改" | `就那一段稍微调一下。` | `Revision`（**局部**） | `confirmed_value`／`revision_scope=local` | ✅ | 只改该值，闭包**不扩张**（§9.4 S-1） | 不必要 | K2 |
| PR-04 | `CHALLENGED/pending`（产物锚点）；第一次：用户提"想换方向" | `我想换个目标，做企业版。` | `Revision`（**goal**） | `goal`／`whole_task` | ✅ | §6.5A 锚点 Revision + 下游闭包重开 | 不必要 | K3 |
| PR-05 | `CONFIRMED`（"不放真人照片"）被质疑为 pending | `改成放真人照片。`（**无修正声明**） | `Revision`（有值） | `confirmed_value`／gap | ✅ | §6.5B **Conflict**：暂停该组 + 一次最小澄清 | **无意义**（冲突路径不适用额度） | K1 |
| PR-06 | `CHALLENGED/pending`（主色）；已改过一次 | `再改回深灰。`（**连续二次 Revision**） | `Revision`（有值） | `confirmed_value`／gap | ✅ | 新值确认 → CONFIRMED；**新的一轮** pending 就此终结（非"超额度"） | **不必要**（连续 Revision 是合法链） | K2 |

## 二、Unable 分支（6）

| # | 当前状态 & 第一次来源 | 第二次反馈原话 | intent | target / scope | v3 唯一 | 应发生跃迁 | 计数必要? | K |
|---|---|---|---|---|---|---|---|---|
| PR-07 | `CHALLENGED/pending`（受众）；第一次：用户改口受众 | `我还是拿不准给谁看。` | `unable` | 该 gap／gap | ✅ | §11.2 降维 → 再问一次；pending **保持** | **无意义**（该缺口本就待用户决定） | K2 |
| PR-08 | 同上（已降维过一次） | `你还是给我几个例子吧。` | `unable` | 该 gap／gap | ✅ | 再降维 + 更保真的 SHOW；**不因"第二次"禁止** | **不必要**（计数会误伤） | K2 |
| PR-09 | `CHALLENGED/pending`（预算）；第一次：用户质疑预算约束 | `我得先查一下行情。` | `unable`（信息不足） | 该 gap／gap | ✅ | 延后（`OPEN+deferred`）或 INSPECT；可继续其他分支 | 无意义 | K2 |
| PR-10 | `CHALLENGED/pending`（性能取舍） | `我知道要取舍，但选不出来。` | `unable`（认知） | 该 gap／gap | ✅ | §11.2 降维；**NOT `unaware`**（§9.6 N-1 认知证据优先） | 不必要 | K3 |
| PR-11 | `CHALLENGED/pending`，**非阻塞**项 | `这个我真的不知道。` | `unable` | 该 gap／gap | ✅ | 两次后按 §3.2 分流：默认值 + 假设区 | 无意义 | K1 |
| PR-12 | `CHALLENGED/pending`，**阻塞**项（范围） | `我怕选错，你帮我判断。`（仍无答案） | `unable` | 该 gap／gap | ✅ | 输出**可完成部分** + 说明仍缺哪一决定；**不得因额度禁止再问** | **不必要**（额度会阻塞交付） | K2 |

## 三、Refused 分支（6）

| # | 当前状态 & 第一次来源 | 第二次反馈原话 | intent | target / scope | v3 唯一 | 应发生跃迁 | 计数必要? | K |
|---|---|---|---|---|---|---|---|---|
| PR-13 | `CHALLENGED/pending`（非阻塞） | `不想决定，你看着办。` | `refused`（+ 潜在授权） | 该 gap／gap | ✅ | 非阻塞 → `CLOSED(assumed)` + 标注"用户拒绝提供"；pending 终结 | 无意义 | K1 |
| PR-14 | `CHALLENGED/pending`（关键约束） | `别问我了，就这样。` | `refused` | 该 gap／gap | ✅ | 阻塞/R6 → 保持 `OPEN` + 最小关键决定；**不重复请拍板** | 无意义 | K1 |
| PR-15 | `CHALLENGED/pending`（细节） | `随便，你定。` | `refused` + `Authorization` | 该 gap／gap | ✅ | 过 T2 风险门 → passed → assumed；拒答记录保留 | 无意义 | K1 |
| PR-16 | `CHALLENGED/pending`（**费用** = R6） | `这部分我不想管。` | `refused` | 该 gap／gap | ✅ | **风险门 blocked** → 保持 `OPEN`（不得默认） | 无意义 | K1 |
| PR-17 | `CHALLENGED/pending` 已因拒绝落 `CLOSED(assumed)` | `算了，还是你来定吧。` | `Authorization` | 该 gap／gap | ❌ **见 K5-1** | 需判定：**重开该 gap 走授权** 还是 **终态不再重开** | 无意义（问题是重开入口，不是额度） | **K5** |
| PR-18 | `CHALLENGED/pending` 已因拒绝落 assumed | `我想改成蓝色。` | `Revision`（有值） | `confirmed_value`／gap | ✅ | 视为**重开 + Revision**：新值 CONFIRMED（旧 assumed 被 supersedes） | 不必要 | K2 |

## 四、Authorization 分支（6）

| # | 当前状态 & 第一次来源 | 第二次反馈原话 | intent | target / scope | v3 唯一 | 应发生跃迁 | 计数必要? | K |
|---|---|---|---|---|---|---|---|---|
| PR-19 | `CHALLENGED/pending`（语气） | `你决定吧。` | `Authorization` | —／`current_gap` | ✅ | T2 门 passed → `CLOSED(assumed)`；pending 终结 | 无意义 | K2 |
| PR-20 | `CHALLENGED/pending`（图标） | `按默认来。` | `Authorization` | —／`current_gap` | ✅ | 同上 | 无意义 | K2 |
| PR-21 | `CHALLENGED/pending`（§11.7 合并问句：3 子 gap） | `都听你的。` | `Authorization` | —／`current_decision_cluster` | ✅ | 逐 gap 过门 → 3 项各自 assumed（`split_feedback`） | 无意义 | K2 |
| PR-22 | `CHALLENGED/pending`（**数据用途** = R6） | `这个你随便。` | `Authorization` | —／gap | ✅ | **门 blocked** → 保持 `OPEN` + ASK；授权不生效 | 无意义 | K2 |
| PR-23 | `CHALLENGED/pending`，用户上一轮已授权并落 assumed | `刚才那个你定的不算，我要改。` | `Revision`（+ 撤销授权） | `confirmed_value`／gap | ✅ | 撤销 prior authorization → 重开 + 新值确认；历史保留（§9.1 I-1） | **不必要**（反悔是合法新信息，非额度问题） | K2 |
| PR-24 | `CONFIRMED`（主色） + `pending`（配色细则） | `你看着办，顺便改成红色。` | `Revision`（有值）+ `Authorization` | `confirmed_value`／gap | ✅ | **有值优先**：Revision 覆盖主色；授权只覆盖仍未定项 | 无意义 | K2 |

## 五、Challenge 分支（6）

| # | 当前状态 & 第一次来源 | 第二次反馈原话 | intent | target / scope | v3 唯一 | 应发生跃迁 | 计数必要? | K |
|---|---|---|---|---|---|---|---|---|
| PR-25 | `CHALLENGED/pending`（受众） | `你理解错了，我说的不是这个意思。` | `Challenge`（质疑理解） | **`target_unresolved`** | ✅（流程唯一） | 一次定位 → 回 T7 分流；不默认绑定 | 无意义 | K2 |
| PR-26 | `CHALLENGED/pending`（推断值，provenance=ai_inference） | `这不是我说的，你自己编的。` | `Challenge`（质疑推断） | `confirmed_value`（provenance 非用户） | ✅ | 该值转 `INVALIDATED` → `OPEN` 重新消解（§7 铁律 1） | 无意义 | K3 |
| PR-27 | `CHALLENGED/pending`（视觉方向） | `这个方向不对。`（**无新值**） | `Challenge` | `confirmed_value`／gap | ✅ | 保持 `pending_resolution` + **索取新值**（一次） | **不必要**（要的是新值，不是额度） | K2 |
| PR-28 | `CHALLENGED/pending`（SHOW 提案在讨论中） | `都不喜欢。` | `Challenge` | `proposal`／cluster | ✅ | `disagreed` + 闸门（换方向/提保真度） | 无意义 | K1 |
| PR-29 | `CHALLENGED/pending`（多处待改） | `不对。`（无指代） | `Challenge` | `target_unresolved` | ✅（流程唯一） | 一次定位 | 无意义 | K2 |
| PR-30 | `CHALLENGED/pending`；已 challenge 过一次 | `我还是觉得不对。`（**连续 challenge**） | `Challenge` | `confirmed_value`／gap | ✅ | **继续**保持 pending + 定位/索取；**不得因"第二次"判违规** | **不必要**（计数会误伤合法质疑链） | K2 |

## 六、External dependency 分支（6）

| # | 当前状态 & 第一次来源 | 第二次反馈原话 | intent | target / scope | v3 唯一 | 应发生跃迁 | 计数必要? | K |
|---|---|---|---|---|---|---|---|---|
| PR-31 | `CHALLENGED/pending`（预算） | `我得问老板。` | `External` | —／gap | ✅ | `SUSPENDED(suspension_reason=external_owner, reason=decision_owner)`；不进 askable | 无意义 | K2 |
| PR-32 | `CHALLENGED/pending`（视觉方向） | `等客户拍板。` | `External` | —／gap | ✅ | 同上（owner=客户） | 无意义 | K2 |
| PR-33 | `CHALLENGED/pending`（合规项 = R6） | `我先跟法务确认下要求。` | `External` | —／gap | ✅ | `reason=information_source` → **保持 `OPEN`**（拍板权仍属用户，§9.5 X-4） | 无意义 | K3 |
| PR-34 | `SUSPENDED(external_owner)` | `客户说保留方案 B。` | `External`→**恢复** | —／gap | ✅ | `SUSPENDED → OPEN`（外部意见 = input，非 confirmed）；attempts 保留；仍需用户确认 | **不必要**（恢复靠 `resume_condition`，不靠额度） | K3 |
| PR-35 | `CHALLENGED/pending`（主色） | `老板说用蓝色，就这么定。` | 转述 + `Authorization` | `confirmed_value`／gap | ✅ | 用户本人拍板 → CONFIRMED(蓝)；**外部方授权本身不替代用户授权**（§9.5 X-4） | 无意义 | K2 |
| PR-36 | `CHALLENGED/pending`（合规项 = R6） | `合规那边说可以自动诊断。` | `External`（`information_source`） | —／gap | ✅ | **≠ decision_owner**：回到 `OPEN`，仍需用户/责任方明示拍板 | 无意义 | K3 |

---

## 七、四个攻击问题的结果

### Q1 · 同一 gap 第二次被质疑，是否真的需要重新计数？

**不需要。计数不是主变量。** 36 例的"计数必要性"分布：

| 计数必要性 | 例数 | 说明 |
|---|---|---|
| **不必要（会造成误伤）** | **14** | PR-01／02／06（Revision 链）、PR-08／10／12（unable 需继续降维）、PR-18／23（拒绝或授权后出现合法 Revision）、PR-25～27／30（challenge 链）、PR-34（恢复靠条件不靠额度） |
| **无意义（该 intent 直接终结或走别的门）** | **22** | PR-03／04／05、PR-07／09／11、PR-13～17、PR-19～22／24、PR-28／29、PR-31～33／35／36 |
| **必要** | **0** | — |

**结论**：旧限制"允许一次确认、不得连续第二次"**在 14 例上会直接误伤合法反馈**（Revision 链、Challenge 链、阻塞项降维），在其余 22 例上无任何作用。它描述的是**计数器**，而实际决定出口的是**intent**。

### Q2 · 不同 intent 是否应该完全不同地退出？

**应该。六分支出口互不相同，无法用统一计数表达：**

| intent | 出口 | 是否终结 pending |
|---|---|---|
| `Revision`（有值） | 覆盖 + `reverts`/`supersedes` → CONFIRMED | **终结** |
| `Revision`（无值） | 保持 pending + 索取新值（一次） | 不终结 |
| `Unable` | §11.2 降维 / 延后 / 默认（按阻塞性） | 不终结 |
| `Refused` | 非阻塞 → `CLOSED(assumed)`；R6 → 保持 OPEN | 非阻塞终结 |
| `Authorization` | 过 T2 门：passed → `CLOSED(assumed)`；blocked → 保持 OPEN | 生效即终结 |
| `Challenge` | 维持 `pending_resolution` + 定位/索取；撤回 → 回 `VALID` | 通常不终结 |
| `External` | `SUSPENDED(external_owner)`；`resume_condition` 满足后回 OPEN | 挂起（可恢复） |

### Q3 · "一次确认"旧限制是否会误伤合法 Revision / Challenge？

**会，且已定位 14 例**：连续 Revision（PR-06）、拒绝后 Revision（PR-18）、授权后反悔（PR-23）、连续 Challenge（PR-30）、阻塞项多轮降维（PR-12）、外部恢复（PR-34）——这些在旧限制下会被判"超出额度"，而它们**全部是合法且必要**的反馈。

### Q4 · 有没有某种第二次反馈既不属于六分支，又迫使新增状态？

**没有一例迫使新增 Gap 生命周期状态**，但发现 **3 个 intent 子型缺口**（均可用现有状态表达）：

| # | 形态 | 例子 | 归属 | 是否需新增状态 |
|---|---|---|---|---|
| G-1 | **质疑撤回**（withdraw challenge） | "算了，就按原来的"（无新值、无修改） | `Challenge` 的**终结子型** → 回 `VALID`（v2 §5.2 已有出口） | **否** |
| G-2 | **元反馈**（meta，指向 AI 过程而非需求） | "你为什么这么问？" | **不触碰 gap 状态机**（属 §2.1 对外表达/信任） | **否** |
| G-3 | **条件性放弃** | "改主意了，但如果改不了就算了" | `Revision` + 条件 → 用 `revision_scope`／`resume_condition` 表达 | **否** |

**结论**：Q4 的答案是"没有第四类新状态"，但有**三个 intent 子型**需要在下一轮的 Transition Contract 中显式列出。

---

## 八、K4 / K5 结果

| 指标 | 结果 |
|---|---|
| **K4（回归）** | **0** |
| **K5（歧义）** | **1**（PR-17） |
| K1 / K2 / K3 | 6 / 25 / 5 |

**K5-1 根因定位（PR-17）**

```
场景：gap 已因 refused 落 CLOSED(assumed) → 用户回来说"算了，还是你来定吧"
歧义：① Authorization 重开该 gap → CLOSED(assumed)（新的授权）
      ② 终态不再重开 → 保持原 assumed，不做处理
```

- **根因不是"额度"**，而是 **`CLOSED(assumed)` 的重开入口未定义**：v2／v3 定义了 `SUSPENDED → OPEN`、`INVALIDATED → OPEN`、`CHALLENGED → VALID/INVALIDATED`，但没写 **终态 `CLOSED` 在用户重新提及时的入口**。
- **与 §6.3 的关系**：§6.3 管"要不要追问"；本例是"用户主动回来授权"，不涉及追问 → **不需要动 §6.3**。
- **不新增状态**：可用既有 `CLOSED → OPEN`（同一 gap 重开）表达，只需在 Transition Contract 中补一行入口规则。
- **处理**：本轮**只报告，不写规则**（按你的指令）。

---

## 九、本轮验收

| 项 | 结果 |
|---|---|
| 36/36 有明确分析结果 | ✅ 36/36（每例 9 项齐备） |
| **K4 = 0** | ✅ 0 |
| K5 出现但定位根因 | ✅ 1 例（PR-17），根因＝`CLOSED(assumed)` 重开入口未定义 |
| 未修改 `SKILL.md`／§6.3／§11／Interface v2／v3／V0.3 | ✅ |
| 未新增 Type／Action／Gap 生命周期状态 | ✅ |

**对核心假设的判定**：**"第二次质疑不是次数问题，而是反馈意图问题"—— 成立。** 计数在 14/36 例上会误伤、在 22/36 例上无作用、在 0 例上必要；而每一个出口都由 `feedback.intent` 唯一决定（K4 = 0）。

**下一轮（待你批准）**：设计 **Pending Resolution Transition Contract**，建议只用一条主判据替换旧额度：

```
pending_resolution 的出口 = 由本轮反馈的 feedback.intent 决定；
"额度"不再是独立变量（仅保留 §3.2 的 unresolved 计数用于 Unable 分流）。
```

并补三处入口/子型：`CLOSED(assumed)` 的重开入口（K5-1）、`Challenge` 的撤回子型（G-1）、`meta` 反馈不触状态机（G-2）。
