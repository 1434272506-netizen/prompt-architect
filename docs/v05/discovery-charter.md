# V0.5 Discovery Charter

> **阶段**：Discovery 0（问题空间定界）→ 对抗案例 → 候选抽象 → （仅在存活后）合同
> **本文件规定**：纪律、对照组协议、案例记录格式、Discovery 0 的出口条件。
> **本文件不规定**：任何行为规则、字段、状态、Action。

---

## 1. 五条硬纪律

```
1. V0.4 remains frozen.
2. V0.5 observations do not modify V0.4 contracts.
3. No new field/state/action is accepted merely because a scenario needs it.
4. First collect ambiguity/failure cases, then derive candidate abstractions.
5. Candidate ≠ contract until adversarial cases survive.
```

**推论**

- V0.4 的任何合同、baseline、evidence **不在本阶段修改范围内**；
- 「某个 case 需要新字段」**不是**引入字段的理由；需要的是先证明**现有表达力**在何处失效；
- 先有**二义性/失败案例**，再有抽象；**顺序不可反**。

---

## 2. V0.4 = 固定对照组（Control Group Protocol）

每个候选抽象都必须回答四问：

```
Q1  它解决了哪个 V0.4 无法表达的真实案例？
Q2  如果去掉新机制，哪个 case 会重新产生二义性？
Q3  它有没有破坏 E1–E8？
Q4  它是在扩展 ownership，还是偷走了另一个 layer 的方向盘？
```

**判定分类（每个 case 必须落到一类）**

| 类别 | 含义 |
|---|---|
| **V0.4-EXPRESSIBLE** | 现有合同已能唯一承接；**不需要 V0.5 任何东西** |
| **V0.4-AMBIGUOUS** | 现有合同§给出两个合法读法（＝V0.5 的真实入口） |
| **V0.4-MISSING-EXPRESSION** | 现有字段/状态**无法表达**该语义（**必须证明**，不能声明） |
| **V0.4-BOUNDARY** | 涉及 V0.4 明确排除的范围（跨会话/跨任务/多主体等） |
| **UNDECIDABLE** | 当前证据不足，**不得**据此设计 |

> **只有 `V0.4-AMBIGUOUS` 与 `V0.4-MISSING-EXPRESSION` 才是 V0.5 的合法入口**；其余不进设计。

---

## 3. 案例记录格式（每条案例 8 项）

```
1. 原话（verbatim）
2. V0.4 现状：由哪一层承接？给出判定与依据（引用具体合同/条款）
3. 碰撞点：语义在哪一步分叉（写清"哪一句被两种读法同时满足"）
4. 缺字段 还是 缺解析？（沿用 V0.4 纪律：先判定，勿跳步）
5. 对照组四问 Q1–Q4 的逐问回答
6. 候选抽象（**仅记录**；可以写"暂无"）
7. 反例/证伪探针：什么样的输入会推翻上面的候选抽象
8. 状态：V0.4-EXPRESSIBLE / V0.4-AMBIGUOUS / V0.4-MISSING-EXPRESSION / V0.4-BOUNDARY / UNDECIDABLE
```

**禁止**：在案例里直接写字段名、状态名、Action 名。

---

## 4. Discovery 0 的出口条件

```
① 三条主线各有 ≥1 份定界说明（README ＋ 本 charter ＋ observations）
② C1 / C2 各 ≥12 个对抗案例，且每条都有第 3 节 8 项记录
③ 每条案例的状态分类已给出（不得留空）
④ failure-inventory 与案例一一可追（不得有"无案例支撑的抽象"）
⑤ 未产生任何 V0.5 合同文本、未新增任何字段/状态/Action
```

---

## 5. 进入合同阶段的门槛（本阶段不启动）

```
① 某条候选抽象在 ≥3 个互不相同的对抗案例中**存活**
② 该抽象在 V0.4 对照组下**不可表达**（Q1 有实证）
③ 去掉它会产生**可复现的二义性**（Q2 有实证）
④ E1–E8 全部保持（Q3）
⑤ ownership 未被偷走（Q4）
```

**满足前四条之前，不写 `V0.5 Contract`。**

---

## 6. 与 V0.4 治理的关系

- V0.5 材料位于 `docs/v05/**`，**不在** V0.4 release baseline 的 scope 内；
- V0.4 的 verifier 只扫描 `docs/v04/*`，故新增 `docs/v05/**` **不会**影响 V0.4 校验结果；
- 若将来需要把 V0.5 产物纳入某个 baseline，**必须走 V0.5 自己的 baseline 协议**（沿用 V0.4 的 BL-01～BL-10 形态），**不得**混入 V0.4 manifest。
