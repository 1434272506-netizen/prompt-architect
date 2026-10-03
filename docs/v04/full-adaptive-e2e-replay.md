# V0.4.9 · Full Adaptive E2E Replay（12 个 5–9 轮五层剧本）

> **被测完整链**
> ```
> User Feedback → Gap / Feedback Interface → V0.3 Resolution → Priority Layer
>    → Scheduler Fairness → Action Bundle → §11（仅 ASK） → User-visible Response
> 旁路：Fairness Ledger → Notification Policy → 用户可见提醒
> ```
> **本轮最重要的一句话**：**Notification 虽然也产生用户可见文本，但绝不能因此变成"第二个 Action Engine"。**
> **纪律**：不改任何冻结正文，不写规则，不加字段；失败只定位"哪层越权／缺接口"。

**八条 E2E 不变量（E1–E6 沿用 V0.4.5，新增 E7／E8）**

```
E1  单一 authoritative current_value
E2  只有 Interface 改 Gap 状态
E3  只有 V0.3 决定 Action 类型
E4  Priority 只排序合法 Action
E5  §11 只在 ASK 被调度后工作
E6  用户可见输出不得暴露内部状态机术语
E7  Scheduler Fairness 不得改变 Gap 状态、Action 类型或显式用户 priority relation
E8  Notification Policy 不得改变调度、Gap、Action；只影响用户可见性
```

**每轮记录 14 项**（压缩为 4 行：`G` 状态／`F` 反馈语义／`A` 动作＋硬约束／`P` 调度；`FA` 公平证据／`N` 通知决策／`§11`；`U` 用户可见／`W` 写回／`owner`／`Violation`）。

---

## 剧本 1 · 纯 starvation，无提醒义务（6 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做个后台工具。` |
| | G＝锚点缺／受众缺／首页布局缺／导出格式(C)缺∣F＝P0 锚点缺失（V0.3 R11）∣A＝**ASK(核心用户)**∣P＝仅 1 个合法动作 |
| | FA＝—∣N＝—∣§11＝参与（ASK 被调度，选"核心用户"问法） |
| | U：「先确认一件事：这个后台主要给谁用？」｜W＝受众 `PROPOSED`｜owner：V0.3＋§11｜**Violation：无** |
| **轮2** | 用户：`给运营人员用。` |
| | G＝受众 `CONFIRMED`；首页布局缺；表格交互缺；C(导出格式)缺∣F＝选择型反馈∣A＝**SHOW(首页布局 3 方向)**＋候选 ASK∣P＝R4：SHOW 未处理完不展开 ASK → `[SHOW]` |
| | FA＝—∣N＝—∣§11＝**不参与**（非 ASK 轮） |
| | U：三方向布局 ＋ "也可以直接说你想要的"｜W＝布局 `PROPOSED`｜owner：V0.3＋Priority｜**Violation：无** |
| **轮3** | 用户：`第二个吧。` |
| | G＝布局 `CONFIRMED`；表格交互缺；C 缺∣F＝选择型∣A＝**ASK(表格交互)**；容量 2，另有 ASK(权限范围) |
| | P＝`[ASK(表格交互), ASK(权限范围)]`；**C 因容量未排上**｜FA＝**C：eligible_unscheduled_cycles=1**｜N＝**record_only**（无 commitment）∣§11＝参与 |
| | U：「表格要支持批量操作吗？」｜W＝布局落 `effective_set`｜owner：Priority 排序｜**Violation：无** |
| **轮4** | 用户：`要，批量删除也要。` |
| | G＝表格交互 `CONFIRMED`；权限范围缺；C 缺∣F＝Revision（有值）∣A＝**ASK(权限范围)** |
| | P＝`[ASK(权限范围)]`；**C 再次因容量未排上**｜FA＝**C: debt=2**，`starvation_candidate=true`｜N＝**record_only**∣§11＝参与 |
| | U：「权限上，运营和管理员要分开吗？」｜W＝表格交互 `CONFIRMED`｜owner：Fairness 记证据｜**Violation：无**（**不得出现"顺便提醒一下导出格式"**——无 visibility commitment） |
| **轮5** | 用户：`分开。` |
| | G＝权限 `CONFIRMED`；C 仍缺（本轮容量被 R6 项占用）∣F＝Revision∣A＝**ASK(费用, R6)** |
| | P＝`[ASK(费用)]`（硬约束优先）；**C 因 hard 未排上 → 该周期不计债**｜FA＝**C: debt 仍=2**（ineligible/hard 周期不增）｜N＝**record_only**∣§11＝参与 |
| | U：「最后一个必须你定：这个工具是内部免费，还是要走采购预算？」｜W＝—｜owner：Fairness（F6）＋§11｜**Violation：无** |
| **轮6** | 用户：`内部免费。` |
| | G＝C(导出格式) 是唯一剩余缺口∣F＝Revision∣A＝**ASK(导出格式)** |
| | P＝`[ASK(导出格式)]`；**C 被调度 → debt 归零**（`last_eligible_cycle` 更新）｜FA＝C: debt=0∣N＝**record_only**∣§11＝参与 |
| | U：「导出要 CSV、Excel，还是都要？」｜W＝费用 `CONFIRMED`｜owner：Priority＋Fairness｜**Violation：无** |

**结果**：跑到底 ✓｜6 轮**零主动提醒**（无 commitment）｜债务按 F1／F6 正确累积与暂停 ✓

---

## 剧本 2 · 纯 starvation（软竞争变体，5 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做个落地页。` → `[ASK(受众)]`；FA/N 均无 |
| **轮2** | 用户：`给客户看。` → `[ASK(主视觉方向)]`；FA：无 debt 对手 |
| **轮3** | 用户：`再简单点。`（Revision，无新值）→ 索取最小必要新值；同轮容量被占，**普通项 C(数据统计) 未排上** → FA：`C: debt=1`，`last_skip_reason=soft_priority`；N＝record_only |
| **轮4** | 容量=1：C 与另一普通项竞争 → C 未选中 → FA：`C: debt=2`（`starvation_candidate=true`）；**N＝record_only**（用户从未表达可见要求） |
| **轮5** | C 排上 → FA：C debt=0；N＝record_only |
| | U（全程无主动提醒语），W＝无异常写回，owner：Priority＋Fairness |

**结果**：跑到底 ✓｜**"等得久"未自动产生提醒** ✓（`fairness evidence ≠ notification obligation`）

---

## 剧本 3 · `不急，但别忘了`（三分离＋checkpoint 提醒＋discharged，7 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做个会员中心。` → G＝锚点 `CONFIRMED`；F＝P0 缺 → A＝`[ASK(核心权益)]`；U：「会员最想要的那一项权益是什么？」 |
| **轮2** | 用户：`配色不急，但别忘了。` |
| | G＝配色缺∣F＝**`deprioritized`＋`visibility_commitment(required=true)`**，无时机 → §6.2 规则 4 → `condition=next_relevant_checkpoint`∣A＝无新动作 |
| | P＝**配色排后（不自动 promotion）**；FA＝**debt 不累积**（F1：deprioritized 非 capacity/soft competition）∣N＝**notify_later**（等 checkpoint）∣§11＝— |
| | U：「行，配色先放着，我不会漏掉它。」｜W＝**gap 状态不变**｜owner：Priority（排序）＋Notification（义务）｜**Violation：无** |
| **轮3** | 用户：`权益是积分。` → A＝`[ASK(权益规则)]`；P＝`[ASK(权益规则)]`（配色仍排后）；FA：debt=0；N＝pending；U：「积分怎么发、怎么用？」 |
| **轮4** | 用户：`按消费。` → A＝`[ASK(权益展示位置)]`；U：「积分显示在哪？」 |
| **轮5** | 用户：`现在到哪一步了？` |
| | **checkpoint 成立**（用户主动要求 status）∣N＝**notify_now 一次**：「还有配色一项你说过别忘，要不要现在定？」∣P＝**配色仍不提升**（用户说了不急）∣W＝`discharged=true` |
| | U＝上述提醒 ＋ 进度说明｜owner：Notification｜**Violation：无** |
| **轮6** | 用户：`配色先不用，继续。` → N＝**不再复催**（已 discharged）→ `never_notify`；P＝无变化 |
| **轮7** | 用户：`权益展示放首页顶部。` → 收敛出稿（假设区标注配色待定） |
| | U＝5 段 Prompt｜W＝各 gap `CONFIRMED`／配色仍 `OPEN`｜owner：Interface｜**Violation：无** |

**结果**：三分离成立 ✓｜**提醒一次** ✓｜**提醒后解除、后续不复催** ✓｜配色未被 fairness 偷偷提升 ✓

> **O-4（F4：已由"观察"升为判定契约）**：`别忘了`（**无时机**）按 Notification Contract §6.2 **规则 4** 解析为 `condition = next_relevant_checkpoint` —— 该解析现已是**规范条款**（**N08 裁决**，D02 冲突封口），不再是待办观察项。
> **W 行注记（F9）**：本剧本 `W＝discharged=true` 指 **Notification 层内部状态**，**不构成 Gap 写回**（**N01**）。

---

## 剧本 4 · `不急但别忘了` 遇高负担（6 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做活动报名页。` → A＝`[ASK(报名要素)]` |
| **轮2** | 用户：`预算不急但别忘了。` → `deprioritized`＋`commitment(trigger=checkpoint)`；N＝`notify_later`；P＝预算排后 |
| **轮3** | 用户：`姓名+手机。` → 同轮出现 **R6 项（费用）** → A＝`[ASK(费用, R6)]`；本轮高负担 |
| | **checkpoint 到达**（该小簇结束）但**高负担** → N＝**notify_later**（**不打断关键拍板**）∣U＝只问费用，**不加提醒**｜owner：Notification｜**Violation：无** |
| **轮4** | 用户：`免费。` → R6 完成；簇结束 → N＝**notify_now 一次**：「预算你说过别忘，现在要定吗？」；W＝`discharged=true`（**Notification 内部状态，非 Gap 写回**，N01） |
| **轮5** | 用户：`先不定。` → N＝`never_notify`（已 discharge；用户未重建）；W＝预算仍 `OPEN` |
| **轮6** | 用户：`先出稿吧。` → 出口（假设区列预算待定） |
| **结果** | `notify_later` 正确使用 ✓｜**关键拍板未被提醒打断** ✓ |

---

## 剧本 5 · 显式用户 priority × fairness（最关键组，7 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做个数据看板。` → A＝`[ASK(看板核心指标)]` |
| **轮2** | 用户：`图表交互（A）一直比导出格式（C）优先。` |
| | F＝**`priority_hint{scope:whole_task, relations:[A ≻ C]}`**（显式、有效）∣A＝无新动作 |
| | P＝保持 **A ≻ C**；FA＝—∣N＝record_only∣U：「好，先按这个顺序。」｜W＝**未写任何 Gap 状态**｜owner：Priority｜**Violation：无** |
| **轮3** | 用户：`指标是日活。` → A＝`[ASK(图表类型)]`；P＝`[ASK(图表类型), ASK(权限)]`；**C 因容量未排上** → FA＝`C: debt=1`；N＝record_only |
| **轮4** | 用户：`折线。` → 容量竞争 → **C 又未排上** → FA＝`C: debt=2`，`starvation_candidate=true` |
| | **关键**：P＝**仍保持 A ≻ C**（fairness **不得**翻转为 C ≻ A）；N＝record_only（无 commitment） |
| | U＝继续按原序推进｜owner：Fairness（只记账）＋Priority（不越权）｜**Violation：无** |
| **轮5** | 用户：`权限要分角色。` → C 第三次未排上 → FA＝`C: debt=3`；P 不变；N＝record_only |
| **轮6** | 用户：`C 导出格式是不是该定了？` |
| | 用户**主动**提及 → N＝record_only（无 commitment，无需系统提醒）；A＝`[ASK(导出格式)]`（用户拉高）→ C 被调度 → FA：C debt 归零；P：A ≻ C 的 relation **未变**（C 现在被调度是**用户主动**，不是 fairness 翻转） |
| | U：「导出要 CSV 还是 Excel？」｜owner：Interface／Priority｜**Violation：无** |
| **轮7** | 用户：`刚才那个顺序算了。`（取消 hint） |
| | F＝**explicit cancellation** → hint 失效∣P＝fairness **立即恢复资格** → 后续软排序可由 fairness 修正；FA＝按新规则重算（旧债已归零）∣U：「好，之后我按实际情况排。」 |
| **结果** | **fairness 全程未偷偷翻转用户序** ✓｜**取消后立即恢复资格** ✓｜**Notification 零越权** ✓ |

---

## 剧本 6 · 显式 priority ＋ 有承诺的重新暴露（6 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做报表工具。` → `[ASK(报表类型)]` |
| **轮2** | 用户：`A（模板）优先于 C（导出）。` → `priority_hint(whole_task, A ≻ C)` |
| **轮3** | 用户：`C 不急，但别忘。` |
| | F＝`deprioritized` ＋ `visibility_commitment(required=true, trigger=checkpoint)`∣FA＝**C debt 不累积**（deprioritized）∣N＝`notify_later`∣P＝A ≻ C 保持 |
| | U：「好，C 先放着，我不会忘。」｜owner：Priority／Notification｜**Violation：无** |
| **轮4** | 用户：`模板要三个。` → 推进；N pending |
| **轮5** | 用户：`有没有落下什么？` → **checkpoint**？—— 用户主动 review 属 checkpoint 之一 |
| | N＝**notify_now 一次**：「C 你说过别忘，要不要现在定？」∣P＝**C 仍未被 promotion**（用户序仍在，且用户自己说不急）∣W＝`discharged=true`（**Notification 内部状态，非 Gap 写回**，N01） |
| **轮6** | 用户：`先不定，继续。` → N＝`never_notify`；P 不变；出口 |
| **结果** | **"有承诺时重新暴露"走的是 Notification，不是 fairness** ✓（这是新架构最关键的一条：**同一结果，两条链，不能混**） |

---

## 剧本 7 · delay 对照 A（无 commitment，5 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做活动报名页。` → `[ASK(活动要素)]` |
| **轮2** | 用户：`报名表单细节（B）以后再说。` |
| | F＝`delay` → B：`OPEN + deferred`（Interface §3）∣P＝B **不参与正常调度**；FA＝**不累积 debt**（非 eligible）∣N＝**never_notify** |
| | U：「行，B 先搁着，我不催你。」｜W＝B `OPEN+deferred`｜owner：Interface｜**Violation：无** |
| **轮3–5** | 用户依次确认其他项；B **仍属于 `askable_set`**（`OPEN + deferred` 不改集合语义），但**在 delay 有效期间不参与当前正常调度**（**CS-06／D06**） |
| | N＝**never_notify**（**delay 无授权不得被催**）∣U 中**无任何 B 的提醒语** |
| **结果** | 四象限 **(delay=是, visibility=否)** ✓ |

---

## 剧本 8 · delay 对照 B（有 commitment，6 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`再做一版活动页。` → `[ASK(活动要素)]` |
| **轮2** | 用户：`报名表单细节（B）以后再说，但别漏掉。` |
| | F＝`delay` **＋** `visibility_commitment(required=true, trigger=checkpoint)`（**两件事，不混**）∣P＝B 不参与调度∣N＝`notify_later` |
| | U：「行，B 先搁着，等合适的时候我提醒你一次。」｜W＝B `OPEN+deferred`（状态），commitment 属 Notification 层｜**Violation：无** |
| **轮3–4** | 推进其他项；B 仍 deferred；N pending |
| **轮5** | 簇即将结束（**checkpoint**）→ N＝**notify_now 一次**：「B 还挂着，要不要一起定掉？」 |
| **轮6** | 用户：`那把 B 也定了吧，用极简表单。` → 用户解除 delay → B 回到正常处理 → 调度 → `CONFIRMED`；N＝`discharged` |
| **结果** | 四象限 **(delay=是, visibility=是)** ✓｜**与剧本 7 严格区分** ✓ |

---

## 剧本 9 · external dependency ＋ notification（7 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做个医疗预约页，要合规。` → `[ASK(服务范围)]`；合规项 OPEN（**R6**） |
| **轮2** | 用户：`主视觉方向等客户回复。` |
| | F＝`External`（owner=客户, reason=`decision_owner`）→ **Interface** 落 `SUSPENDED(external_owner)` |
| | P＝该 gap **不进 askable** → 不调度；U：「行，主视觉等客户那边。」｜**Violation：无** |
| **轮3** | 用户：`客户回复以后提醒我。` |
| | F＝`visibility_commitment(required=true, trigger=condition)` → **复用该事项已有的恢复条件**（合同 §6.2 规则 3）∣N＝`notify_later` |
| | U：「好，客户一有结论我就跟你说一次。」｜owner：Notification｜**Violation：无** |
| **轮4** | 用户：`服务范围就线上问诊。` → `CONFIRMED`；主视觉仍 `SUSPENDED`；N pending；P 不调度 suspended gap |
| **轮5** | 用户：`客户说方案 B 可以。` |
| | **Interface**：`SUSPENDED → OPEN`（外部意见＝input，**不自动 confirmed**）∣F＝用户已主动提到 → commitment **视为满足** → `discharged`；N＝不额外提醒；P＝`[ASK(主视觉确认)]` |
| | U：「客户倾向 B，那我们就按 B 定下来吗？」｜W＝主视觉 `OPEN`｜owner：**Interface**（resume）｜**Violation：无** |
| **轮6** | 用户：`对，就 B。` → 主视觉 `CONFIRMED`（→ `effective_set`） |
| **轮7** | 用户：`合规那项我再想。` → 合规仍 `OPEN`（R6 不可默认）→ 出口标注「合规待定」 |
| **结果** | SUSPENDED 不进 askable ✓｜resume 由 Interface 处理 ✓｜Notification 只决定可见性 ✓｜**不自动 confirmed** ✓ |

---

## 剧本 10 · resolution generation（6 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做个官网。` → `[ASK(受众)]` |
| **轮2** | 用户：`首页方向（A）不急但别忘。` → `deprioritized`＋`commitment(trigger=checkpoint)`；另一普通项 C 开始累积 → FA＝`C: debt=1`；N＝`notify_later` |
| **轮3** | 用户：`受众是客户。` → `CONFIRMED`；C 又未排上 → FA＝`C: debt=2`；N pending |
| **轮4** | 用户：`算了，不是官网了，改成 SaaS 后台。` |
| | F＝`Revision`（target=`goal`，scope=`whole_task`）→ 下游 `CHALLENGED`；**产生新 resolution generation** |
| | U：「你刚把目标换成 SaaS 后台，我先按新目标重新捋一遍。」｜W＝锚点 `CONFIRMED(新值)`＋`supersedes`｜owner：Interface｜**Violation：无** |
| **轮5** | 新目标下重新规划（无新动作需求前先确认核心用户） |
| | **FA＝旧 C 的 debt 终止（不继承）**∣**N＝旧 A 的 commitment 不继承**（需重新表达）∣P＝按新目标重排 |
| | U＝只问新目标相关项，**不提醒旧官网的 A**｜owner：Fairness／Notification｜**Violation：无** |
| **轮6** | 用户：`后台这块配色别忘。` → **新 generation 下重新建立 commitment**；N＝`notify_later` |
| **结果** | **过期 generation 债务泄漏 = 0** ✓｜旧 commitment 不自动继承 ✓ |

---

## 剧本 11 · notification 与高负担轮冲突（5 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`做个支付页。` → `[ASK(支付方式)]` |
| **轮2** | 用户：`配色不急但别忘。` → commitment(trigger=checkpoint)；N＝`notify_later` |
| **轮3** | 用户：`支付走微信、支付宝。` → 同轮出现 **R6 项（费率）** |
| | **checkpoint 到达**＋**高负担**（R6 待拍板）→ N＝**notify_later**（**不打断关键拍板**） |
| | U＝只问费率，**不加配色提醒**｜owner：Notification｜**Violation：无** |
| **轮4** | 用户：`费率 0.6%。` → R6 完成 → 下一 checkpoint → N＝**notify_now 一次**：「配色你说过别忘，现在定吗？」；W＝`discharged`（**Notification 内部状态**，N01） |
| **轮5** | 用户：`先不定。` → N＝`never_notify`；出口（假设区标注配色待定） |
| **结果** | `next_relevant_checkpoint` 的"**不打断高优先流程**"在 E2E 中被证实 ✓ |

---

## 剧本 12 · 大混合压力剧本（9 轮）

| 轮 | 记录 |
|---|---|
| **轮1** | 用户：`帮我做一个高级 AI 官网。` → G＝锚点缺／受众缺／视觉方向缺；A＝`[ASK(产物形态)]`；U：「给普通用户看的产品官网，还是给专业用户的工作台？」 |
| **轮2** | 用户：`给客户看的产品官网。` → 受众 `CONFIRMED`；A＝`[SHOW(视觉方向 3 方向)]`；§11 不参与（非 ASK）；U＝三方向 |
| **轮3** | 用户：`选材质做工。还有，先做首页，其他后面。` |
| | G＝视觉 `CONFIRMED`；F＝选择 ＋ **`priority_hint{scope:current_round, 首页 ≻ 其他}`**；P＝首页先行（round scope，绑定本 bundle）；U：「好，先首页。」 |
| **轮4** | 用户：`首页交互（A）一直比图标细节（C）优先。` → 新增 **`priority_hint{scope:whole_task, A ≻ C}`**；W＝无状态写回；owner：Priority |
| **轮5** | 用户：`C 不急，但别忘。` |
| | F＝`deprioritized` ＋ `commitment(trigger=checkpoint)`；C 已连续 eligible-unscheduled → FA＝`C: debt=2`，`starvation_candidate=true`；**P＝保持 A ≻ C（不 promotion）**；N＝`notify_later` |
| | **debt provenance（ER-09）**：轮3 `soft_competition` **0→1**｜轮4 `soft_competition`（显式 hint A≻C）**1→2**｜轮5 起 `user_deprioritization` **increment = 0** ⇒ **`deprioritized` 不清零、不新增**（≠ reset to 0） |
| | U：「好，C 先放着。」｜owner：Priority／Fairness／Notification **三层各司其职**｜**Violation：无** |
| **轮6** | 用户：`配色先等客户确认。` → `SUSPENDED(external_owner)`；不进 askable；P 不调度；U：「好，配色等客户。」 |
| **轮7** | 用户：`客户说暖色系。` |
| | **Interface**：`SUSPENDED → OPEN`（不自动 confirmed）∣**checkpoint＋commitment 触发** → N＝**notify_now 一次**：「C（图标细节）你说过别忘，现在定吗？」∣P＝`[ASK(配色确认)]` |
| | U＝ASK 配色确认 ＋ C 的提醒一句（**两件事、两条链**）｜W＝配色 `OPEN`；C 的 commitment `discharged`（**Notification 内部状态**，N01）｜**Violation：无** |
| **轮8** | 用户：`配色就暖色。另外，改成企业版吧。` |
| | 配色 `CONFIRMED`；F＝**实质 Revision（goal 变）→ 新 generation** → 下游 `CHALLENGED`；**旧 debt／旧 commitment 不继承**；U：「目标换成企业版了，我按新目标重新捋。」｜owner：Interface |
| **轮9** | 用户：`核心用户是采购负责人。` → 新目标下推进；出口（假设区列出 assumed 项） |
| **结果** | 9 轮全程：**没有任何一层替别的层做决定** ✓；E1–E8 全通过 ✓ |

---

## E1–E8 验证汇总

| 不变量 | 结果 | 关键取证 |
|---|---|---|
| **E1** 单一 authoritative current_value | ✅ | 剧本 10 轮4（revision 后下游全 `CHALLENGED`）、剧本 12 轮8 |
| **E2** 只有 Interface 改 Gap 状态 | ✅ | **逐 mutation 链见 [`release-evidence-closure.md`](release-evidence-closure.md) ER-07（M-01～M-11，final writer 全部 = Interface）**；负例：Notification 的 `discharged` 属本层内部状态（M-10） |
| **E3** 只有 V0.3 决定 Action | ✅ | **E3-A ＝ 剧本 1 轮2**（V0.3 → SHOW；Priority 仅调位；最终仍 SHOW）；**E3-B ＝ 剧本 1 轮1**（V0.3 → ASK）；`information_source` 正例 ＝ **V0.4.5 `E2E-08` 轮2**（保持 `OPEN`，不落 SUSPENDED）。**旧引用（剧本 2 轮2＝ASK、剧本 9 轮2＝SUSPENDED）已按 ER-08 修正** |
| **E4** Priority 只排序合法 Action | ✅ | 剧本 5（A ≻ C 保持）、剧本 9（不调度 suspended gap） |
| **E5** §11 只在 ASK 被调度后工作 | ✅ | **E5-A（negative control）＝ 剧本 1 轮2 ＋ 剧本 12 轮2 两个 SHOW 轮**（§11 均"不参与（非 ASK 轮）"）；**E5-B（positive control）＝ 剧本 1 轮1／轮3**（ASK 被调度后 §11 才选具体问法）。**旧引用（剧本 3 轮2、5 轮2＝非 SHOW 轮）已按 ER-08 修正** |
| **E6** 用户可见输出无内部机制词 | ✅ | 全部剧本 `U` 行为自然语言（无 gap／CHALLENGED／pending／commitment／debt 等词） |
| **E7** Fairness 不改 Gap／Action／用户序 | ✅ | 剧本 5 轮3–6（debt 累积而 A ≻ C 不动）、剧本 6（C 的暴露走 Notification） |
| **E8** Notification 不改调度／Gap／Action | ✅ | 剧本 3/4/6/11（提醒不改变任何排序与状态）、剧本 8（`deferred` 状态由 Interface 管） |

## Release Gate

| 指标 | 结果 |
|---|---|
| 12 个剧本跑到底 | ✅ **12/12** |
| E1–E8 | ✅ **全通过** |
| Layer ownership violation | ✅ **0** |
| 错误重复询问 | ✅ **0** |
| hard constraint 被越过 | ✅ **0** |
| explicit priority 被 fairness 偷偷覆盖 | ✅ **0** |
| starvation 自动变提醒 | ✅ **0** |
| visibility commitment 漏兑现 | ✅ **0** |
| 重复主动提醒 | ✅ **0** |
| **错误主动提醒** | ✅ **0** |
| **承诺触发后漏提醒** | ✅ **0** |
| 过期 generation 债务泄漏 | ✅ **0** |
| 机制词用户可见泄漏 | ✅ **0** |
| **K4 / K5** | ✅ **0 / 0** |

## 观察（供 V0.4.8-B 之后收束，不构成规则变更）

| # | 观察 |
|---|---|
| **O-4**（**已升为判定契约**） | `别忘了`（**无时机**的可见请求）归 `condition = next_relevant_checkpoint` —— 现为 **Notification Contract §6.2 规则 4** 的规范内容（**N08 裁决**），**不再是待办观察** |
| **O-5** | `deprioritized` 的项**不累积 fairness debt**（F1），因此"长期没排上"与"用户自己说往后排"在证据层就分开了——这是 E7 成立的重要前提，值得在 README 写明 |
| **O-6**（新增 · 引用修复 F5） | 剧本 3／4／11 的 `W` 行 `discharged` 一律指 **Notification 层内部状态**（**N01**），**不含 Gap 写回**；本文件的 `W` 列语义据此统一 |

## 边界与状态

| 项 | 状态 |
|---|---|
| 全部冻结正文（§11／V0.3／Interface v1–v3／§10／Priority v1.1／Fairness v1／Notification v1） | **未修改** |
| 新增规则／字段／Action／Type／Gap state | **无** |
| 本轮产物 | 本文件（审计记录，仅测试） |
| 下一步（用户已给出顺序） | 若全绿 → **停止继续加 V0.4 行为规则** → 写 **V0.4 Final Architecture README** → **V0.4 正式封版** |
