# V0.3 冻结基线（Freeze Baseline）

> 冻结批准：2026-10-01（用户裁决）· 封版版本：**V0.3 Uncertainty Resolution Engine**
> 复算命令：`python .gh-search/freeze_v03.py`（**只读比对，漂移时非零退出**）；重新登记：`python .gh-search/freeze_v03.py --write`（**只替换 §2 哈希区，写前自动备份 `.bak`**）

## 1. 冻结范围（正式封版）

- Unknown Classification（Type A–E）+ §2.5
- ASK / SHOW / INSPECT / TEACH / DISCOVER 五动作体系 + `strategies/` 五件套
- **契约 R1–R14**（含 R14 高风险 Type C 前置 + §3.1 完整判据）
- §6.6 Decision Record（五状态 + Resolution）
- **§11.0 Action Selection**（动作选择优先，V0.3 冻结）
  - **注**：同章的 **§11.1–§11.7（Question Selection，V0.2）自 2026-10-02 起正式冻结**（此前为 Freeze Candidate；权威状态见 `tests/acceptance.md`）。
- 测试体系：专项 4 文件（unknown-known / evidence-unknown / blind-spot / high-risk-c）+ 对抗 4 文件 + 迁移回归 + 失败模式映射

## 2. 保护基线（全量文件哈希，SHA-256）

<!-- HASH-TABLE-START -->
| `SKILL.md` | 682 | `b220bc24138e4d31a5ea9268e24d2de532e395be2f8d5738db916c2684707ef7` |
| `core/uncertainty-classifier.md` | 274 | `32dcd87b3eb9e45797e6b0cc6fd49475f0ce983623e0a1ed7b66eeaa4878fd92` |
| `strategies/ask.md` | 128 | `13271961bb179552a55647c63e9675a9c3e2c4e4cdda1d019ec7d266f46057b1` |
| `strategies/show.md` | 116 | `1ceb0f2007c5240c2374e606e817f77930aeaf068646226fc88304248b64f96e` |
| `strategies/inspect.md` | 122 | `120be6b5707141086c7c6bcd2209affd02abc4613ca6f8e6ef749b0a2079f40c` |
| `strategies/teach.md` | 118 | `0f5246929de72a0de6fe375f0c01d235f9fa2f69c22e154b6dcb13c5ca064b77` |
| `strategies/discover.md` | 129 | `5fc3923624421c94e218599b7636e925b59484adc809594bc82a361c5a6463f1` |
| `docs/failure-map.md` | 199 | `54144e0f368ed5ed56e268557f275960065d94fd4dcacaf16a6c4e41c077edf8` |
| `tests/acceptance.md` | 424 | `22aed1b8c183eed279b771fc57d13aee3eaea20723ae2f9a6c2509da4b33816f` |
| `tests/cases.md` | 253 | `4e8bab226fe9ff75a6995fb370788c349b7617506cfcd127186c7f4432203442` |
| `tests/unknown-known.md` | 243 | `4b149c26fc95a7a94a887efff4eef2f448e10c802868ce41f6bdf8fa099458c2` |
| `tests/evidence-unknown.md` | 237 | `be9dcd9ebe7dc75168ce14ed5c52f43f926a3876ec8e407a1eff95f300626703` |
| `tests/blind-spot.md` | 222 | `7ead8e8fadec10e2ecb0858a01095cad24984514c52d279dedc15a37a1cb0476` |
| `tests/high-risk-c.md` | 203 | `ab486116e1ccacc58c7c38a2f9b694963007f41aca30ec4e7b8d4ad5e03890a7` |
| `tests/adversarial-2.1.md` | 182 | `44bc6f712f5da0ff1ca025111a47930bb9cc9a88eb0fb3b9f76ccfcda3545a5c` |
| `tests/adversarial-question-selection.md` | 419 | `13d9d72507950ead5406608d67816d8f9abeae89b8cc0821cd9f19e69519c6a5` |
| `tests/adversarial-merge-questions.md` | 207 | `ba17057b670c55f262ece51dae58b914f8c066fb38f601c4dc3ff052c05f1257` |
| `tests/adversarial-interview-core.md` | 251 | `1b5086715a903418f91e4793600caff843aff719e2216ca9c920ca9a30d4a010` |
| `examples/case-01-vague-video.md` | 148 | `9387dbaf900c8fb15ba7273e881e1f5c6048287ae8340af7c9ef405813472dab` |
| `examples/case-02-enough-info.md` | 72 | `189e25851931550f1422431546b3c602409f3e9445f4f4897cc3f6e09b3ec011` |
| `examples/case-03-no-idea.md` | 127 | `a620a427fa3b001b59461c4f19693bed2a498594ecc9db3fde3c522ca13f8b9d` |
| `examples/case-04-stop-rules.md` | 141 | `2632837cab955820284e9d2ce4ea62fc080b48a2cb48e2e04ec6301d08b1ae8e` |
| `examples/case-05-vague-website.md` | 136 | `2c28ba489474fd0db49ca7c3cb0eaaab425ec36157d4c291690554b5a622a773` |
| `README.md` | 403 | `9627165e3086e1dd63bdc8304966c82cbf14f22ed54dfc3b8a8d054fc00224ae` |

**合计 24 个受保护文件，5436 行。**
<!-- HASH-TABLE-END -->

## 3. SKILL.md 冻结章节哈希（异常修改模式下的重点保护对象）

| 章节 | 行区间 | sha256 | 状态 |
|---|---|---|---|
| §2.1 | 87～155 | `26e207d736b0ad747fa3bb69bded41fb1720b2fbf8b109a6634f96e8b4ad3d38` | MATCH 原始基线 |
| §3 | 159～221 | `24efa40f9b64f335ba2b4dd5c2d053cadadef22a73bb1e697703cb25a122d1cd` | V0.3.3 新基线（追加适用范围注，判据未改） |
| §6.3 | 359～372 | `8571705186f487b20712c2d8e2f25d96d9b799acf3be45d4248dfbb1d5c04b52` | MATCH 原始基线 |
| §6.4 | 374～382 | `60315aa5681c0814193e1575c4b4792a22512c922944a465cf9d1212740d3e47` | MATCH 原始基线 |
| §6.5 | 384～421 | `aef796ad3a5bda6a5c2fc00480be083b33dbb02e5eb54a8780090511819792b0` | MATCH 原始基线 |

> 复核方式：`python .gh-search/freeze_check.py`（按本表口径自动取块比对，5/5 MATCH）。

## 4. 冻结语义（异常修改模式）

冻结**不是禁止修改**，而是把修改置于证据门槛之下。任何对受保护文件的改动必须**同时**满足：

1. 新测试发现**真实冲突**（可复现失败案例）
2. **非修改不可消除**歧义（无法通过新增章节 / 契约条款解决）
3. 修改范围**最小**（能加适用范围注，就不改判据原文）
4. **全量回归**通过（专项 + 迁移 + 冻结哈希）
5. **重新冻结**并登记新哈希

**程序要求（事故后新增，硬性）**

> 冻结期的正确顺序是 **① 先登记意图 → ② 再改 → ③ 跑全量回归 → ④ 显式 `--write` 重新冻结**。
> **禁止**"改完发现不合规再补登记"。`freeze_v03.py` 默认**只读比对**、漂移即非零退出；`--write` 只替换 §2 哈希区并自动备份，**不得**用它重写文档正文。

**例外登记**

| # | 对象 | 轮次 / 日期 | 触发案例 | 改动内容 | 是否改变判据 | 新哈希 |
|---|---|---|---|---|---|---|
| **#1** | §6.5 | V0.1"采访决策缺口修复"轮 | D1 / D2 / F1 | 新增 §6.5 章节（Revision / 兼容更新 / 局部重开） | 是（新增规则，经批准） | 见 §3 |
| **#2** | §3「常见错位」 | V0.3.3，2026-10-01 | Case A / W6 与契约 R11 解释冲突 | **追加一行适用范围注**（P0 锚点口径） | **否**（判据原文未改） | `b21c73bf…` → `24efa40f…` |
| **#3** | `SKILL.md` + `README.md` | V0.3 封版后，2026-10-01 | Lead 自查（**无失败案例**） | 见下 | **否**（非冻结区，未改任何判据） | 见 §2 |
| **#4** | `README.md` | V0.4.1 阶段，2026-10-02 | Lead 自查（**无失败案例**；按"先登记再执行"**事前**声明） | 文件结构表新增 4 行 V0.4 文档入口（failure-inventory / gap-ledger-proposal / gap-ledger-replay / gap-ledger-coverage） | **否**（非冻结区，未改任何判据） | `84005fc1…`（358 行）→ `1e1a5405…`（362 行） |

> **#4 的意义**：这是**第一次按"先登记意图 → 再改 → 再重新冻结"正确顺序执行的修改**（#3 是事后补登记）。它证明该协议可执行，而非纸面要求。

| **#5** | `README.md` | V0.4.1 阶段，2026-10-02 | Lead 自查（**无失败案例**；按"先登记再执行"**事前**声明） | 文件结构表接入 V0.4.1 三份产物（proposal / replay / coverage），并把失效点计数由 32 更正为 **34** | **否**（非冻结区，未改任何判据） | `1e1a5405…` → `9ccfc1a0…` |
| **#6** | `SKILL.md` + `README.md` + `tests/acceptance.md` + `tests/adversarial-merge-questions.md` | V0.2 收口 + §11×Gap Ledger 兼容测试，2026-10-02 | **31 个失败/不唯一案例**（V0.2 破坏测试 11 例不唯一 → Q1–Q7；兼容测试 C-01～C-15 中 10 例不唯一） | ① §11.1 定位澄清（一级/二级裁界）② §11.7 追加「补充判据（约束型依赖 vs 共同决策）」③ V0.2 状态与测试标签同步 ④ 接口层验收项 | **部分**：§11 属 V0.2 层（**非** 5 个冻结章节）；冻结章节内 **5/5 MATCH、判据一字未改** | `f2adf2f8…`(674) → `b220bc24…`(682)；另 3 文件见 §2 |
| **#7** | `tests/acceptance.md` + `README.md` | V0.4.2 前置裁决，2026-10-02 | **无失败案例**（状态登记：§11 由 Freeze Candidate → **✅ 冻结**；Phase 1 → Frozen Interface v1；Phase 2 启动） | ① 冻结范围与版本状态更新 ② Phase 2 文档入口（`feedback-semantics-discovery.md`）③ §11 冻结依据登记（35/35 + 15/15 + 五零指标） | **否**（非冻结区；§11 判据未改、5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#8** | `tests/acceptance.md` + `README.md` | V0.4.2 Phase 2.1，2026-10-02 | **无失败案例**（状态登记：Phase 2 = Discovery ✅ / Transition Design ✅；新增 `feedback-transition-design.md` 入口） | ① 版本状态行更新 ② 文件结构接入 Phase 2.1 产物 ③ 注明"设计未实现为规则，暂不进验收勾选项" | **否**（非冻结区；§6.3 **未解冻**、§11 未改、5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#9** | `tests/acceptance.md` + `README.md` | V0.4.2 Phase 2.2，2026-10-02 | **无失败案例**（状态登记：Phase 1.5 Interface v2 = 🟡 Freeze Candidate；Phase 2.2 Language Mapping ✅ 30 例 + TD 20/20） | ① 版本状态行更新 ② 文件结构接入 `feedback-language-map.md` ③ 登记工程纪律（映射出问题先判"字段不足 vs 解析不足"，不改 v2） | **否**（非冻结区；未改 §11／§6.3／v2 正文，5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#10** | `tests/acceptance.md` + `README.md` | V0.4.2 Phase 2.3，2026-10-02 | **无失败案例**（状态登记：Interface v2 → **✅ 冻结**；Phase 2.3 State Extension ✅ 六字段设计 + 30 例；L-20/23/24/25/30 转固定回归） | ① 版本状态行更新 ② 文件结构接入 `feedback-state-extension-design.md` ③ 登记新的 5 例固定回归 | **否**（非冻结区；**Interface v2 冻结正文未改**、§11／§6.3 未改、5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#11** | `tests/acceptance.md` + `README.md` | V0.4.2 Phase 2.3-B，2026-10-02 | **无失败案例**（状态登记：Phase 2.3-B ✅ 30 例；**Interface v3 = 🟡 落盘候选**，待迁移测试） | ① 版本状态行更新 ② 文件结构接入 `feedback-responsibility-extension-design.md` ③ 登记 v3 冻结前置（完整迁移测试） | **否**（非冻结区；**Interface v2 冻结正文未改**、§11／§6.3 未改、未新增 Gap 状态、5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#12** | `tests/acceptance.md` + `README.md` | V0.4.2 Interface v3 迁移测试，2026-10-02 | **迁移测试发现 1 项 K5**（unaware 证伪探针）；**非 v2 回归**（K4 = 0），属 v3 候选契约缺口 | ① 版本状态行更新 ② 文件结构接入 Manifest 与迁移测试 ③ 登记"8 通过 / 1 未通过 → 不冻结" | **否**（非冻结区；**未落盘 Interface 正文**、未改 v2 冻结正文／§11／§6.3／v3 设计、5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#13（预登记）** | v3 候选设计（2 份）+ `docs/v04/gap-ledger-interface.md`（v3 并入）+ `tests/acceptance.md` + `README.md` | V0.4.2 v3 收口，2026-10-02，**按"先登记再执行"事前声明** | 迁移测试 **V3-C4 单点失败（K5 = 1）**：`unaware` 判据缺否证条件 | ① 修订 `unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness`（派生证据，不新增 Gap 状态／持久字段）② 新增 UA-01～UA-04 证伪集 ③ **Interface v3 增量并入接口正文（§9）** ④ 状态文档更新 | **是**（v3 候选契约判据一行修订；**v2 冻结正文不反向修改**、§11／§6.3／V0.3 不动） | 见 §2（重冻结） |

> **#13 执行结果**：UA-01～04 **4/4**、V3-C4 **PASS**、**K5 = 0**、无新 K4；**raw release regression 201/201**；Interface v3 **已并入并冻结**；v2 章节逐字保留。执行顺序严格为 **预登记 → 修订 → 回归 → 并入 → 重冻结**（对照 #3 的事后补登记）。

| **#14** | `tests/acceptance.md` + `README.md` | V0.4.3 二次质疑 Discovery，2026-10-02 | **无失败案例**（状态登记：V0.4.3 ✅ 36/36、K4 = 0、K5 = 1 已定位根因；新增 `pending-resolution-second-challenge-discovery.md` 入口） | ① 版本状态行更新 ② 文件结构接入 V0.4.3 产物 ③ 登记下一轮 Transition Contract 待批 | **否**（非冻结区；未写任何规则、未改 §11／§6.3／Interface v2／v3／V0.3、未新增 Type／Action／Gap 状态，5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#15** | `tests/acceptance.md` + `README.md` | V0.4.3 Transition Contract，2026-10-02 | **无失败案例**（状态登记：Contract ✅ 并入候选；PC-01～18 = 18/18、PR 36/36、PR-17 K5 消失、K4=0／K5=0） | ① 版本状态行更新 ② 文件结构接入 Contract 产物 ③ 登记"未并入冻结正文、待批准" | **否**（非冻结区；未改 `SKILL.md`／§6.3／§11／Interface v2／v3 冻结正文／V0.3；未新增 Type／Action／Gap 状态／字段；5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#16（预登记）** | Contract 设计文档 + `docs/v04/gap-ledger-interface.md`（Contract 并入 §10）+ `tests/acceptance.md` + `README.md` | V0.4.3 R-2 封口，2026-10-02，**按"先登记再执行"事前声明** | **结构性矛盾（用户发现）**：R-2 原写"保持 `CLOSED(assumed)` 仅把 `confidence` 升为 `confirmed`"，与 **v1 冻结谓词 `effective_set = CONFIRMED ∩ valid`** 冲突 → gap 进不了生效集合；且造成 `status` 与 `confidence` **争夺 authoritative truth**（双重事实源） | ① 修正 R-2 为**直接确认跃迁** `CLOSED(assumed) → CONFIRMED`（**不经 OPEN**）② 新增 **RC-01～RC-04** 探针 ③ Contract **并入接口正文 §10** ④ 状态文档更新 | **是**（仅 Contract 的 R-2 语义修正；**不改 `effective_set` 谓词、不解冻 v1／v2／v3**、不改 §11／§6.3／V0.3） | 见 §2（重冻结） |

> **#16 说明**：本次**只封 R-2 一处**，不改动 Contract 其他任何部分（六分支结构、无独立额度、material re-entry、withdrawal、meta、intent 不绕过门均已获批准）。执行顺序：**预登记 → 修正 R-2 → RC-01～04 + 相关回归 → 并入正文 → 201 raw + PC-18 + canary → 重冻结**。

| **#17** | `tests/acceptance.md` + `README.md` | V0.4.4 Priority Model Discovery，2026-10-02 | **无失败案例**（状态登记：V0.4.4 ✅ 30/30；职责边界与 `deprioritized` 定位成立；冲突 0；新增 `priority-model-discovery.md` 入口） | ① 版本状态行更新 ② 文件结构接入 V0.4.4 产物 ③ 登记 3 项待裁决 | **否**（非冻结区；未写规则、未改 §11／V0.3／Interface v1–v3／§10，未新增 Action／Type／Gap state，未设计数值评分，5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#18（预登记）** | 新建 `docs/v04/priority-layer-contract.md` + `tests/acceptance.md` + `README.md` | V0.4.4 Priority Layer Contract v1，2026-10-02，**按"先登记再执行"事前声明** | **无失败案例**（Discovery 30/30 已证明职责边界、`deprioritized` 纯调度、冲突 0；用户裁决：建层 + `priority_hint` 批准） | ① 独立建层（只调度、不产动作、不改状态、不覆盖冻结规则）② 六条原则 P1–P6 ③ 硬约束收紧为既有规则已判定必须前置者 ④ `priority_hint` 偏序规格（非数值）⑤ `expressed_priority` vs `effective_priority` ⑥ `deferred_by_capacity ≠ Interface deferred` ⑦ 12 个 Priority canary | **否**（新建独立层文档；**不改** §11／V0.3／Interface v1–v3／§10；未新增 Action／Type／Gap state；未设计数值评分） | 见 §2（重冻结） |

> **#18 说明**：Priority Layer 为**独立层**（不并入 Gap Ledger Interface 正文）。执行顺序：**预登记 → 建层 → 回归（P1–P5 30/30、§11 35/35、V0.3 priority-sensitive）→ canary（PCY-01～12）→ 重冻结**。

| **#19** | `tests/acceptance.md` + `README.md` | V0.4.5 端到端 replay，2026-10-02 | **无失败案例**（状态登记：E2E **12/12 跑到底**；E1–E6 全成立；违规/重复询问/硬约束越权/过期 hint/机制词泄漏 **全 0**；新增 `e2e-adaptive-replay.md` 入口 + 3 条残留观察移交 V0.4.6） | ① 版本状态行更新 ② 文件结构接入 V0.4.5 产物 ③ 登记 O-1～O-3 | **否**（非冻结区；未写规则、未改 §11／V0.3／Interface v1–v3／§10／Priority Contract v1，未新增 Action／Type／Gap state／字段，5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#20** | `tests/acceptance.md` + `README.md` | V0.4.6 Priority Hint Discovery，2026-10-02 | **K5 = 1（B-03 scope 歧义，非回归）**；其余全部通过 | ① 版本状态行更新 ② 文件结构接入 V0.4.6 产物 ③ 登记 O-1/O-2 收口结论与 B-03 待裁项 | **否**（非冻结区；未改 Priority Contract v1／§11／V0.3／Interface v1–v3／§10；未新增规则／字段／Action／Type／Gap state；未设计数值评分；5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#21（预登记）** | `docs/v04/priority-layer-contract.md`（+§9 增量）+ `docs/v04/priority-hint-language-discovery.md`（封口）+ `tests/acceptance.md` + `README.md` | V0.4.6 收口，2026-10-02，**按"先登记再执行"事前声明** | **B-03 K5（scope 歧义）已定位**；用户裁决三项收口 | ① **L1** `scope` 与 temporal lifetime **正交**（`scope ∈ {current_round, current_cluster, whole_task}` ＋ 可附 `valid_until`／expiry condition；**不新增 `timed` scope**）② **L2** `current_round` = **一次 scheduler action bundle 的完整生命周期**（单条 user/assistant 消息**不**自动结束）③ **L3** `deprioritized` vs `delay` 按**效果**（是否仍允许当前窗口处理）区分，**不按关键词** | **是**（Priority Layer 增量：新增 `valid_until` 调度属性 + `current_round` 结束条件 + 效果判据；**不改 §11／V0.3／Interface**，**不新增 timed scope／Gap 状态／Action／Type／数值权重**） | 见 §2（重冻结） |

> **#21 说明**：本轮只落 **3 件增量**（L1–L3）＋ **8 个 PHC canary**；随后 **V0.4.6 正式冻结**。**O-3（starvation/fairness）不进本轮**，单列下一阶段。

| **#22** | `tests/acceptance.md` + `README.md` | V0.4.7 Fairness & Starvation Discovery，2026-10-02 | **K5 = 2（同一类：`fairness vs user preference`，C-01／C-04，非回归）**；其余全部通过 | ① 版本状态行更新 ② 文件结构接入 V0.4.7 产物 ③ 登记 F1–F5 结论与 4 项待裁 | **否**（非冻结区；未改 Priority Contract v1.1／Interface／§11／V0.3；未新增字段／Gap state／Action／Type／priority score；5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#23（预登记）** | 新建 `docs/v04/scheduler-fairness-contract.md` + `tests/acceptance.md` + `README.md` | V0.4.8-A Scheduler Fairness Contract，2026-10-02，**按"先登记再执行"事前声明** | **无失败案例**（Discovery 30/30 已证明 starvation 定义与 debt identity；用户四项裁决） | ① 独立建合同（sibling of Notification Policy）② 调度层次四层 ③ F1–F6 ④ Fairness Ledger（scheduler-local，identity+generation，计数非阈值）⑤ 18 个 SFC 证伪案例 ⑥ **O-3 关闭并分裂为 A/B** | **是**（新增 Scheduler-local 观测账与四层调度层次；**不改 Priority Contract v1.1／Interface／§11／V0.3**，**不新增 Gap state／Action／Type／数值评分**，**不产生用户可见通知**） | 见 §2（重冻结） |
| **#24** | `tests/acceptance.md` + `README.md` | V0.4.8-B Notification Policy Discovery，2026-10-02 | **K5 = 2 类（`notification boundary`／`timing`，非回归）**；其余全部通过 | ① 版本状态行更新 ② 文件结构接入 V0.4.8-B 产物 ③ 登记 Q1–Q5 结论与 3 项待裁 | **否**（非冻结区；未改 Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3；未新增 Gap state／Action／Type／数值化通知频率评分；**`visibility_commitment` 仅为本层字段，不进 Scheduler**；5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |
| **#25（预登记）** | 新建 `docs/v04/notification-policy-contract.md` + `docs/v04/notification-policy-discovery.md`（封口）+ `tests/acceptance.md` + `README.md` | V0.4.8-B 收口，2026-10-03，**按"先登记再执行"事前声明** | **K5-1／K5-2 已定位**（Discovery 30/30）；用户裁决 | ① 写入 **K5-1 零表达边界**（`fairness evidence ≠ notification obligation`）② 写入 **K5-2 `next_relevant_checkpoint`**（含时机解析顺序 1–5）③ 写入 **one commitment → at most one proactive notification** ④ 10 个 **NPC canary** ⑤ **建立 Notification Policy Contract v1**（sibling of Scheduler Fairness）⑥ sibling boundary regression | **是**（新增 sibling contract 与本层字段 `visibility_commitment`；**不改 Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3**；**不新增 Gap state／Action／Type／计数器**） | 见 §2（重冻结） |

> **#25 说明**：本轮**不做新 discovery**，只封两个 K5 ＋ 建 sibling contract v1 ＋ 10 个 canary 回归。冻结成功后，**O-3 整条债视为完成**（Fairness／starvation observation／user explicit priority／notification visibility 四块齐）。

| **#25 执行结果** | `docs/v04/notification-policy-contract.md`（新建）+ `docs/v04/notification-policy-discovery.md`（封口）+ `tests/acceptance.md` + `README.md` | V0.4.8-B 收口，2026-10-03 | **无失败案例**：K5-1／K5-2 **均已关闭** | ① K5-1 零表达边界入册 ② K5-2 `next_relevant_checkpoint` 入册 ③ one commitment → one notification 入册 ④ **NPC-01～10** 全唯一 ⑤ **Notification Policy Contract v1 建立并冻结** ⑥ sibling boundary regression 通过 | **是**（新增 sibling contract 与本层字段 `visibility_commitment`；**未改** Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3；**未新增** Gap state／Action／Type／计数器） | 见 §2（重冻结） |

| **#26** | `tests/acceptance.md` + `README.md` | V0.4.9 五层 E2E replay，2026-10-03 | **无失败案例**（12/12 跑到底；E1–E8 全通过；全部 gate 指标 0；**K4=0、K5=0**） | ① 版本状态行更新 ② 文件结构接入 V0.4.9 产物 ③ 登记 O-4／O-5 为 README 澄清项 ④ 登记"下一步停止加规则、写 Final Architecture README" | **否**（非冻结区；未写规则／加字段；未改 §11／V0.3／Interface v1–v3／§10／Priority v1.1／Fairness v1／Notification v1；5 个冻结章节 5/5 MATCH） | 见 §2（重冻结） |

| **#27** | 新建 `docs/v04/v04-defect-ledger.md` + `tests/acceptance.md` + `README.md` | V0.4 D 账本 · D02 裁决，2026-10-03 | **D02 口径冲突（真实缺陷）**：裸"别忘了"在 `NA-01／NPC-02`（`trigger=now`→`notify_now`）与 `§6.2 规则 4／剧本 3／O-4`（checkpoint）之间给出**两个语义**，且 NPC-02 行内自相矛盾 | ① 建立 D 账本 ② **裁决 D02 取 B**（`trigger=condition`，`condition=next_relevant_checkpoint`）③ 关键净化：**`notify_now` 是兑现形态而非独立触发**，`trigger=now` 收窄为"用户明确要求立即说" ④ 列出传播修复 F1–F5 与最小回归 D02-A～D ⑤ 导出 D03–D10 候选 | **否**（仅新建账本＋状态登记；**未改任何冻结正文**、未动 Type／Action／Gap state／字段枚举；传播修复按裁决顺序留待后续步骤） | 见 §2（重冻结） |

| **#28（预登记）** | `docs/v04/notification-policy-contract.md` + `docs/v04/scheduler-fairness-contract.md` + `docs/v04/notification-policy-discovery.md` + `docs/v04/full-adaptive-e2e-replay.md` + `docs/v04/v04-defect-ledger.md` + `tests/acceptance.md` + `README.md` | V0.4 N 批次收口，2026-10-03，**按"先登记再执行"事前声明** | **编号碰撞（用户指出）**：我此前把本轮批次编成 `D03–D10`，与**旧审计账本固定编号**冲突（旧 D03 = PR-17/Authorization、D04 = feedback gate 原子性、D05 = External 摘要漏 `information_source`、D06 = delay/askable_set 冲突、D07 = E2 owner 取证、D08 = E3/E5 引用错误、D09 = debt 来源不透明、D10 = Discovery "30/30保持"表述）；且**原 D03 未闭合**（`算了，还是你来定吧。` ≠ 确认具体 assumed value ⇒ 不能 `CLOSED(assumed) → CONFIRMED`） | ① **改用 N01–N10 编号**，旧 D 编号原样保留 ② 执行已批准修复 **F1–F6、F7a、F8–F9**；**F7b（`≥1`）拆出 HOLD**；**N04／N07 不落** ③ 最小回归 **NR-01～NR-07** ④ 账本新设**旧审计 D03–D10 段**并标注未闭合 ⑤ 登记 **N10（R-2 条件收紧＋PR-17 重裁）为原 D03 闭合候选** | **是**（Notification Contract §4.1／§4.2／§6.2 规则 4·6／§6.3／§7.1；Fairness Contract §3.3；Discovery 追加更正；E2E O-4／O-6／`W` 行） | 见 §2（重冻结） |

> **#28 执行结果**：N08／N09 已裁并落盘；N01 ✅／N02 🟡改后落（删除"每 checkpoint 至多尝试一次"）／N03 🟡仅别名（不改 debt 语义）／**N04 ⛔ HOLD（不落 `≥1`）**／N05 🟡改后落（删除"仅 generation 变化才终止"）／N06 ✅（append-only 更正）／**N07 ⛔ HOLD（不落"重提＝兑现"）**；最小回归 **NR 7/7 唯一**、NPC 10/10 保持、**K4 = 0、K5 = 0**、错误主动提醒 0、漏兑现 0、**结构零新增**。**原审计 D03 仍未闭合**（我方 V0.4.3 的 R-2 适用**超出字面条件**，其"K5 = 0"结论需随 N10 重裁）。

| **#29（预登记）** | `docs/v04/pending-resolution-transition-contract.md` + `docs/v04/gap-ledger-interface.md` + `docs/v04/notification-policy-discovery.md` + `docs/v04/v04-defect-ledger.md` + 新建 `docs/v04/v05-architecture-candidates.md` + `tests/acceptance.md` + `README.md` | V0.4 N10 收口（原审计 D03 闭合），2026-10-03，**按"先登记再执行"事前声明** | **P1 语义所有权缺陷**：V0.4.3 把 `算了，还是你来定吧。` 判为 **R-2 confirmatory**（理由是"追认由 AI 定"）→ 直接 `CLOSED(assumed) → CONFIRMED`；**该适用超出 R-2 字面条件**（R-2 要求接受**具体值**），导致旧 `K5 = 0` 基于过宽读法 | ① **裁决 N10：Authority transfer ≠ value confirmation** ② **不改 R-2 定义**，只更正 PR-17 分类为 **Authorization** ③ PR-17 重放（**不写死后续状态**，复用既有 Authorization／T1／T2／Interface）④ RC-01～RC-03 重跑 ⑤ **NR-08 negative ＋ NR-09 positive control** ⑥ 依赖复核（含 E2E-06 边界）⑦ **K5 重确认** ⑧ 回填旧 D03=CLOSED ⑨ 旧 D01/D02 含义补齐 ⑩ 建 V0.5 架构候选（C1/C2） | **是**（Contract §3.4 更正框／**§3.5 N10 边界**／§8.1；Interface §10.5 归因更正） | 见 §2（重冻结） |

> **#29 执行结果**：**PR-17 分类＝Authorization**（不确认具体值、不产生 `CONFIRMED`）；**R-2 定义未改**；**RC-01～03 = 3/3 唯一**；**NR-08／NR-09 成对唯一**；**K4 = 0；K5 = REOPENED FOR N10 → 重确认 = 0**（旧 K5=0 **明确不作为最终证据**）；**原审计 D03 = ✅ CLOSED BY N10**；旧 **D02 = RESOLVED BY N08/N09**、旧 **D01 = OPEN BY DESIGN**；映射 **D02 ← N08+N09**、**D03 ← N10**。**未新设 transition path、未新增字段。**

| **#30** | `docs/v04/gap-ledger-interface.md` + `docs/v04/full-adaptive-e2e-replay.md` + `docs/v04/v04-defect-ledger.md` + `docs/v04/v05-architecture-candidates.md` + `tests/acceptance.md` + `README.md` | V0.4 D04–D06 closure sweep（语义澄清组），2026-10-03 | **三处口径混淆（旧审计 D04／D05／D06）**：① D04 合同一处说"禁止部分执行"、另一处允许同簇逐 Gap 过门 → **原子性作用域**未定；② D05 §10 六分支把 External 泛化为 `SUSPENDED(external_owner)`，与既有 X-4（`information_source` → 保持 `OPEN`、用户仍为决策者）冲突；③ D06 V0.4.9 剧本 7 把 `askable_set` **成员资格**与**当前调度资格**合并 | ① **CS-04**：原子性 = **per-Gap 完整门链**（≠ feedback 事务 ≠ cluster 事务），G-8.3c 改成正例 ② **CS-05**：`information_source ≠ external_owner`；§10 摘要按既有 reason 分派并**引用 X-4**（不新增第七分支／子类型）③ **CS-06**：`OPEN + deferred` **仍属 `askable_set`**，但**不参与当前正常调度**；剧本 7 措辞修正 ④ 跑 **AR-01/02 ＋ EX-01～03 ＋ DL-01～03 = 8/8 唯一** ⑤ D04–D06 一次性回填 **CLOSED** | **是**（Interface §8.1 原子性作用域 ＋ §10.2 External 行；E2E 剧本 7 措辞） | 见 §2（重冻结） |

> **#30 说明**：本轮为**用户直接裁决并指令"直接落盘"**，登记与执行**同轮**（裁决全文引用于 `docs/v04/v04-defect-ledger.md` **§七**）。
> **#30 执行结果**：**8 个 closure probes 全部唯一**｜**K4 = 0、K5 = 0**｜**未新增状态／字段／计数**｜**D04 = CLOSED（per-Gap 完整门链原子性）**、**D05 = CLOSED（`information_source ≠ external_owner`，X-4 恢复）**、**D06 = CLOSED（askable 成员资格 ≠ 调度资格）**；新洞见（`participation / information provision / decision authority` 三维）已记入 **V0.5 候选（未编号）**，**不改 V0.4 ontology**。

| **#31** | 新建 `docs/v04/release-evidence-closure.md` + `docs/v04/full-adaptive-e2e-replay.md` + `docs/v04/v04-defect-ledger.md` + `tests/acceptance.md` + `README.md` | V0.4 D07–D09 evidence repair，2026-10-03 | **三处证据链缺陷（旧审计 D07／D08／D09）**：① D07 只断言"Interface 有写权限"，**缺少逐 mutation 的 write-owner 追溯**；② D08 E3/E5 汇总**4 条引用错误**（`剧本 2 轮2` 称 SHOW 实为 ASK；`剧本 9 轮2` 称"不落 SUSPENDED"实为该轮即 SUSPENDED；`剧本 3 轮2`／`剧本 5 轮2` 被当作 SHOW 证据但并非 SHOW 轮）；③ D09 scenario 12 的 `debt=2` **无 skip reason／increment 记录**，无法证明其非 `deprioritized` 后新生成 | ① **ER-07** ownership trace（六行表）＋ **M-01～M-11 逐 mutation 完整链**（含负例 M-10）② **ER-08** 逐条打开旧引用 → **修正 4 条错引用**，重建 **E3-A／E3-B／E5-A（negative control）／E5-B（positive control）**；**无 `NOT EVIDENCED`、不补造** ③ **ER-09** scenario 12 逐轮 provenance（轮3 +1、轮4 +1、轮5 起 increment=0、轮8 generation 终止）＋ 明确 **`deprioritized` 不清零／不新增**（≠ reset to 0）④ 跑 **EV-07／EV-08／EV-09** 证据一致性探针 ⑤ D07–D09 回填 CLOSED | **否**（**只修证据链**：新增 evidence artifact ＋ 汇总行引用修正；**未改任何行为规则／字段／状态／计数**） | 见 §2（重冻结） |

> **#31 执行结果**：**EV 3/3 通过** —— EV-07 **11/11 mutation 的 final writer = Interface**（无越权 writer）；EV-08 **修正后 4/4 一致**（旧 4 条错引用已登记替换）；EV-09 **每次 +1 有合法 skip reason、`deprioritized` 后 increment = 0、`debt=2` 可由前序完整推出**（**O-5 未被混合场景违反**）。**D07 ✅ CLOSED BY ER-07｜D08 ✅ CLOSED BY ER-08｜D09 ✅ CLOSED BY ER-09**。

| **#32** | 新建 `docs/v04/historical-discovery-governance.md` + `docs/v04/notification-policy-discovery.md` + `docs/v04/v04-defect-ledger.md` + `tests/acceptance.md` + `README.md` | V0.4 D10 历史治理 ＋ D02 证据回链（收口批），2026-10-03 | **① 旧 D10**：Discovery 的**历史身份与现行规范身份未正式分开**，"30/30 保持"易被读成"所有历史结论今天仍有效"；**② 旧 D02**：行为裁决已完成但**证据未回链**（`RESOLVED ... pending linkback`） | ① 落 **Historical Discovery Governance 5 条**（append-only／candidate findings／后续合同权威／取代者须标注／**`30/30` 仅表历史执行覆盖**）② **HG-10** 文档身份探针（C-03／C-06 ＋ **未被取代对照 NB-01**）③ **D02 closure chain**（root conflict → adjudication → contract propagation → regression → structural check）④ **EL-02** 链路完整性探针 ⑤ **D10 ✅ / D02 ✅**（**不再保留 pending linkback**） | **否**（**纯文档身份治理 ＋ 证据回链**；未改任何运行时规则／字段／状态／计数；D10 不重复修改 C-03／C-06） | 见 §2（重冻结） |

> **#32 执行结果**：**HG-10 = PASS**（历史证据仍在／取代者已标注／现行来源已指明／**无静默改写**；含未被取代对照 NB-01）｜**EL-02 = PASS**（`D02 → N08/N09 → contract change → NPC-02 → NR-01～NR-07 → 现行解释` **全链无断链**）｜**D10 ✅ CLOSED BY historical-governance closure**｜**D02 ✅ CLOSED BY N08/N09 + EL-02**。
> **账本终局**：**D02–D10 全部 CLOSED**；**D01 是唯一仍 OPEN 的审计项，且本来就是 OPEN BY DESIGN**。
> **项目状态**：**V0.4 architecture + defect closure complete; release governance and final documentation remain.**

| **#33** | 新建 `.gh-search/generate_v04_baseline.py` + `.gh-search/verify_v04_release_baseline.py` + `docs/v04/v0.4-release-baseline.json` + `docs/v04/v0.4-release-baseline.md` + `docs/v04/v04-defect-ledger.md` + `tests/acceptance.md` + `README.md` | V0.4 Release Baseline Protocol（BL-01～BL-10），2026-10-03 | **D11**：V0.4 核心合同**没有独立可复核的冻结哈希**；**D12**：旧治理脚本在 `--write`／退出码／章节校验／哨兵替换上存在**治理缺陷**（曾出现"显示 DIFF 但进程仍像成功"与哨兵重复） | ① 三层分类（**normative／governance／evidence**；`release-evidence-closure` 身份 = evidence **≠** normative source）② **SHA-256 raw bytes**（file hash 权威／section hash 仅诊断）③ **V0.3 baseline 只引用不复制** ④ **新增** generator（可写，仅初始化／经批准 rebaseline）＋ verifier（**永远只读**）⑤ **退出码语义**：DIFF／MISSING／UNREGISTERED／治理违规 ⇒ **非零** ⑥ **bootstrap 五阶段**（enumerate → approval → init → immediate verify → future verify），首建**不叫 MATCH** ⑦ **prospective-only 声明** ⑧ **BL-08 反向探针** ⑨ D11／D12 回链闭合 | **是**（新增 V0.4 release baseline 记录与治理工具；**未改任何运行时规则／字段／状态／计数**） | 见 §2（V0.3 重冻结；V0.4 baseline 自 `effective_at` 生效） |

> **#33 执行结果**：**BL-04 候选清点** 20 个 artifact（normative 6／governance 3／evidence 11），inventory OK｜**BL-06** 已写 JSON ＋ Markdown（`INITIAL BASELINE`，`prospective_only = true`）｜**BL-07** 只读校验 **V0.3 MATCH 24 DIFF 0 UNREGISTERED 0** ＋ **V0.4 MATCH 20 DIFF 0 MISSING 0 UNREGISTERED 0 = PASS**｜**BL-08** 反向探针：临时副本注入 drift ⇒ **DIFF 且 exit 1**；恢复 ⇒ **MATCH 且 exit 0**｜**D11 ✅ CLOSED BY V0.4 INITIAL RELEASE BASELINE**｜**D12 ✅ CLOSED BY GOVERNANCE CHECKER REPAIR**。
> **Phase C 迭代记录（诚实记录，非缺陷）**：**尝试 #1 在 Phase D 被否决** —— verifier 检出 **2 个 UNREGISTERED**（`docs/v04/failure-inventory.md` 未分类、baseline 自身 Markdown 未列入 out-of-scope）⇒ **撤回该次初始化（不构成 baseline）**，修正 scope 后重新初始化；随后又因**本轮记录文案修正（artifact 计数 19→20）**与 **V0.3 哈希表机械刷新**触发**两次经批准的 rebaseline**（`--reason`）→ 最终 **baseline-3**。这些动作本身就是 **D12 修复后的治理工具正常工作的证据**（DIFF／MISSING／UNREGISTERED 均能非零退出，且初始化与验证分权）。

| **#34** | `docs/v04/README.md`（D01 Final Architecture README）＋ 新建 `.gh-search/verify_readme_reverse_refs.py` ＋ `docs/v04/gap-ledger-interface.md`（CS-06 normative home 补齐）＋ `docs/v04/v04-defect-ledger.md` ＋ `tests/acceptance.md` ＋ `README.md` | V0.4 D01 ＋ Final Release Gate（FRG-01～08），2026-10-03 | **D01**：`docs/v04/README.md` 仍是早期章程（"本轮只做破坏测试、不设计规则"），不适合作当前架构入口；**FRG-07 另抓到真实缺陷**：**CS-06 的传播修复不完整**（D06 澄清只落在账本与 E2E 措辞，**从未落进 Interface 正文**） | ① 写 Final Architecture README（17 节 ＋ **Appendix A · 28 条 claim index**）② 早期章程**显式标注 Superseded** ③ **补 CS-06 normative home**（Interface §1.2 `OPEN + deferred` 成员资格 ＋ `delay ≠ remove_from_askable_set`）④ 新增 **FRG-07 只读审计器**（claim → source ＋ anchor 逐条校验）⑤ 跑 **FRG-01～08** ⑥ **D01 CLOSED** ⑦ README 纳入 V0.4 baseline（governance 类）→ 经批准 **rebaseline-4** | **是**（新增 Final README 与审计器；**Interface 补一条澄清**；README 纳入 baseline scope） | 见 §2（V0.3 重冻结；V0.4 rebaseline-4） |

> **#34 执行结果**：**FRG-01** V0.3 `MATCH 24/DIFF 0/UNREGISTERED 0` ✅｜**FRG-02** V0.4 `MATCH 21/DIFF 0/MISSING 0/UNREGISTERED 0`（**当前 baseline 见 manifest `baseline_id`**；README 入 scope）✅｜**FRG-03** EV-07/08/09 PASS ✅｜**FRG-04** HG-10 PASS ✅｜**FRG-05** EL-02 PASS ✅｜**FRG-06** D02–D12 CLOSED ✅｜**FRG-07** **28/28 claims 可追**（审计器首跑抓出 3 条问题：**1 条真实缺陷**（CS-06 未落 Interface 正文，已补 normative home）＋ 2 条引用错误，均已修）✅｜**FRG-08** README 入 baseline ＋ rebaseline ＋ 最终 verifier PASS ✅。
> **终局**：**D01 ✅ CLOSED BY FINAL ARCHITECTURE README** → **D01–D12 ALL CLOSED** → **V0.4 RELEASE READY**。

> **#13 说明**：本次**先登记、后执行**（对照 #3 的事后补登记）。执行范围严格限定为"一个失败 → 一个最小原因 → 一个最小修订"，不顺手优化任何其他规则。

> **#6 性质（用户裁决原文）**：**"合法内容变化，但流程违规"** —— 内容经 35/35 回归、§11.6/§11.7 冲突验证、V0.1 五节 MATCH 验证；但发生在宣布封版**之后**且未先登记。**处置：不回滚，补登记 + 重冻结。**

**#6 明细**

- **触发证据**：V0.2 破坏测试 23 例（11 例不唯一 → Q1–Q7）；合并提问 12 例（M3/M5/M9 约束型依赖反例）；§11 × Gap Ledger 兼容测试 15 例（原 10 例不唯一）。
- **改动清单**：`SKILL.md` §11.1 收窄为二级裁界、§11.7 增加边界判据；`README.md` V0.2 变更记录与接口层入口；`tests/acceptance.md` §11/接口层验收项、冻结候选状态、哈希基线口径更正；`tests/adversarial-merge-questions.md` 固定回归标签。
- **回归证据**：Question Selection **23/23**、合并提问 **12/12**、采访核心 **21/21**、§2.1 **12/12**、Golden Case 0 命中；5 个冻结章节哈希 **5/5 MATCH**。
- **影响评估**：4 个文件均**不在**冻结章节内；冻结章节内容零改动；新增接口层文件 `docs/v04/gap-ledger-interface.md` 不修改 §11 / Model / V0.3 判据。

**#3 明细（如实登记，不作为规范例外）**

- **现象**：宣布封版**之后**，Lead 又做了两次文档编辑 —— ① `SKILL.md` §10 把"V0.2 候选"一行替换为"V0.4 候选"（路线图指针，指向 `docs/v04/README.md`）；② `README.md` 加入封版状态表、V0.4 章程入口与 V0.3.4 相关文件行。
- **新旧哈希**：

| 文件 | 封版时 | #3 之后 |
|---|---|---|
| `SKILL.md` | `c603487d…` | `f2adf2f8…` |
| `README.md` | （封版时快照） | `84005fc1…`（357 行） |

- **性质**：**流程瑕疵** —— 未走五条件（尤其缺"新测试发现真实冲突"，因为本来就没有冲突；纯属文档同步本应在封版前完成）。
- **影响评估**：两个文件都**不在**冻结章节（§2.1 / §3 / §6.3 / §6.4 / §6.5）内，5 个冻结章节哈希 **5/5 MATCH**；其余 22 个受保护文件哈希未变。
- **处置**：① 保留两次编辑（回退会造成文档与 V0.4 阶段脱节）；② 在本表登记，新值写入 §2 基线；③ **自本条起，冻结后对任何受保护文件的编辑（含非冻结区）都必须先登记、再执行。**

## 5. 冻结流程事故记录（2026-10-01，已修复）

**事故 A：复算命令实为"洗基线命令"**
- **现象**：旧版 `freeze_v03.py` 每次运行都会**直接覆写 `docs/freeze-v0.3.md`**，且无比对、无校验、无失败退出 —— 它把**当前文件状态登记成"新基线"**。一名 V0.4 成员按文档写明的"复算命令"执行后，基线被静默刷新。
- **严重性**：**高**（任何人跑一次就能把任意改动合法化，冻结语义事实上失效）。
- **修复**：改为**只读比对器**（默认只报告 + 漂移**非零退出** + 仅 `--write` 才登记 + §3 状态列真实比对）。

**事故 B：`--write` 用模板覆盖了手写正文**
- **现象**：修复 A 之后的 `--write` 仍会**重写整篇文档**，把 §4 的人工例外登记（含 #3 明细与事故记录）替换成脚本模板，文档从 ~150 行退回 90 行 —— **同类缺陷第二次发作**。
- **严重性**：**高**（工具在"人写的内容"上做无备份覆写，属数据丢失）。
- **修复**：`--write` 改为**只替换 §2 哈希表区域**（以 `<!-- HASH-TABLE-START/END -->` 界定），**永不重写正文**；写前自动生成 `.bak` 备份；找不到哈希区则**拒绝写入**并非零退出。

**验证证据（非目测）**

```
制造 1 处漂移（README.md 追加空行）
  → README.md DIFF   summary: MATCH=23 DIFF=1   **退出码 1**
还原
  → summary: MATCH=24 DIFF=0                    **退出码 0**
```

**教训（长期生效）**：冻结期的**验证工具本身也必须受约束** —— 只读工具不得有写副作用；写操作必须①显式 ②限定范围 ③先备份。**任何"自动登记"都必须能被手写内容所否决。**

## 6. 已冻结版本链

| 版本 | 定位 | 状态 |
|---|---|---|
| V0.1 | Interview Control（采访控制层） | ✅ 冻结 |
| V0.2 | Question Selection（问题选择层，§11.1–§11.7） | ✅ **冻结（2026-10-02）**——原 Freeze Candidate 的唯一保留理由（与 Gap Ledger 状态生命周期耦合风险）已由接口层消解 |
| **V0.3** | **Uncertainty Resolution Engine（不确定性消解层）** | ✅ **本次冻结** |
| V0.4 | Adaptive Interview（反馈适应层） | 🚧 进行中（**Phase 1 Gap Ledger = ✅ Frozen Interface v1**；**Phase 2 Feedback Semantics = 🚀 已启动**，Discovery 第一轮 30 例完成、未写规则） |

> **状态口径（用户裁决 2026-10-02）**：`docs/freeze-v0.3.md` 是**版本冻结历史说明**，`tests/acceptance.md` 是**当前验收状态**；两者冲突时**以 acceptance.md 为准**。

## 7. V0.4 边界与已知发现

**边界声明（重要）**：**`docs/v04/**`、`docs/migration-*.md`、`docs/r14-rerun.md` 不属于冻结范围**，也**不进 §2 基线**。
理由：它们是 V0.4 的活动产物（破坏测试、失效点总账）。冻结它们会导致"每写一份文档就要重新冻结一次"，反而贬损冻结语义。
**V0.3 的冻结对象是"规范与测试"**（`SKILL.md`、`core/`、`strategies/`、`tests/`、`examples/`、`README.md`），**不含研究 / 阶段文档**。

- **B5（SHOW 无反应按未答处理）**：属**交互持续性**问题，不归不确定性分类 → 归入 V0.4「SHOW 无反应」（用户裁决）。
- 剩余盲区（`docs/failure-map.md`，12 条：B1–B6 完全无支撑 + B7–B12 部分支撑）**不阻断 V0.3 冻结**，按性质分流到 V0.4。
- V0.4 第一轮破坏测试结果见 [`docs/v04/failure-inventory.md`](v04/failure-inventory.md)（**34 个真失效点** —— 该数字经两次更正：24 → 32 → **34**，最终以 `\.gh-search/count_cases.py` 的逐文件核对为准：38 例 − 4 例对照）。
- **V0.4.1（Gap Ledger 设计）** 见 [`docs/v04/gap-ledger-proposal.md`](v04/gap-ledger-proposal.md)（Gap Entity + 七态生命周期）、重跑验证 [`gap-ledger-replay.md`](v04/gap-ledger-replay.md)、独立覆盖复核 [`gap-ledger-coverage.md`](v04/gap-ledger-coverage.md)。
  - **设计要点留痕**：生命周期由六态扩为**七态**（新增 `SUSPENDED`），`kind` 新增 `conflict_group` —— 均为 V0.4 设计产物，**不影响 V0.3 冻结内容**。
- **V0.4 Phase 1（Gap Ledger Interface）** 见 [`docs/v04/gap-ledger-interface.md`](v04/gap-ledger-interface.md)（Patch v1：有效/可问集合谓词、`validity_state` 三态、§11.2 三出口映射、重复询问定义、优先级声明、§11 消费契约）。
  - **兼容性验证**：[`docs/v04/gap-ledger-x-v11-compat.md`](v04/gap-ledger-x-v11-compat.md) —— C-01～C-15 兼容案例（Patch v1 后 **15/15 唯一**，重复询问 0）+ 新增固定回归 **I-01～I-12**（12/12 唯一，覆盖 `CHALLENGED` / `INVALIDATED` / `CLOSED(partial)` / `supersedes`）。
  - **边界**：接口层**独立于 §11**，不修改 §11 判据、不修改 Gap Model 正文、不重新定义 Type、不新增 Action。
- **V0.4.2（Feedback Semantics）第一轮** 见 [`docs/v04/feedback-semantics-discovery.md`](v04/feedback-semantics-discovery.md)：**30 个反馈语句破坏测试**（F1 授权 / F2 无法回答 / F3 拒绝投入 / F4 否定 / F5 修正），**未写规则**。结果：可承接 **6** / 半承接 **8** / **不可承接 16**；**8 项新语义**（授权、风险门、`unaware`、决策权不在场、`deprioritized`、否定目标、`reset` 范围、`split_feedback`）；**10 条缺失状态转换**；三个验收错误命中：**E1=8、E2=6、E3=10**。
  - **待裁决**：是否触碰冻结 §6.3 的**字面授权清单**（FS-06/FS-10/FS-15 与既有 F2-02/F2-03/S-01 同源，Phase 2 单独无法解决）。
- **V0.4.2 Phase 2.1（Feedback Transition Design）** 见 [`docs/v04/feedback-transition-design.md`](v04/feedback-transition-design.md)：**只设计、不写 SKILL**。产出 **T2 风险门（Effective Authorization）→ T7 否定目标 → T1 授权作用域** 三个状态模型 + **20 个破坏案例**（TD-01～TD-20）+ **7 个新字段**，规范落入 [`gap-ledger-interface.md`](v04/gap-ledger-interface.md) **Interface v2 §8**。
  - **裁决落地**：**不解冻 §6.3**——§6.3 负责"用户是否交出判断权"，风险门负责"AI 是否有资格接受"，两层分离；风险门放在接口层。
  - **承接统计**：现状可承接 **6** / 需新增字段 **6** / 需新增字段 + 新转换 **8**（合计 20）。
  - **冻结影响**：**零触碰**——§2.1／§3／§6.3／§6.4／§6.5、§11.1–§11.7、V0.3 规则、Gap Model 正文均未改动；R6／R14 仅被**读取**作为风险门输入。
  - **延期**：`refused / unable / evaded` 语言分类（Phase 2.2）、`pending_resolution` 二次质疑计数、`deprioritized` / `reset_scope` / `reverted_to` / `revision_scope` / `pending_external` / `unaware`。
- **V0.4.2 Phase 2.2（Feedback Language Mapping）** 见 [`docs/v04/feedback-language-map.md`](v04/feedback-language-map.md)：**只设计、不写 SKILL**。产出三层映射契约（Layer 1 表面表达族 → **候选槽位**；Layer 2 上下文解析 `target`/`scope`；Layer 3 契约输出）+ **30 个边界案例**（授权 10 / 否定 10 / 修正 10，L-01～L-30）+ **TD-01～TD-20 回归 20/20 通过**。
  - **关键验证**：同一句"不要这个"落在 `proposal`（L-14）或 `artifact`（L-15）；同一句"你看着办"在语气项 passed（L-10）、在费用项 **blocked**（L-04）→ **词面相同、跃迁相反**，证明 target/scope 是**状态量**。
  - **唯一性**：30 例中 **25 唯一**（23 直接 + 2 流程唯一）；**5 不唯一全部为已延期字段缺失（4）或语句复合（1），语义解析不足 0 例**。
  - **纪律**：映射层未回头修改 **Interface v2**（v2 = 🟡 Freeze Candidate），也未申请新字段——缺的全部是已明确延期的 Phase 2.3 项。
  - **冻结影响**：**零触碰**（§2.1／§3／§6.3／§6.4／§6.5、§11.1–§11.7、V0.3 规则、Gap Model 正文均未改动）。
  - **转正**：**Interface v2 已正式冻结（2026-10-02 用户裁决）**——门槛：未改 §11／未改 §6.3／未新增 Type／未新增 Action／未把 Layer 1 词面直接映射状态／失败暴露为字段缺口而非规则缺陷／TD 20/20／L 30 例。
- **V0.4.2 Phase 2.3（Feedback State Extension）** 见 [`docs/v04/feedback-state-extension-design.md`](v04/feedback-state-extension-design.md)：**只设计、不写 SKILL**，**未修改 Interface v2 冻结正文**。产出 **六字段设计**（A 组先做：`reset_scope`／`revision_scope`／`reverted_to`；B 组设计批准暂缓：`deprioritized`／`pending_external`／`unaware` ＋ `feedback.intent` 分类）+ **30 个案例**（reset 8／revert 5／revision scope 5／external owner 4／unaware 4／refused-unable-evaded 4）+ 一处解析契约补充（复合语句分解）。
  - **结果**：**30/30 均有唯一裁定路径**（27 直接 + 3 流程唯一）；**Phase 2.2 遗留的 5 个不唯一案例全部关闭**。
  - **新增固定回归（用户裁决）**：**L-20（reset）／L-23（revert）／L-24（revision scope）／L-25（split feedback）／L-30（revision+conflict）**——今后任何字段改动必须继续通过。
  - **落盘形态**：本设计即 **Interface v3 候选**（v2 之上纯增量），待批准后才并入接口正文。
  - **冻结影响**：**零触碰**（§11／§6.3／Interface v2 冻结正文／V0.3 规则／Gap Model 正文均未改动；未新增 Type／Action）。
- **V0.4.2 Phase 2.3-B（Feedback Responsibility Extension）** 见 [`docs/v04/feedback-responsibility-extension-design.md`](v04/feedback-responsibility-extension-design.md)：**只设计、不写 SKILL**，**未修改 Interface v2 冻结正文**。
  - **第一组 · 责任边界**：`pending_external{owner, reason, resume_condition}` + **`suspension_reason: external_owner`**（**不新增 Gap 状态**，继续用 `SUSPENDED`）—— **10 例，10/10 唯一**。边界：`reason=information_source` 时用户仍是拍板人（保持 `OPEN`）；**外部方授权不替代用户授权**；无 owner ≠ `pending_external`。
  - **第二组 · 认知边界**：`feedback.intent: unaware｜unable｜refused｜evaded`（**属性，非 Gap 状态**）—— **20 例，20/20 唯一**；`topic_presented` **由既有字段派生**（`attempts ≥ 1 ∨ history 含 TEACH/SHOW`），**不新增字段**。
  - **核心证明**：同一句"不知道"，靠状态量分别判为 `unaware`（未呈现过）／`unable`（已呈现且承认要决定）／`refused`（明确不承担）／`evaded`（无产出且绕开）——**措辞相同、跃迁相反**。
  - **Interface v3（落盘候选，不冻结）** = A 类三字段 + `reverts` 反向边 + B 类 `pending_external`/`suspension_reason` + `feedback.intent` 四态。**冻结前置**：完整迁移测试（v2 全量 C-01～C-15、I-01～I-12 ＋ Phase 2 全部 L／TD ＋ 2.3-A/B 六十例）。
  - **暂缓**：`deprioritized`（→ Priority Layer）、`pending_resolution` 二次质疑计数（待 `feedback.intent` 落地）。
  - **冻结影响**：**零触碰**（§11／§6.3／Interface v2 冻结正文／V0.3 规则／Gap Model 正文均未改动；未新增 Type／Action／Gap 状态）。
- **V0.4.2 Interface v3 迁移测试** 见 Manifest [`interface-v3-migration-manifest.md`](v04/interface-v3-migration-manifest.md) 与结果 [`interface-v3-migration-test.md`](v04/interface-v3-migration-test.md)：**未落盘 Interface 正文、未改任何冻结内容**。
  - **Manifest 数字修正**：上一轮汇报的"约 130 例"错误；按清单相加为 **Raw 167**（V0.4 范围）／**201**（含 V0.1–V0.3 基线 34）；精确别名簇 **28**（覆盖 **59** 例，显式标注、不静默去重）→ **唯一场景 136**（全量 170）；**固定回归 5**、**canary 4**。另登记 **ID 冲突**：2.3-A 与 2.3-B 都用 `EXT-nn` → 本 manifest 记为 `2.3A-EXT-nn` / `2.3B-EXT-nn`。
  - **K 分类（167）**：**K1 48 / K2 48 / K3 71 / K4 = 0 / K5 = 1**。K4 通过 6 个反回归假说攻击（R-1～R-5 未成立）。
  - **四条历史不变量**：A 历史不可覆写、B 当前值唯一、C reset 不删历史、D local revision 不扩大闭包 → **全部通过**。
  - **`pending_external` 恢复路径**：V3-C2 suspend→resume 五问（恢复状态／信息性质／attempts 保留／回 askable／是否仍需用户确认）**5/5 唯一**；**外部方授权不替代用户授权**（EXT-07 边界保持）。
  - **跨轮 intent 变化**：`unable → refused`（及反向）**允许且不覆盖历史**，intent 是**事件属性**而非用户标签 → 通过。
  - **唯一阻塞项（K5 = 1）**：`unaware` 证伪探针 —— "系统未呈现过 + 用户显式表明知道"时，现行契约（`unaware ⟺ ¬topic_presented`）与"显式认知"给出**两个合法解释**。最小修订一行：`unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness`（按 #13 预登记执行）。
  - **冻结门槛（首轮）**：9 项中 **8 通过 / 1 未通过** → 当时 v3 未并入正文、未冻结。
- **V0.4.2 v3 收口（例外 #13，先登记后执行）**：
  - **修订执行**：`unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness`（`user_evidences_awareness` = 用户明确承认该决策存在，**或**能主动描述其选项／取舍／后果；**派生证据，不新增 Gap 状态／持久字段**）。落盘：[`feedback-state-extension-design.md`](v04/feedback-state-extension-design.md) B-2、[`feedback-responsibility-extension-design.md`](v04/feedback-responsibility-extension-design.md) §2.3。
  - **证伪集 UA-01～UA-04**：**4/4 唯一**；**V3-C4 → PASS**；**K5 = 0；无新 K4**。受影响的 unaware／unable 既有案例重跑 **20/20 唯一**。
  - **Interface v3 并入正文**：[`gap-ledger-interface.md`](v04/gap-ledger-interface.md) 新增 **§9**（9.1 四条历史一致性不变量 I-1～I-4｜9.2 `reverted_to` + `reverts` 反向边 V-1～V-3｜9.3 `reset_scope` R-1～R-3｜9.4 `revision_scope` S-1～S-2｜9.5 `pending_external` + `suspension_reason` X-1～X-4｜9.6 `feedback.intent` 四态 + 修订判据 N-1～N-3；共 19 条规则）。**v2（§1–§8）逐字保留**，为纯增量并入。
  - **Release regression（raw 口径，按用户裁决）**：**201/201**（B0 34 + B1 27 + B2 80 + B3 60）；canary V3-C1／C2／C3／C4 ＋ UA-01～04 **全 PASS**；**K4 = 0、K5 = 0**。`170 unique` 仅作覆盖统计，不替代 release regression。
  - **状态**：**Interface v3 = ✅ 已并入并冻结（2026-10-02）**。
  - **冻结影响**：§11／§6.3／V0.3 规则／Gap Model 正文**均未改动**；v2 冻结章节逐字保留；`SKILL.md` 仍为 681 行未动。
  - **下一步（已批准，待启动）**：`pending_resolution` 二次质疑语义设计（计数不是主变量，**反馈意图才是**）；`deprioritized` 继续延期至 Priority Layer。
- **V0.4.3 `pending_resolution` Second-Challenge Discovery** 见 [`docs/v04/pending-resolution-second-challenge-discovery.md`](v04/pending-resolution-second-challenge-discovery.md)：**只做破坏测试，不写规则**；未改 `SKILL.md`／§6.3／§11／Interface v2／v3／V0.3，未新增 Type／Action／Gap 状态。
  - **规模**：**36 例**（Revision／Unable／Refused／Authorization／Challenge／External dependency 六分支各 6 例），每例记录 9 项（含"计数必要性"与 K 判定）。
  - **结果**：**36/36 有明确分析结果**；**K4 = 0**；**K5 = 1**（PR-17）；K1／K2／K3 = 6／25／5。
  - **核心假设判定**：**"第二次质疑不是次数问题，而是反馈意图问题"成立**——旧"一次确认额度"**误伤 14 例**（Revision 链、Challenge 链、阻塞项多轮降维、外部恢复）、**无作用 22 例**、**必要 0 例**；六分支出口互不相同（Revision 有值→CONFIRMED；无值→索取；Unable→降维；Refused→assumed 或保持 OPEN；Authorization→过 T2 门；Challenge→维持 pending／撤回→VALID；External→SUSPENDED 可恢复）。
  - **K5-1 根因（PR-17）**：`CLOSED(assumed)` 的**重开入口未定义**（"已 assumed 的 gap 在用户回来说'还是你来定'时，是重开走授权还是终态不重开"）。与 §6.3 无关（不是追问问题），**不需新增状态**，只需在下一轮的 Transition Contract 补一行入口规则。
  - **Q4 结论**：**没有**一例迫使新增 Gap 生命周期状态；发现 **3 个 intent 子型**缺口（质疑撤回→VALID；meta 反馈→不触状态机；条件性放弃→用 `revision_scope`／`resume_condition` 表达）。
  - **下一轮（待批准）**：**Pending Resolution Transition Contract**——以 `feedback.intent` 替换"确认额度"；补 `CLOSED(assumed)` 重开入口、`Challenge` 撤回子型、`meta` 不触状态机。
- **V0.4.3 Pending Resolution Transition Contract** 见 [`docs/v04/pending-resolution-transition-contract.md`](v04/pending-resolution-transition-contract.md)：**设计阶段 → 并入候选**（本轮**未并入冻结正文**）；未改 `SKILL.md`／§6.3／§11／Interface v2／v3／V0.3，未新增 Type／Action／Gap 状态／字段。
  - **模型（按裁决收紧）**：两段式 —— `intent dispatch`（**选跃迁族**）→ `target / scope / risk / blocking / provenance / resume_condition`（**定具体出口**）；**非 `intent → state` 一跳映射**（同一 `Authorization` 在普通项 assumed、在 R6 项 blocked）。**废弃**"剩余确认次数 → 是否还能再问"局部模型。
  - **计数口径（限定）**：Contract **不自带计数器**；`pending_resolution` **不新增独立额度**；既有 `unable`／`evaded`／`no_signal` 计数**仍归其原冻结规则**（**未改写**）。
  - **K5-1 修复 · `CLOSED(assumed)` 重进四类**：**R-1 material**（改变决策 → 重开走正常处理）／**R-2 confirmatory**（不重开，`confidence: assumed → confirmed`，无 `OPEN→CLOSED` 抖动）／**R-3 无决策意义**（状态不变）／**R-4 原值已被 supersede**（按现有状态）。**PR-17 的 K5 由此消失**（判为 R-2）。
  - **G-1 质疑撤回**：三条件（无新值 ∧ 明确撤回 ∧ 原值仍在）+ 恢复原 authoritative value + 历史保留 `challenged → withdrawal`。**G-2 meta feedback**：`target = interaction_process`，状态不变，**不是第七种业务 Intent**，不新增状态。
  - **验收**：PR **36/36** 保持｜**PC-01～PC-18 = 18/18 唯一**｜**PR-17 K5 消失**｜**K4 = 0、K5 = 0**｜不变量 **A（无独立额度）／B（intent 不绕过门）／C（可重处理且历史不删）** 全部通过。
  - **下一步（待批准）**：Contract **并入接口正文**（届时走 `登记 → 并入 → 全量回归 → 重新冻结`）。
- **V0.4.3 R-2 封口 + Contract 并入正文（例外 #16，先登记后执行）**：
  - **发现的矛盾（用户）**：R-2 原写"保持 `CLOSED(assumed)` 仅把 `confidence` 升为 `confirmed`"，与 **v1 冻结谓词 `effective_set = CONFIRMED ∩ valid`** 冲突——该 gap 仍进不了生效集合；且 `status` 与 `confidence` 会**争夺 authoritative truth**（双重事实源）。
  - **最小修复（已执行）**：R-2 改为**直接确认跃迁** `CLOSED(assumed) → CONFIRMED`（**未经 OPEN**）+ `confidence := confirmed` + `provenance += user_confirmed_after_assumed`；历史只追加。**未改 `effective_set` 谓词、未解冻 v1／v2／v3**，并仍禁止无意义的 `OPEN → CLOSED` 抖动。
  - **确立原则**：**`status` 决定需求生命周期；`confidence`／`provenance` 只描述"这个状态为什么成立"**——不允许 `confidence` 反向改写生命周期意义。
  - **探针 RC-01～RC-04**：**4/4 唯一**；PC-02 更新后唯一；依赖面重跑（`effective_set`／`CLOSED(assumed)`／`CLOSED(partial)`／Revision+`reverts`／§11 消费契约）**全部唯一**。
  - **并入**：[`gap-ledger-interface.md`](v04/gap-ledger-interface.md) 新增 **§10 Pending Resolution Transition Contract**（两段式模型、六分支骨架、R-1～R-4、G-1／G-2、Release Gate 分栏）。**v2（§1–§8）与 v3（§9）逐字保留**。
  - **Release Gate（分栏，用户要求）**：**Base raw 201/201**｜**Pending Contract 18/18**｜**R-2 probes 4/4**｜**V3 canaries PASS**｜**K4 = 0**｜**K5 = 0**（**PR-17 的 K5 消失**）。
  - **状态**：**Contract = ✅ 已并入接口正文并冻结（2026-10-02）**；`pending_resolution` 自 Phase 1 遗留的"额度"债**正式结清**。
  - **冻结影响**：`SKILL.md`（仍 681 行未动）／§6.3／§11／Interface v2／v3 冻结章节／`effective_set` 谓词／V0.3 **均未改动**；未新增 Type／Action／Gap 状态／字段。
- **V0.4.4 Priority Model Discovery** 见 [`docs/v04/priority-model-discovery.md`](v04/priority-model-discovery.md)：**只做破坏测试，不写规则**；未改 §11／V0.3／Interface v1–v3／§10，未新增 Action／Type／Gap state，**未设计数值评分**。
  - **规模**：**30 例**（组 1 用户显式优先级 6／组 2 blocker×降权 6／组 3 risk×priority 6／组 4 dependency×priority 6／组 5 多 action 竞争 6），每例记录 9 项。
  - **结论 A · 职责边界**：**Priority 层是"调度器"，不是"决策器"**——输入 = active gaps（state／blocking／risk／dependency）＋ 已由 V0.3 §11.0 选出且经 R4／R6／R14 过滤的动作集合 ＋ 用户显式优先级 ＋ 同轮容量（1–3）；输出 = **有序 action 队列**。禁止：决定"做不做"、覆盖 R4／R6／R14、**改写 gap 状态**、设计数值评分。
  - **结论 B · `deprioritized`**：**应作为纯调度属性**——但必须与"**延后**（delay → `OPEN+deferred`）"和"**放弃**（Refused → assumed）"区分。三条边界：① 降权**不能作用于阻塞／R6／高风险 C**（被硬约束吸收，不改状态：P2-01／P2-05／P2-06）；② 上游降权后下游重评由 Interface §9 负责，**不属 Priority 层**（P4-06）；③ `deprioritized` **不参与"是否继续提问"**（由 Interface §5 闸门／§10 Contract 决定）。
  - **冲突检查**：与冻结规则冲突 **0 例**。三处疑点判明非冲突：P3-06（§6.3 授权默认 vs R3 先教再问 → **TEACH 不是追问**，可共存：教完直接 assumed）、P4-01／P4-03（用户显式序 vs §11.6 上游依赖 → **依赖是硬约束**，偏好胜不过）、P5-03／P5-05（用户偏好 vs R4 顺序／R6 闭集 → 硬约束吸收）。
  - **字段需求**：**需要 1 个非数值承载位 `priority_hint`**（表达"先 A 后 B"的相对序；`deprioritized` 的 bool 表达不了）；**本层不需要持久化排序结果**（每轮派生物）。其余全部复用现有字段。
  - **待裁决**：① 是否建立 `priority_hint`（非数值、纯序）；② 确认 `deprioritized` = 纯调度属性；③ Priority Layer 职责边界是否独立成层（**暂不并入任何冻结正文**）。
- **Priority Layer Contract v1（例外 #18，先登记后执行）** 见 [`docs/v04/priority-layer-contract.md`](v04/priority-layer-contract.md)：**独立成层并冻结**（**独立层文档，不并入 Gap Ledger Interface 正文**）；未改 §11／V0.3／Interface v1–v3／§10，未新增 Action／Type／Gap state，**未设计数值评分**。
  - **裁决落地**：`priority_hint` **批准建立**（非数值偏序 + `scope`）；`deprioritized` **正式确认为纯调度属性**；Priority Layer **批准独立成层**。
  - **职责**：**只对已经合法的 active actions 做调度；不产生动作、不改变 Gap 状态、不覆盖冻结规则。** 架构：Gap Ledger → V0.3 Resolution Engine → **Priority Layer** → §11 Question Selection。
  - **六条原则 P1–P6**：硬约束 > 用户提示｜提示只排序合法候选｜`deprioritized` 只降调度优先级｜只排序 V0.3 已选动作（不重选 ASK/SHOW/INSPECT/TEACH/DISCOVER）｜一旦调度到 ASK，§11 独占问题选择与合并判断｜每轮派生排序不持久化，仅 `priority_hint` 在 scope 内保留。
  - **硬调度约束（收紧）**：**四类白名单**——当前 blocker／R6、**R14 三闸门全过的** high-risk C、**§11.6 约束型依赖**、R4 既有顺序与容量；**明确不扩大**为"所有 Type C"（PCY-02）或"所有 dependency"（PCY-03）。
  - **`deprioritized` 措辞修正**：区分 **`expressed_priority`（偏好始终记录）vs `effective_priority`（本轮实际生效）**——"用户可以表达降权，但**硬调度约束可使该降权在当前轮不生效**"。
  - **`deferred_by_capacity` ≠ Interface `deferred`**：前者为"本轮容量不足"的纯调度事实，**绝不写回 gap 状态**（PCY-04）。
  - **回归与 Canary**：原 **P1～P5 30/30**｜**§11 35/35**｜**V0.3 priority-sensitive 11/11**（`high-risk-c` HR-01～08 ＋ `unknown-known` UB-05 ＋ `blind-spot` BS-07 ＋ `evidence-unknown` EU-10）｜**Priority canary PCY-01～12 = 12/12 唯一**（含 PCY-01～04 四个硬 canary）。
  - **状态**：**Priority Layer Contract v1 = ✅ 建立并冻结（2026-10-02）**。
- **V0.4.5 End-to-End Adaptive Replay** 见 [`docs/v04/e2e-adaptive-replay.md`](v04/e2e-adaptive-replay.md)：**只跑真实多轮对话，不写规则、不加字段、不做数值评分**；未改任何冻结正文／Priority Contract v1。
  - **规模**：**12 个 4–8 轮真实会话**，6 类各 2 —— 正常收敛（E2E-01/02）／中途 Revision（03/04）／授权+风险门（05/06）／外部依赖（07/08）／Priority 与依赖冲突（09/10）／反复质疑与回退（11/12）。每轮记录 **10 项 + `Layer owner` + `Violation?`**。
  - **六条系统不变量 E1–E6 全部成立**：E1 单一 authoritative current_value｜**E2 只有 Interface 改 Gap 状态**｜**E3 只有 V0.3 决定 Action 类型**｜**E4 Priority 只排序合法 Action**｜**E5 §11 只在 ASK 被调度后工作**｜**E6 用户可见输出无内部机制词**。
  - **通过指标（全 0）**：Layer ownership violation **0**｜错误重复询问 **0**｜硬约束被 `priority_hint` 越过 **0**｜过期/无效 hint 泄漏 **0**｜authoritative 冲突 **0**｜机制词泄漏 **0**｜K5 **0**。
  - **结论**：**未发现任何"某层越权／缺接口"实例**；**未为全绿补规则**。四层协同在真实多轮下成立。
  - **残留观察（移交 V0.4.6）**：O-1 `priority_hint.scope=current_round` 的"一轮"边界未定义；O-2 "顺序偏好 + 延后决定"同句需拆为两件事（本轮由 §10 复合语句分解契约承载）；O-3 `deferred_by_capacity` 连续容量不足时的累积可见性。
  - **下一步**：**V0.4.6 Priority Hint Language & Lifecycle**（含 O-1／O-2 收口）。
- **V0.4.6 Priority Hint Language & Lifecycle Discovery** 见 [`docs/v04/priority-hint-language-discovery.md`](v04/priority-hint-language-discovery.md)：**只做破坏测试**；未改 Priority Contract v1／§11／V0.3／Interface v1–v3／§10，未新增规则／字段／Action／Type／Gap state，未设计数值评分（O-3 未进入本轮）。
  - **规模**：**30 例** —— A 顺序表达解析 8／B scope 判定 8／C 生命周期与 Revision 6／D 冲突·条件·复合 8；每例 11 项（含 **Reason for expiry** 五类枚举）。
  - **解析契约验证**：只产出**能确定的偏序边**——`优先做 A` → `A ≻ {others}`（**不脑补** B/C 之间）；`B 放后面` → `{others} ≻ B`；`A 做完再处理 B` → `A ≻ B` 且**不生成 dependency**；`A 和 B 都可以，你判断` → **不产出 relation**（属授权，不是 hint）。
  - **H1–H5 全部成立**：H1 只表达偏序｜H2 scope 不泄漏（cluster 外项 C 不受影响）｜**H3 Revision 不无脑删 hint**（C-01 目标变更后 **keep**、C-04 值失效但 gap 活跃 **keep**、C-05 `target removed` 才 expire）｜**H4 supersede/shadow 可解释**（D-05／D-06 supersede；C-06 shadow + cluster 结束自动恢复）｜**H5 不制造 dependency/blocker/risk**（A-07、D-01、D-02）。
  - **O-1 收口（结论，未落规则）**：**Interpretation B 胜出** —— `current_round` 应绑定**一次调度周期（action bundle）**，而非"某条消息"；证据 B-08（按 A 解释同一 bundle 后半段会丢 hint）。
  - **O-2 收口（结论，未落规则）**：`先 A，B 以后再说` **必须拆两事件** = `priority_hint(A≻B)` ＋ `delay(B)`（gap 状态由 Interface §3 承担）；并确立 `deprioritized` vs `delay` 判定口径：**"不管／不处理／以后再决定" → delay**；**"排后面／不急／优先级低" → deprioritized**。
  - **通过标准**：错误状态写回 0｜错误 Action 改写 0｜硬约束被越过 0｜scope 泄漏 0｜delay/refused 当 priority 0｜priority 当 dependency 0｜**K4 = 0**｜**K5 = 1**。
  - **K5-1 定位**：**B-03 `今天先做 A`** → **scope 歧义**（时间窗表达在 `{current_round, current_cluster, whole_task}` 无对应项；两读法：近似 round／最近似 whole_task）。**处置**：**未自动补字段**——现有 `source/scope/relations` **结构足够**，缺的是**判定契约**（时间窗 → 最近似 scope 映射 + 到期语义），**待裁决**（可选最小修法：`scope: timed{until}` 或"时间窗 → 取 `whole_task` + 附到期时间"）。
  - **O-3**：仍未进入本轮（属 scheduler fairness / starvation / notification policy 层）。
- **V0.4.6 收口（L1–L3 落盘，例外 #21 先登记后执行）**：
  - **L1**：`scope` 与 temporal lifetime **正交** —— `scope ∈ {current_round, current_cluster, whole_task}` ＋ 可附 **`valid_until`**／expiry condition；**不新增 `timed` scope**；结构作用域无更窄证据时取 `whole_task`，由 `valid_until` 限生命周期（**不是**"时间窗近似成 whole_task"）。
  - **L2**：`current_round` = **一次 scheduler action bundle 的完整生命周期**（起于 bundle 生成；止于全部完成／被取消／因需求状态变化失效并触发重排）；**单条 user/assistant 消息不自动结束它**。
  - **L3**：`deprioritized` vs `delay` 按**效果**区分、**不按关键词**；机械判据＝"**还能不能在当前处理窗口里顺手处理？**"（能但别优先 → `deprioritized`；现在不要处理 → `delay`）；关键词仅作 cue，不足时一次最小澄清。
  - **重跑**：**B-03 K5 消失**｜原 **30/30 保持**｜**PHC-01～08 = 8/8 唯一**｜**K4 = 0、K5 = 0**｜scope leakage **0**｜delay/prioritization 混淆 **0**。
  - **落盘位置**：[`priority-layer-contract.md`](v04/priority-layer-contract.md) **§9（v1.1 增量；§1–§8 未动）**。
  - **状态**：**V0.4.6 Priority Hint Language & Lifecycle = ✅ 正式冻结（2026-10-02）**。
  - **未新增**：`timed` scope／Gap 状态／Action／Type／数值权重。**O-3 单列下一阶段**（"一个合法但总排不上的 action，scheduler 什么时候必须主动照顾它？"）。
- **V0.4.7 Scheduler Fairness & Starvation Discovery** 见 [`docs/v04/scheduler-fairness-starvation-discovery.md`](v04/scheduler-fairness-starvation-discovery.md)：**只做破坏测试**；未改 Priority Contract v1.1／Interface／§11／V0.3，未新增字段／Gap state／Action／Type／priority score，未规定"连续 3 轮必须提升"。
  - **规模**：**30 例** —— A 真 starvation 6／B 假 starvation 6／C starvation×用户 priority 6／D fairness×hard constraints 6／E notification·可见性 6；每例 11 项（④ 连续次数为**观测数据，非规则**）。
  - **F1 最小定义**：`starvation candidate ⟺ eligible ∧ 真实原因是容量／软排序竞争 ∧ 无 hard 阻断 ∧ 跨调度周期计数 > 0`；**同一 bundle 内未轮到不算**（A-04）；"连续没执行"太宽（B 组 6 例证伪）；**不设阈值**。
  - **F2**：fairness 可修正软排序竞争；**绝不可越过** R6／R14／R4／§11.6（D 组 6/6）；用户显式 soft hint 属**未决**。
  - **F3**：`deprioritized`（"C 不急"）连 10 轮未做 ⇒ **不是 starvation**（忠实执行用户偏好）；"不急，**但别忘了**"产生 **`must_not_starve` 需求证据**（效果＝通知义务，非自动提升）；**本轮禁止新增该字段**。
  - **F4**：**scheduler fairness ≠ user notification policy** —— "应提醒但不应提升"（E-01/03/04）与"可提升但无需提醒"（A-02、C-05、D 组）同时存在，**必须分开**。
  - **F5**：**debt 绑 `gap identity + 当前 resolution generation`，不绑 action 类型** —— 同 gap `ASK→SHOW` **继承**（A-05）；全新 gap 同动作类型 **不继承**（A-06）；失效 action **不继承**（B-05）。
  - **通过标准**：ineligible 误判 starvation **0**｜fairness 越过 hard constraint **0**｜delay 误当 starvation **0**｜失效 action 继承等待债 **0**｜**K4 = 0**｜**K5 = 2（同一类 `fairness vs user preference`：C-01／C-04）**。
  - **fairness ledger 证据（不设计）**：跨轮观测需**跨轮留存**；`must_not_starve` 属 **notification policy**；**本轮未新增任何字段**。
  - **下一步（待裁决）**：① C-01／C-04 判定契约（fairness vs 用户显式 soft hint）；② 是否需要 Fairness Ledger（跨轮观测 + identity＋generation）；③ `must_not_starve` 是否成立为独立需求；④ **Fairness Contract / Notification Policy 是否独立建层**。
- **V0.4.8-A Scheduler Fairness Contract v1（例外 #23，先登记后执行）** 见 [`docs/v04/scheduler-fairness-contract.md`](v04/scheduler-fairness-contract.md)：**独立合同建立并冻结**；未改 Priority Contract v1.1／Interface／§11／V0.3，未新增 Gap state／Action／Type／数值评分。
  - **四项裁决落地**：① fairness **不自动压过仍有效的用户显式 soft hint**（可触发重新暴露，不可偷偷改序）② **Fairness Ledger** 批准为 **scheduler-local 观测账**（绑 `gap identity + resolution generation`，**计数是证据非阈值**）③ `must_not_starve` 语义成立但**归 Notification Policy**，命名 **`visibility_commitment`** ④ **Scheduler Fairness Contract 与 Notification Policy 拆为两个独立合同**。
  - **调度层次（仅调度层，非全系统优先级总表）**：`Hard scheduling constraints > explicit active user priority > fairness adjustment > ordinary soft scheduling preference`；核心原则 = **用户明确偏好可被硬约束覆盖，但不被内部软机制偷偷覆盖**。
  - **六条原则 F1–F6**：F1 仅 eligible-but-unscheduled ∧ 原因属 capacity／soft competition 才累积 debt｜F2 hard 永不因 fairness 被越｜F3 仍有效的 explicit user priority 不被自动覆盖｜F4 无显式用户排序时 fairness 可修正普通软排序｜F5 debt 绑 `gap identity + resolution generation`（**不绑 action 类型**）｜F6 ineligible 周期不增债、generation 变化旧债终止。
  - **Fairness Ledger 最小模型**：`gap_id／resolution_generation／eligible_unscheduled_cycles／last_skip_reason／last_eligible_cycle／starvation_candidate`；`resolution_generation` = 当 gap 的当前 resolution problem 被 Revision／invalidation／replacement 实质重建时前进的 **Scheduler 派生 identity epoch**，**不进 Gap 生命周期正文**，**不影响** current_value／confidence／validity／Action／§11；**`count` 是证据不是政策**（不产生"N → 必须 promotion"）。
  - **fairness 恢复资格的三种情形**：`scope expired`（含 `valid_until`）／用户取消或修改 hint／C 不再被该 relation 覆盖。此前行为 = 保持用户序 ＋ 交给 Notification Policy 判断是否重新暴露。
  - **验收**：V0.4.7 **30/30 保持**｜**SFC-01～18 = 18/18 唯一**｜**K5-1（C-01／C-04）关闭**｜公平越 hard **0**｜偷偷覆盖有效用户排序 **0**｜ineligible 累积 debt **0**｜失效/新 identity 继承旧债 **0**｜通知越权 **0**｜**K4 = 0、K5 = 0**。
  - **O-3 正式关闭** → 分裂为 **A. Scheduler Fairness**（本合同）／**B. Notification Policy**（V0.4.8-B）。
  - **下一步**：**V0.4.8-B Notification Policy**（正式引入 `visibility_commitment`）。
- **V0.4.8-B Notification Policy Discovery** 见 [`docs/v04/notification-policy-discovery.md`](v04/notification-policy-discovery.md)：**只做破坏测试**；未改 Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3，未新增 Gap state／Action／Type／数值化通知频率评分。
  - **规模**：**30 例** —— A commitment 成立与强度 6／B 时机与触发条件 6／C 一次够不够与义务解除 6／D 防骚扰与交互负担 6／E delay·deprioritized·starvation candidate 与提醒 6；每例 11 项。
  - **Q1 必须提醒**：⟺ `visibility_commitment.required=true` ∧ 触发条件成立 ∧ 事项仍存在且合法；**`starvation candidate` 单独不足以**主动提醒（NA-06／NE-01）。
  - **Q2**：**一次足够**（未回应不逐轮复催；同承诺去重；已提醒 2 次进静默）。
  - **Q3**：用户 `知道了` → **解除**（`discharged=true`，历史保留痕迹）；`先放着吧` → 降级 record_only；`那你现在做吧` → 承诺达成并解除；新 generation → 旧承诺结束。
  - **Q4 防骚扰五条**：一承诺一次／合并进既有输出／负担优先／冷静期／不催已明确 delay 且未要求可见的事。
  - **Q5**：`delay` 且无 commitment → **不允许提醒**；`delay` ＋ `别漏掉`／`但别忘` → **允许且一次为限**（delay 决定"现在不处理"，不决定"是否可以提"）。
  - **架构验证**：`promotion ≠ notification` 成立（Fairness 只提供 `starvation candidate` 作为输入）；**调度公平／用户优先权／用户可见性三维度分离**（同一事项可 `deprioritized=true` ＋ `visibility_commitment=true` ＋ 调度序不变）；30/30 例"改调度=否""改 Gap=否"。
  - **K4 = 0**；**K5 = 2 类**：**K5-1 `notification boundary`**（纯 starvation candidate＋零用户表达时是否应主动提醒）、**K5-2 `timing`**（`这个以后提醒我` 的"以后"未指定时机）。
  - **K5 处置**：**未自动补字段**——`visibility_commitment{required, trigger, discharged}` **结构够用**，缺的是**判定契约**（时机 + 零表达边界）。**待裁决**。
  - **下一步（待裁决）**：① K5-1 零表达边界；② K5-2 时机判定契约；③ 是否把 Notification Policy 立为正式 sibling contract（v1）。
- **V0.4.8-B Notification Policy Contract v1（例外 #25，先登记后执行）** 见 [`docs/v04/notification-policy-contract.md`](v04/notification-policy-contract.md)：**正式 sibling contract 建立并冻结**；未改 Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3，未新增 Gap state／Action／Type／通知计数器。
  - **第 1 条（宪法条款）**：Notification Policy **不得**改变 `ordered_actions`／promotion／gap status／Action／创建 blocker·risk；只回答"有哪些长期未处理事项现在应该让用户知道？"。输出词表封闭：`notify_now｜notify_later｜record_only｜never_notify`。
  - **K5-1 封口**：**零表达的 `starvation_candidate` 默认 `record_only`**；钉成 **`fairness evidence ≠ notification obligation`**；例外保住——**任务结束前披露未完成内容属既有交付完整性责任**，不由 starvation 触发（避免层串）。
  - **K5-2 封口**：`以后提醒我` → **`condition = next_relevant_checkpoint`**（**不是**"下一轮"、**不是**"有空位"）；机械定义＝"当前高优先流程不会被打断，且重新暴露该事项已经能帮助用户继续决策的最早自然边界"；典型 checkpoint ＝ cluster 即将结束／外部依赖恢复／阶段性交付前／准备结束任务前／用户主动要求 review；**时机解析顺序 1–5**（时间 → 条件 → 复用既有恢复条件 → checkpoint → 仅在错误时机有明显损失时最小澄清）；**默认不立刻反问"什么时候"**。
  - **`visibility_commitment` 定位原则**：**用户可见性义务 ≠ 需求状态 ≠ 调度优先级** → `true` **不意味着** priority↑／starvation debt↑／action eligibility↑。
  - **一次足够（收紧）**：**one commitment → at most one proactive notification**；仅三种情形可重建（用户明确重建 reminder／新 resolution generation／用户明确要求重复或条件性提醒）；**禁止**"第 1 次 → 第 2 次 → 冷静期"式次数债。
  - **delay 四象限**（正式入册）：否·否＝正常处理无义务｜否·是＝正常处理但须满足可见承诺｜**是·否＝延后且不主动催**｜**是·是＝延后处理但 trigger 后允许提醒一次**。
  - **回归与验收**：原 Discovery **30/30 保持**｜**NPC-01～10 = 10/10 唯一**｜**K4 = 0、K5 = 0**｜Notification 改调度 **0**｜Notification 改 Gap **0**｜starvation 自动生成通知义务 **0**｜delay 无授权被催 **0**｜重复主动提醒 **0**｜**sibling boundary regression 通过**（Fairness 侧未变、Notification 侧零写权、`promotion ≠ notification` 双向成立）。
  - **O-3 整条债完成**：Fairness ✅／starvation observation ✅／user explicit priority ✅／notification visibility ✅。
  - **状态**：**Notification Policy Contract v1 = ✅ 建立并冻结（2026-10-03）**。
- **V0.4.9 Full Adaptive E2E Replay** 见 [`docs/v04/full-adaptive-e2e-replay.md`](v04/full-adaptive-e2e-replay.md)：**五层全链审计**（含 Fairness ＋ Notification 接入旧链）；未改任何冻结正文，未写规则／加字段。
  - **规模**：**12 个 5–9 轮剧本** —— 纯 starvation 无义务 ×2｜`不急但别忘了`×2（含高负担延后）｜显式 priority × fairness ×2（含取消 hint 后恢复资格）｜delay 对照 A/B ×2｜external dependency ＋ notification｜resolution generation｜notification 与高负担冲突｜**9 轮大混合压力剧本**。
  - **不变量升级**：E1–E6 沿用，**新增 E7／E8** —— E7 *Scheduler Fairness 不得改变 Gap 状态／Action 类型／显式用户 priority relation* ✅；E8 *Notification Policy 不得改变调度／Gap／Action，只影响用户可见性* ✅。
  - **关键结论**：① **fairness 全程未偷偷翻转用户序**（剧本 5/6：debt 累积而 `A ≻ C` 不动）；② **同一结果两条链不可混**——"有承诺时重新暴露"走 **Notification**，不走 fairness（剧本 6）；③ 关键拍板**不被提醒打断**（`notify_later`，剧本 4/11）；④ **Notification 未变成"第二个 Action Engine"**。
  - **Release Gate（全部为 0）**：Layer ownership violation｜错误重复询问｜hard constraint 被越过｜explicit priority 被 fairness 偷偷覆盖｜starvation 自动变提醒｜visibility commitment 漏兑现｜重复主动提醒｜**错误主动提醒**｜**承诺触发后漏提醒**｜过期 generation 债务泄漏｜机制词用户可见泄漏｜**K4／K5**。
  - **观察（README 澄清项，非规则变更）**：**O-4** `别忘了`（无时机可见请求）按 Notification 合同 §6.2 **规则 4** 归 `next_relevant_checkpoint`；**O-5** `deprioritized` 项**不累积 fairness debt**（F1），是 E7 成立的前提，应在 README 写明。
  - **下一步（用户已定顺序）**：**停止继续加 V0.4 行为规则** → 写 **V0.4 Final Architecture README** → **V0.4 正式封版**。

---

生成时间：2026-10-01（封版登记；哈希表由 `freeze_v03.py --write` 局部刷新）
