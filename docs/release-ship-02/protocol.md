# SHIP-02 · Runtime Smoke 协议（v0.4.0-rc.2 → v0.4.0）

> **唯一剩余 Gate**。三组真实模型 smoke 全过 ⇒ 打 `v0.4.0` Stable。
> **不新增 V0.4 功能、不重跑整套架构证明、不动 V0.5。**
> **本协议不修改任何冻结产物**（不改 `SKILL.md`／Interface／V0.3 基线／V0.4 基线）。

---

## 0. 运行环境要求（执行前确认）

```
① 真实可运行的 Skill 环境（能真正加载 prompt-architect 这个 Skill）
② 一个真实模型（非离线规则模拟）
③ 能保留【原始输入】与【原始输出】的逐字记录
④ 运行基点：tag v0.4.0-rc.2（commit 7c0c9bd）——即本次发布候选
```

**执行命令（任何人可复现的起点）**

```bash
git worktree add --detach /tmp/ship02 v0.4.0-rc.2
cd /tmp/ship02
# 在此 worktree 中加载 Skill、跑下面三组
```

---

## 1. Runtime A · Authority

**发送（逐字）**

```
算了，还是你来定吧。
```

**上下文（必须先建立，否则无意义）**
```
前置：某 gap 已处于 CLOSED(assumed)（此前用户拒绝拍板／系统已按默认落假设）
```

**契约级期望**
```
pending-resolution-transition-contract §3.5（N10）
  "你来定 / 还是你来定吧 / 你看着办" = Authorization ≠ Value Acceptance
  ⇒ 不得仅凭该句产生 CONFIRMED
  ⇒ 后续跃迁复用既有 Authorization / T1 / T2 路径
```

**判定（PASS 条件，三者必须同时成立）**
```
① 模型把该句当作【授权】，不是"用户接受了某个具体值"
② 模型【没有】把该 gap 直接升级为 CONFIRMED
③ 模型没有凭空编造"用户已确认的值"
```

**常见 FAIL 形态（记录时对照）**
```
✗ 直接输出 "已确认：<某个值>"
✗ 声称"你已同意了 X"
✗ 报错／无法判定（属 implementation bug）
```

---

## 2. Runtime B · Notification timing（对照实验，必须成对）

**B-1 发送**
```
别忘了。
```

**B-2 发送（独立一轮）**
```
现在告诉我还差什么。
```

**契约级期望**
```
notification-policy-contract §6.2
  规则 4：任何不含时机的可见请求（含裸"别忘了"）→ condition = next_relevant_checkpoint
  规则 6：用户明确要求当场（"现在告诉我"）→ trigger = now
  （已冻结的不变式：条件已成立 ≠ 改判为 trigger=now）
```

**判定（PASS 条件）**
```
① "别忘了" → 表现为【记下承诺 / 稍后在合适时点再提】，而不是当场追问或立即打断
② "现在告诉我还差什么" → 表现为【当场结算并告知】
③ 两者行为【可区分】，且方向与上表一致（不出现对调、不出现两者都立即）
```

**要点**：不要以"措辞是否含关键词"判分，以**可观察行为**判分。

---

## 3. Runtime C · Mixed ownership（多轮）

**场景脚本（逐轮发送）**
```
轮1  帮我做一个高级 AI 官网。
轮2  给客户看的产品官网。
轮3  先做首页，其他后面。
轮4  首页交互一直比图标细节优先。
轮5  图标细节不急，但别忘了。
轮6  配色先等客户确认。
轮7  客户说暖色系。
轮8  配色就暖色。另外，改成企业版吧。
```

**必须确认的四条（任一违反即 FAIL）**
```
① Fairness 不翻用户排序      轮4 设定序后，后续轮次不得把"图标细节"提到"首页交互"之前
② Notification 不抢 scheduler 轮5 的"别忘了"不得改变任何排序或让该 gap 被提前调度
③ §11 不越界                 非 ASK 轮不得出现具体问题选择；ASK 未被调度时 §11 不介入
④ Gap state writer 不串层     状态变化只能在 Interface 语义下发生；不得由 Notification／
                              Fairness／Priority／§11 直接写 Gap 状态
```

**判定（PASS 条件）**：四条全部成立，且用户可见输出**不出现内部机制词**（如 gap／CHALLENGED／pending_resolution／commitment／debt）。

---

## 4. 证据记录规范（唯一允许的记法）

每一组按 `record-template.md` 填写，**必须包含**：

```
raw_input        逐字输入（含必要前置上下文）
model_output     逐字输出（不得改写、不得摘要）
observable       可观察判定：模型实际做了什么（不是它声称遵循什么）
contract_ref     引用的冻结条款位置
verdict          PASS / FAIL
notes            异常、歧义、或需要人类裁决之处
```

**禁止**：
```
✗ 只写结论不贴原始输出
✗ 用"看起来符合"替代可观察判定
✗ 事后美化输出
✗ 因某组 FAIL 而改写协议（应记录 FAIL 并进入修复流程）
```

---

## 5. 判定与后续（**预先写死，不得事后放宽**）

```
A PASS ∧ B PASS ∧ C PASS
        ⇒ 打 v0.4.0（Stable）

任一 FAIL（implementation / runtime bug）
        ⇒ 修复 → 新 commit → v0.4.0-rc.3
        ⇒ 不得移动 v0.4.0-rc.2 的 tag
```

**升 v0.4.0 的附带条件**：标签所指向的 commit 必须**包含本次 SHIP-02 的证据记录**，且三 Gate 仍全绿：

```
FRG-01 V0.3   MATCH 24 / DIFF 0
FRG-02 V0.4   MATCH 21 / DIFF 0
FRG-07        28/28
```
