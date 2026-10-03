# V0.5 · Candidate Abstraction Convergence #1

> **范围**：**仅族 1（Obligation Identity / Cardinality）**
> **阶段**：候选抽象竞争（**不写合同、不设计 schema、不新增状态**）
> **纪律**：V0.4 frozen；模型**不得**为通过测试而临时补概念；回答不了＝记失败。

---

## 0. 先自查出的重复计数（诚实修正）

> **`C2-14` 与 `C2-29` 是同一个场景**（"客户回复后提醒我；周五如果还没回复也提醒我"）——第二批用于 identity，第三批用于 fallback，**我重复计了一次**。

```
族 1 案例：原先记 11 → 去重后【10 个独立案例】
  C2-05  同 Gap 多承诺
  C2-11  同 Gap 两承诺同时到期
  C2-13  重复表达
  C2-14 ≡ C2-29  fallback（合并为一例，两个分析角度）
  C2-15  一句多 Gap
  C2-16  trigger 修订
  C2-30  OR ＋ 显式一次
  C2-31  显式两次
  C2-32  重复强调
  C2-36  OR ＋ one-shot
```

**门槛复核**：10 ≥ 5，**门槛仍然全过**（结论 1 不受影响）。

---

## 1. 三个模型（按用户裁定修正后的定义）

### Model 0 · No-new-abstraction baseline
```
继续使用 V0.4 visibility_commitment
只允许【判定契约澄清】（例如 condition 取值空间）
不改变 identity / cardinality 抽象
```

### Model A′ · Atomic Obligation
```
最小 identity 单位 = 一条可【独立满足 / 取消 / 失效】的 visibility obligation

表达次数   ≠ obligation 数量
trigger 数 ≠ obligation 数量
消息条数   ≠ obligation 数量

cardinality 的判据（候选解释，非规则）：
  用户表达了几个【独立的 delivery intent】
```

### Model B′ · Obligation Set
```
一个用户可见承诺形成一个 obligation-set；
set 内允许多 trigger / 多 delivery opportunity；
set 内部决定 first-of / all-of / partial fulfillment
```

---

## 2. 五个必答问题（每模型 × 每案例）

```
Q1 有几个 obligation？
Q2 每个 obligation 的 target 是什么？
Q3 trigger 与 obligation 是什么关系？
Q4 一次 delivery 后什么被消耗？
Q5 剩余什么继续 active？
```

**三模型的统一回答（能答则答，不能答则记失败）**

| 问题 | **Model 0** | **Model A′** | **Model B′** |
|---|---|---|---|
| **Q1 几个 obligation？** | **无法答**（无 cardinality 判据；1 或 N 均合法） | **答**：＝独立 delivery intent 数 | **答**：1 个 set（成员数仍待判 ⇒ 部分退回 Q1） |
| **Q2 target？** | 单 gap（一句多 Gap 时需 fan-out，规则缺失） | 每个 obligation 指向一个 target（gap／gap 组） | set 的 target 可为多 gap |
| **Q3 trigger 与 obligation 关系？** | 单值 trigger ↔ 单 obligation | **N:M**（复合 trigger 可服务 1 条义务） | set 内多 opportunity |
| **Q4 一次 delivery 消耗什么？** | 一条 commitment | **一条 obligation（不一定是整组）** | **set 还是 member？→ 必须再引入 member identity** |
| **Q5 剩余 active？** | 其余 commitment（若存在） | 其余 obligation（含"同题不同 intent"者） | 其余 member ← **即 member 才是生命周期单位** |

---

## 3. 逐例 replay（10 个独立案例）

**图例**：`PASS` ＝ 唯一且正确；`PASS*` ＝ 通过但需引入额外概念；`FAIL` ＝ 无法唯一/错误；`FAIL(dup)` ＝ 因重复计数不计入分母

| 案例 | 输入要点 | **Model 0** | **Model A′** | **Model B′** |
|---|---|---|---|---|
| **C2-13** | 重复表达（无新次数语义） | **FAIL** 1 条 / 2 条无判据 | **PASS** 1 intent → 1 obligation（重复仅强化） | **PASS\*** 需同一套 intent 判定才知道 set 有几个 member |
| **C2-14 ≡ C2-29** | fallback（reply ∨ (Friday ∧ ¬reply)） | **FAIL** 单值 trigger 装不下；若拆两条 ⇒ **周五仍会误触发** | **PASS** 1 intent ＋ **复合 trigger（含否定守卫）** → 1 次兑现 | **PASS** set 内 opportunity ＋ 守卫 |
| **C2-15** | 一句多 Gap | **FAIL** fan-out 规则缺失；N 条 ⇒ 可能 N 次提醒 | **PASS** 2 intent → **2 obligations**；**presentation 可合并为 1 条消息** | **PASS\*** set 跨 2 Gap ⇒ 触发 B-Q2（generation 部分失效）⇒ 需 member identity |
| **C2-16** | trigger 修订 | **PASS**（行为唯一：替换后 1 次） | **PASS** 同义务、trigger 替换 | **PASS** set 内 opportunity 替换 |
| **C2-05** | 同 Gap 多承诺 | **FAIL** 2 条 / 1 条无判据 | **PASS** 2 intent → 2 obligations（同 target） | **PASS\*** 需 partial fulfillment ⇒ member identity |
| **C2-11** | 同 Gap 两承诺同时到期 | **FAIL** 无跨 commitment 规则 | **PASS** 2 obligations 同时到期 → **可合并 1 条消息兑现 2 条** | **PASS\*** 同上，需 member identity |
| **C2-30** | OR ＋ 显式一次 | **FAIL** 单值 trigger | **PASS** 1 intent ＋ 复合 trigger ＋ 一次 | **PASS** |
| **C2-31** | 显式两次独立交付 | **FAIL** §7"每条最多一次"＋无"一句多义务"规则 ⇒ **可能吞掉第二次** | **PASS** 2 intent → 2 obligations | **PASS\*** 1 set 2 opportunities；但**若第一次兑现即 discharge 整组 ⇒ 吞第二次**，故仍需 partial fulfillment ＝ member |
| **C2-32** | 重复强调 | **FAIL** 膨胀风险（2 条 → 2 次） | **PASS** 1 intent → 1 obligation | **PASS\*** 仍需 intent 判定 |
| **C2-36** | OR ＋ one-shot | **FAIL** 单值 trigger | **PASS** 1 intent ＋ 复合 trigger | **PASS** |

**计分（10 例）**

| 模型 | PASS | PASS\* | FAIL |
|---|---|---|---|
| **Model 0** | 1（C2-16） | 0 | **9** |
| **Model A′** | **10** | 0 | 0 |
| **Model B′** | 5 | **5** | 0 |

---

## 4. M1–M7 指标

| 指标 | Model 0 | **Model A′** | **Model B′** |
|---|---|---|---|
| **M1 Coverage** | **1/10** | **10/10** | 10/10（其中 5 例需 member identity） |
| **M2 Exceptions（特判数）** | **≥6**（复合触发 5 ＋ 基数 3 ＋ fan-out 1，重叠后仍 ≥6） | **0** | **≥1 结构性**：需引入 member identity（partial discharge / generation）＋ 仍需同一套 intent 判定 |
| **M3 Ownership（硬否决）** | PASS（不越权） | **PASS** | PASS |
| **M4 Over-notification** | **✗ 1 例确证**（C2-14：客户已回复后周五仍触发）＋ C2-32 膨胀风险 | **✓ 无** | ✓ 无（若 set 不重复触发） |
| **M5 Under-delivery** | **✗ 1 例**（C2-31 可能被压成一次） | **✓ 无** | ⚠ 有风险（first-discharge 吞第二次） |
| **M6 C2-29 fallback** | **✗** | **✓** | ✓ |
| **M7 Lifecycle coherence** | **✗** identity 单位（commitment 的基数）**本身不确定** | **✓** identity ＝"可独立满足/取消/失效"的最小单位，与生命周期边界**一致** | **✗（或冗余）**：partial fulfillment / generation 部分失效**迫使** set 内部出现 member identity ⇒ **有效生命周期单位＝member＝Atomic Obligation**，set 只是外层包装 |

---

## 5. 结论

### 5.1 Model 0 被证据淘汰 ⇒ **V0.5 确实需要新抽象**

```
M1 1/10｜M2 ≥6 特判｜M4 1 例确证 over-notification｜M5 1 例 under-delivery
⇒ Model 0（只加判定契约澄清）无法在【不改变 identity/cardinality 抽象】的前提下解释族 1
⇒ 这是"需要新抽象"的**实证**，而不是偏好
```

> 注意：Model 0 的失败**不是**"缺字段"，而是**缺 identity 单位**——V0.4 的 `visibility_commitment` 是一个**没有确定基数**的容器。

### 5.2 Model B′ 不构成独立优势（把问题藏进 set 内部）

```
B-Q1 partial discharge      → 迫使 set 内出现可独立生命周期单元 ⇒ 即 Atomic Obligation
B-Q2 generation replacement → set 跨 gap 部分失效 ⇒ 再次需要 member identity
B-Q3 C2-32 重复强调          → set 仍需同一套 cardinality 判定
⇒ B′ 的有效生命周期单位**收敛到 A′**；外加一层 set 只增加 partial/all-of 语义负担
```

### 5.3 Model A′ 胜出（10/10、0 例外、M3–M7 全过）

关键区分（第三批逼出、本轮回放确认）：

```
Obligation identity   ≠  Trigger structure   ≠  Delivery presentation

2 obligations / 1 message   → C2-11、C2-15（presentation coalescing）
1 obligation  / 1 message   → C2-14、C2-30、C2-36（复合 trigger，一次兑现）
2 obligations / 2 messages  → C2-31（显式两次）
1 obligation  / 0 inflation → C2-32（重复强调）
```

---

## 6. 命名（**抽象命名，不设计 schema**）

> **候选抽象：Atomic Visibility Obligation**
>
> **最小 identity 单位 = 一条可独立满足 / 取消 / 失效的 visibility obligation。**
> `trigger` 结构可复合；`delivery presentation` 可合并；**两者都不改变 obligation 的 identity 与基数。**

**明确不是**：❌ 字段设计 ❌ 状态枚举 ❌ V0.5 合同。

---

## 7. A′ 的残余代价（必须记录，不得隐藏）

| # | 残余 | 说明 | 证伪探针 |
|---|---|---|---|
| **R-1** | "delivery intent 计数"仍需**语义判定** | 与 V0.4 一脉相承：这是**判定契约**，不是 parser 关键词 | 模糊表达（"有空提醒我一下"）intent 数不明 ⇒ **应当最小澄清**，而不是猜 |
| **R-2** | 复合 trigger 的**求值能力** | A′ 允许复合，但"能否求值"是实现能力 | 若某复合条件**不可判定**（如依赖外部状态）⇒ 应回退为一次澄清 |
| **R-3** | presentation coalescing 的**上限** | 合并展示是否会让用户误以为只有一件事 | 5 条义务合并成一条消息时，用户是否仍感知到 5 件？ |

---

## 8. 本阶段边界

- **未写任何字段/状态/合同**；`Atomic Visibility Obligation` 仅为**候选抽象命名**；
- 族 2／族 3／族 4 **未进入**本次对打（性质不同，见 Clustering Review #2）;
- V0.4 **frozen 不变**；本文件位于 `docs/v05/**`，不影响 V0.4 baseline 校验。
