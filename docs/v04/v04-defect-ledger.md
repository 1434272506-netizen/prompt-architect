# V0.4 Defect Ledger（D/N 双账本）

> **编号治理（2026-10-03 修正）**
> - **`D01–D10` = 旧审计账本（Prompt-Architect-V0.4 交接文档），含义已固定，不得挪用**；
> - **`N01–N10` = 本轮 Notification/Fairness 口径批次**（替代此前误用的 D 编号）；
> - **`NR-01–NR-07` = 本轮最小回归探针**（替代此前的 "D02-A～D"）。
> **纪律**：不改 Type／Action／Gap state／字段枚举；改冻结正文需先登记 ＋ 最小回归。

---

## 一、旧审计账本（**编号保留，含义不得挪用**）

| 编号 | 固定含义 | 状态 |
|---|---|---|
| **D01** | **Final Architecture README 缺失**（`docs/v04/README.md` 仍为早期章程，**不是** Final Architecture README） | **OPEN BY DESIGN**（必须等行为矛盾、证据、冻结治理全部闭合后才处理） |
| **D02** | **无时机"别忘了"的通知时机冲突**（旧冲突：`NPC-02 = now` vs `V0.4.9 / O-4 = next_relevant_checkpoint`） | **✅ CLOSED BY N08/N09 + EL-02**（完整 closure chain 见 §十三） |
| **D03** | **PR-17 / Authorization**：`算了，还是你来定吧。` **≠ 确认某个具体 assumed value**；没有明确接受具体值，**不能**直接 `CLOSED(assumed) → CONFIRMED` | **✅ CLOSED BY N10**（见 §四） |
| **D04** | feedback gate 原子性粒度 | **✅ CLOSED BY CS-04**（原子性 = **per-Gap 完整门链**；见 §七） |
| **D05** | External 摘要漏 `information_source` | **✅ CLOSED BY CS-05**（`information_source ≠ external_owner`；§10 摘要引用 X-4；见 §七） |
| **D06** | `delay` / `askable_set` 冲突 | **✅ CLOSED BY CS-06**（`askable` 成员资格 ≠ 当前调度资格；见 §七） |
| **D07** | E2 owner 取证 | **✅ CLOSED BY ER-07**（ownership trace ＋ M-01～M-11 逐 mutation 链；见 §十） |
| **D08** | E3/E5 引用错误 | **✅ CLOSED BY ER-08**（4 条错引用已改；E3-A/B ＋ E5-A/B 重建；无 `NOT EVIDENCED`） |
| **D09** | debt 来源不透明 | **✅ CLOSED BY ER-09**（scenario 12 逐轮 provenance：+1 有据、`deprioritized` 后 increment=0） |
| **D10** | Discovery "30/30保持"表述问题 | **✅ CLOSED BY historical-governance closure**（治理条款 ＋ N06 应用实例 ＋ HG-10；见 §十三） |

**旧 D ↔ 新 N 映射**

```
D02  ←  N08 + N09
D03  ←  N10
```

> **按用户指令**：本轮通过的 Notification/Fairness/N10 规则**不能**替代旧审计 D04–D10 的闭合；须在 Final Architecture README → Release Ready **之前**单独扫完。

---

## 二、本轮 N 批次（Notification / Fairness 口径）

### N08 · 裸"别忘了。"的语义（**已裁 ✅ 生效**）

```
裸"别忘了／别漏掉／记着"（无时机、无"以后/之后/下次/等…之后"）
   → 建立 visibility_commitment
   → trigger = condition
   → condition = next_relevant_checkpoint
   ⇒ 不产生 notify_now
```

**关键净化**：**`notify_now` 是"兑现形态"，不是独立触发条件**；若解析时刻本身即自然检查点，则条件当场满足、当场兑现。

**理由**：① "不急"与"立刻提醒"自相矛盾；② 规则 4 的语义本就是"无时机的可见请求"；③ 净化后语义唯一；④ E2E 剧本 3/4/11 已按 checkpoint 跑通且零违规；⑤ 不动字段枚举。

**已落盘**：Notification Contract **§6.2 规则 4**（扩围）＋ **NPC-02**（trigger 修正）。

---

### N09 · `trigger=now` 的适用范围（**已裁 ✅ 生效**）

**判定表（正式）**

| 用户表达 | `trigger` | 依据 |
|---|---|---|
| "**现在**就说／现在告诉我还差什么／马上提一下" | **`now`** | **规则 6**（本次新增） |
| 明确时间（"周五"／"今天"） | `time_window` | 规则 1 |
| 明确条件（"客户回复后"／"上线前"） | `condition` | 规则 2 |
| 事项自带恢复条件（`SUSPENDED.resume_condition`） | `condition`（复用） | 规则 3 |
| "以后／之后／下次／到时候 提醒我" | `condition = next_relevant_checkpoint` | 规则 4 |
| **裸"别忘了／别漏掉／记着"** | `condition = next_relevant_checkpoint` | **N08**（规则 4 扩围） |
| 时机错误会造成明显损失 | 最小澄清 | 规则 5 |

**三条边界**：**B1** `now` 不是"更紧急"（不改调度／Gap）｜**B2** **只有系统自选时机适用 burden 延后；用户指定时机不因 burden 延后**｜**B3** `now` 仍须"事项仍存在且合法"。

**已落盘**：Notification Contract **§6.2 规则 6** ＋ **§6.2 的重要区分**（B2）。

---

### N01–N07 · 逐条裁决与执行

| 编号 | 条目 | 裁决 | 执行状态 |
|---|---|---|---|
| **N01** | `discharged` 写权限 | **✅ 通过** | **已落**：合同 **§4.1**（`Notification owns discharged ≠ Gap state write`）＋ **F9** E2E `W` 行注记 |
| **N02** | `notify_later` / burden 语义 | **🟡 改一句通过** | **已落**：合同 **§6.2**（B2：burden 只作用于系统自选时机）＋ **§6.3**（`notify_later` 落点＝后续满足条件的 relevant checkpoint 再评估）；**"每 checkpoint 至多尝试一次"已按裁决删除**（避免 attempt counter／checkpoint debt） |
| **N03** | `cycle ≡ current_round` | **🟡 条件通过（仅别名）** | **已落**：Fairness 合同 **§3.3**（采用批准文本："仅作为同义术语…**不改变既有 debt accumulation semantics**"）；**未触碰** debt 何时 +1／bundle 能否 +2／用户消息是否切 cycle／hard 周期计法 |
| **N04** | `starvation_candidate ⇔ ≥1` | **⛔ 暂缓** | **未落**：Fairness **§3.3 明确 HOLD**（不写 `≥1` 字面阈值；现有证据只支持"存在符合既有 debt 观察条件的 eligible-but-unscheduled 事件"） |
| **N05** | commitment 跨 cluster | **🟡 改写通过** | **已落**：合同 **§4.2**（绑 `gap identity + generation`；**cluster 结束不失效**；结束遵循既有出口 discharge／generation replacement／对象不再合法）；**"仅 generation 变化才终止"已按裁决删除** |
| **N06** | Discovery C-03/C-06 更正 | **✅ 通过** | **已落**：Discovery **追加更正（append-only）**，历史结果保留、标注 superseded |
| **N07** | 用户重提＝兑现 | **⛔ HOLD（需 NB-06 正式证据）** | **未落**：合同 **§7.1 记为未决**；安全形式（"用户主动重新使该事项进入当前对话**且系统实际处理**该事项 → 可视为已兑现，且不得仅因此创建第二次提醒义务"）留待证据齐备后再裁 |

---

### F 修复计划执行状态

| # | 对象 | 状态 |
|---|---|---|
| **F1** | NPC-02 trigger | ✅ 已改 |
| **F2** | 规则 4 扩围 ＋**新增规则 6（明确当场→now）** | ✅ 已改（**按 approved contract change 落笔，未写成"纯 README 澄清"**） |
| **F3** | Discovery append-only 更正（覆盖 NA-01／C-03／C-06） | ✅ 已改 |
| **F4** | O-4 升为正式判定契约 | ✅ 已改 |
| **F5** | 剧本 3/4/11 引用修复 | ✅ 已改（新增 O-6 统一 `W` 列语义） |
| **F6** | burden 只作用于系统自选时机 ＋ `notify_later` 落点 | ✅ 已改 |
| **F7a** | `cycle` 术语别名 | ✅ 已改（仅别名） |
| **F7b** | `starvation_candidate ≥1` | ⛔ **拆出，未落**（N04 HOLD） |
| **F8** | `discharged` 写权限 | ✅ 已改 |
| **F9** | E2E `W` 行＝Notification internal state | ✅ 已改 |

---

## 三、最小回归 NR-01～NR-07（按更新后合同重跑）

| # | 输入 | 期望判定 | 依据 | 结果 |
|---|---|---|---|---|
| **NR-01** | 裸`别忘了。`（无时机） | `trigger=condition`，`condition=next_relevant_checkpoint` → `notify_later` | §6.2 规则 4（N08） | **唯一 ✅** |
| **NR-02** | `现在告诉我还差什么。` | `trigger=now` → `notify_now` | §6.2 规则 6（N09） | **唯一 ✅** |
| **NR-03** | `以后提醒我。` | `condition=next_relevant_checkpoint` | §6.2 规则 4 | **唯一 ✅**（防回归） |
| **NR-04** | 裸`别忘了。`＋**解析时刻即自然检查点** | 条件当场满足 → 兑现一次（**仍非 `trigger=now`**） | §6.2 ＋ N08 净化 | **唯一 ✅** |
| **NR-05** | `现在说。`＋本轮有 **R6** 拍板 | **仍立即兑现一次** | §6.2 B2（用户指定时机不受 burden 延后） | **唯一 ✅** |
| **NR-06** | `现在说。`＋无 R6 | `notify_now` | 规则 6 | **唯一 ✅** |
| **NR-07** | `以后提醒我。`＋本轮有 R6 | `notify_later` → 后续 relevant checkpoint 再评估 | §6.3（N02 裁决文本） | **唯一 ✅** |

**重跑集**：NPC-02（trigger 已修正 → 唯一）／NPC-03（不变 → 唯一）／V0.4.9 剧本 3·4·11（`W` 行语义统一后仍零违规）。

**门槛核对**：NR **7/7 唯一**｜NPC **10/10 保持**｜**K4 = 0**｜**K5 = 0**｜错误主动提醒 **0**｜漏兑现 **0**｜**结构零新增**（无 attempt counter／无 checkpoint debt／无字面阈值）。

---

## 四、N10 · Authority transfer ≠ Value confirmation（**已执行 · 原 D03 由此闭合**）

**用户裁决（原文口径）**

> **Authority transfer is not value confirmation.**
> `你来定 / 还是你来定吧 / 你看着办` → Decision Authority / Authorization **≠** Value Acceptance → **不得仅凭这句话触发 R-2，不得仅凭这句话产生 `CONFIRMED`**。
> 执行方式：**不是"收紧 R-2"，而是"恢复 R-2 的既有适用边界，并修正 PR-17 的错误分类"**。

### Step 1–2 · 登记与改法

```
N10 — Authorization ≠ Confirmatory Acceptance

R-2 保持既有定义：
只有用户明确接受当前 assumed 的【具体值】，才属于 confirmatory feedback。

PR-17：
"算了，还是你来定吧。"
重新分类为 Authorization。

该表达本身：
- 不确认具体值；
- 不产生 CONFIRMED；
- 后续状态迁移复用既有 Authorization / T1 / T2 / Interface 合同。
```

**执行结果**：R-2 **定义未改**；仅更正 PR-17 分类（**纠错，非重新设计**）。落盘位置：[`pending-resolution-transition-contract.md`](pending-resolution-transition-contract.md) **§3.4（更正框）／§3.5（N10 边界）／§8.1（重确认）**、[`gap-ledger-interface.md`](gap-ledger-interface.md) §10.5。

### Step 3 · PR-17 重放（**不写死最终状态**）

```
输入：gap 已因 refused 落 CLOSED(assumed) → 用户："算了，还是你来定吧。"
classification = Authorization（≠ R-2）
⇒ 该句【不确认具体值】【不产生 CONFIRMED】
⇒ 后续跃迁交由既有 Authorization / T1 / T2 / Interface 合同决定
   （本合同不为它新设任何通道）
```

**判据（分类分界）**：**"你来定／你看着办"（无可指认值）→ Authorization**；**"就按 X／按你刚才定的那个 X"（值可指认）→ R-2**。

### Step 4 · RC-01～RC-03 重跑

| 探针 | 输入 | 结果 |
|---|---|---|
| **RC-01** | `CLOSED(assumed)` → 用户确认**同一具体值** | **R-2 → `CONFIRMED`**（进 `effective_set`）**唯一 ✅**（R-2 正向仍成立） |
| **RC-02** | 用户给出**不同值** | R-1 material → `OPEN` → Revision **唯一 ✅** |
| **RC-03** | 原值已 superseded，用户又确认旧值 | **不得直接 CONFIRMED** → 走 `revert`／当前状态规则 **唯一 ✅** |

### Step 5–6 · 最小语义对（negative ＋ positive control）

| 探针 | 输入 | 期望 | 结果 |
|---|---|---|---|
| **NR-08（negative）** | `还是你来定吧。`（仅授权、未接受具体值） | **Authorization；NOT `CONFIRMED`** | **唯一 ✅** |
| **NR-09（positive control）** | 已有 `assumed value = X`；用户 `就按 X。` | **R-2 → `CONFIRMED`** | **唯一 ✅** |

> 二者**必须成对存在**：任何人再次混淆 Authorization 与 Value Acceptance，会立刻撞红。

### Step 7 · 依赖 PR-17 的 V0.4.3 结论复核

| 依赖点 | 处理 |
|---|---|
| `pending-resolution-transition-contract.md` §3.4 | **已加更正框**（原表述保留备查） |
| 同文件 §8「PR-17（原 K5）」＋门槛核对行 | **已加更正指向 §8.1** |
| `gap-ledger-interface.md` §10.5 | **已更正归因** |
| `pending-resolution-second-challenge-discovery.md` PR-17 行 | **原表 intent 即记 `Authorization`** → 历史保留，追加跨文档更正说明（**不改写历史表格**） |
| `tests/acceptance.md` V0.4.3 条目 | **已补更正指向** |
| **旧 `K5 = 0`** | **不作为最终证据**；按项目定义**重跑后重确认** |
| `e2e-adaptive-replay.md` E2E-06 轮5（"还是按你刚才定的"） | **边界复核**：该句**指向可指认的具体值**（AI 先前 assumed 的 Linear，且用户自己刚选过）→ 仍属 **R-2 值接受**；**不属** N10 的"纯授权转移"。判据与 NR-08/09 一致 |

### Step 8 · K4 / K5 重确认（口径按要求改写）

```
N08/N09 regression:  NR-01～NR-07 = 7/7
K4:                  保持当前已验证结果（其定义未受 N10 影响）→ 0
K5:                  REOPENED FOR N10 → 现已重确认 = 0
                     previous K5=0 is NOT accepted as final evidence
```

| 指标 | 结果 |
|---|---|
| **K4** | **0**（定义未受 N10 影响） |
| **K5** | **0（重确认）** —— 新归因：**分类唯一**（Authorization）⇒ 无第二合法读法；**不再依赖 R-2 的扩大解释** |
| 旧 `K5=0`（V0.4.3） | **明确标注为"不作为最终证据"** |

### Step 9 · 回填旧 D03

```
D03 · PR-17 / Authorization
→ ✅ CLOSED BY N10
证据链：分类更正（§3.5）＋ PR-17 重放（Step 3）＋ RC-01～03（Step 4）
        ＋ NR-08 negative ＋ NR-09 positive control（Step 5–6）
        ＋ 依赖复核（Step 7）＋ K5 重确认（Step 8）
```

### Step 10 · 后续

**旧 D04–D10 closure sweep**（三组，按用户分组）：

```
语义澄清   D04 feedback gate atomicity ／ D05 external·information_source ／ D06 delay·askable_set
证据修复   D07 E2 owner ／ D08 E3·E5 citation ／ D09 debt provenance
历史治理   D10 Discovery 30/30
```

**本步边界**：只修分类与归因；**未写死 PR-17 后续状态**（不新设 transition path）；**R-2 定义未改**。

---

## 五、V0.5 架构候选（只记录，不改 V0.4）

见 [`v05-architecture-candidates.md`](v05-architecture-candidates.md)：**C1 Authority / Value Separation**（由 N10 发现）｜**C2 Notification lifecycle decomposition**（`Commitment → Trigger → Delivery → Discharge`，由 N08/N09 发现）。

---

## 七、D04–D06 closure sweep（第一批 · **语义澄清组**）· 全部 CLOSED

**执行编号**：**CS-04／CS-05／CS-06**（传播修复；**不再新起 defect 编号**）。
**登记**：例外 **#30**（本轮为**用户直接裁决并指令「直接落盘」**，登记与执行同轮，裁决全文见 `docs/freeze-v0.3.md` #30 行）。

### CS-04 · D04 feedback gate atomicity

**裁决**

> **Feedback gate atomicity 的最小原子单位是单个 Gap 的完整 gate chain**，不是整条 feedback，也不是整个 cluster。

```
atomicity = per-Gap transition atomicity
≠ whole-feedback transaction
≠ whole-cluster transaction
```

**落盘**：[`gap-ledger-interface.md`](gap-ledger-interface.md) **§8.1 原子性作用域（normative clarification）**；**G-8.3c（逐 gap 过 T2 门）改为该原则的正例**，不再是"例外"。**不新增状态、不加 rollback 机制、不加 cluster transaction。**

### CS-05 · D05 External / `information_source`

**裁决**

> **External 描述依赖来源；`SUSPENDED(external_owner)` 描述决策权／可继续处理能力是否真的离开了"用户—系统"闭环。**

```
reason = information_source  → 外部方只提供信息 → decision authority 仍属用户 → Gap 保持 OPEN（§9.5 X-4）
reason = external_owner      → 才进入既有 SUSPENDED(suspension_reason=external_owner)
```

**落盘**：[`gap-ledger-interface.md`](gap-ledger-interface.md) **§10.2 External 行已改为"按既有 reason 分派 + 引用 X-4"**（**不新增第七分支、不新增子类型**）。

**同类纪律（记入 V0.5 候选，未编号）**：`participation / information provision / decision authority` 是三个不同维度——**不要从"谁参与"推导"谁拥有决定权"**。

### CS-06 · D06 `delay` / `askable_set`

**裁决**

```
OPEN + deferred
  Gap state              : OPEN
  askable_set membership : YES
  normal scheduling now  : NO
```

> **`askable` 描述"该类 Gap 是否属于 ASK 可处理的需求类别"；`deferred` 描述"现在是否允许正常调度它"。两个维度完全不同。**
> `delay ≠ remove_from_askable_set`；`delay = suppress current normal scheduling`。

**落盘**：[`full-adaptive-e2e-replay.md`](full-adaptive-e2e-replay.md) 剧本 7 措辞改为"**仍属于 `askable_set`，但在 delay 有效期间不参与当前正常调度**"；**正式 `askable_set` predicate 未改**（机检：V0.4.5／V0.4.9 中其余 `askable` 表述均针对 `SUSPENDED`（X-2 正确），无同类误用）。

### 8 个 closure probes（全部唯一）

| # | 输入 | EXPECT | 结果 |
|---|---|---|---|
| **AR-01** | 同 cluster：A、B；**A 在风险门失败**，B 全门通过 | A **不发生部分状态写回**；B **正常完成自己的合法跃迁** | **唯一 ✅** |
| **AR-02** | 单 Gap A；**前置门通过、后置门失败** | A **不保留中间态**；该次 transition **整体不提交** | **唯一 ✅** |
| **EX-01** | "等供应商把报价发来，我再决定。" → `reason = information_source` | `OPEN`；**decision authority = user**；**NOT `SUSPENDED(external_owner)`** | **唯一 ✅** |
| **EX-02** | "必须等法务审批，法务决定后才能继续。" → `reason = external_owner` | 走既有 external-owner 路径；**可 SUSPENDED**；resume 由既有 Interface 规则管理 | **唯一 ✅** |
| **EX-03** | `information_source` 到达 | 补充信息进入既有处理链；**不得因曾经是 external information 而自动 `CONFIRMED`** | **唯一 ✅** |
| **DL-01** | `OPEN`；用户"这个先别处理" | → `OPEN + deferred`；**askable = YES**；**scheduling = NO** | **唯一 ✅** |
| **DL-02** | deferred 解除／用户恢复处理 | **无需重建 Gap、无需重新进入 `askable_set`**；只恢复当前调度资格 | **唯一 ✅** |
| **DL-03** | `OPEN + deferred` ＋ active `visibility_commitment` | delay 仍控制 scheduling；commitment 仍由 Notification 独立处理；**Notification 不得通过提醒偷偷取消 deferred 或调度该 Gap**（再次验证 **E8**） | **唯一 ✅** |

**门槛**：**8/8 唯一**｜**K4 = 0**｜**K5 = 0**｜未新增字段／状态／计数。

### 回填

```
D04  ✅ CLOSED      atomicity = per-Gap complete gate-chain atomicity
D05  ✅ CLOSED      information_source ≠ external_owner（X-4 restored in External summary）
D06  ✅ CLOSED      askable membership ≠ current scheduling eligibility
```

---

## 八、下一批（用户已指定思路）

**D07–D09 evidence repair**：**不再裁行为，只修证据链** —— D07 E2 ownership｜D08 E3/E5 错引用｜D09 scenario 12 的 debt provenance。
随后 **D10**（历史治理）。全部闭合后才是 **D01（Final Architecture README）→ Release Ready**。

---

## 十、D07–D09 evidence repair（第二批 · **只修证据链**）· 全部 CLOSED

**执行编号**：**ER-07／ER-08／ER-09**（evidence artifacts；**不再裁行为**）。
**产物**：[`release-evidence-closure.md`](release-evidence-closure.md)｜**登记**：例外 **#31**。

### ER-07 · D07 E2 ownership trace

**要证明的**：**每一次实际 Gap-state mutation，最终 write owner 都能追到 Interface**（不是"Interface 理论上有写权限"）。

- **六行 ownership trace**：V0.3 选 Action／§11 选问题／Priority 排序／Fairness 调调度竞争／Notification 本层 `visibility`·`discharged`——**五者皆"不写 Gap state"**；**Gap state commit = Interface**。
- **M-01～M-11**：把 V0.4.9 被引轮次的每次 mutation 展开为完整链（V0.3 → §11 → Priority／Fairness → **Interface commit**），含**负例 M-10**（剧本 3 轮5：`discharged` 仅 Notification 内部 → **Interface 无 mutation**）。
- **负向核对**：Action／§11／Priority／Fairness／Notification **均未被写成 Gap-state writer**（Fairness 的 `debt` 是自有观测账，非 Gap 字段）。

### ER-08 · D08 E3/E5 corrected evidence index

**要证明的**：E3 = **Action 类型始终由 V0.3 决定**；E5 = **§11 的 invocation condition = ASK has been scheduled**。

**旧汇总的 4 条索引损坏（逐条打开确认）**

| 旧引用 | 实际 | 处理 |
|---|---|---|
| `剧本 2 轮2` 称 SHOW | 实为 **`ASK(主视觉方向)`** | 改为 **剧本 1 轮2** |
| `剧本 9 轮2` 称"不落 SUSPENDED" | **该轮正是 `SUSPENDED(external_owner)`** | 改为 **V0.4.5 `E2E-08` 轮2**（法务＝`information_source` → 保持 `OPEN`） |
| `剧本 3 轮2` 称 SHOW 轮 | 实为 **deprioritized＋commitment 轮** | 移出 E5 |
| `剧本 5 轮2` 称 SHOW 轮 | 实为 **`priority_hint` 轮** | 移出 E5 |

**重建后的 index**：**E3-A** 剧本 1 轮2（SHOW；Priority 仅调位；最终仍 SHOW）｜**E3-B** 剧本 1 轮1（ASK）｜**E5-A** 剧本 1 轮2 ＋ 剧本 12 轮2（两个 SHOW 轮，§11 均不参与）｜**E5-B** 剧本 1 轮1／轮3（ASK 被调度后 §11 才选问法）。**无 `NOT EVIDENCED`；未补造轮次**（V0.4.9 SHOW 轮共 2 个）。

### ER-09 · D09 scenario-12 debt provenance trace

| 轮 | eligible | scheduled | skip_reason | debt |
|---|---|---|---|---|
| 轮3 | ✅ | ❌ | `soft_competition`（`current_round` 首页 ≻ 其他） | **0 → 1** |
| 轮4 | ✅ | ❌ | `soft_competition`（显式 hint `A ≻ C`） | **1 → 2** |
| 轮5 起 | ✅ | ❌ | `user_deprioritization` | **2 → 2（increment = 0）** |
| 轮8 | — | — | **generation replacement** | 旧债终止 |

**两个必须分开的命题**：

```
deprioritized does not erase existing debt   ← 已有债不清零
deprioritized does not add new debt          ← 不新增债
```

**⛔ 明确不是** `deprioritized → debt reset to 0`（未采用，那会改语义）。同源补证：剧本 10 轮2／轮3 的 debt=1／2 亦补齐 skip reason。

### 证据一致性探针

| # | 探针 | 结果 |
|---|---|---|
| **EV-07** | 所有被 E2 引用的 mutation → final writer 是否全 = Interface | ✅ **11/11**；无越权 writer |
| **EV-08** | 逐条打开 E3/E5 citation → 与汇总描述是否一致 | ✅ **修正后 4/4 一致**；旧 4 条错误引用已登记替换；无 `NOT EVIDENCED` |
| **EV-09** | 逐轮重建 scenario 12 debt | ✅ 每次 +1 有合法 skip reason；`deprioritized` 后 increment = 0；`debt=2` 可由前序完整推出（**O-5 未被混合场景违反**） |

```
D07 ✅ CLOSED BY ER-07    D08 ✅ CLOSED BY ER-08    D09 ✅ CLOSED BY ER-09
```

**本阶段门槛**：EV **3/3**｜**未新增行为规则／字段／状态**｜**未补造证据**。

---

## 十一、下一批

**D10** 历史治理（Discovery "30/30" 表述的正式闭合动作）→ **D02** 最终 evidence linkback → **V0.4 freeze governance baseline** → **D01 Final Architecture README** → **Release Ready**。

---

## 十二、处理顺序

```
N08／N09（已裁 ✅）→ N01–N07（已执行）→ F1–F6／F7a／F8–F9（已落；F7b HOLD）
   ↓
NR-01–07（7/7）＋ NPC 重跑                        ← 完成
   ↓
N10：分类更正 ＋ RC-01～03 ＋ NR-08/09 ＋ 依赖复核   ← 完成
   ↓
K4 / K5 重确认（K4=0；K5 重确认=0）                ← 完成
   ↓
原 D03 ✅ CLOSED BY N10                           ← 完成
   ↓
D04–D06 ✅ CLOSED BY CS-04/05/06                  ← 完成
   ↓
D07–D09 ✅ CLOSED BY ER-07/08/09                  ← 完成
   ↓
D10 ✅ + D02 ✅（历史治理 ＋ 证据回链，本步）        ← 完成
   ↓
【下一刀】V0.4 freeze governance baseline
   ↓
D01 Final Architecture README（OPEN BY DESIGN）
   ↓
V0.4 正式封版（Release Ready）
```

**本步边界（汇总）**：未挪用旧 D 编号；未落 N04（`≥1`）与 N07（"重提＝兑现"）；未改 R-2 定义；未新设 transition path；`SKILL.md`／Interface v1–§10 语义（除 §10.5 归因更正）／§11／V0.3／Priority Contract 未改。

---

## 十三、D10 历史治理 ＋ D02 证据回链（第三批 · 收口）· 全部 CLOSED

**登记**：例外 **#32**（用户直接指令本轮执行 1–8）。
**产物**：[`historical-discovery-governance.md`](historical-discovery-governance.md)（D10 治理条款）。

### D10 · 历史治理条款闭合

**只做一件事**：**把 Discovery 的历史身份与现行规范身份彻底分开**（不改任何运行时规则）。

5 条治理条款（全文见治理文件）：① append-only 历史证据、不得覆写；② Discovery 结论是 **candidate findings**，不自动成为规范合同；③ 后续已批准合同对同一语义问题作出不同裁决时，**以后续合同为现行行为权威**；④ 被取代结论**保持可见**并须标注**历史状态／取代者／现行解释**；⑤ **`30/30` 只表示历史执行／覆盖成功**，**不得**读作"30 个历史结论今天仍是现行规范行为"。

**证据层次**：

```
治理规则（Historical Discovery Governance）
   → 实际应用（N06 append-only 更正）
      → 历史 artifact（C-03／C-06 仍保留在 Discovery 正文）
```

**N06 与 D10 的关系**：**N06 是实例修复，D10 是治理规则闭合**——本轮**未重复修改 C-03／C-06**。

### HG-10 · Historical Governance 探针（**文档身份检查，非行为测试**）

| 检查项 | C-03 | C-06 | **NB-01**（未被取代对照） |
|---|---|---|---|
| historical evidence still present | ✅ | ✅ | ✅ |
| superseded case explicitly marked | ✅ | ✅ | —（本就不需标注） |
| current normative source identified | ✅ 规则 4 | ✅ 规则 4 | ✅ 规则 4 |
| **historical output silently rewritten** | **NO** | **NO** | **NO** |

**HG-10 = PASS**（刻意纳入一个**未被取代**的案例：治理条款**不得**降级仍有效的历史结论）。

### D02 · 最终 evidence linkback（closure chain）

```
D02
├─ root conflict
│    NPC-02: trigger=now
│    vs
│    V0.4.9 / O-4: next_relevant_checkpoint
│
├─ adjudication
│    N08: bare visibility request → condition = next_relevant_checkpoint
│    N09: explicit immediate request → trigger = now
│
├─ contract propagation
│    §6.2 规则 4 扩围（"任何不含时机的可见请求"）
│    §6.2 规则 6 新增（用户明确要求当场 → now）
│    NPC-02 修正为 trigger=condition
│
├─ regression
│    NR-01～NR-07 = 7/7
│    NPC = 10/10
│    V0.4.9 剧本 3／4／11 语义对齐
│
└─ structural check
     no new Action
     no new Gap state
     no counter / debt
```

**EL-02 · D02 Evidence Linkback 探针（链路完整性）**

| 环节 | 是否能从旧 D02 条目追到 | 结果 |
|---|---|---|
| D02 → N08／N09 裁决 | ✅（本 §十三 ＋ N 批次 §二） | 无断链 |
| N08／N09 → contract change | ✅（Notification Contract §6.2 规则 4／规则 6） | 无断链 |
| contract change → NPC-02 | ✅（NPC-02 已改为 `trigger=condition`） | 无断链 |
| NPC-02 → NR-01～NR-07 | ✅（NR-01～NR-04 直接覆盖该语义；NR-05～NR-07 覆盖 N09 边界） | 无断链 |
| → current normative interpretation | ✅（"无时机 → checkpoint；明确要求当场 → now"） | 无断链 |

**EL-02 = PASS**（全链无断链）。

### 回填

```
D10  ✅ CLOSED BY historical-governance closure
     evidence: governance clause ＋ N06 append-only correction ＋ superseded examples（＋ HG-10）
D02  ✅ CLOSED BY N08/N09 + EL-02
     evidence: root conflict ＋ adjudication ＋ contract propagation ＋ regression ＋ structural check
```

### 账本终局（本阶段）

```
D01  OPEN BY DESIGN（Final Architecture README —— 唯一仍 OPEN 的审计项，且本就是设计如此）
D02  ✅ CLOSED BY N08/N09 + EL-02
D03  ✅ CLOSED BY N10
D04  ✅ CLOSED BY CS-04
D05  ✅ CLOSED BY CS-05
D06  ✅ CLOSED BY CS-06
D07  ✅ CLOSED BY ER-07
D08  ✅ CLOSED BY ER-08
D09  ✅ CLOSED BY ER-09
D10  ✅ CLOSED BY historical-governance closure
```

> **V0.4 architecture + defect closure complete; release governance and final documentation remain.**

### 下一刀（已锁定）→ **已于本轮执行，见 §十四**

**V0.4 freeze governance baseline** —— 目的不是继续找 bug，而是把**现在这一刻**变成未来可验证的 **V0.4 approved baseline**：

```
所有 D02–D10 CLOSED
   ↓
确定最终 approved V0.4 contract set
   ↓
登记【从此刻起生效】的 V0.4 baseline
   ↓
记录 hash / manifest / approval provenance
   ↓
修 governance checker
   ↓
从此未来 drift 可独立验证
```

**⛔ 绝不能写**："这些 hash 证明过去它们一直就是冻结版本"。
**✅ 正确表述**：**"这是 closure 完成以后建立的首个可追溯 V0.4 release baseline。"**

---

## 十四、V0.4 Release Baseline Protocol（BL-01～BL-10）· D11／D12 闭合

**登记**：例外 **#33**。**产物**：`docs/v04/v0.4-release-baseline.json`（machine source of truth）＋ `docs/v04/v0.4-release-baseline.md`（human record）；工具 `.gh-search/generate_v04_baseline.py`（可写，仅初始化／经批准 rebaseline）＋ `.gh-search/verify_v04_release_baseline.py`（**永远只读**）。

### BL-01 · Artifact Classification（三层，**不把全部叫"合同"**）

| 层 | 身份 | 文件 |
|---|---|---|
| **A · Normative** | 真正决定运行语义 | `gap-ledger-proposal.md`｜`gap-ledger-interface.md`｜`pending-resolution-transition-contract.md`｜`priority-layer-contract.md`｜`scheduler-fairness-contract.md`｜`notification-policy-contract.md` |
| **B · Governance** | 历史／冻结／发布证据如何解释 | `historical-discovery-governance.md`｜`v04-defect-ledger.md`｜`docs/freeze-v0.3.md` |
| **C · Evidence** | 证明 Release Gate 的材料 | `interface-v3-migration-manifest.md`｜`interface-v3-migration-test.md`｜`pending-resolution-second-challenge-discovery.md`｜`priority-model-discovery.md`｜`priority-hint-language-discovery.md`｜`scheduler-fairness-starvation-discovery.md`｜`notification-policy-discovery.md`｜`e2e-adaptive-replay.md`｜`full-adaptive-e2e-replay.md`｜`release-evidence-closure.md` |

> **`release-evidence-closure.md` 身份 = release evidence ≠ normative source**（可与合同同时 MATCH，但**权威不同**）。

### BL-02 · Candidate Inventory

路径唯一／全部存在／类已分配／**scope 与 out-of-scope 无交集**（机检，见 `--enumerate` 输出）。**out of scope** 明确列出（含 `docs/v04/README.md` ＝ 将由 D01 取代、`v05-architecture-candidates.md` ＝ V0.5 前瞻、Phase 2 中间设计记录等）。

### BL-03 · Hash Specification

```
file hash    = SHA256(raw bytes)   → 权威冻结值（不做 trim／换行归一化／排序／语义归一化）
section hash = 按 `## ` 切节的诊断哈希 → 只用于定位漂移
```

**禁止**：`file DIFF + section MATCH ⇒ 整体通过`。

### BL-04 · Candidate Hash Run（只读）

`python .gh-search/generate_v04_baseline.py --enumerate` → 输出候选表；**此时不声称 MATCH**（bootstrap：尚无比对对象）。

### BL-05 · Approval Provenance（**不引用聊天本身**）

manifest 的 `approval_provenance` 回链**已落仓库**的材料：`v04-defect-ledger`（D02–D10）｜`N08/N09/N10`｜`CS-04～06`｜`ER-07～09`｜probes（`NR-01..07`／`AR`／`EX`／`DL`／`EV-07..09`／`HG-10`／`EL-02`）｜`freeze-v0.3.md §4` 例外 `#13..#33`｜协议步骤 `BL-01..BL-10`。

### BL-06 · Initialize V0.4 Baseline

`python .gh-search/generate_v04_baseline.py --init` → 写 JSON ＋ Markdown；**标记 `INITIAL BASELINE`**；记录 `effective_at`；**`prospective_only = true`**，声明：

> *This is the first traceable V0.4 release baseline established after architecture and defect closure. It is effective prospectively from the recorded baseline timestamp and does not prove that these files were historically identical before that point.*

**V0.3 关系**：只**引用**既有 V0.3 baseline（`docs/freeze-v0.3.md` ＋ `freeze_v03.py`），**不复制那 24 个 hash**（避免两个 source of truth）。

### BL-07 · Read-only Verification

`python .gh-search/verify_v04_release_baseline.py`（**永远只读，无写入参数**）→ 组合输出：

```
V0.3     MATCH 24  DIFF 0  UNREGISTERED 0
V0.4     MATCH 20  DIFF 0  MISSING 0  UNREGISTERED 0
SECTIONS （诊断）
RESULT   PASS
```

**退出码**：`0 PASS`／`1 DRIFT（DIFF·MISSING·UNREGISTERED·治理违规）`／`2 manifest 缺失或不可读`／`3 V0.3 校验无法执行或未通过`。**修复 D12 的"显示 DIFF 但仍像成功"问题。**

### BL-08 · Governance Negative Probe（证明 checker **不是摆设**）

| 步骤 | 期望 | 实测 |
|---|---|---|
| 1. 临时副本（镜像相对路径）中改动一个字符 | verifier 必须 **DIFF** 且 **exit ≠ 0** | **DIFF 1，exit 1** ✅ |
| 2. 恢复原件 | verifier 必须 **MATCH** 且 **exit = 0** | **DIFF 0，exit 0** ✅ |

### BL-09 · D11 / D12 Closure

```
D11 · V0.4 核心合同缺少独立可复核的冻结哈希
✅ CLOSED BY V0.4 INITIAL RELEASE BASELINE
证明：approved artifact set 明确｜effective_at 明确｜SHA-256（raw bytes）manifest
      ｜approval provenance 回链｜prospective-only 声明｜独立 verification PASS

D12 · 旧治理脚本存在治理缺陷（--write／退出码／章节校验／哨兵替换）
✅ CLOSED BY GOVERNANCE CHECKER REPAIR
证明：verify 路径**只读**（无写入参数）｜DIFF ⇒ 非零｜MISSING ⇒ 非零｜UNREGISTERED ⇒ 非零
      ｜section comparison 仅诊断且确定｜无哨兵替换风险（新 verifier 不写文件）
      ｜baseline initialization 与 verification **分权**（generator ≠ verifier）
```

### BL-10 · Freeze

**自 `effective_at` 起**，该 manifest 成为 **V0.4 首个可追溯 release baseline**；**不声称**"这些文件过去一直如此"。

**本段边界**：**未改任何运行时规则／字段／状态／计数**；仅新增 baseline 记录与治理工具。

### 账本终局（含 D11／D12）

```
D01  OPEN BY DESIGN（Final Architecture README）        ← 唯一仍 OPEN
D02–D10  ✅ CLOSED
D11  ✅ CLOSED BY V0.4 INITIAL RELEASE BASELINE
D12  ✅ CLOSED BY GOVERNANCE CHECKER REPAIR
```

---

## 十五、D01 · Final Architecture README ＋ Final Release Gate（FRG-01～08）· **全部 CLOSED**

**登记**：例外 **#34**。**产物**：[`docs/v04/README.md`](README.md)（Final Architecture README，取代早期章程）＋ `.gh-search/verify_readme_reverse_refs.py`（FRG-07 只读审计器）。

### D01 · 写入规格（按 17 节）

首页状态块（Architecture／Defect／Evidence closure complete ＋ traceable release baseline）｜**System Purpose**（按"系统为什么存在"讲，不按文件讲）｜**Architecture at a Glance**（主链 ＋ 旁路 visibility path，并明确第二条链是**架构视图不是新状态机**）｜**Ownership Matrix**（六层：输入／输出／**唯一写权限**／明确禁止）｜Interface（锚 ＋ **D04/D05/D06 三条 clarified boundaries**）｜Resolution & Value（**N10**：`Decision Authority ≠ Value Acceptance` ＋ "不要从参与关系推导事实承诺"）｜Priority｜Fairness（含 **O-5** 两个命题 ＋ N04 表述）｜Notification（四出口 ＋ timing 表 ＋ **B2** ＋ "条件已成立 ≠ 改触发类型"）｜**Notification vs Fairness**｜ASK/§11 边界｜**E1–E8**（状态：Architecture definition CLOSED ／ Evidence index repaired & verified）｜Historical Governance｜Release Evidence（只做索引）｜Freeze & Release Governance｜**Known Non-goals**（N04／N07／D12 residual 三项，措辞均为"deferred／excluded／legacy debt"，**不是 Release blocker**）｜V0.5 Candidates（C1／C2）｜**Final Release Gate**｜**Appendix A · README Claim Index**（28 条，机器可校验）。

### **FRG-07 抓到的真实缺陷（本轮新增，已修）**

| # | 现象 | 判定 | 处理 |
|---|---|---|---|
| **1** | `CL-07` anchor 在 Interface 中**不存在** | ⚠ **真实缺陷**：**CS-06 的传播修复不完整** —— D06 澄清只落在**缺陷账本**与 **E2E 措辞**，**从未落进 Interface 正文**（`askable_set` 定义处没有 `OPEN + deferred` 的成员资格说明） | **已补齐 normative home**：Interface **§1.2** 新增 `OPEN + deferred` 成员资格说明 ＋ `delay ≠ remove_from_askable_set`（维度分离：`askable` = 需求类别；scheduling = 当前执行窗口） |
| **2** | `CL-10` anchor 在 priority-layer-contract 中不存在 | 引用错误（`explicit active user priority` 的规范落点在 **fairness 合同 §1**） | README **§6 注明双来源**；`CL-10` 改指 `scheduler-fairness-contract.md` |
| **3** | `CL-11` anchor 不存在（该措辞在 fairness N03 别名行） | 引用错误 | `CL-11` anchor 改为 `current_round :=`（priority-layer-contract §9.2 的真实定义处） |

> **这三条正是 FRG-07 存在的理由**：README 会**引用错**，也可能**掩盖下层缺漏**。审计后复跑 **28/28 全部可追**。

### Final Release Gate · 结果

| # | Gate | 结果 |
|---|---|---|
| **FRG-01** | V0.3 freeze verification | ✅ `MATCH 24 / DIFF 0 / UNREGISTERED 0`（exit 0） |
| **FRG-02** | V0.4 baseline verification | ✅ `MATCH 21 / DIFF 0 / MISSING 0 / UNREGISTERED 0`（exit 0；**当前 baseline 见 manifest `baseline_id`**，README 已入 scope） |
| **FRG-03** | Release evidence | ✅ **EV-07** 11/11 mutation writer = Interface｜**EV-08** 修正后 4/4 一致｜**EV-09** provenance 完整 |
| **FRG-04** | Historical governance | ✅ **HG-10 = PASS** |
| **FRG-05** | D02 closure linkage | ✅ **EL-02 = PASS**（全链无断链） |
| **FRG-06** | Defect ledger | ✅ **D02–D12 CLOSED**；**D01 complete** |
| **FRG-07** | README reverse-reference audit | ✅ **28/28 claims 可追**；无 README-only rule |
| **FRG-08** | Baseline integrity after README addition | ✅ README 纳入 baseline（governance 类）→ **经批准 rebaseline** → 最终 verifier **PASS** |

### D01 闭合条件核对

```
Final README written                                  ✅
no historical-stage wording as current architecture   ✅（早期章程已显式标注 Superseded）
no README-only normative rule                         ✅（FRG-07）
all contract links valid                              ✅（FRG-07 逐条校验 source ＋ anchor）
Known Non-goals clearly separated                     ✅（§15 三项，均非 blocker）
baseline / evidence references correct                ✅（FRG-02／08）
FRG-01～08 PASS                                       ✅
```

```
D01  ✅ CLOSED BY FINAL ARCHITECTURE README
```

### 终局

```
D01–D12 ALL CLOSED
Architecture closure       PASS
Evidence closure           PASS
Governance closure         PASS
Release baseline           PASS
Final Architecture README  PASS
Final Release Gate         PASS

V0.4 RELEASE READY
```
