# V0.4.8-B · Notification Policy Contract v1（sibling of Scheduler Fairness）

> **地位**：**正式 sibling contract v1**（2026-10-03 建立并冻结）。与 [`scheduler-fairness-contract.md`](scheduler-fairness-contract.md) **共享证据、互不写权**。
> **来源**：Discovery [`notification-policy-discovery.md`](notification-policy-discovery.md)（30/30）＋ 本轮裁决（K5-1／K5-2 封口 ＋ one-commitment-one-notification）。
> **边界**：❌ 不改 Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3 ❌ 不新增 Gap state／Action／Type／计数器。

---

## 第 1 条（本合同的宪法条款）

> **Notification Policy 不得改变 `ordered_actions`，不得 promotion，不得改变 gap status，不得改变 Action，不得创建 blocker／risk。**

它只回答一个问题：

> **有哪些长期未处理事项现在应该让用户知道？**

---

## 第 2 条 · 架构（共享证据，没有互相写权限）

```
                     Scheduler Fairness
                         │
                         │ fairness evidence
                         ▼
                  Fairness Ledger
                         │
                         ├──────────────┐
                         │              │
                         ▼              ▼
                  Scheduler       Notification Policy
               调度是否提升         是否让用户知道
```

- **Fairness → Notification**：只传**证据**（`starvation_candidate` 等）；
- **Notification → Fairness**：**零写权**（不得回写 debt、不得影响 promotion）；
- **两者共同**：不得改 Gap 状态、不得改 Action。

---

## 第 3 条 · 输出词表（封闭）

```
notify_now  ｜  notify_later  ｜  record_only  ｜  never_notify
```

---

## 第 4 条 · `visibility_commitment`

```yaml
visibility_commitment:
  required: true | false
  trigger: now | condition | time_window
  discharged: true | false
```

**钉死的原则**：

> **它是"用户可见性义务"，不是需求状态，也不是调度优先级。**

因此 `visibility_commitment = true` **不意味着**：

```
❌ priority ↑
❌ starvation debt ↑
❌ action eligibility ↑
```

（与"调度公平／用户优先权／用户可见性"三维分离一致。）

### 4.1 `discharged` 的写权限（N01）

> **`discharged` 是 Notification 层自有的内部状态／标记，由本层维护。**

```
Notification owns discharged  ≠  Gap state write
```

它**不是** Gap 字段、**不写入** gap status／confidence／validity；本层的任何输出都不改变 `ordered_actions`／promotion／Action／Gap（见第 1 条）。

### 4.2 commitment 的绑定与结束（N05）

```
visibility_commitment 绑定 gap identity + resolution generation；
cluster 结束本身不使其失效。
commitment 的结束仍遵循既有出口：discharge、generation replacement、
以及对象不再存在／不再合法（never_notify）。
```

**删除式澄清**：本合同**不写**"仅 generation 变化才终止"——因为 `discharged`（正常兑现）与"对象不再合法"同样是既有出口。

---

## 第 5 条 · K5-1 封口：零表达的 starvation candidate 默认不主动提醒

> **`starvation_candidate` 只证明调度层存在长期未处理现象，不自动创造用户可见通知义务。**

```
starvation_candidate = true
visibility_commitment.required = false
无其他显式提醒要求
        ↓
record_only
```

**钉成一句**：

```
fairness evidence ≠ notification obligation
```

**不要因为"等得久"就主动打断用户**；否则 Notification Policy 会重新偷偷变成 Scheduler Fairness 的第二套出口。

### 5.1 必须保住的重要例外（**不是** Notification 的职责）

若任务**最终准备结束**，而仍有未处理、会影响**交付完整性**的事项：它是否需要在最终输出中披露，**由既有的交付完整性／未解决项规则处理**，**不是因为 starvation 自动触发 Notification Policy**。

```
长期没排上                ≠ 自动提醒
任务结束前必须披露未完成内容 = 另一个已有责任
```

---

## 第 6 条 · K5-2 封口：`next_relevant_checkpoint`

`以后提醒我` **不定义为"下一轮"**（太机械、往往太早），**也不定义为"有空位"**（会把 notification 绑回 scheduler capacity）。

```yaml
visibility_commitment:
  required: true
  trigger: condition
  condition: next_relevant_checkpoint
  discharged: false
```

### 6.1 机械定义

> **当前高优先流程不会被打断，且重新暴露该事项已经能帮助用户继续决策的最早自然边界。**

**典型 checkpoint（可用）**

```
当前 decision cluster 即将结束
外部依赖恢复
阶段性交付 / 汇总前
准备结束整个任务前
用户主动要求 review / status / recap
```

**明确不是 checkpoint**

```
下一条用户消息
下一次 assistant 回复
scheduler 恰好有一个空位
```

### 6.2 时机解析顺序（正式）

```
1. 用户明确给时间        → time_window
2. 用户明确给条件        → condition
3. 事项本身已有自然恢复／检查条件 → 复用该 condition
4. 任何不含时机的可见请求  → condition = next_relevant_checkpoint
   （含"以后 / 之后提醒"，也含裸"别忘了 / 别漏掉 / 记着"）
5. 只有【错误时机可能产生明显损失】时，才最小澄清"什么时候提醒"
6. 用户明确要求当场        → now
   （"现在就说 / 现在告诉我还差什么 / 马上提一下"）
```

**N02／N03 相关的重要区分**

```
系统自选时机（checkpoint）      → burden 可以影响兑现时刻（notify_later）
用户明确指定时机（now / time_window / 明确 condition）
                                → burden 不得偷偷改写用户时机
```

> 该区分**只限制 Notification 如何解释自己的可见性义务**，**不让 Notification 获得任何调度权**（第 1 条不变）。

因此 **"这个以后提醒我。" 默认不需要立刻反问"什么时候？"**——避免为通知时机新增无价值采访。

### 6.3 `notify_later` 的落点（N02，已按裁决删减）

```
notify_later 不在当前 checkpoint 主动兑现；
若 commitment 仍 active，则在后续满足条件的 relevant checkpoint 再评估。
```

**删除式澄清**：本合同**不写**"每 checkpoint 至多尝试一次"——那会引入 attempt 计数器／checkpoint debt 等**新的记账机制**，与冻结纪律冲突。

---

## 第 7 条 · 一次足够：one commitment → at most one proactive notification

> **一个 active `visibility_commitment` 默认最多产生一次主动通知。**

```
notify  →  commitment discharged
```

**可重新建立义务的三种情形（仅此三种）**

```
① 用户明确重新建立 reminder
② 新 resolution generation 产生新的事项
③ 用户明确要求重复 / 条件性提醒
```

**禁止**设计成"第 1 次 → 第 2 次 → 冷静期"这类**次数债**：不要在语义已足够时再发明计数器。

### 7.1 未决（N07 · HOLD）

> **"用户主动再次提到该事项＝兑现"暂不写入本合同。**

原因：用户主动重提与系统主动通知**不是同一种事件**；至少需区分 A（用户重提且系统实际处理）／B（用户重提但未处理）／C（重提同时改变 requirement 或 generation）／D（用户再次说"别忘了"＝强化还是新承诺）四种边界。**NB-06 目前只是案例结果，不足以支撑全局合同条款**；待其取得正式证据后再裁（届时可采用"若用户主动重新使该事项进入当前对话**且系统实际处理**该事项，则该 obligation 可视为已兑现，且不得仅因此创建第二次主动提醒义务"的安全形式）。

---

## 第 8 条 · delay 四象限（正式入册）

```
delay                 = 当前不要处理
visibility_commitment = 未来是否必须重新让用户看到
```

| delay | visibility | 含义 |
|---|---|---|
| 否 | 否 | 正常处理，无通知义务 |
| 否 | 是 | 正常处理，但需满足显式可见承诺 |
| **是** | **否** | **延后，且不要主动催** |
| **是** | **是** | **延后处理，但满足 trigger 后允许提醒一次** |

---

## 第 9 条 · NPC Canary（10，本轮固定回归）

| # | 场景 | 判定 | 唯一 |
|---|---|---|---|
| **NPC-01** | 纯 starvation candidate，无用户表达 | **`record_only`**（**K5-1 关闭**：证据 ≠ 义务） | **唯一** |
| **NPC-02** | starvation candidate ＋ `别忘了` | `visibility_commitment(required=true, trigger=condition, condition=next_relevant_checkpoint)` → **到触发点提醒一次** | **唯一** |
| **NPC-03** | `以后提醒我` | `trigger=condition`，`condition=next_relevant_checkpoint` → **不是下一消息／下一回复** | **唯一**（**K5-2 关闭**） |
| **NPC-04** | `周五提醒我` | `trigger=time_window`（周五） | **唯一** |
| **NPC-05** | `客户回复后提醒我` | `trigger=condition`（**复用外部依赖恢复条件**） | **唯一** |
| **NPC-06** | `delay`，无 commitment | **不提醒**（四象限：是／否） | **唯一** |
| **NPC-07** | `delay` ＋ `别漏掉` | 到 trigger 后**允许提醒一次**（四象限：是／是） | **唯一** |
| **NPC-08** | 已主动提醒一次、用户没回应 | **不逐轮复催**；**不生成第 2 次**、无冷静期计数器 | **唯一** |
| **NPC-09** | 用户 `知道了，不用再提醒` | `discharged=true` → **`never_notify`** | **唯一** |
| **NPC-10** | 新 resolution generation | 旧 commitment **不自动继承**（需重新表达） | **唯一** |

**结果：NPC-01～10 = 10/10 唯一。**

---

## 第 10 条 · 回归与验收

| 项 | 结果 |
|---|---|
| 原 Discovery **30/30** | **保持** |
| **NPC-01～10** | **10/10 唯一** |
| **K4 / K5** | **0 / 0**（K5-1／K5-2 关闭） |
| Notification 改调度 | **0** |
| Notification 改 Gap | **0** |
| starvation 自动生成通知义务 | **0** |
| delay 无授权被催 | **0** |
| 重复主动提醒 | **0** |
| **Sibling boundary regression** | ✅ Fairness 侧未变（`sha256` 与冻结版一致）；Notification 侧零写权；`promotion ≠ notification` 双向成立 |

---

## 第 11 条 · 状态

| 项 | 状态 |
|---|---|
| Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3 | **未修改** |
| 新增 | **本合同 v1** ＋ 本层字段 `visibility_commitment` |
| 未新增 | Gap state／Action／Type／通知计数器 |
| **O-3** | **整条债完成**：Fairness ✅／starvation observation ✅／user explicit priority ✅／notification visibility ✅ |
| 本合同状态 | **✅ Notification Policy Contract v1 建立并冻结（2026-10-03）** |
