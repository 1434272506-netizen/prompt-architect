# V0.4.3 · Pending Resolution Transition Contract（设计 + 18 例证伪测试）

> **阶段**：**设计阶段 → 并入候选**（本轮**不并入冻结正文**）。
> **不修改**：`SKILL.md`／§6.3／§11／Interface v2／v3 冻结正文／V0.3。**不新增**：Type／Action／Gap 生命周期状态。
> **上游**：[`pending-resolution-second-challenge-discovery.md`](pending-resolution-second-challenge-discovery.md)（PR-01～36；K4 = 0、K5 = 1 ＝ PR-17）
> **冻结门槛**：PR 36/36 保持｜新增 18 例全部唯一｜**PR-17 K5 消失**｜**K4 = 0、K5 = 0**｜三条不变量通过。

---

## 1. 核心模型（两段式，**不是 `intent → state` 一跳映射**）

```
pending_resolution
        ↓
第二次反馈
        ↓
① intent dispatch          （决定进入哪一类「跃迁分支」）
        ↓
② target / scope / risk / blocking / provenance / resume_condition
                            （决定该分支的「具体出口」）
        ↓
具体跃迁
```

**正式废弃**（旧局部模型）：

```
pending_resolution → 剩余确认次数 → 是否还能再问        ❌ 废弃
```

**修正后的准确表述（按你的收紧）**：

> `feedback.intent` **决定进入哪一类跃迁分支**；`target`／`scope`／`blocking`／`risk`／`provenance`／`resume_condition` **决定该分支的具体出口**。
> 例：同一个 `Authorization`，普通项 → `CLOSED(assumed)`；R6 项 → 门 blocked → 保持 `OPEN`。

**关于计数（严格限定，不改既有规则）**：

> **Contract 自己不拥有新的"二次确认计数器"。**
> `pending_resolution` **不新增独立额度**；既有 `unable`／`evaded`／`no_signal` 等计数**仍由它们原本所属的冻结规则负责**，本 Contract **不改写**其归属与语义。

---

## 2. 六分支主合同骨架

| intent | 分支出口（① 之后的 ② 判定） |
|---|---|
| **Revision** | **有新值** → 走正常 Revision（`supersedes`／`reverts`）；**无新值** → 保持待解决 + **索取最小必要新值**；**不受"已经确认过一次"限制** |
| **Unable** | 走现有降维／`defer`／`default` 逻辑；**`blocking = true` 时仍不能静默默认** |
| **Refused** | 非阻塞 → 允许 `CLOSED(assumed)`；**blocking／R6 → 保持未决**（`OPEN`） |
| **Authorization** | **必须重新经过 T1 scope + T2 risk gate**；`effective` 才能 assumed；`blocked` → 仍未决 |
| **Challenge** | **新质疑** → 继续 `pending_resolution`；**质疑撤回** → 恢复原有效值（见 §4）；**target 不明** → 先定位 target |
| **External dependency** | `SUSPENDED(suspension_reason = external_owner)`；`resume_condition` 满足后**重新进入正常处理**（再走一次 ① ②） |

**三条结构性约束**

1. 分支**只能决定"进入哪一族"**，不得绕过 ② 的判定直接落状态。
2. **同一 intent 在不同 `risk`／`blocking` 下出口不同**（Authorization／Refused／Revision／Unable 均有对照例）。
3. **不存在"用尽额度"这条出口**：出口只有"终结（CONFIRMED／assumed／INVALIDATED）"、"继续待解决"、"挂起（SUSPENDED）"三类。

---

## 3. K5-1 · `CLOSED(assumed)` 的重进入口（**不是"永远 OPEN"**）

**问题**：`CLOSED(assumed)` **不是永不可触碰的墓碑**；用户后续主动给出**有决策意义的新反馈**时，它必须能重新进入处理。但**不能简单写成"用户一提起就 OPEN"**——那会产生无意义的 `CLOSED → OPEN → CLOSED` 抖动。

### 3.1 重进入口分四类

```
R-1 material re-entry（改变决策）
    条件：反馈会改变 assumed 值，或产生新的决策
          （明确新值 / 撤销"让你默认"自己选 / 改变目标或范围）
    跃迁：CLOSED(assumed) → OPEN → 走 intent dispatch（正常处理）
    历史：原 assumed 值保留（supersedes / reverts 记录），**不删除**

R-2 confirmatory re-entry（只是确认原假设 → **直接确认跃迁**）
    条件：用户**明确追认当前 assumed value**，且该值未被 supersede / invalidated
    跃迁：CLOSED(assumed) → **CONFIRMED**（**不经过 OPEN**）
    同步：confidence := confirmed；provenance += user_confirmed_after_assumed
    历史：只追加，**不删除**原 assumed 记录
    禁止：产生 OPEN → CONFIRMED 之外的无意义 `OPEN → CLOSED` 抖动

R-3 无决策意义（闲聊 / 无关提及）
    跃迁：不触发 re-entry；状态不变

R-4 原 assumed 值已被后续 Revision invalidated
    跃迁：不适用 re-entry；按该 gap 的**现有状态**处理（旧值已被 supersede）
```

### 3.2 为什么 R-2 必须是**状态跃迁**，而不是"保持 CLOSED 只升 confidence"

**（R-2 封口修正，2026-10-02，预登记 #16）**

原写法的结构性矛盾：

```
R-2 原：CLOSED(assumed) 不变，仅 confidence: assumed → confirmed
而 v1 冻结谓词：effective_set = CONFIRMED ∩ valid
→ 该 gap 仍然进不了 effective_set  →  R-2 声称的"成为生效事实"与谓词冲突
```

**最小修复（已采纳）**：R-2 改为**直接确认跃迁** `CLOSED(assumed) → CONFIRMED`（**不经 OPEN**），于是

```
status = CONFIRMED ∧ validity_state = stable   →  自然满足 effective_set = CONFIRMED ∩ valid
```

**不需要修改任何冻结谓词**，也仍然满足原目标：**禁止无意义的 `OPEN → CLOSED` 抖动**。

**为什么不接受"保持 CLOSED，只升级 confidence"**：

```
status      = CLOSED(assumed)
confidence  = confirmed          ← 两个维度争夺 authoritative truth
```

那以后所有消费者都必须回答"到底读 status 还是读 confidence"，会重新制造此前花大力气消灭的**双重事实源**。更干净的原则：

> **`status` 决定需求当前处于什么生命周期；`confidence`／`provenance` 只描述"这个状态为什么成立"。**
> 不允许 `confidence` 反过来偷偷改写生命周期意义。

### 3.3 修正后的四条重进（R-1～R-4）

| 类 | 条件 | 跃迁 | 是否经 OPEN |
|---|---|---|---|
| **R-1 material** | 反馈改变 assumed 值／产生新决策 | `CLOSED(assumed)` → `OPEN` → 走 intent dispatch | **经** |
| **R-2 confirmatory** | 用户明确追认当前 assumed 值，且未被 supersede／invalidated | `CLOSED(assumed)` → **`CONFIRMED`**（confidence := confirmed；provenance += `user_confirmed_after_assumed`） | **不经** |
| **R-3 无决策意义** | 闲聊／无关提及 | 状态不变 | — |
| **R-4 原值已被 supersede** | 用户又确认已被替代的旧值 | **不得直接 CONFIRMED**：走 `revert`（`reverted_to`）或当前状态规则 | 视路径 |

### 3.4 PR-17 的 K5 由此消失 —— **⚠ 本节原判已被 N10 更正（2026-10-03）**

> **原表述（保留备查，已更正）**：本节曾判定 PR-17 为 **R-2 confirmatory**，理由是"用户明确追认**由 AI 定**这一既有假设"→ 直接 `CONFIRMED`。
> **更正原因**：`算了，还是你来定吧。` **转移的是决定权（Authorization），不是对某个具体值的接受**；R-2 的既有定义要求"明确追认**当前 assumed value（具体值）**"。原判**超出 R-2 的字面条件**。
> **正确处置**：见 §3.5（N10 边界）。**R-2 定义本身不变**。

```
场景：gap 已因 refused 落 CLOSED(assumed) → 用户："算了，还是你来定吧。"
N10 结论：classification = Authorization（≠ R-2）
          → 该句本身【不确认具体值】【不产生 CONFIRMED】
          → 后续状态迁移复用既有 Authorization / T1 / T2 / Interface 路径（本合同不为它新设通道）
```

### 3.5 N10 边界：**Authority transfer is not value confirmation**

> **`你来定 / 还是你来定吧 / 你看着办` = Decision Authority / Authorization ≠ Value Acceptance。**

```
分类：Authorization
      ⟹ 不触发 R-2
      ⟹ 不得仅凭该表达产生 CONFIRMED
```

**判据（区分"授权"与"值接受"）**

| 表达 | 分类 | 依据 |
|---|---|---|
| "你来定／还是你来定吧／你看着办／随便" | **Authorization** | **没有可指认的具体值** |
| "就按 X／就用线性／按你刚才定的那个 X" | **R-2 confirmatory** | **值可被明确指认**（用户接受该具体值） |

**边界说明**：R-2 的**定义不变**（"用户明确追认当前 assumed 值"）；本次修的是**分类**（PR-17 曾被误归一 R-2），**不是重新设计 R-2**。

**未写死**：N10 **不**规定"授权后必然落到哪个状态"——由既有 Authorization／T1／T2／Interface 合同自行决定。

---

## 4. G-1 · `Challenge` 撤回（challenge withdrawal）

**触发三条件（同时满足）**：① 无新值；② 明确撤回质疑；③ **原值仍存在**且未被其他 Revision `INVALIDATED`。

```
pending_resolution
   → challenge withdrawn
   → 原 authoritative value 恢复有效（回 VALID / CONFIRMED）
   → 历史必须保留 challenged → withdrawal（**不得删除质疑痕迹**）
```

任一条件不满足 → 不适用撤回（例：原值已被 Revision 取代 → 按现有状态处理）。

---

## 5. G-2 · meta feedback（**不是第七种业务 Intent**）

```
target = interaction_process        # 质疑的是「采访过程」，不是需求值
结果：解释原因 → gap 状态不变 → 原 pending_resolution 保留 → 解释完成后继续原流程
```

- **不新增 Gap 生命周期状态**；
- **不塞进 `Challenge`**（用户质疑的是过程，不是值）；
- 与 §2.1 对外表达一致（用户侧不出现机制词）；同轮容量与顺序仍受 V0.3 契约 R4 约束（属动作层，不改状态）。

---

## 6. 18 个 Contract 证伪案例

字段：`ID ｜ 当前状态 ｜ 第二次反馈原话 ｜ intent ｜ target/scope/risk/blocking ｜ 出口 ｜ 唯一 ｜ K`

### 6.1 `CLOSED(assumed)` re-entry（5）

| # | 当前状态 | 原话 | intent | ② 判定 | 出口 | 唯一 | K |
|---|---|---|---|---|---|---|---|
| **PC-01** | `CLOSED(assumed)`（图标风格） | `图标还是用线性的吧。` | `Revision`（有新值） | 新值明确 | **R-1 material** → 重开 → Revision → CONFIRMED(线性)；历史保留原 assumed | **唯一** | K3 |
| **PC-02** | `CLOSED(assumed)`（图标风格=线性） | `算了，还是按你刚才定的。` | 追认（无新值） | 明确追认当前 assumed 值 | **R-2 confirmatory** → `CLOSED(assumed)` **→ `CONFIRMED`（不经 OPEN）**；`confidence := confirmed`；`provenance += user_confirmed_after_assumed`；**进 `effective_set`**；**无 OPEN 抖动** | **唯一** | K3 |
| **PC-07** | `CLOSED(assumed)`（配色=AI 选） | `刚才那个别默认了，我要自己选。` | `Revision`（撤销默认） | 撤销授权的决定 | **R-1 material** → 重开 → ASK（用户自己选） | **唯一** | K3 |
| **PC-08** | `CLOSED(assumed)`（旧值已被后续 Revision 取代） | `还是用最早那个默认的吧。` | `Revision`（回退） | 原 assumed 已被 supersede | **R-4**：不适用 re-entry；按现有状态走 `reverted_to=target_snapshot` | **唯一** | K2 |
| **PC-09** | `CLOSED(assumed)` | `顺便问下，你们怎么收费？` | 无关（元对话） | 无决策意义 | **R-3**：不触发 re-entry；状态不变 | **唯一** | K1 |

### 6.2 Challenge withdrawal / meta feedback（4）

| # | 当前状态 | 原话 | intent | ② 判定 | 出口 | 唯一 | K |
|---|---|---|---|---|---|---|---|
| **PC-03** | `pending_resolution`（受众） | `你为什么这么问？` | **meta**（`target = interaction_process`） | 质疑过程 | 解释原因；**gap 状态不变**；pending 保留；继续原流程 | **唯一** | K3 |
| **PC-04** | `pending_resolution`（视觉方向） | `算了，就按原来的。` | `Challenge` → **withdrawal** | 无新值 ∧ 明确撤回 ∧ 原值仍在 | 原 `authoritative value` 恢复有效；历史保留 `challenged → withdrawal` | **唯一** | K3 |
| **PC-10** | `pending_resolution`；原值已被别的 Revision `INVALIDATED` | `算了，就按原来的。` | `Challenge` → withdrawal（**条件不满足**） | 原值不存在 | 撤回无效 → 按现有状态处理（新值路径） | **唯一** | K3 |
| **PC-11** | `pending_resolution`（SHOW 提案讨论中） | `你能不能一次少问点？` | **meta**（过程投诉） | 同 PC-03 | 状态不变；同轮容量调整属动作层（R4），**不改状态** | **唯一** | K2 |

### 6.3 六 intent × risk / blocking 交叉（5）

| # | 当前状态 | 原话 | intent | ② 判定 | 出口 | 唯一 | K |
|---|---|---|---|---|---|---|---|
| **PC-05** | `pending_resolution`；gap ∈ **R6**（费用） | `这个你随便吧。` | `Authorization` | T1 scope=gap；**T2 risk gate blocked** | 保持 `OPEN` + ASK（不得 assumed） | **唯一** | K2 |
| **PC-12** | `pending_resolution`；gap ∈ R6（**数据用途**） | `改成只存 30 天。` | `Revision`（有新值） | 用户**明示**新值（即完成拍板） | Revision 覆盖 → CONFIRMED(30 天)；风险门由**用户明示**满足 | **唯一** | K2 |
| **PC-13** | `pending_resolution`；`blocking = true` | `我还是不知道上限多少。` | `Unable` | blocking ∧ 无答案 | §11.2 降维 / 延后；**不得静默默认**；输出可完成部分 | **唯一** | K2 |
| **PC-14** | `pending_resolution`；gap ∈ R6 | `这部分我不想定。` | `Refused` | blocking + R6 | 保持 `OPEN`（**不得**因拒绝而 assumed）；不重复请拍板 | **唯一** | K2 |
| **PC-15** | `pending_resolution`；gap ∈ R6 | `我去问法务怎么说。` | `External` | `reason = information_source` | 保持 `OPEN`（拍板权仍属用户）；可继续其他分支 | **唯一** | K3 |

### 6.4 连续 Revision / Challenge 不受额度误伤（2）

| # | 当前状态 | 原话 | intent | ② 判定 | 出口 | 唯一 | K |
|---|---|---|---|---|---|---|---|
| **PC-06** | `pending_resolution`；已改过两次 | `再改成墨绿。`（**第三次合法 Revision**） | `Revision`（有新值） | 有新值 ∧ 非冲突 | 正常 Revision → CONFIRMED；**不得因"确认次数"拒绝处理** | **唯一** | K2 |
| **PC-16** | `pending_resolution`；已 challenge 两次 | `我还是觉得不对，你先别改。`（**第三次 Challenge**） | `Challenge` | 无新值 ∧ 原值仍在 | 继续 `pending_resolution` + 定位/索取；**不得因额度拒绝** | **唯一** | K2 |

### 6.5 External suspend → resume → 再次 challenge（2）

| # | 当前状态 | 原话 | intent | ② 判定 | 出口 | 唯一 | K |
|---|---|---|---|---|---|---|---|
| **PC-17** | `SUSPENDED(external_owner)` → 外部已回复 → 该值 CHALLENGED | `客户说的那个我还是不放心。` | `Challenge` | 外部意见非 confirmed | 保持 `pending_resolution`；**需用户本人拍板**；历史保留外部输入与 challenge | **唯一** | K3 |
| **PC-18** | 同上（外部已回复） | `那就按客户说的定吧，你决定细节。` | `Authorization`（用户转述拍板） | T2 门 passed | assumed（细节）；主值由用户明示 → CONFIRMED；**外部授权本身仍不替代用户授权** | **唯一** | K3 |

---

## 7. 三条不变量验证

| 不变量 | 内容 | 取证 |
|---|---|---|
| **A** | **`pending_resolution` 不拥有独立确认额度** | PC-06（第三次 Revision）、PC-16（第三次 Challenge）**均被正常处理**，无"额度用尽"出口；Contract 明文声明不新设计数器、不改写既有 `unable/evaded/no_signal` 归属 |
| **B** | **intent 只选择跃迁族，不绕过 risk／blocking／target／scope** | 同一 `Authorization`：PC-05（R6 → blocked 保持 OPEN）vs PC-18（passed → assumed）；同一 `Revision`：PC-12（用户明示 → CONFIRMED）；`Unable`／`Refused` 在 blocking 下均不 assumed（PC-13／PC-14） |
| **C** | **`CLOSED(assumed)` 可被后续有效反馈重新处理，但历史不可删除** | PC-01／PC-07（material 重开 → OPEN）、PC-02（confirmatory → **直接 CONFIRMED**，不经 OPEN，进 `effective_set`）、PC-08（历史保留，旧 assumed 仍可查） |

---

## 7A. R-2 封口探针 RC-01～RC-04（4/4 唯一）

| # | 输入 | 判定 | 跃迁 | `effective_set` | 唯一 | K |
|---|---|---|---|---|---|---|
| **RC-01** | `CLOSED(assumed)`（图标=线性）→ 用户确认**同一个值**（"就用线性，没意见"） | **R-2 confirmatory** | `CLOSED(assumed)` → **`CONFIRMED`**（不经 OPEN）；`confidence=confirmed`；`provenance += user_confirmed_after_assumed` | **包含该 gap** ✅（`CONFIRMED ∧ valid`） | **唯一** | K3 |
| **RC-02** | `CLOSED(assumed)`（图标=线性）→ 用户给出**不同值**（"还是用填充吧"） | **R-1 material** | `CLOSED(assumed)` → `OPEN` → **Revision 路径** → `CONFIRMED(填充)`；历史保留原 assumed | 包含该 gap（新值） | **唯一** | K3 |
| **RC-03** | `CLOSED(assumed)`；原值**已被 supersede**；用户又确认**旧值** | **R-4** | **不得直接 CONFIRMED** → 走 `revert`（`reverted_to=target_value/target_snapshot`）或按当前状态规则 | 仅在 revert 成立后进入 | **唯一** | K3 |
| **RC-04** | `CLOSED(assumed)`（图标=线性）→ 用户**只是闲聊提到**该值（"线性看着还行哈"） | **R-3 无决策意义** | **状态不变**（不升级、不重开） | 不包含该 gap | **唯一** | K1 |

**探针要点**：
- **RC-01 vs RC-04** 的差别不是措辞，而是**是否构成"明确追认"**（决策性反馈）；RC-04 只是评价性提及 → 不触发状态变化。
- **RC-02 vs RC-03** 的差别是**目标值是否已被替代**：未替代 → material 重开；已替代 → 必须走 revert，**不得**直接 CONFIRMED 一个已被 supersede 的值。

### 7B. 依赖回归（`effective_set` 等）

| 依赖面 | 重跑案例 | 结果 |
|---|---|---|
| `effective_set = CONFIRMED ∩ valid` | C-01（CONFIRMED 出候选）、I-04（确认旧值仍适用）、RC-01、PC-02 | **全部唯一**；RC-01／PC-02 后该 gap **确实进入** `effective_set` |
| `CLOSED(assumed)` | PC-01／02／07／08／09、RC-01／02／03／04、FS-04／INT-08／INT-11 | 唯一；仅 R-2 与 R-1 改变状态，R-3 不动、R-4 走 revert |
| `CLOSED(partial)` | I-07、C-14、RSC-05 | 唯一（`partial` 仍可问、**不得**作为已确认依据；本次修正**未触碰** `partial` 语义） |
| Revision / `reverts` | V3-C1（A→B→C→revert A）、L-23／L-30／REV-01／02、PC-01、RC-02、RC-03 | 唯一；**当前值唯一**不变量保持（§9.1 I-2） |
| §11 消费契约 | §11.1 裁界基数（有效下游）、§11.7 合并子问题 ⊆ `askable_set`、§6.4 重复询问口径 | 唯一；RC-01 后该 gap **离开 `askable_set`**（已 CONFIRMED），**不再被重复询问** |

---

## 8. 回归：PR-01～PR-36 与 PR-17

| 项 | 结果 |
|---|---|
| **PR-01～PR-36 在新 Contract 下** | **36/36 保持**（无出口改变；Contract 仅把 Discovery 已证明的出口**形式化**，未新增/删除任何出口） |
| **PR-17（原 K5）** | **K5 消失** → 由 **R-2 confirmatory**（**直接 `CONFIRMED`，不经 OPEN**）唯一裁定 |
| **新增 PC-01～PC-18** | **18/18 唯一** |
| **新增 RC-01～RC-04** | **4/4 唯一** |
| **K4** | **0** |
| **K5** | **0** |

**最终 Release Gate（分栏，不合并成一个数字）**

```
Base raw regression      201/201      # B0 34 + B1 27 + B2 80 + B3 60
Pending Contract          18/18       # PC-01～PC-18
R-2 confirmation probes    4/4        # RC-01～RC-04
V3 canaries               PASS        # V3-C1/C2/C3/C4 + UA-01～04
K4                           0
K5                           0
```

> 分栏理由（用户裁决）：未来出问题时能直接定位**是哪一层坏了**，而不混成一个大数字。

**门槛核对**：PR 36/36 ✅｜PC 18/18 ✅｜RC 4/4 ✅｜PR-17 K5 消失 ✅（**其归因已由 N10 更正**）｜K4 = 0 ✅｜K5 = 0（**N10 前口径；N10 后重确认见 §8.1**）｜不变量 A／B／C ✅。

### 8.1 N10 更正与重确认（2026-10-03）

| 项 | 结果 |
|---|---|
| PR-17 分类 | **Authorization**（**不是** R-2；该句不确认具体值，不产生 `CONFIRMED`） |
| R-2 定义 | **未修改**（仅更正分类） |
| 依赖复核 | `§3.4`（已加更正框）／`§8` PR-17 行（本表）／Interface §10.5（已更正）／`tests/acceptance.md`（K5 状态改为 REOPENED→重确认） |
| 旧 `K5 = 0` | **不作为最终证据**（其归因基于过宽读法）；本轮按项目定义**重跑后重确认** |
| 重确认结果 | **K4 = 0；K5 = 0**（新归因：分类唯一 → 无第二合法读法；**不再依赖 R-2 的扩大解释**） |

---

## 9. 边界与状态

| 项 | 状态 |
|---|---|
| `SKILL.md`／§6.3／§11／Interface v2／v3 冻结正文／V0.3 | **未修改** |
| `effective_set = CONFIRMED ∩ valid`（v1 冻结谓词） | **未修改**（R-2 改为直接 `CONFIRMED`，**自然满足**该谓词） |
| 新增 Type／Action／Gap 生命周期状态 | **无** |
| 新增字段 | **无**（R-2 只用既有 `status`／`confidence`／`provenance`／`history`；重进入口是**规则**，不是状态） |
| 原则（本次确立） | **`status` 决定生命周期；`confidence`／`provenance` 只描述"这个状态为什么成立"**——不允许 `confidence` 反向改写生命周期意义 |
| 本 Contract 状态 | **✅ 已并入接口正文（§10）并冻结（2026-10-02）** |
| `deprioritized` | 继续延期至 Priority Layer |

**本轮的抽象落点**：

> 不是"AI 最多还能确认几次"，而是"**当前这次反馈意味着需求状态应该发生什么变化**"。
