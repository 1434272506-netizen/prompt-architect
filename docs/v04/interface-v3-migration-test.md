# Interface v3 · Migration Test（K1–K5 + 四条不变量 + 恢复路径）

> **目标**：证明 **v3 是 v2 的纯增量扩展**，而不是偷偷改变已稳定的行为。
> **本轮不写新规则、不修失败、不并入 Interface 正文**；只把 v3 候选模型**覆盖在旧测试上跑**。
> **Manifest**：[`interface-v3-migration-manifest.md`](interface-v3-migration-manifest.md)（167 raw / 136 唯一场景 / 5 固定回归 / 3 canary）
> **被测对象**：v3 候选 = A 类（`reset_scope`／`revision_scope`／`reverted_to` + `reverts` 反向边）+ B 类（`pending_external`／`suspension_reason`／`feedback.intent` 四态）
> **对照基线**：**Interface v2 冻结正文**（未改动）

**K 分类**：`K1` 旧行为保持｜`K2` 结果不变、状态表示更精确｜`K3` 旧模型无法表达、v3 正确接管｜`K4` **旧模型原本正确、v3 改错**｜`K5` **两个解释都合法**

---

## 1. 全量 K 分类（167 raw）

| 区块 | Raw | K1 | K2 | K3 | K4 | K5 |
|---|---|---|---|---|---|---|
| B1 v2（C 15 / I 12） | 27 | 20 | 7 | 0 | 0 | 0 |
| B2 Phase 2（FS 30 / TD 20 / L 30） | 80 | 28 | 23 | 29 | 0 | 0 |
| B3 Phase 2.3（2.3A 30 / 2.3B 30） | 60 | 0 | 18 | 42 | 0 | 0 |
| **合计** | **167** | **48** | **48** | **71** | **0** | **0** |

**逐块明细**

| 区块 | K2（结果不变、表示更精确） | K3（v3 接管） |
|---|---|---|
| C-01～C-15 | C-06、C-07、C-09、C-11、C-13 | — |
| I-01～I-12 | I-05、I-06 | — |
| FS-01～FS-30 | FS-01、07、13、15、22、24、26、30（原"半承接 8"） | FS-02、03、05、06、08、09、10、12、14、17、20、21、23、25、27、29（原"不可承接 16"） |
| TD-01～TD-20 | TD-03、10、11、12、13、16、19 | TD-01、02、04、05、06、07、14、17 |
| L-01～L-30 | L-07、08、11、12、13、14、15、18 | **L-20、L-23、L-24、L-25、L-30**（原 5 例不唯一） |
| 2.3A（RST/REV/RSC/EXT/UNW/FBC） | FBC-01～04 | RST-01～08、REV-01～05、RSC-01～05、2.3A-EXT-01～04、UNW-01～04 |
| 2.3B（EXT/INT） | 2.3B-EXT-01～04、INT-06～10、INT-16～20 | 2.3B-EXT-05～10、INT-01～05、INT-11～15 |

**K4 = 0（无回归）**：为证明这一点，专门做了 6 个"反回归假说"攻击（见 §3），全部未成立。
**K5 = 0（本表内）**：167 例在 v3 下均只有一个合法裁定。**但新增证伪探针 V3-F1 触发 1 例 K5**（见 §5）——它不是既有案例，而是按你 §四 要求新加的探针。

---

## 2. 四条历史一致性不变量

### 不变量 A · 历史不可覆写

```
A → B → C ，用户："还是用 A"（V3-C1）
期望： A → B → C 全部保留；新增 reverts 边 C→A；A 为当前值
禁止： 把历史改造成只剩 A
```
**结果：通过。** `reverts` 是**追加边**（不改写 `history`）；审计仍能解释"为什么曾经到过 B/C"。支持案例：V3-C1、L-30／REV-02、L-23／REV-01。

### 不变量 B · 当前值唯一（authoritative current_value）

```
任意 gap 在同一时刻：历史节点可多个，当前真值只能一个
```
**结果：通过。** revert 后 B/C 转 `INVALIDATED`（历史可读、不再 authoritative）；A 恢复 `CONFIRMED`。唯一性谓词：

```
authoritative(g) := ∃! v ∈ history(g) : v.status = CONFIRMED ∧ v.confidence = confirmed ∧ g.validity_state = stable
```

反向测试：若 revert 后不把 C 置 `INVALIDATED`，则 A 与 C 同时可读 → **该反例被检出并判为禁止**（说明这条不变量有真实约束力，不是空话）。

### 不变量 C · reset 不删除历史

```
RST-05（whole_task reset）：旧结论 → 失效；新分支开始；旧记录保留
```
**结果：通过。** reset 只改**当前有效集**与**分支起点**，`history` 只追加；出口给"旧稿效力清单"。

### 不变量 D · local revision 不扩大闭包

```
RSC-01／RSC-02（revision_scope=local）+ 一个很大的 affected 图
期望：只改该值本身；**不**因 affected 图大而重开整页设计
```
**结果：通过。** 传播在 `local` 边界处**硬停**：`local ⇒ 不扩张传递闭包`。对照：`cluster`（RSC-03）簇内传播；`global`（RSC-04）全闭包。

---

## 3. 反回归假说（K4 攻击记录）

| # | 假说 | 结果 | K 判定 |
|---|---|---|---|
| R-1 | `reverts` 会破坏 `supersedes` 的下游 `CHALLENGED` 传播 | 不成立：回退后下游按**回退目标**重算，而非保留被 C 污染的状态 | K2 |
| R-2 | `reset` 会抹掉历史导致审计断裂 | 不成立（不变量 C） | K1/K2 |
| R-3 | `revision_scope=local` 会因 `affected` 图大而失效 | 不成立（不变量 D） | K2 |
| R-4 | revert 后 A 的 `validity_state` 卡在 `challenged` | 不成立：回退即恢复 `stable` | K2 |
| R-5 | `pending_external` 与 `CHALLENGED` 传播互相打架 | 不成立：`SUSPENDED(external_owner)` 不参与 `CHALLENGED` 传播 | K1 |
| R-6 | `unaware` 判据会把"已知道但没想过"的人判错 | **成立 → 见 §5（V3-F1）** | **K5** |

---

## 4. `pending_external` 的完整 suspend → resume 回归（V3-C2）

```
Round 1  用户：我要问客户。
         → SUSPENDED / suspension_reason = external_owner / owner = 客户
         → 不进 askable_set；出口"待客户确认"
Round 3  用户：客户说保留方案 B。
         → resume_condition 满足
```

**五个必须唯一回答的问题**

| # | 问题 | 唯一答案 |
|---|---|---|
| 1 | Gap 从什么状态恢复？ | 从 `SUSPENDED` 回到 **`OPEN`**（外部意见 ≠ 自动生效） |
| 2 | 新信息算 `confirmed_value` 还是 `proposal`？ | 外部方转述 = **input/proposal**；仅当**用户本人**确认后才成 `confirmed_value` |
| 3 | 原来的 `unresolved`／`attempts` 是否保留？ | **保留**（历史不可覆写；不因恢复清零） |
| 4 | 是否重新进入 `askable_set`？ | **是**（解除 SUSPENDED → `OPEN` ∈ `askable_set`）；若用户已确认则 `CLOSED` |
| 5 | 是否仍需用户本人确认？ | **需要**：一次 ASK 后再落 `CONFIRMED`（**EXT-07 边界**：外部方授权不替代用户授权） |

**结果：通过（5/5 唯一）。** 该回归同时覆盖"能暂停"与"能回来"。

---

## 5. `unaware` 证伪探针（V3-F1）——**本轮唯一失败点**

```
输入：用户："我知道这个问题，但以前一直没想清楚。"
      系统状态：该岔路口从未被呈现过（attempts = 0，history 无 TEACH/SHOW）
```

| 读法 | 依据 | 结论 |
|---|---|---|
| 判 `unaware` | 现行契约 `unaware ⟺ ¬topic_presented` → 成立 | TEACH → ASK |
| 判 `unable`／`undecided` | 用户**显式表明认知**（"我知道这个问题"） | §11.2 降维 → 再问一次 |

**两个都合法 → K5 = 1。**

**你的判断是对的**：`topic_presented` 是 `unaware` 的**重要证据**，但不应成为"用户认知状态"的**唯一来源**。

**最小修订（未落盘，待你裁决）**——一行，仅改 v3 候选契约，不触碰 v2／SKILL：

```
unaware ⟺ ¬topic_presented ∧ ¬user_declares_awareness
（user_declares_awareness := 用户本轮或历史中明示"我知道／我了解过／以前想过"）
```

**处理纪律**：本轮**不自行修改设计**（按你的指示）。修订后需重跑 V3-F1 → 若唯一，则 K5 归零。

### 5.1 修订已执行（预登记 #13）

```
unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness

user_evidences_awareness := 用户在当前或已有对话中
                           ① 明确承认该决策存在，或
                           ② 能主动描述该决策的选项 / 取舍 / 后果
```

- 命名按裁决收紧为 `user_evidences_awareness`（不限于字面"我知道"）。
- 仍是**派生证据**：**不新增 Gap 状态、不新增持久字段**。
- 落盘位置：[`feedback-state-extension-design.md`](feedback-state-extension-design.md) B-2、[`feedback-responsibility-extension-design.md`](feedback-responsibility-extension-design.md) §2.3。

### 5.2 证伪集 UA-01～UA-04（重跑）

| # | 系统状态 | 用户原话 | 判定 | 路径 | 唯一 |
|---|---|---|---|---|---|
| **UA-01** | 未呈现 | `我知道这个问题，但以前一直没想清楚。` | **NOT `unaware`** → `unable`／`undecided` | §11.2 降维 → 再问一次 | **唯一**（`user_evidences_awareness = true` ①） |
| **UA-02** | 未呈现 | 用户**主动讨论两种方案的取舍**（"性能和续航我要权衡，只是还没定"） | **NOT `unaware`** → `unable` | §11.2 降维 | **唯一**（证据 ② 能描述取舍） |
| **UA-03** | 未呈现 | `不知道，还需要考虑这个吗？` | **`unaware`** | TEACH → ASK | **唯一**（`¬presented ∧ ¬evidences`） |
| **UA-04** | **已呈现** | `不知道怎么选。` | **`unable`** | §11.2 降维 | **唯一**（`topic_presented = true`） |

**结果：UA-01～UA-04 = 4/4 唯一；V3-F1（V3-C4）→ PASS；K5 = 0；无新 K4。**

### 5.3 受影响的既有案例重跑（unaware / unable 全量）

| 案例组 | 重跑结果 |
|---|---|
| UNW-01～04（2.3-A 认知边界） | 4/4 唯一（UNW-01／02 仍 `unaware`：用户未表现认知；UNW-03 仍 `unable`；UNW-04 `unaware`） |
| INT-01～05（Phase 2.3-B `unaware`） | 5/5 唯一（判据未变：均无认知证据） |
| INT-06～10（Phase 2.3-B `unable`） | 5/5 唯一（含 INT-07 = AL-21，与 UNW-03 同判） |
| AL-19～AL-22（精确别名簇对） | 4 簇一致（两成员判据相同，无分叉） |
| FS-08／UNW-02（"没想过"家族，OC-05） | 2/2 唯一（"没想过"= 未表现认知 → 保持 `unaware`） |

**合计重跑 20 例，20/20 唯一，无新 K4、无新 K5。**

---

## 6. `feedback.intent` 跨轮变化回归（V3-C5）

```
Round 1  AI：预算上限是多少？
         用户：不知道。                → intent = unable（已呈现该岔路）
Round 2  AI 降维：1 万以内 / 1–5 万 / 更高？
         用户：这个我不想定。            → intent = refused
```

| 检查项 | 期望 | 结果 |
|---|---|---|
| 同一 gap 的 intent 是否允许变化 | **允许**（intent 是**事件属性**，不是用户永久标签） | 通过 |
| 是否覆盖历史 intent | **不覆盖**：`feedback.history` 记录 `unable → refused` | 通过 |
| 反向（refused → unable）是否同样允许 | 允许（用户后续愿意回答） | 通过 |
| 是否因第一次 `refused` 而永久判定该缺口 | **否** | 通过 |

**结果：通过（4/4）。** 结论：**不得把一次 `refused`／`unable` 写进用户画像**，只写进该 gap 的反馈账。

---

## 7. Canary 汇总

| Canary | 内容 | 结果 |
|---|---|---|
| **L-20** | "重新来" ← 范围不明 → `reset_scope=unresolved` | **PASS** |
| **L-23** | "还是原来的" → `reverted_to=previous_state` | **PASS** |
| **L-24** | "稍微调一下" → `revision_scope=local` + 索取新值 | **PASS** |
| **L-25** | "改成蓝色，另外页面重来" → 复合分解为两条链 | **PASS** |
| **L-30** | "回到最开始那版" → `reverted_to=target_snapshot` | **PASS** |
| **V3-C1** | A→B→C→revert A：唯一 `current_value` | **PASS**（不变量 A/B） |
| **V3-C2** | external suspend → 外部回复 → resume（5 问唯一） | **PASS** |
| **V3-C3** | local revision + 大 `affected` 闭包 | **PASS**（不变量 D） |
| **V3-C4** | （本文件 V3-F1）unaware 证伪探针 | **PASS**（修订后） |
| **UA-01～UA-04** | unaware 证伪集（新增） | **4/4 PASS** |

---

## 8. 冻结门槛核对

| # | 条件 | 结果 |
|---|---|---|
| 1 | 全量 manifest 所有案例都有唯一裁定 | ✅ 167/167（另 34 例 B0 基线不受影响） |
| 2 | **K4 Regression = 0** | ✅ **0** |
| 3 | **K5 Ambiguous = 0** | ✅ **0**（V3-C4 修订后；UA-01～04 = 4/4） |
| 4 | 五个原固定回归持续通过 | ✅ 5/5 |
| 5 | 三个新 canary 通过（V3-C1/C2/C3） | ✅ 3/3 |
| 6 | v2 冻结正文未被反向修改 | ✅ 未改动（v3 以**增量章节**并入，v2 章节逐字保留） |
| 7 | §11 / §6.3 / V0.3 全部无改动 | ✅ `SKILL.md` 仍为 681 行；`core/`／`strategies/` 未动 |
| 8 | 历史一致性四条不变量均有测试覆盖 | ✅ A/B/C/D 各 1 组 |
| 9 | `pending_external` 至少一条完整 suspend→resume 回归 | ✅ V3-C2（5 问唯一） |
| **10** | **（用户补充）raw release regression** | ✅ **201/201**（见 §9）；`170 unique` 仅作覆盖统计 |

**结论：9 项原始门槛 + 1 项 release gate 全部通过 → 满足 v3 并入与冻结条件。**

---

## 9. Release Regression（raw 口径）

> **口径（用户裁决）**：去重用于**理解覆盖率**（170 unique）；**raw 用于版本发布验收**（201）。固定回归可能位于 alias 簇内，故不因去重而跳过。

| 区块 | Raw | 结果 |
|---|---|---|
| B0 V0.1–V0.3 冻结基线（21 + 12 + 1） | 34 | 34/34 通过 |
| B1 v2 接口（C 15 + I 12） | 27 | 27/27 通过 |
| B2 Phase 2（FS 30 + TD 20 + L 30） | 80 | 80/80 通过 |
| B3 Phase 2.3（2.3A 30 + 2.3B 30） | 60 | 60/60 通过 |
| **合计** | **201** | **201/201** |

**release gate**

```
V0.1–V0.4 raw regression : 201/201
V3 canaries              : PASS（V3-C1/C2/C3/C4 + UA-01～04）
K4                       : 0
K5                       : 0
```

**未做**：未修改 v2 冻结正文（v3 为增量章节）、未修改 `SKILL.md`／§11／§6.3、未进入 `pending_resolution` 与 `deprioritized`。
