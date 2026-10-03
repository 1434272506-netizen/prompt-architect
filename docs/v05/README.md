# Prompt Architect V0.5 · Discovery

> **状态**：**DISCOVERY**（尚未有任何 V0.5 合同）
> **目标**：**不是继续修 V0.4**，而是研究 V0.4 已经暴露出的**下一层问题**。
> **V0.5 材料的位置**：`docs/v05/**` —— **不在 V0.4 release baseline 的 scope 内**（V0.4 保持冻结，互不影响）。

---

## 0. 项目认知切换（V0.4 之后）

```
Prompt Architect V0.4
=====================
状态：FROZEN / RELEASE READY

允许：
- 修复明确的 implementation bug
- 修复文档链接 / 拼写等非语义问题
- 按正式 exception governance 处理必要变更

不再做：
- 新行为规则
- 新 ontology
- 新 Action / Gap semantics
- 为新需求继续扩充 V0.4
```

```
Prompt Architect V0.5
=====================
状态：DISCOVERY

目标：
研究 V0.4 已经暴露出的下一层问题，
而不是继续修 V0.4。
```

---

## 1. 三条主线

| 主线 | 内容 | 文件 |
|---|---|---|
| **第一主线** | **Decision Rights / Authority–Value Separation**（V0.4 只到 `Decision Authority ≠ Value Acceptance` 的二分） | [c1-authority-value-discovery.md](c1-authority-value-discovery.md) |
| **第二主线** | **Notification Lifecycle**（V0.4 浮现 `Commitment → Trigger → Delivery → Discharge`） | [c2-notification-lifecycle-discovery.md](c2-notification-lifecycle-discovery.md) |
| **第三主线（暂不编号）** | **跨会话身份与持久化边界**（哪些必须跨会话保持 identity，哪些只是当前 scheduler 的局部证据） | [observations.md](observations.md) |

---

## 2. 五条 Discovery 纪律（本阶段硬约束）

```
1. V0.4 remains frozen.
2. V0.5 observations do not modify V0.4 contracts.
3. No new field/state/action is accepted merely because a scenario needs it.
4. First collect ambiguity/failure cases, then derive candidate abstractions.
5. Candidate ≠ contract until adversarial cases survive.
```

---

## 3. V0.4 = V0.5 的固定对照组

任何 V0.5 新机制都必须回答四问：

```
1. 它解决了哪个 V0.4 无法表达的真实案例？
2. 如果去掉新机制，哪个 case 会重新产生二义性？
3. 它有没有破坏 E1–E8？
4. 它是在扩展 ownership，还是偷走了另一个 layer 的方向盘？
```

> 这样"不断向前"就不会变成"不断加功能"，而是每一代都比上一代拥有**更强的解释能力**。

---

## 4. 文件地图

```
docs/v05/
├── README.md                                ← 本文件（索引与认知切换）
├── discovery-charter.md                     ← 章程、纪律、案例记录格式、Discovery 0 出口条件
├── failure-inventory.md                     ← 待研究的问题清单（尚未成为案例）
├── c1-authority-value-discovery.md          ← C1 第一批对抗案例
├── c2-notification-lifecycle-discovery.md   ← C2 第一批对抗案例
└── observations.md                          ← 未编号观察（含跨会话持久化边界）
```

---

## 5. 当前进度

| 项 | 状态 |
|---|---|
| Discovery 0（问题空间定界） | **✅ 本文件 ＋ charter** |
| C1 第一批（12 例） | **✅** |
| C1 第二批 · Constraint-bounded Authority（C1-13～20，8 例） | **✅ 4 EXPRESSIBLE / 4 AMBIGUOUS** |
| C2 第一批（12 例） | **✅** |
| C2 第二批 · A identity／B lifecycle／C trigger（C2-13～28，16 例） | **✅ A 4/4 不唯一；B 6/6 行为唯一；C 4/6 不唯一** |
| **Failure Clustering Review #1** | **✅**（48 例） |
| C1 第三批 · 补门槛 ＋ wording robustness（C1-21～24） | **✅ 族 α 5 例/4 形态；β 判定被吸收** |
| C2 第三批 · 族 1 压力测试（C2-29～32）／族 2 补密（33～36）／族 3 正例（37～40） | **✅ 族 1 四问全不可唯一回答；族 2 降为"判定契约可解候选"；族 3 正例全过** |
| **Failure Clustering Review #2**（累计 60 例） | **✅** |
| C1 第四批 · 族 4 第 5 逻辑形态（C1-25～26） | **✅ 族 4 门槛达成（5 形态）；不阻塞族 1** |
| **Candidate Abstraction Convergence #1 · 族 1** | **✅ 完成**：Model 0 **淘汰**（M1 1/10、≥6 特判、1 例 over-notification、1 例 under-delivery）｜Model B′ **不构成独立优势**（partial discharge/generation 迫使其收敛到 member identity）｜**Model A′ 胜出**（10/10、0 例外、M3–M7 全过） |
| **候选抽象命名** | **`Atomic Visibility Obligation`**（**仅命名，无 schema、无字段、无状态**） |
| **Candidate Abstraction Falsification #1**（AF-01～12 ＋ **M8**） | **✅ 完成 → 判定 `A′ REVISE`**：原子单位**存活**（12/12 无隐藏 set）；**判据被证伪**（AF-07 命中预写的 REVISE 条件）；未达 REJECT 条件。修订判据：**独立 lifecycle intent**（而非 delivery intent 计数） |
| 附加产物 | 🔺 **S-1** identity ≠ satisfaction criterion｜**S-2** 一条 obligation 可多次 delivery｜**S-3** identity ≠ target｜**S-4** 批量操作＝操作层耦合｜**⚠ S-5** 若采用 A′-revised，V0.4 `notify → discharged` 需按历史治理做 **supersede** 处理（**本阶段不改 V0.4**） |
| **Candidate Abstraction Falsification #2**（AF2-01～10 ＋ **M8′**） | **✅ 完成 → 判定 `A′ REVISE again`**：三条核心条件**同时成立**（同满足＋可独立→split／不同满足＋内在不可拆→不 split／外部操作耦合→不 merge）；判据补上限定词 **intrinsic**；仪器 M8 被 AF2-09 证伪并修订为 **M8′** |
| **首次得到的实质成果** | **稳定 identity law**：`identity` 沿 **L 轴（lifecycle 独立性）**分布，与 **S 轴（满足语义）无关** ⇒ 候选定义：**intrinsically independently lifecycle-addressable obligation** |
| 附加产物 | **S-6** cardinality reveal/refinement｜**S-7** 满足差异＝证据非决定条件｜**S-1（强化，仍不设计）**｜**S-4 并入 M8′**｜**S-5 维持**（版本演进，非 V0.4 defect） |
| 任何 V0.5 合同 | **未开始**（下一步才是"最小语义契约"，仍不是 schema） |

**Review #2 一句话**：**60 例中 `MISSING-EXPRESSION = 0`**；**族 1（Obligation Identity，11 例）门槛全过**并获准进入**候选抽象竞争**；**族 2 降级为"判定契约可解候选"**（澄清 `condition` 取值空间）；**族 3 是真缺口但可能复用既有出口**；**族 4 口径待裁**（5 案例 / 4 逻辑形态）；**β 撤销**（被族 α ＋ 既有软偏好吸收）。
