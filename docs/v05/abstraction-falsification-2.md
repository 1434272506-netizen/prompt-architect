# V0.5 · Candidate Abstraction Falsification #2

> **Target**：**revised A′ 的 identity 判据** —— "独立 lifecycle intent 是否足以决定 obligation identity？"
> **不打**：`Atomic Visibility Obligation` 本身的存在价值（Falsification #1 已确认原子单位存活）
> **纪律**：V0.4 frozen；**不写字段／状态／合同**；不得为通过测试临时补概念；**S-1 只记录证据，不设计 satisfaction contract**。
> **判决标准已预先写死**（§1）。

---

## 1. 预先写死的判决条件

### Revised criterion SURVIVES
```
obligation identity 由【内在的 lifecycle independence】决定，
而不是 trigger / message / target 数量，也不是外部 batch / operation / dependency 规则。
尤其需同时得到：
  AF2-03/04 → 2 obligations（同满足内容，但生命周期独立）
  AF2-05/06 → 1 obligation （不同满足内容，但内在生命周期不可拆）
  AF2-09    → 仍 2 obligations（尽管操作政策把它们联动）
```

### REVISE again
```
若发现还需补一个限定（例如必须说「intrinsic」，
而不能用一般的 counterfactual independence）
```

### REJECT
```
出现稳定案例族：无论怎样区分 trigger / presentation / operation policy，
都无法决定最小生命周期 identity；或必须引入隐藏 set 才能解释
```

---

## 2. 四象限框架（S ＝ 满足语义；L ＝ 生命周期可独立操作）

|  | **L 不可独立** | **L 可独立** |
|---|---|---|
| **S 相同** | **Q1**（AF2-01／02） | **Q2**（AF2-03／04） |
| **S 不同** | **Q3**（AF2-05／06） | **Q4**（AF2-07／08） |

（Q1／Q4 在 Falsification #1 已部分见过；本轮专门补 **Q2／Q3**。）

---

## 3. 逐例对抗（AF2-01～AF2-10）

### Q1 · 满足相同 ＋ 生命周期不可独立

#### AF2-01 · `上线这件事周一提醒我一次、周五再提醒一次，这是一个完整提醒计划，不能单独取消其中一次。`
- **攻击点**：2 deliveries ＋ 同满足目标 ＋ 用户明确不可拆 ⇒ revised A′ 会不会仍按"次数"拆成 2？
- **A′（lifecycle 判据）**：最小**可独立**满足/取消单位＝**整体** ⇒ **1 obligation ＋ multiple delivery schedule** ✓
- **M8**：取消"周一那次" → 整体语义被破坏（用户不允许）⇒ **不独立** ⇒ 1 单位 ✓
- **判定**：**PASS**（若拆 2 即失败——未发生）

#### AF2-02 · `分早晚两次提醒我吃药，这两次是一整套；要取消就一起取消。`
- **注意**：**不使用领域知识**，只看用户表达（"一整套／一起取消"）。
- **A′**：2 delivery events，**1 identity** ✓
- **M8**：取消早间 → 整体需一起取消 ⇒ 不独立 ⇒ 1 单位 ✓
- **判定**：**PASS** ⇒ **`2 delivery events ≠ 2 obligation identities`** 再次确认

### Q2 · 满足相同 ＋ **生命周期可独立**（本轮最重要的新攻击）

#### AF2-03 · `上线这件事周一提醒一次、周五再提醒一次。周一那次以后可以单独取消，周五的不受影响。`
- **攻击点**：target／满足内容／Gap **全部相同**，仅**取消能力**不同。
- **A′（lifecycle 判据）**：可独立取消 ⇒ **2 obligations** ✓
- **M8**：取消 A → B 不受影响 ⇒ 独立 ✓
- **判定**：**PASS（2 条）**
- **⇒ 直接证明**：**identity 不能由 target／满足措辞决定**（同 target 同满足，仍可 2 条）

#### AF2-04 · `预算这件事月底提醒我两次。` → 随后：`第一次提醒如果取消，第二次照常。`
- **攻击点**：初始表达**模糊**（"提醒两次"未说是否可拆）；后续信息是否**揭示已有 cardinality**，而不是机械新建。
- **A′**：后续句揭示两次是**内在可独立**的（取消第一次不影响第二次）⇒ **cardinality = 2**，且这是**揭示/细化（reveal）**，**不是**"再新建一条 obligation"。
- **M8**：取消第一次 → 第二次照常 ⇒ 独立 ✓
- **判定**：**PASS（2 条）**
- **连带发现 S-6**：存在 **cardinality reveal / refinement**（后续话语**揭示**既有独立性），需与"新建 obligation"区分——**属判定契约候选，非新 identity 单位**。

### Q3 · **满足不同** ＋ 生命周期不可独立（对 AF-12 的反向攻击）

#### AF2-05 · `客户回复后提醒我看报价；如果到周五还没回复就提醒我催客户。但这是同一个完整的跟进承诺，只要其中一个分支触发，另一边就作废，不能分别保留。`
- **攻击点**：满足内容不同（review quote vs chase client），但用户明确 **mutually exclusive ＋ single lifecycle**。
- **若按"满足差异 → 拆 2"**：会得出 **2 obligations ＋ coupling rule** ⇒ 与用户表达的"一边触发另一边作废"需要额外耦合规则 ⇒ 引入隐藏复杂度。
- **A′（lifecycle 判据优先）**：**内在不可独立** ⇒ **1 obligation，携带 branch-specific satisfaction semantics** ✓
- **M8**：触发/满足任一支 ⇒ 另一支作废 ⇒ 不独立 ⇒ 1 单位 ✓
- **判定**：**PASS（1 条）**
- **⇒ 修正 Falsification #1 的那句话**：
  ```
  旧表述：满足/生命周期差异才改 identity
  精炼为：满足差异是 identity 的【证据】，但不是【决定条件】；
          intrinsic lifecycle independence 才是决定性判据
  ```

#### AF2-06 · `项目通过就提醒我发庆祝邮件；没通过就提醒我写复盘。两者只会发生一个，而且我只能整体取消这个结果提醒。`
- **A′**：不同满足内容 ＋ 互斥 trigger ＋ **不可独立取消** ⇒ **1 obligation（互斥分支）** ✓
- **M8**：不独立 ⇒ 1 单位 ✓
- **判定**：**PASS（1 条）**
- **⇒ AF-12 的旧结论被精炼（非推翻）**：满足差异在两例中都出现，但**只有当生命周期可独立时才分裂**。

### Q4 · 满足不同 ＋ 生命周期可独立（强正例）

#### AF2-07 · `客户回复后提醒我看报价；周五也提醒我催客户。即使客户已经回复，我周五那条催办提醒仍然保留，两个可以分别取消。`
- **A′**：满足不同 ＋ 可独立 ⇒ **2 obligations** ✓
- **M8**：A 已满足/取消 → B 不受影响 ⇒ 独立 ✓
- **判定**：**PASS（2 条）**

#### AF2-08 · `上线前提醒我做备份；上线后再提醒我做复盘。任何一个都可以单独取消。`
- **A′**：满足不同（备份／复盘）＋ 可独立 ⇒ **2 obligations** ✓
- **M8**：独立 ✓
- **判定**：**PASS（2 条）**

### 专门攻击 M8 本身

#### AF2-09 · `预算提醒和上线提醒都保留。但以后如果取消其中一个，就自动把另一个也取消。`
- **攻击点**：行为上 `cancel A → cancel B`；**M8 的朴素形式会误判为"共享 identity"**。
- **正确解读**：这是 **operation policy couples A/B**（外部操作规则导致的联动），**不是** share identity。
- **A′**：**仍 2 obligations** ✓（联动属操作层，S-4 升级为**必须显式排除的干扰项**）
- **判定**：**PASS（2 条）**
- **⇒ M8 被修订（本轮第二个被证伪的"仪器"）**：
  ```
  M8（naive，已废弃）：
      任何 change(A) 导致 change(B) ⇒ same identity        ✗ 会把外部耦合误判为 identity

  M8′（修订，本轮采用）：
      在【排除外部批量操作／依赖／用户策略】的前提下，
      change(A) 是否必然改变 B 的语义？
        是 ⇒ 内在耦合 ⇒ 可能同一 identity
        否 ⇒ intrinsic independence ⇒ 支持独立 identity
  ```

#### AF2-10 · `先提醒我确认预算；预算确认后再提醒上线。如果预算提醒取消，上线提醒继续保留，只是等条件满足。`
- **攻击点**：存在 **dependency**（B 的条件依赖 A 的完成），dependency 是否等于共享 identity？
- **A′**：B 的 trigger 引用 A 的结果，但 **A 被取消不改变 B 的语义**（只是等条件满足）⇒ **2 obligations ＋ dependency edge** ✓
- **M8′**：在排除依赖策略后，变更 A 不必然改变 B 的**语义** ✓
- **判定**：**PASS（2 条）** ⇒ **`dependency ≠ shared identity`**

---

## 4. 四象限结论表（本轮核心产物）

| 象限 | 案例 | **S** | **L** | 结果 | 说明 |
|---|---|---|---|---|---|
| **Q1** | AF2-01／02 | 相同 | **不可独立** | **1 obligation**（多 delivery schedule） | 次数≠identity |
| **Q2** | AF2-03／04 | **相同** | **可独立** | **2 obligations** | **identity 不由 target/满足决定** |
| **Q3** | AF2-05／06 | **不同** | **不可独立** | **1 obligation**（分支式满足语义） | **满足差异不是决定条件** |
| **Q4** | AF2-07／08 | 不同 | 可独立 | **2 obligations** | 与 AF-12 一致 |

```
⇒ identity 完全沿【L 轴】分布，与【S 轴】无关
⇒ obligation identity = intrinsic lifecycle independence
```

---

## 5. 总判定：**REVISE again**（并首次得到稳定 identity law 的实质）

| 项 | 结果 |
|---|---|
| **三条核心条件是否同时成立** | **✅ 全部成立**：① 同满足＋可独立 → **split**（AF2-03/04）② 不同满足＋内在不可拆 → **不 split**（AF2-05/06）③ 外部操作耦合 → **不 merge identity**（AF2-09） |
| **是否需补限定** | **✅ 需要**：M8 的朴素形式被 AF2-09 证伪 ⇒ 判据必须写 **intrinsic** |
| **REJECT 条件** | **未触发**（无无法判定 identity 的稳定族；无需隐藏 set） |
| **⇒ 预写死判定** | **REVISE again** |

**修订后的候选定义（**仍是 candidate，无字段、无契约**）**

```
Atomic Visibility Obligation（revised #2）

identity 判据：
  intrinsic lifecycle independence
  —— 在【不考虑外部批量操作／依赖／用户策略】的前提下，
     一条义务是否可被独立【满足 / 取消 / 失效 / generation 终止】

即：intrinsically independently lifecycle-addressable obligation

推论（与四象限一致）：
  · trigger / message / target 的差异  → 不改变 identity
  · 满足内容的差异                    → 是 identity 的【证据】，但非【决定条件】
  · 外部操作/依赖耦合                 → 不改变 identity
  · 一条 obligation 可含多个 delivery / 多个互斥分支
```

**M8′（修订后的检验仪器）** 已在 AF2-09 后被采用，并在 AF2-04／05／09／10 上给出正确判别。

---

## 6. 连带发现（登记，不设计）

| # | 发现 | 归属 | 是否新 identity 单位 |
|---|---|---|---|
| **S-6** | **cardinality reveal / refinement**：后续话语可**揭示**既有独立性，而非新建义务（AF2-04） | **判定契约候选** | **否** |
| **S-7** | 满足差异是 identity 的**证据**而非**决定条件**（AF2-05/06 vs 07/08） | 精炼 Falsification #1 的结论 | **否** |
| **S-1（强化，仍不设计）** | `identity ≠ satisfaction criterion`；"我没觉得你真的提醒到我"仅作 **证据** 记录 | 留给后续 **独立 Discovery family** | **否** |
| **S-4（升级）** | 操作层耦合**必须**在判据中被显式排除（AF2-09） | 已并入 M8′ | **否** |
| **S-5（维持）** | V0.4 `notify → discharged`／"最多一次主动通知" 与 revised A′ 的冲突属 **版本演进**：V0.5 采纳时为 **superseding contract**，**不是 V0.4 defect** | 治理（历史条款） | **否** |

---

## 7. 边界

- ❌ 未写字段／状态／合同；未设计 satisfaction contract（按用户指示，S-1 仅记录证据）；
- ✅ 判据命名与仪器修订均停留在 **candidate** 层；
- 族 2／族 3／族 4 **未参与**；族 4 维持 `THRESHOLD PASS · ELIGIBLE · NOT STARTED`；
- V0.4 **frozen 不变**。
