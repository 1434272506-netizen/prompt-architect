# V0.4.5 · End-to-End Adaptive Replay（12 个 4–8 轮真实会话）

> **本轮性质**：把四层装起来跑真实多轮对话——**不改冻结正文、不写规则、不加字段、不做数值评分**。
> **失败处置**：只定位"**哪一层越权／缺接口**"，**不自动修**。
> **被测链路**：`User Feedback → Feedback Semantics／Gap Ledger → V0.3 Resolution Engine → Priority Layer → §11 Question Selection → User-visible response → feedback 写回 ↺`

**每轮记录 10 项 + 2 列**：① 用户输入｜② active gaps｜③ authoritative values｜④ intent·target·scope｜⑤ V0.3 action｜⑥ hard scheduling constraints｜⑦ Priority 输出｜⑧ §11 是否参与·为什么｜⑨ 用户可见输出｜⑩ 状态写回｜**Layer owner**｜**Violation?**
（下文按 `G`／`F`／`A`／`P`／`U`／`W` 六行压缩记录，含义对应上述顺序。）

**六条系统不变量（E2E Gate）**

```
E1  单一 authoritative current_value
E2  只有 Interface 改 Gap 状态
E3  只有 V0.3 决定 Action 类型
E4  Priority 只排序合法 Action
E5  §11 只在 ASK 被调度后工作
E6  用户可见输出不得暴露内部状态机术语
```

---

## E2E-01 · 正常收敛（模糊起点 → 完整交付）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`帮我做一个高级 AI 官网。` |
| G | gap：产物锚点=缺；受众=缺；成功标准=缺；视觉方向=缺；硬约束=缺。authoritative：∅ |
| F | intent＝`REVISION_CANDIDATE`? 否——首轮无反馈意图；按 V0.3 契约 R11：**P0 锚点缺失** → 先 ASK 产物 |
| A | V0.3 §11.0：**ASK(产物形态)**（可读环境无相关证据 → INSPECT 不适用）；硬约束：R6（目标不可 DISCOVER） |
| P | 仅 1 个合法动作 → `ordered=[ASK 产物]`；`deferred_by_capacity=[]` |
| U | "先确认一件事：这是给普通用户看的产品官网，还是给专业用户用的工作台？" |
| W | 用户答 → 产物锚点 `CONFIRMED`；其余 OPEN |
| owner / Violation | Interface（改状态）／**无** |

| 轮 | 内容 |
|---|---|
| **轮2** | 用户：`给普通用户看的产品官网，要"高级"。` |
| G | 锚点 `CONFIRMED`；受众 `CONFIRMED`；视觉方向 OPEN（含模糊词"高级"）；成功标准缺 |
| F | 无修正意图；"高级"＝Type B（模糊审美）→ 但要先看 P0 |
| A | §11.0 规则 8：P0 **修饰**槽位（成功标准）缺失**不冻结 SHOW** → **SHOW(高级：3 正交方向)** |
| P | 合法动作 {SHOW, ASK(成功标准)}；**R4**：SHOW 结果未处理完不得展开 ASK → `ordered=[SHOW]`，ASK 顺延 |
| U | 三方向：极简克制／材质做工／稀缺暗场 ＋ "也可以直接描述你想要的" |
| W | 视觉方向：`PROPOSED`（未确认） |
| owner / Violation | V0.3 定动作、Priority 定顺序／**无** |

| 轮 | 内容 |
|---|---|
| **轮3** | 用户：`选第二个吧，材质做工。` |
| G | 视觉方向 `PROPOSED`；成功标准 OPEN |
| F | intent＝`Revision`? 否 → **选择型反馈**（`accepted/selected`）；target＝`proposal` |
| A | 无需新动作（SHOW 已得选择）→ 回 §11.0 重排：剩 ASK(成功标准) |
| P | 合法动作 {ASK(成功标准)} → `ordered=[ASK]` |
| U | "好，材质做工。那这个站你最希望访客做什么？" |
| W | 视觉方向 `CONFIRMED`；`effective_set` 加入该项 |
| owner / Violation | Interface 写回／**无**；E1 单值 ✓ |

| 轮 | 内容 |
|---|---|
| **轮4** | 用户：`先让访客留联系方式，其他不重要。` |
| G | 成功标准（"留联系方式"）；另提到"其他不重要"→ 触发 `deprioritized` 候选 |
| F | intent＝`Revision`（给值）+ **降权表达**（`deprioritized`）；target＝`confirmed_value` |
| A | §11.0：无新动作需求；剩余缺口语义槽位 → 可视情况 ASK（如联系方式形式） |
| P | **`expressed_priority`：其他细节降权**；`effective_priority`：仍受硬约束（R6 无涉及）→ `ordered=[ASK(联系方式形式)]`；hint 记为 `scope=current_cluster` |
| U | "好，第一屏就放联系入口。联系方式用二维码还是电话？" |
| W | 成功标准 `CONFIRMED`；降权=**纯调度属性**，**未改任何状态** |
| owner / Violation | Priority 记 hint（本层自有）／**无**；E4 ✓ |

| 轮 | 内容 |
|---|---|
| **轮5** | 用户：`二维码吧，够了。` |
| G | 所有 P0 齐；剩余=措辞级 |
| F | intent＝`Revision`/选择；target＝`proposal`(选项) |
| A | §6.1 三项同时满足 → 停止追问，进 §8 出口 |
| P | 合法动作 = ∅（无待发动作）→ `ordered=[]` |
| U | 5 段 Prompt + "待确认假设"（若 AI 自定内容） |
| W | 各 gap `CONFIRMED`；无新增状态 |
| owner / Violation | Interface／**无**；E2/E3 ✓ |

**剧本结果**：跑到底 ✓｜Layer ownership violation **0**｜重复询问 **0**｜机制词泄漏 **0**。

---

## E2E-02 · 正常收敛（含中途用户排序提示）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`做个作品集网站。` |
| G | 锚点 `CONFIRMED`（作品集）；受众/成功/内容组织 OPEN |
| A | §11.0：P0 已有产物 → ASK(受众/成功)；`priority_hint.scope=current_round` 尚未产生 |
| P | `ordered=[ASK(受众)]`；其余 `deferred_by_capacity=[]`（选择其一，非容量问题） |
| U | "这个站主要给谁看？—— 潜在客户 / 同行 / 招聘方" |
| W | 受众 `PROPOSED` |
| owner / Violation | 全链正常／**无** |

| 轮 | 内容 |
|---|---|
| **轮2** | 用户：`先定内容结构，受众我晚点说。` |
| G | 受众 OPEN（用户显式延后）；内容组织 OPEN |
| F | intent＝**`priority_hint` 表达**（顺序偏好）+ 轻量 defer；**不是 Revision** |
| A | V0.3 已可选动作：ASK(受众)、ASK(内容组织) → 都合法 |
| P | `priority_hint{source:user, scope:current_round, relations:[{before:[内容组织, 受众]}]}` → `effective_priority`：内容组织先行；**受众不 assumed、不关闭** |
| U | "好，先说内容结构：按项目分集，还是按时间线？" |
| W | 无状态变化（受众保持 `OPEN`，hint 存于 Priority 层） |
| owner / Violation | **Priority 层**（排序）／**无**；E4 ✓、E2 ✓（未写 gap 状态） |

| 轮 | 内容 |
|---|---|
| **轮3** | 用户：`按项目分集。` |
| G | 内容组织 `CONFIRMED`；受众仍 OPEN；`priority_hint` 已到期（`scope=current_round` 在上轮结束即失效） |
| A | ASK(受众) 成为候选 |
| P | **hint 未泄漏**：`current_round` 已过期 → 用默认序 → `ordered=[ASK(受众)]` |
| U | "那受众呢？给潜在客户、同行还是招聘方看？" |
| W | 内容组织 → `CONFIRMED`（→ `effective_set`） |
| owner / Violation | Priority（scope 到期）／**无**；**过期 hint 泄漏 = 0** ✓ |

| 轮 | 内容 |
|---|---|
| **轮4** | 用户：`潜在客户。` |
| G | P0 齐 |
| A | §6.1 → 收敛 → §8 出口 |
| P | `ordered=[]` |
| U | 5 段 Prompt |
| W | 受众 `CONFIRMED` |
| owner / Violation | Interface／**无** |

**剧本结果**：跑到底 ✓｜**硬约束被 hint 越过 0**｜**无效/过期 hint 泄漏 0**｜Layer violation **0**。

---

## E2E-03 · 中途 Revision（产物级变更）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`做个公司官网。` → 锚点 `CONFIRMED`；受众/成功 OPEN ｜`ordered=[ASK(受众)]` |
| **轮2** | 用户：`给客户看。` → 受众 `CONFIRMED`；视觉方向 OPEN ｜`ordered=[SHOW(视觉方向)]` |
| **轮3** | 用户：`选极简克制。` → 视觉方向 `CONFIRMED` |
| **轮4** | 用户：`算了，不是官网了，改成 SaaS 后台。` |
| G | 锚点 `CONFIRMED(官网)`；下游：受众、视觉方向、成功标准（均基于"官网"） |
| F | intent＝`Revision`（**有新值**）；target＝**`goal`**；scope＝`whole_task` |
| A | §11.0：Revision 本身不产生动作；但下游需重评 → V0.3 重算：ASK(后台受众/成功) |
| P | 硬约束：**§11.6 约束型依赖**（锚点 → 下游全部）→ `ordered=[ASK(后台核心用户)]`；旧下游项进 `deferred_by_capacity`? **否**——它们是 `CHALLENGED`（失效），不是容量问题 |
| U | "你刚刚把目标从官网换成 SaaS 后台了，所以我先确认这一点，再继续后面的细节。这个后台主要给谁用？" |
| W | 锚点 `CONFIRMED(新值)` + `supersedes` 边；下游 `CHALLENGED`（Interface §9.1／§9.2） |
| owner / Violation | V0.3 重算 + Interface 传播／**无**；E2 ✓（只有 Interface 改状态） |

| 轮 | 内容 |
|---|---|
| **轮5** | 用户：`给运营人员用。` |
| A | 受众确认 → 剩余：成功标准、视觉方向（需重问，旧值已失效） |
| P | `ordered=[ASK(成功标准)]`；§11：**不重复问"失效前与该目标无关"的旧项**（旧官网视觉方向不复活） |
| U | "那后台上线后，你们用什么判断它有用？" |
| W | 受众 `CONFIRMED` |
| owner / Violation | Interface／**无**；**错误重复询问 0**（旧官网视觉方向未被重问） |

**剧本结果**：跑到底 ✓｜authoritative 单值 ✓｜Layer violation **0**｜重复询问 **0**。

---

## E2E-04 · 局部 Revision（不得扩大闭包）

| 轮 | 内容 |
|---|---|
| **轮1–3** | 依次确认：锚点(营销落地页)、受众(客户)、主色(蓝)、按钮文案(A 版)、页脚结构(3 列) |
| **轮4** | 用户：`按钮文案稍微调一下。` |
| G | 已有 5 项 `CONFIRMED`；`affected` 图从"按钮文案"仅连到该按钮区块 |
| F | intent＝`Revision`（**无新值**）；target＝`confirmed_value`；**`revision_scope=local`** |
| A | V0.3：无需改动作；需索取新值 → ASK(新文案) |
| P | `ordered=[ASK(新文案)]`；**硬约束**：`revision_scope=local` 处硬停（Interface §9.4 S-1） |
| U | "好，把按钮文案改成什么？" |
| W | 仅该 gap 进入待更新；**主色/页脚/受众不动** |
| owner / Violation | Interface 限定闭包／**无**；E2 ✓ |

| 轮 | 内容 |
|---|---|
| **轮5** | 用户：`改成"立即开始"。` |
| F | intent＝`Revision`（有新值） |
| A | 覆盖该值 → CONFIRMED；**闭包不扩张** |
| P | `ordered=[]`（如无其他缺口） |
| U | 更新后的交付（仅按钮文案变化） |
| W | 该 gap `CONFIRMED`；其余 `CONFIRMED` 不动；历史保留旧文案 |
| owner / Violation | Interface／**无**；不变量 I-4（local 不扩大闭包）✓ |

**剧本结果**：跑到底 ✓｜闭包未扩大 ✓｜Layer violation **0**。

---

## E2E-05 · 授权 + 风险门（普通项 vs R6 项）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`做个活动报名页。` → 锚点 `CONFIRMED`；其余 OPEN |
| **轮2** | 用户：`风格你决定，费用也你决定，用户数据怎么用也你决定。` |
| G | 视觉风格 OPEN（非 R6）；费用 OPEN（**R6**）；数据用途 OPEN（**R6**） |
| F | intent＝`Authorization`（多次，作用不同 gap）；scope＝`current_decision_cluster` |
| A | V0.3：T2 风险门逐 gap 判定（Interface §8.2） |
| P | `ordered=[ASK(费用), ASK(数据用途)]`（两项 blocked → 仍待拍板，**与风格并列竞争时优先**）；风格项可 assumed |
| U | "风格这块我按材质做工的方向定了，会写进待确认假设。费用和数据用途这两项得你来定，我先不替你决定。" |
| W | 视觉风格 → `CLOSED(assumed)`；费用/数据用途 → 保持 `OPEN`（`authorized_rejected_by_policy` 记录） |
| owner / Violation | Interface 门（T2）+ Priority 排序／**无**；E4 ✓ |

| 轮 | 内容 |
|---|---|
| **轮3** | 用户：`费用按人头 99。` → 费用 `CONFIRMED` |
| **轮4** | 用户：`数据就不存了，只留报名信息。` → 数据用途 `CONFIRMED` |
| **轮5** | 收敛 → 出口（假设区列出风格默认） |
| 结果 | 普通项未被追问；**R6 项没有被"都你决定"吞掉** ✓ |

**剧本结果**：跑到底 ✓｜R6 未越权 ✓｜Layer violation **0**。

---

## E2E-06 · 授权后反悔

| 轮 | 内容 |
|---|---|
| **轮1–2** | 用户：`图标风格你定。` → `CLOSED(assumed)`（Linear 图标）；配色也 `CLOSED(assumed)` |
| **轮3** | 用户：`刚才那个别默认了，图标我要自己选。` |
| G | 图标 gap = `CLOSED(assumed)` |
| F | intent＝`Revision`（撤销默认）；**R-1 material re-entry**（Interface §10.3） |
| A | V0.3：ASK(图标风格) |
| P | `ordered=[ASK(图标风格)]`；配色 assumed 不动 |
| U | "好，图标这块你自己挑：线性 / 填充 / 双色？" |
| W | 图标 gap：`CLOSED(assumed)` → `OPEN`（**不经无意义抖动**）；历史保留原 assumed |
| owner / Violation | Interface 重进／**无**；E2 ✓；不变量 I-1（历史不删）✓ |

| 轮 | 内容 |
|---|---|
| **轮4** | 用户：`线性吧。` → `CONFIRMED`（→ `effective_set`） |
| **轮5** | 用户：`等等，还是按你刚才定的。` |
| F | intent＝追认；**R-2 confirmatory** → `CONFIRMED`（已在 CONFIRMED 态，**无需再跃迁**） |
| U | "好，就按线性。" |
| W | 无状态抖动；`provenance` 追加 `user_confirmed_after_assumed` 语义 |
| owner / Violation | Interface／**无** |

**剧本结果**：跑到底 ✓｜无额度概念 ✓｜Layer violation **0**。

---

## E2E-07 · 外部依赖（暂停 → 恢复）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`做个产品落地页。` → 锚点确认 |
| **轮2** | 用户：`主视觉方向我得问客户。` |
| G | 主视觉 OPEN；其余缺口语义槽位正常 |
| F | intent＝`External`（owner=客户, reason=`decision_owner`） |
| A | V0.3：**不是 ASK**（不对本人追问）→ 转 `SUSPENDED(external_owner)` |
| P | **该 gap 不进 `askable_set`** → Priority **不得再调度它**；`ordered=[其他合法动作]`（如 ASK 成功标准） |
| U | "行，主视觉先挂着等你客户那边；我们先定别的：访客进来你最希望他做什么？" |
| W | 主视觉 → `SUSPENDED(suspension_reason=external_owner)` |
| owner / Violation | Interface §9.5 + Priority 遵守 `askable_set`／**无**；**Priority 未误调度 suspended gap** ✓ |

| 轮 | 内容 |
|---|---|
| **轮3** | 用户：`先让访客预约试用。` → 成功标准 `CONFIRMED` |
| **轮4** | 用户：`客户说方案 B 可以。` |
| G | 主视觉仍 `SUSPENDED`；`resume_condition` 满足 |
| F | intent＝`External`→**恢复**（外部意见＝input） |
| A | `SUSPENDED → OPEN`；V0.3：ASK(由用户本人拍板) |
| P | `ordered=[ASK(主视觉确认)]` |
| U | "客户倾向 B，那我们就按 B 定下来吗？" |
| W | 主视觉 → `OPEN`；`attempts` 保留；**未自动 confirmed** |
| owner / Violation | Interface §9.5 X-3／**无**；E1 ✓ |

| 轮 | 内容 |
|---|---|
| **轮5** | 用户：`对，就 B。` → 主视觉 `CONFIRMED`；`resume` 完成 |
| 结果 | SUSPENDED → 不进入 askable → resume → OPEN → **用户本人确认** ✓ |

**剧本结果**：跑到底 ✓｜**外部授权不替代用户授权** ✓｜Layer violation **0**。

---

## E2E-08 · 外部依赖（外部回复 ≠ 自动生效）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`做个医疗预约页，要合规。` → 锚点确认；合规项 OPEN（**R6**） |
| **轮2** | 用户：`合规这块我去问法务。` |
| F | intent＝`External`；`reason = information_source`（**只需信息，拍板权仍属用户**） |
| A | **不落 SUSPENDED**（Interface §9.5 X-4）→ 保持 `OPEN`，可继续其他分支 |
| P | `ordered=[ASK(服务范围)]`（合规项待信息，但不阻断其他） |
| U | "好，法务那边有结论前，我们先把服务范围定下来：主要是线上问诊还是到店预约？" |
| W | 合规项保持 `OPEN`（未 SUSPENDED）；服务范围 `PROPOSED` |
| owner / Violation | Interface §9.5 X-4／**无** |

| 轮 | 内容 |
|---|---|
| **轮3** | 用户：`线上问诊为主。` → `CONFIRMED` |
| **轮4** | 用户：`法务说可以收健康信息，但要加密。` |
| F | intent＝`External`（information 到达）＋ 信息本身 |
| A | 合规项仍在 `OPEN`；V0.3：需用户/责任方**明示拍板** → ASK(确认合规方案) |
| P | `ordered=[ASK(合规确认)]`；硬约束：**R6 mandatory**（合规不可 DISCOVER、不可默认） |
| U | "收到，法务要求加密存储。这条就按"加密存储健康信息"定下来吗？" |
| W | 合规项 `OPEN`；未自动 `CONFIRMED` |
| owner / Violation | Interface／**无** |

| 轮 | 内容 |
|---|---|
| **轮5** | 用户：`对，就按加密方案。` → `CONFIRMED` |
| 结果 | `information_source ≠ decision_owner` 全程保持 ✓ |

**剧本结果**：跑到底 ✓｜R6 未被外部信息替代 ✓｜Layer violation **0**。

---

## E2E-09 · Priority 与依赖冲突（颜色依赖品牌定位）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`做个品牌官网。` → 锚点确认；受众 `CONFIRMED(客户)` |
| **轮2** | 用户：`先做颜色，品牌定位以后说。` |
| G | 颜色 OPEN；品牌定位 OPEN；**依赖边：颜色 ←(约束型) 品牌定位** |
| F | intent＝`priority_hint` 表达（顺序偏好）＋ 延后语气；**不是 Revision** |
| A | V0.3 合法动作：ASK(颜色)、ASK(品牌定位) → 均合法 |
| P | `expressed_priority`：颜色先行（记录）；**`effective_priority` 服从硬约束**（§11.6 约束型依赖）→ `ordered=[ASK(品牌定位)]`；颜色进 `deferred_by_capacity`? **否**——是**依赖未决**，非容量 |
| U | "颜色确实要看品牌定位才能定，所以我先问一句：这个品牌想给人什么感觉？（东方雅致 / 精密可靠 / 亲切实用）" |
| W | 两项均保持 `OPEN`；**Priority 未改任何 gap 状态** |
| owner / Violation | Priority 排序（服从硬约束）／**无**；E4 ✓ |

| 轮 | 内容 |
|---|---|
| **轮3** | 用户：`东方雅致。` → 品牌定位 `CONFIRMED` |
| **轮4** | 用户：`现在可以定颜色了。` |
| P | 依赖已满足 → `ordered=[ASK(颜色)]`；**用户原偏好（颜色先行）自然生效** |
| U | "好，颜色的方向：墨绿系 / 哑光木色 / 低饱和米白？" |
| W | 颜色 `PROPOSED` → 用户答后 `CONFIRMED` |
| 结果 | 偏好保留 + 硬依赖优先 + 用户可见解释 + **Priority 未写状态** 全部成立 ✓ |

**剧本结果**：跑到底 ✓｜**硬约束被 hint 越过 0** ✓｜Layer violation **0**。

---

## E2E-10 · `priority_hint` scope 失效（不得泄漏到后续轮次）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`做个后台工具。` → 锚点确认；核心用户 OPEN |
| **轮2** | 用户：`这一轮先处理首页，其他下一轮。` |
| F | intent＝`priority_hint{scope: current_round, relations:[{before:[首页, 其他]}]}` |
| A | V0.3 合法动作：ASK(首页布局)、ASK(其他项) |
| P | `ordered=[ASK(首页布局)]`；其他 `deferred_by_capacity`（**仅调度事实**） |
| U | "好，先说首页：信息密度高一点，还是留白多？" |
| W | **不写回任何 gap 的 `deferred` 状态**（Interface §10 铁律）；首页/其他均为 `OPEN` |
| owner / Violation | Priority／**无**；E2 ✓ |

| 轮 | 内容 |
|---|---|
| **轮3** | 用户：`留白多。` → 首页布局 `CONFIRMED`；**`current_round` hint 到期** |
| **轮4** | （AI 准备继续） |
| P | hint 已过期 → 用默认序（§11.1）→ `ordered=[ASK(其他项)]`；**无残留影响** |
| U | "接下来把这个也定一下：……" |
| W | 无泄漏；无状态异常 |
| **轮5–6** | 其他项依次确认 → 收敛出稿 |
| 结果 | **过期 hint 泄漏 = 0** ✓；`deferred_by_capacity` 未被写成 gap 状态 ✓ |

**剧本结果**：跑到底 ✓｜Layer violation **0**。

---

## E2E-11 · 反复质疑 / 回退（A→B→C→回 A→质疑 A）

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`主色用蓝色。` → 主色 `CONFIRMED(A)` |
| **轮2** | 用户：`还是用墨绿吧。` → `Revision`（有值）→ `CONFIRMED(B)`；`supersedes(A→B)` |
| **轮3** | 用户：`再改成深灰。` → `CONFIRMED(C)`；`supersedes(B→C)` |
| **轮4** | 用户：`还是 A（蓝色）吧。` |
| F | intent＝`Revision`（回退型）；`reverted_to = target_value(蓝)` |
| A | V0.3：无需新动作（值已明确） |
| P | `ordered=[]`（若还有其他缺口则继续其调度） |
| U | "好，回到蓝色。" |
| W | `reverts(C→A)` 反向边；A 恢复 `CONFIRMED`；**B/C 保留但 `INVALIDATED`**；**authoritative 唯一** |
| owner / Violation | Interface §9.2／**无**；E1 ✓（不变量 I-1／I-2 同时满足） |

| 轮 | 内容 |
|---|---|
| **轮5** | 用户：`等等，A 也不太对。` |
| F | intent＝`Challenge`（**无新值**）；target＝`confirmed_value(A)` |
| A | V0.3：无新动作类型变化；仍为 ASK(新值) |
| P | `ordered=[ASK(新主色)]` |
| U | "好，那你想换成什么颜色？" |
| W | A → `CHALLENGED`；`validity_state = pending_resolution`（影响当前交付）；**不新增额度计数** |
| owner / Violation | Interface §9.6 + §10／**无** |

| 轮 | 内容 |
|---|---|
| **轮6** | 用户：`算了，还是蓝色吧，我多想了。` |
| F | intent＝`Challenge` → **withdrawal**（三条件满足：无新值 ∧ 明确撤回 ∧ 原值仍在） |
| A | 无动作 |
| P | `ordered=[]` |
| U | "行，就蓝色。" |
| W | A 恢复 `CONFIRMED`；历史保留 `challenged → withdrawal`；**未删除质疑痕迹** |
| owner / Violation | Interface §10.4 G-1／**无** |

**剧本结果**：跑到底 ✓｜**authoritative 唯一** ✓｜**无独立确认额度**（轮5–6 自由往返，未被"用尽"阻断）✓｜Layer violation **0**。

---

## E2E-12 · 撤回 + meta 反馈混入

| 轮 | 内容 |
|---|---|
| **轮1** | 用户：`图标用线性。` → `CONFIRMED` |
| **轮2** | 用户：`等等，图标风格我不太确定。` → `CHALLENGED` + `pending_resolution` |
| **轮3** | 用户：`你为什么一直问图标？` |
| F | intent＝**meta**（`target = interaction_process`） |
| A | V0.3：**不产生动作**（不改 gap） |
| P | 原 pending 保留；Priority 输出不变（其他合法动作照排） |
| U | "因为图标是首页第一眼会看到的部分，而且之前定过一次，我想确认它没被你的其他改动带偏；如果你想，我们可以先放着。" |
| W | **gap 状态不变**；pending 保留 |
| owner / Violation | §2.1 对外表达层（不触状态机）／**无**；E6 ✓（无机制词） |

| 轮 | 内容 |
|---|---|
| **轮4** | 用户：`好吧，那就不动它了。` |
| F | intent＝`Challenge`→withdrawal |
| A | 无动作 |
| P | `ordered=[]` |
| U | "好，保持线性。" |
| W | 原值恢复 `CONFIRMED`；历史保留 `challenged → withdrawal` |
| owner / Violation | Interface §10.4／**无** |

| 轮 | 内容 |
|---|---|
| **轮5** | 用户：`其他的你看着办。` |
| F | intent＝`Authorization`（`scope=current_decision_cluster`） |
| A | 逐 gap 过 T2 门 |
| P | `ordered=[ASK(费用)]`（若含 R6 项则仍待拍板） |
| U | "行，其他细节我按判断定了，会写进待确认假设；只有费用得你定。" |
| W | 非 R6 项 → `CLOSED(assumed)`；R6 项保持 `OPEN` |
| owner / Violation | Interface／**无** |

**剧本结果**：跑到底 ✓｜meta 不触状态机 ✓｜Layer violation **0**｜机制词泄漏 **0**。

---

## E2E Gate 汇总（12/12）

| 不变量 | 结果 | 取证 |
|---|---|---|
| **E1** 单一 authoritative current_value | ✅ | E2E-03（锚点 Revision 后下游全 `CHALLENGED`）、E2E-11（A→B→C→revert A，B/C `INVALIDATED`） |
| **E2** 只有 Interface 改 Gap 状态 | ✅ | 全部剧本：Priority 仅记 hint、V0.3 仅定动作、§11 仅问题选择 |
| **E3** 只有 V0.3 决定 Action 类型 | ✅ | E2E-01 轮2（R4 让 SHOW 先行、ASK 顺延）、E2E-08 轮2（不落 SUSPENDED） |
| **E4** Priority 只排序合法 Action | ✅ | E2E-09（依赖硬约束胜于 hint）、E2E-07（不调度 suspended gap） |
| **E5** §11 只在 ASK 被调度后工作 | ✅ | E2E-01 轮2（SHOW 轮内 §11 不介入）、全部 SHOW/TEACH 轮 |
| **E6** 用户可见输出无内部机制词 | ✅ | 全部 12 剧本的 `U` 行均为自然语言（无 CHALLENGED／pending_resolution／gap／Type 等字样） |

| 通过标准 | 结果 |
|---|---|
| 12 个多轮剧本全部跑到底 | ✅ **12/12** |
| Layer ownership violation | ✅ **0** |
| 错误重复询问 | ✅ **0** |
| 硬约束被 `priority_hint` 越过 | ✅ **0** |
| 无效/过期 hint 泄漏到后续轮次 | ✅ **0**（E2E-02、E2E-10 专项） |
| authoritative current_value 冲突 | ✅ **0** |
| 内部机制词用户可见泄漏 | ✅ **0** |
| K5（歧义） | **0**（未出现两个合法裁定的轮次） |

**未发现任何"某层越权/缺接口"的实例**；也**未为了全绿而补规则**。

---

## 残留观察（→ 移交 V0.4.6，不是本轮失败）

| # | 观察 | 归属 |
|---|---|---|
| O-1 | `priority_hint.scope = current_round` 的**"一轮"边界**未定义：是"用户回答后失效"还是"下一次 AI 输出后失效"（E2E-02 轮3、E2E-10 轮3–4 都踩在这个边界上，本轮按"用户回答即本轮结束"处理，结果唯一但不排除另一种读法） | **V0.4.6 Priority Hint Language & Lifecycle** |
| O-2 | 用户把"顺序偏好"与"延后决定"用同一句话表达时（"先 A，B 以后再说"），**需要拆成 `priority_hint` + delay 两件事**；本轮依赖 §10 复合语句分解契约处理，未新增字段 | V0.4.6 |
| O-3 | `deferred_by_capacity` 在多轮连续容量不足时的**累积可见性**（用户是否需要知道"已连续 2 轮没排上"）——本轮未出现，记为观察 | 后续（Priority 层，暂不处理） |

---

## 边界与状态

| 项 | 状态 |
|---|---|
| 冻结正文（§11／V0.3／Interface v1–v3／§10／Priority Contract v1） | **未修改** |
| 新增规则／字段／Action／Type／Gap state | **无** |
| 数值评分 | **未设计** |
| 本轮产物 | 本文件（replay 记录，仅测试） |
| 下一步（按裁决顺序） | **V0.4.6 Priority Hint Language & Lifecycle**（含 O-1／O-2 收口） |
