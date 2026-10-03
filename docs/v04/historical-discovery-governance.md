# Historical Discovery Governance（D10 治理条款）

> **性质**：**文档身份治理**，不改任何运行时规则（不碰 Notification 语义、不碰 Gap/Action/Type）。
> **解决**：旧审计 **D10** —— Discovery 的历史身份与**现行规范身份**此前未被正式分开，导致"30/30 保持"容易被读成"所有历史结论今天仍有效"。
> **证据层次**：`治理规则（本文件） → 实际应用（N06 append-only 更正） → 历史 artifact（Discovery 案例 C-03／C-06）`。

---

## 1. 正式条款（5 条）

```
Historical Discovery Governance

1. Discovery artifacts are append-only historical evidence.
   已执行的历史案例、原始输出与当时结论不得覆写或伪装成从未发生。

2. Discovery conclusions are candidate findings, not automatically normative contracts.

3. When a later approved contract adjudicates the same semantic question differently,
   the later contract is authoritative for current behavior.

4. Superseded Discovery findings remain visible and must be marked with:
   - historical status
   - superseding contract / adjudication
   - current normative interpretation

5. "30/30" denotes historical execution / coverage success only.
   It MUST NOT be interpreted as:
   "all 30 historical conclusions remain current normative behavior."
```

**关键（第 5 条）**：从此仓库里看到 `30/30`，**只能推出**"30 个历史案例都有记录／当时跑完"，**不能推出**"30 个当时的语义出口今天全部仍有效"。

---

## 2. 应用实例（N06 已落，**本轮不重复修改**）

| Discovery 案例 | 历史输出（**保留**） | 取代者 | 现行规范解释 |
|---|---|---|---|
| **NA-01** `不急，但别忘。` | `trigger=now` → `notify_now` | **N08**（Notification Contract §6.2 规则 4） | `condition = next_relevant_checkpoint` |
| **C-03** `不急，但别忘了` | "应提醒"（未指明 trigger） | **N08** | `condition = next_relevant_checkpoint` |
| **C-06** `无所谓，但别漏` | "应提醒"（未指明 trigger） | **N08** | `condition = next_relevant_checkpoint` |
| **NB-01** `这个以后提醒我` | `notify_later` | —（**未被取代**） | **不变**（规则 4 覆盖） |
| **C-02** `C 不急` 连 10 轮 | **不是 starvation**（忠实执行用户偏好） | —（**未被取代**） | **不变**（Fairness F1／SFC-06） |

> **N06 是实例修复；D10 是治理规则闭合。** 二者关系：`D10 治理原则 → N06 实际应用 → C-03／C-06 成为具体例子`。

---

## 3. HG-10 · Historical Governance 探针（文档身份检查）

| 检查项 | C-03 | C-06 | **NB-01**（未被取代的对照） | 结果 |
|---|---|---|---|---|
| historical evidence still present（历史证据仍在） | ✅ | ✅ | ✅ | ✅ |
| superseded case explicitly marked（被取代者已标注） | ✅ | ✅ | —（**本就不需标注**） | ✅ |
| current normative source identified（现行规范来源已指明） | ✅ 规则 4 | ✅ 规则 4 | ✅ 规则 4 | ✅ |
| **historical output silently rewritten（历史输出被静默改写）** | **NO** | **NO** | **NO** | ✅ |

**HG-10 = PASS**（无静默改写：C-03／C-06 的原始输出仍在 `notification-policy-discovery.md` 正文中，仅在**追加的更正表**里标注 superseded）。

---

## 4. 适用边界（防止治理条款被滥用）

- 本条款**只**规定文档身份与证据层次，**不改变**任何现行合同语义；
- 标为 `superseded` **不等于**"历史输出是错的"——只表示**现行规范采用另一解释**；
- 未被取代的历史结论**继续有效**（如 NB-01／C-02），**不因本条款而降级**；
- 本合同**不影响**运行时行为，也不引入任何字段／状态／计数。
