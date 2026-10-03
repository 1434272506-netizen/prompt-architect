# V0.5 · Candidate Abstraction Falsification #1

> **Target**：**`Atomic Visibility Obligation`**（V0.5 第一个有实证支持的新抽象）
> **目的**：**尝试证伪，不是继续确认。**
> **纪律**：V0.4 frozen；**不写字段、不写状态、不写合同**；不得为通过测试临时补概念。
> **淘汰标准已在测试前写死**（见 §1，先写死再跑，避免事后找补）。

---

## 1. 淘汰标准（测试前固定）

### A′ SURVIVES
```
所有 AF case 都能保持同一 Atomic identity 原则解释
允许：clarification · trigger composition · presentation coalescing · batch operation
不需要：隐藏的 set lifecycle · 大量 case-specific exception · 偷其他层 ownership
```

### A′ REVISE
```
atomic unit 仍成立，但「独立 delivery intent」不是可靠 identity 判据
（例如证据支持 independent lifecycle intent）
⇒ 抽象保留，判定原则修订（不是失败）
```

### A′ REJECT
```
出现稳定问题族，使得：
  多个所谓 atomic obligations 必须共享【不可分割生命周期】
  或
  一个所谓 atomic obligation 必须长期拥有【多个彼此独立生命周期】
且不能靠 presentation / trigger composition / batch operation 解释掉
```

### 新增指标 M8 · Counterfactual Independence
```
对候选的两条 obligation：
  只改变其中一条的 trigger / 取消 / generation / satisfaction
  → 另一条能否保持语义不变？

可以     ⇒ 支持二者 identity 独立
必然改变 ⇒ 怀疑它们本不该被拆成两条 atomic obligation
```

---

## 2. 逐例对抗（AF-01～AF-12）

### AF-01 · 合并展示后用户认为漏了一件
- **攻击点**：`presentation coalescing` 是否会**吞掉用户真实感知**（一条消息是否同时 discharge A+B）。
- **A′ 逐问**：Q1＝2 obligations（budget／launch）｜Q2 target 明确｜Q3 各自 trigger｜**Q4 一次 delivery 消耗什么？→ 这里打中**：合并消息若按"出现在一次交付事件里"算，两条同时 discharge。
- **M8**：变更 A（取消 budget）→ B 不受影响 ⇒ **identity 独立 ✓**（问题不在 identity）
- **判定**：**identity 层存活**；暴露一个新区分：**`obligation identity` ≠ `satisfaction criterion`**。
  > V0.4 的 `notify → discharged`（§7）在**聚合交付**下过粗：用户不认为"顺带提了一句"构成正式提醒。
  > ⇒ 这是**判定契约/语义**问题（delivery 对某条 obligation 是否成立），**不是新的 identity 单位**。
- **结论**：**PASS（连带发现 S-1：delivery 判定 ≠ identity）**

### AF-02 · 一条 obligation 被拆成两条消息
- **攻击点**：`message count` 是否会污染 identity（2 messages 是否变成 2 obligations）。
- **A′**：obligation 数＝独立 lifecycle 单位数；**消息数不参与 identity** ⇒ 仍 1 条。
- **M8**：无第二单位可比 ⇒ n/a
- **结论**：**PASS**（正向强化：A′ 显式把 message 与 identity 解耦）

### AF-03 · 两个义务只能一起取消
- **输入**：`这两个提醒一起取消；如果只能取消一个，那就都别动。`
- **攻击点**：是否意味着真正 identity 应是 set？
- **A′**：2 obligations ＋ **batch operation**（一次操作作用于两条）；"只能取消一个就别动"是**用户对批量操作的条件偏好**，不是共享生命周期。
- **M8**：默认情况下变更 A → B 不变 ✓；**用户偏好**可在**操作层**引入条件耦合（≠ identity 耦合）
- **结论**：**PASS**（**批量操作 ≠ 共享 identity**——这正是 REJECT 条件明确排除的情形）

### AF-04 · 部分取消
- **输入**：`预算不用提醒了，上线时间那个保留。`
- **A′**：cancel A；B 保持 active ⇒ 天然简单。
- **M8**：变更 A → B 不变 ✓
- **结论**：**PASS**（正向）

### AF-05 · generation 部分替换
- **输入**：A→Gap X gen1、B→Gap Y gen1；仅 X 发生 Revision。
- **A′**：A 终止/重评；**B 不受影响**；**无需任何 group exception**。
- **M8**：变更 A 的 generation → B 语义不变 ✓
- **对照**：此例正是 Model B′ 需要 member identity 的地方（B-Q2）⇒ A′ 优势再次确认。
- **结论**：**PASS**（强正向）

### AF-06 · 一个 intent 明确要求两阶段提醒
- **输入**：`上线前提醒我一下，临上线的时候再重点提醒一次。` → 后续：`第一次保留，临上线那次不用了。`
- **问题**：1 delivery intent with 2 opportunities，还是 2 independently satisfiable intents？
- **A′**：后续句**自然成立**（可只取消第二次而保留第一次）⇒ 存在**独立生命周期** ⇒ **2 obligations**。
- **M8**：变更"临上线那次" → "上线前那次"不受影响 ✓
- **结论**：**PASS**；并给出**判别试验**：**"能否被独立取消"** 是决定性判据（比"数了几次"更准）。

### AF-07 · 两次提醒但不可独立取消　⚠ **打中判据**
- **输入**：`这是一整套提醒：周一提醒一次，周五再提醒一次，不能拆开。`
- **攻击点**：用户**明确把它定义为一个不可拆整体**；若 A′ 仍强制拆成两个独立 lifecycle units，即**过度原子化**。
- **A′（按当前"delivery intent 计数"判据）**：数到 2 次交付 ⇒ 判 **2 obligations** ⇒ **与用户明确表达的不可拆性冲突** ⇒ ❌ **判据失败**。
- **A′（按修订判据：独立 lifecycle）**：两段交付**不能独立取消/满足** ⇒ **最小可独立生命周期单位＝整体** ⇒ **1 obligation**（其 trigger structure 含两个交付机会）⇒ 与用户表达**一致** ✓。
- **M8**：变更"周一那次"→ 整体语义改变（用户说"不能拆开"）⇒ **不独立** ⇒ **1 单位** ✓
- **判定**：**抽象单位存活；判据被证伪** ⇒ 命中**预先写死的 A′ REVISE 条件**。
- **连带**：A′ 必须允许**一条 obligation 拥有多次 delivery**（其"原子"指**identity 不可再分**，不指"只交付一次"）。

### AF-08 · 模糊 cardinality
- **输入**：`有空多提醒我一下这个事。`
- **攻击点**：A′ 是否会猜 2／3／unbounded。
- **A′**：**cardinality cannot be determined → 最小澄清**。（抽象不要求每句话无问询解析。）
- **M8**：无第二单位 ⇒ n/a
- **结论**：**PASS**（R-1 的代价被接受为"澄清"，而不是硬猜）

### AF-09 · 用户看见了，但明确说"这不算提醒"
- **攻击点**：`delivery happened ≠ user considers obligation satisfied`。
- **A′**：identity 层不受影响；受攻击的是**满足判据**（同 AF-01 的 S-1）。
- **M8**：变更 A 的 satisfaction → B 不变 ✓
- **判定**：**identity 层存活**；**必须区分**：
  ```
  obligation identity
  ≠
  satisfaction criterion
  ```
- **结论**：**PASS（连带发现 S-1 强化）**；同时说明 V0.4 的 `notify → discharged` 属**过粗规则**，V0.5 若采用 A′ 需**改写/更精确化**该判据（属**判定契约**，非新 identity 单位）。

### AF-10 · 用户处理事项但仍要求提醒
- **输入**：`事情现在已经解决了，但下周还是提醒我回顾一下。`
- **A′**：**旧 obligation 终止**（target 已完成）＋ **新 delivery intent** ⇒ **新 obligation**（target 不同：回顾 ≠ 处理）。
- **M8**：旧单位结束后新单位独立 ✓（且"同一话题"不影响 identity）
- **结论**：**PASS**（并显式区分 `identity ≠ target`）

### AF-11 · fallback trigger ＋ trigger 修改
- **输入**：`客户回复就提醒；如果没回复，周五提醒。` → `周五那个备用提醒取消，但客户回复后还是提醒。`
- **A′**：**trigger composition 修改**（移除一个分支）⇒ **仍 1 obligation**；无需"取消一条义务、保留另一条"。
- **M8**：变更 trigger 分支 → obligation 语义保持（仍是"客户回复后提醒"）✓ ⇒ 1 单位
- **结论**：**PASS**（**复合 trigger 可部分修改**，不牵动 identity）
- **附带**：此例**反向检验**了 C2-14 的单义务解释——**C2-14 的单义务读法成立**（可被分支级修改），未被推翻。

### AF-12 · 两 trigger 后续可分别改变 delivery 内容　⚠ **最强 identity 测试**
- **输入**：`客户回复时提醒我看报价；周五没回复的话提醒我去催客户。`
- **攻击点**：表面像 fallback，但两分支对应**不同的用户期望内容/满足条件**。
- **A′**：
  ```
  分支 1 满足＝"我看了报价"；分支 2 满足＝"我催了客户" ⇒ 满足条件不同
  且可独立取消（"报价我看了，催客户那条保留"） ⇒ 独立生命周期
  ⇒ 2 obligations
  ```
- **M8**：变更分支 1（已看报价）→ 分支 2 不受影响 ✓ ⇒ **2 单位**
- **结论**：**PASS**，且**给出真正的边界**：
  ```
  trigger difference                （AF-11）→ 不改变 identity（1 条）
  satisfaction difference           （AF-12）→ 改变 identity（2 条）
  ```
  ⇒ **判据从"trigger 差异"升级为"满足/生命周期差异"**。

---

## 3. M8 汇总（Counterfactual Independence）

| 案例 | 反事实操作 | 另一单位是否保持 | 结论 | 与 A′ 判据一致？ |
|---|---|---|---|---|
| AF-01 | 取消 budget | launch 不变 | 独立 | ✓ |
| AF-03 | 取消 budget（默认） | launch 不变 | 独立（**操作层**可条件耦合） | ✓ |
| AF-04 | 取消 budget | launch 不变 | 独立 | ✓ |
| AF-05 | 改 Gap X generation | B 不变 | 独立 | ✓ |
| AF-06 | 取消"临上线那次" | 第一次不变 | 独立 | ✓（2 条） |
| **AF-07** | 取消"周一那次" | **整体语义改变**（"不能拆开"） | **不独立** | ✓（1 条）— **但"delivery intent 计数"判据在此失败** |
| AF-11 | 取消备用分支 | 义务语义不变 | 不独立 | ✓（1 条） |
| AF-12 | 分支 1 已满足 | 分支 2 不变 | 独立 | ✓（2 条） |

**M8 判定**：**在全部 12 例中与"独立生命周期"判据一致**，且在 **AF-07 处正确否证了"delivery intent 计数"**。⇒ M8 可用作 identity 判据的**操作性检验**（仍属**假说**，非合同）。

---

## 4. 总判定：**A′ REVISE**

| 项 | 结果 |
|---|---|
| **原子单位是否存活** | **✅ 存活**（12/12 无需隐藏 set lifecycle；batch／presentation／trigger composition 均足够解释） |
| **判据是否被证伪** | **✅ 被证伪**：`独立 delivery intent 计数` 在 **AF-07** 上给出与用户明确表达**相反**的基数 |
| **是否满足 REJECT 条件** | **❌ 未满足**（没有任何案例迫使多个单位共享**不可分割**生命周期，或单个单位长期拥有**彼此独立**的生命周期） |
| **⇒ 预写死判定** | **A′ REVISE**（抽象保留，判定原则修订） |

**修订后的候选定义（**仍非合同、无字段**）**

```
Atomic Visibility Obligation（revised）

最小 identity 单位 = 一条【可独立满足 / 取消 / 失效 / 被 generation 终止】
的 visibility obligation

identity 判据（假说）：
  独立【lifecycle】intent
  —— 而非独立 delivery intent 计数、trigger 计数、消息计数

推论：
  · 一条 obligation 可含复合 trigger（AF-11）
  · 一条 obligation 可产生多次 delivery（AF-07）
  · 一次 delivery 可能同时兑现多条 obligation（AF-01／C2-11）
```

---

## 5. 连带发现（不得省略）

| # | 发现 | 归属 | 是否新 identity 单位 |
|---|---|---|---|
| **S-1** | `obligation identity` **≠** `satisfaction criterion`（AF-01／AF-09：聚合交付或"顺带一提"不构成满足） | **判定契约** | **否** |
| **S-2** | 一条 obligation **可产出多次 delivery**（AF-07） | 修订 A′ 的定义域 | **否** |
| **S-3** | `identity` **≠** `target`（AF-10：同一话题可结束旧单位、新建单位） | 语义澄清 | **否** |
| **S-4** | 批量操作可在**操作层**引入条件耦合，但不动 identity（AF-03） | 操作层 | **否** |
| **S-5** | **V0.4 的 `notify → discharged` 过粗**：若 V0.5 采用 A′-revised，则该判据需**更精确化** | **⚠ 会触及 V0.4 冻结条款（Notification §7）** | **否（但需 supersede 处理）** |

> **S-5 必须显式上报**：V0.4 是 frozen，**本阶段不改它**；但若将来 V0.5 采纳 A′-revised，则 Notification Contract §7 的"`notify → discharged`"与"一条 commitment 最多一次主动通知"需要**按历史治理条款**（后合同权威 ＋ superseded 标注）处理，而**不是**静默改写。**留给 V0.5 的合同阶段裁定**。

---

## 6. 本阶段边界

- ❌ 未写字段／状态／合同；
- ✅ 抽象**命名与定义修订**仅停留在 candidate 层；
- 族 2／族 3／族 4 **未参与**本轮（按用户指示）；
- V0.4 **frozen 不变**（见 §7 校验）。
