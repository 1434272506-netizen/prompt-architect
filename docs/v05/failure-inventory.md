# V0.5 Failure Inventory（待研究问题清单）

> **性质**：**问题清单**，不是案例集、不是设计文档。
> **纪律**：**不得**出现"无案例支撑的抽象"；每条在 C1/C2 文件中必须能找到对应案例编号。

---

## 0. 来源分类

| 来源 | 说明 |
|---|---|
| **V0.4-DEFERRED** | V0.4 明确 HOLD／排除、**刻意不修**的项 |
| **V0.4-RESIDUAL** | V0.4 遗留的工具/治理债（不影响运行时架构） |
| **V0.5-OBSERVED** | V0.4 closure 过程中新出现、尚无归属的观察 |
| **V0.5-BOUNDARY** | 涉及 V0.4 明确排除的范围（跨会话/跨任务/多主体） |

---

## 1. V0.4-DEFERRED

| # | 问题 | V0.4 的处理 | 对应案例 |
|---|---|---|---|
| **F-01** | **数值型 starvation 阈值**（`starvation_candidate ⇔ count ≥ N`） | **未定义**（"count 是证据不是政策"） | 待造（C3 候选；**当前无案例**，不得据此设计） |
| **F-02** | **"用户再次提到 = 兑现"的泛化**（原 N07） | **泛化被刻意排除**；NB-06 仅作局部行为 | **[C2-03](c2-notification-lifecycle-discovery.md)（含 A/B/C/D 四边界）** |
| **F-03** | **`priority_hint` 的时间窗表达**（"今天/这周"） | 以 `scope` ＋ `valid_until` 处理；**未扩 scope 枚举** | 待造 |

## 2. V0.4-RESIDUAL

| # | 问题 | 定位 | 处理 |
|---|---|---|---|
| **F-R1** | 旧 `freeze_v03.py --write` **哨兵重复** | **legacy tooling debt，outside runtime architecture** | 已由 V0.4 护栏覆盖（`docs/freeze-v0.3.md` 受 V0.4 baseline 覆盖 → 损坏即 DIFF）；**不在 V0.5 设计范围** |
| **F-R2** | V0.4 文档中"迭代记录"与实际 baseline 版本号的耦合 | 治理流程噪音 | 已通过"文档不硬编码版本号，指向 manifest `baseline_id`"缓解；**仅记录** |

## 3. V0.5-OBSERVED

| # | 问题 | 观察来源 | 对应案例 |
|---|---|---|---|
| **F-11** | 一个 commitment 能否绑定**多个 trigger** | C2 定界 | **[C2-01](c2-notification-lifecycle-discovery.md)** |
| **F-12** | trigger 满足后 **delivery 被阻塞**（burden／高优先流程） | C2 | **[C2-02](c2-notification-lifecycle-discovery.md)** |
| **F-13** | 多个 commitment 指向**同一 Gap** 时是否合并 | C2 | **[C2-05](c2-notification-lifecycle-discovery.md)** |
| **F-14** | **撤销** commitment 与 **discharge** 的区别 | C2 | **[C2-09](c2-notification-lifecycle-discovery.md)** |
| **F-15** | commitment 指向的 Gap 被 **generation replacement** 取代后的归属 | C2 | **[C2-10](c2-notification-lifecycle-discovery.md)** |
| **F-16** | 任务结束时**未兑现**的 commitment 归谁（Notification vs 交付完整性） | C2 | **[C2-12](c2-notification-lifecycle-discovery.md)** |
| **F-21** | **提议 / 选择 / 批准 / 否决 / 拥有最终值** 是否可分离 | C1 定界 | **[C1-03](c1-authority-value-discovery.md) · [C1-06](c1-authority-value-discovery.md) · [C1-08](c1-authority-value-discovery.md)** |
| **F-22** | **分域授权**（"预算你定，颜色我定"）是否只是两次 Authorization | C1 | **[C1-04](c1-authority-value-discovery.md)** |
| **F-23** | **带约束的授权**（"不违法都行"／"不超过 5000"／"不许用红色"） | C1 | **[C1-05](c1-authority-value-discovery.md) · [C1-07](c1-authority-value-discovery.md) · [C1-10](c1-authority-value-discovery.md)** |
| **F-24** | 授权后的**保留撤销权**（"我保留随时改"） | C1 | **[C1-11](c1-authority-value-discovery.md)** |
| **F-25** | **共同决策**（"我们俩一起定"）与 §11.7 共同决策判据的关系 | C1 | **[C1-12](c1-authority-value-discovery.md)** |

## 4. V0.5-BOUNDARY

| # | 问题 | 为什么是边界 | 对应案例 |
|---|---|---|---|
| **F-31** | **跨会话 / 跨任务的 visibility commitment** | V0.4 明确"不含跨会话载体" | **[C2-04](c2-notification-lifecycle-discovery.md)** ／ [observations.md](observations.md) |
| **F-32** | **跨会话的 fairness evidence** | 同上 | [observations.md](observations.md) |
| **F-33** | **多主体决策权**（"最终得老板点头"） | V0.4 的 `pending_external` 只处理**外部 owner 暂停**，不处理**内部多主体** | **[C1-08](c1-authority-value-discovery.md)** ／ [observations.md](observations.md) |
| **F-34** | **shared ledger 的边界**（哪些必须跨会话保持 identity） | 一旦做错会催生"万能共享账本"，破坏 V0.4 ownership | [observations.md](observations.md) |

---

## 5. 状态汇总

```
V0.4-DEFERRED          3（其中 1 条已有案例：F-02）
V0.4-RESIDUAL          2（均不在 V0.5 设计范围）
V0.5-OBSERVED         10（全部已有对应案例）
V0.5-BOUNDARY          4（3 条已有案例，1 条为第三主线观察）
```

> **未出现"无案例支撑的抽象"**；所有 C1/C2 案例均可在此表中反查。

---

## 6. 第二批新增（C1-13～20／C2-13～28）＋ 聚簇结论

**新增问题项**

| # | 问题 | 来源 | 对应案例 |
|---|---|---|---|
| **F-41** | 用户声明边界能否成为 T1 scope / 门条件 | C1-13／15／17 | **[C1-13](c1-authority-value-discovery.md)｜[C1-15](c1-authority-value-discovery.md)｜[C1-17](c1-authority-value-discovery.md)** |
| **F-42** | 用户声明约束之间的**优先级**（无解时回问还是放宽） | C1-19 | **[C1-19](c1-authority-value-discovery.md)** |
| **F-51** | obligation **基数**（一句话 = 几条义务） | C2-13／15 | **[C2-13](c2-notification-lifecycle-discovery.md)｜[C2-15](c2-notification-lifecycle-discovery.md)** |
| **F-52** | obligation **fan-out**（一句多 Gap） | C2-15 | **[C2-15](c2-notification-lifecycle-discovery.md)** |
| **F-53** | trigger **修订 vs 取消＋新建**（identity） | C2-16／27 | **[C2-16](c2-notification-lifecycle-discovery.md)｜[C2-27](c2-notification-lifecycle-discovery.md)** |
| **F-54** | trigger **复合**（OR／AND） | C2-23／24 | **[C2-23](c2-notification-lifecycle-discovery.md)｜[C2-24](c2-notification-lifecycle-discovery.md)** |
| **F-55** | trigger **有效期**（过期／不可能／状态变更后重评） | C2-26／28／08 | **[C2-26](c2-notification-lifecycle-discovery.md)｜[C2-28](c2-notification-lifecycle-discovery.md)｜[C2-08](c2-notification-lifecycle-discovery.md)** |
| **F-56** | 义务**结束原因**不可区分（兑现／取消／对象消失） | C2-22 | **[C2-22](c2-notification-lifecycle-discovery.md)**（**未证明需要表达**） |

**已被证明"V0.4 已覆盖"（撤回研究）**

| 项 | 依据 |
|---|---|
| 软偏好（C1-14）／白名单（C1-16）／域分区（C1-18）／撤销权（C1-20） | 分别由 AI 取值判断／T1 scope／逐 gap scope ＋ 既有 R6 类／无条件 Revision 覆盖 |
| delivery→discharge（C2-21）／取消提醒≠取消需求（C2-18）／交付后再要一次（C2-17） | §7 ＋ 三维分离 |
| **用户重提（N07，C2-19／20）** | **B3 出口（对象消失 ⇒ never_notify）＋"是否被实际处理"**；**无需泛化条款** |
| trigger 建立前已成立（C2-25） | §6.2 已规定"条件已成立 ⇒ 可立即交付，但不改判为 `now`" |
| trigger 替换（C2-27） | 行为唯一（identity 归族 1） |

**聚簇评审**：见 [failure-clustering-review.md](failure-clustering-review.md)。

```
【Review #1 快照（48 例时）】
族 1  Obligation identity / cardinality      7 例  → 门槛全过
族 2  Trigger composition                    ~3–4  → 未过
族 3  Trigger validity                       3     → 未过
族 4  User-declared boundary → T1 scope/gate 4 形态 → 未过
C1 族 β  Constraint priority                 1     → 远未达
```
（Review #2 与最新状态见 §7；族 1 最终计数为 **10**。）

---

## 7. 收口状态（Convergence #1 之后）

### 已结清

| 项 | 状态 | 依据 |
|---|---|---|
| **族 1** | **✅ 已收敛**：候选抽象 **`Atomic Visibility Obligation`**（仅命名） | [abstraction-convergence.md](abstraction-convergence.md)：Model 0 淘汰、B′ 收敛到 member identity、**A′ 10/10** |
| **C1-β · Constraint Priority** | **✅ DISSOLVED** | 全部案例可分解为"族 α 硬边界 ＋ 既有软偏好" |
| **族 4** | **✅ 门槛达成（5 独立逻辑形态）** | C1-25（允许区间 ＋ 区间外升级）补足第 5 形态；wording robustness ＋ 强负对照 PASS |
| **C2-B（delivery／discharge／cancel）** | **✅ 非缺口** | 6/6 行为唯一；N07 由既有 B3 出口回答 |
| **N07（用户重提）** | **✅ 降级为"已被既有行为覆盖"** | C2-19／20 成对：差别在"**是否被实际处理**" |

### 仍在 Discovery（未进 abstraction）

| 项 | 状态 | 下一步 |
|---|---|---|
| **族 2 · Trigger composition** | 倾向**判定契约可解**（`condition` 取值空间） | 先裁：复合能否含**时间项**（`condition` ＋ `time_window` 混合） |
| **族 3 · Trigger validity** | 真缺口，但可能**复用既有出口** | 需先证明**不能**复用"对象不存在／不合法 ⇒ `never_notify`"，才谈新 lifecycle 状态（**远未到加 `expired` 的时候**） |
| **族 4 · User-declared boundary** | 门槛达成，**未启动 convergence** | 待族 1 之后安排 |
| **第三主线 · 跨会话身份与持久化** | **暂缓** | 需先有跨会话真实案例（C2-04 仅 1 例） |

### 计数修正（自查）

```
族 1：11 → 10 个独立案例（C2-14 ≡ C2-29 重复计数已修正；门槛仍全过）
```


