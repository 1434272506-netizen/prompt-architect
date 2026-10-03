# SHIP-02 Evidence Record（填写模板）

> **运行基点**：tag `v0.4.0-rc.2`（commit `7c0c9bd`）
> **纪律**：原始输入与原始输出**逐字**记录；判定基于**可观察行为**；不得事后美化。

---

## 环境信息（每次运行必须齐备）

| 项 | 值 |
|---|---|
| `runtime_base_tag` | `v0.4.0-rc.2` |
| `runtime_base_commit` | `7c0c9bd` |
| `protocol_commit` | |
| `protocol_sha256` | |
| `model / model version` | |
| `Skill loader / platform` | |
| `execution timestamp` | |
| `fresh session?` | YES / NO |
| `context / preconditions` | （另见下节，逐字记录） |
| 运行目录 | （如 `/tmp/ship02`） |
| 记录人 | |

---

## 前置上下文逐字记录（**A 组不可或缺**）

> A 组依赖"该 gap 已处于 `CLOSED(assumed)`"。**只保存最后一句输入会使 A 组不可复现。**

### Runtime A setup
```
轮1 raw_input  ：
     model_output：
轮2 raw_input  ：            ← 由 Authorization 落 CLOSED(assumed)
     model_output：
轮2 后可观察状态：（是否进入"待确认假设"）
轮3 raw_input  ：            ← ★ A 测试点
     model_output：
```

### Runtime B-1 setup（fresh session = YES/NO）
```
轮1 raw_input  ：
     model_output：
轮2 raw_input  ：            ← ★ B-1 测试点："别忘了"
     model_output：
```

### Runtime B-2 setup（fresh session = YES/NO）
```
轮1 raw_input  ：
     model_output：
轮2 raw_input  ：            ← ★ B-2 测试点："现在告诉我还差什么"
     model_output：
```

---

## Runtime A · Authority

```
raw_input      ：
前置上下文     ：
model_output   ：
observable     ：
contract_ref   ：pending-resolution-transition-contract §3.5（N10）
verdict        ：PASS / FAIL
notes          ：
```

---

## Runtime B · Notification timing（成对）

### B-1 `别忘了。`
```
raw_input      ：
前置上下文     ：
model_output   ：
observable     ：
contract_ref   ：notification-policy-contract §6.2 规则 4
verdict        ：
notes          ：
```

### B-2 `现在告诉我还差什么。`
```
raw_input      ：
前置上下文     ：
model_output   ：
observable     ：
contract_ref   ：notification-policy-contract §6.2 规则 6
verdict        ：
notes          ：
```

### B 组对照结论
```
两者行为可区分：YES / NO
方向与契约一致：YES / NO
```

---

## Runtime C · Mixed ownership（多轮）

| 轮 | raw_input | model_output（逐字） | observable |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |

```
① Fairness 不翻用户排序        ：PASS / FAIL  证据：
② Notification 不抢 scheduler  ：PASS / FAIL  证据：
③ §11 不越界                   ：PASS / FAIL  证据：
④ Gap state writer 不串层      ：PASS / FAIL  证据：
⑤ 用户可见输出无机制词          ：PASS / FAIL  证据：
```

---

## 汇总

```
A ：PASS / FAIL
B ：PASS / FAIL
C ：PASS / FAIL

总判定：
  ☐ 三组全过 → 打 v0.4.0（Stable）
  ☐ 存在 FAIL → 修复 → 新 commit → v0.4.0-rc.3（不移动 rc.2 tag）
```

## 三 Gate 复核（发布前必跑）

```
FRG-01 V0.3 freeze verifier                ：MATCH __ / DIFF __      exit __
FRG-02 V0.4 baseline verifier              ：MATCH __ / DIFF __      exit __
FRG-07 README reverse-reference audit      ：claims __ / __          exit __
```
