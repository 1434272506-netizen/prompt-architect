# V0.5 · Minimal Semantic Contract #1（MSC-01 · **candidate**）

> **状态**：**CANDIDATE SEMANTIC CONTRACT**（**非 schema、非字段设计、非正式发布**）
> **依据**：Falsification #1（REVISE）＋ Falsification #2（REVISE again，四象限 → 稳定 identity law）
> **纪律**：V0.4 frozen；**不写字段名、不写状态枚举、不写存储表示**；S-1 只作否定规则，**不设计 satisfaction contract**。

---

## 1. MSC-01 · Identity Law

> **Atomic Visibility Obligation（AVO）是 Notification 层中最小的、内在可独立生命周期寻址的用户可见义务单位。**

**"内在"必须保留**（Falsification #2 的 AF2-09 逼出的限定）。

**判断两个未来可见义务是否是两个 identity，不看的维度**

```
表达次数 · trigger 数量 · delivery 次数 · 消息数量 · target wording · satisfaction wording
```

**判据：M8′ Counterfactual Independence Test**

```
先排除：
  · 外部批量操作规则
  · dependency
  · 用户人为联动策略
  · presentation grouping

然后问：只改变 A 的【满足 / 取消 / 失效 / generation termination】，B 能否保持语义完整？

  YES → intrinsic lifecycle independence → 支持【两个】AVO
  NO  → intrinsic lifecycle coupling      → 支持【同一个】AVO
```

**四象限证据（Falsification #2）**

```
Satisfaction same / different  ×  Lifecycle separable / inseparable
⇒ identity 始终跟【L 轴】走，不跟【S 轴】走
```

---

## 2. 一条 AVO 能表达什么

### 2.1 可以有多次 delivery（**Atomic ≠ one-shot**）

```
1 obligation → Monday delivery → Friday delivery        （AF-07 / AF2-01 / AF2-02）
条件：这些 delivery 属于同一个【内在不可拆】的 lifecycle commitment
⇒ "原子"说的是 **identity**，不是 delivery count
```

### 2.2 可以有复合 / 分支 trigger

```
客户回复 OR 周五仍未回复                              （AF-11）
⇒ 修改 fallback branch 不改变 identity
```

### 2.3 可以有**分支式满足语义**

```
通过 → 提醒我庆祝
没通过 → 提醒我复盘                                    （AF2-05 / AF2-06）
条件：两分支互斥 ＋ 整个 lifecycle 不允许独立存在
⇒ 仍可能是【一个】AVO
```

**因此正式推翻旧表述**：

```
❌ satisfaction difference → different obligation        （已被 AF2-05／06 否掉）
✅ satisfaction difference → identity 的【证据】，但不是【决定条件】
```

### 2.4 多个 AVO 可以合并展示（＋**重要限定**）

```
2 obligations → 1 user-visible message                  （C2-11 / C2-15）
限定：presentation coalescing 本身
      【不能】证明所有 obligation 都已 satisfied / discharged     ← S-1 给出的边界
```

> 本轮**只写这条否定规则**，**不设计** Satisfaction Contract。

---

## 3. S-6 · Cardinality Reveal（无需任何字段）

```
T1  月底提醒我两次。
T2  第一次可以取消，第二次照常。
```

T2 **不是** `create another obligation`，而是**揭示 T1 中原本存在的 lifecycle independence**。

**候选判定原则**

> 后续用户反馈可以 refinement 当前对 obligation cardinality 的解释；当反馈只是**揭示原始意图中已经存在的独立生命周期**时，应视为 **cardinality reveal / refinement**，而**不是**新的 obligation creation event。

**历史处理（append-only，与既有 Historical Governance 一致）**

```
原解释            → 保留
新证据            → append refinement
current interpretation → 使用更明确的 cardinality
（不倒改过去，也不伪装成系统从一开始就知道）
```

---

## 4. 必须显式 **supersede** 的 V0.4 条款（**不是 V0.4 错了**）

> V0.5 若最终采用 AVO，就必须**显式声明**下列 V0.4 Notification 语义被新版本替代（按历史治理：后合同权威 ＋ superseded 标注）。

### S5-A · `one commitment → max one proactive notification`
```
V0.4：one active visibility commitment → default max one proactive notification
AVO ：one obligation → can legitimately require multiple deliveries（AF2-01/02、AF-07）
⇒ 若采纳 AVO，该通用 one-shot 假设必须被 supersede
```

### S5-B · `notify → discharged`
```
V0.4：notify → discharged  （不能继续作为 universal rule）
AF-07：第一次 delivery 完成，但同一 AVO 还有第二次
⇒ V0.5 至少需要：delivery ≠ automatically lifecycle completion

⛔ 到此停止：本轮【不定义】什么时候才叫 satisfaction / discharge（属 S-1 的独立 Discovery family）
```

---

## 5. **不应**被 supersede 的 V0.4 原则（继承清单）

```
Notification 不改变 Gap state
Notification 不选择 Action
Notification 不修改 scheduler order
Notification 不是第二个 Action Engine

explicit user timing 不被内部 soft burden 偷偷改写

generation semantics 仍然约束旧义务是否继续有效

history append-only

E8 ownership boundary 继续成立
```

> **AVO 是 Notification 内部 identity/lifecycle 抽象的升级，不是重写整个 Prompt Architect。**

---

## 6. MSC-01 明确**不解决**什么（Non-goals）

```
NOT YET DEFINED:
  - satisfaction criterion
  - exact discharge rule
  - trigger expression grammar
  - persistence schema
  - storage representation
  - field names
  - implementation type
  - coalescing UX limit
  - cross-session persistence
```

尤其：**`S-1 identity ≠ satisfaction criterion` 应成为下一条独立 Discovery family**，**不趁 MSC-01 顺手解决**。

---

## 7. 接受条件（**先 replay，再宣布**）

不凭"文档写好"就宣布 Contract Accepted。执行下 6 个 semantic replay：

### MSC-T01 · same satisfaction ＋ independent lifecycle → **split**
```
输入：上线这件事周一提醒一次、周五再提醒一次。周一那次可以单独取消，周五不受影响。
期望：2 identities（同 target／同满足）
```
**结果：✅ 唯一** —— 沿 L 轴分裂（＝ AF2-03）

### MSC-T02 · different satisfaction ＋ inseparable lifecycle → **same identity**
```
输入：项目通过提醒我庆祝；没通过提醒我复盘。两者只会发生一个，只能整体取消。
期望：1 identity（分支式满足语义）
```
**结果：✅ 唯一** —— 满足差异**不**触发分裂（＝ AF2-06）

### MSC-T03 · external batch cancel → **identities remain separate**
```
输入：两条都保留。但以后取消其中一个，就自动取消另一个。
期望：2 identities；联动属【操作层策略】，不并入 identity
```
**结果：✅ 唯一** —— M8′ 排除外部耦合后仍判 2（＝ AF2-09）

### MSC-T04 · dependency → **identities remain separate**
```
输入：先提醒确认预算；预算确认后再提醒上线。预算提醒取消，上线提醒继续保留、只是等条件满足。
期望：2 identities ＋ dependency edge
```
**结果：✅ 唯一**（＝ AF2-10）

### MSC-T05 · multi-delivery inseparable plan → **first delivery 后 obligation 仍 active**
```
输入：周一、周五两次提醒是一个完整计划，不能单独取消。
情形：周一那次已交付。
期望：1 obligation 且【仍 active】（剩余 delivery 未完成）
```
**结果：✅ 唯一** —— 直接演示 `delivery ≠ lifecycle completion`（S5-B 的实证）

### MSC-T06 · later independence evidence → **refinement，not creation**
```
输入：T1「月底提醒我两次」→ T2「第一次取消，第二次照常」
期望：cardinality 由 1（未定）refinement 为 2；T1 原解释保留（append），不产生"新建 obligation"
```
**结果：✅ 唯一**（＝ S-6）

**门槛：6/6 唯一**

```
Minimal Semantic Contract #1
ACCEPTED as V0.5 candidate contract
（注意：仍是 candidate；尚无 schema）
```

---

## 8. 边界

- ❌ 无字段名／无状态枚举／无存储表示／无 trigger 语法；
- ✅ 全部结论为 **candidate**；正式采用需后续 V0.5 合同阶段（含 S5-A／S5-B 的 supersede 声明）；
- V0.4 **frozen 不变**。
