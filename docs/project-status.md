# 项目状态 · 版本矩阵 · 冻结基线

> 本文件承接原 README 中的**内部工程信息**：版本状态矩阵、冻结语义、变更记录、逐文件清单、外部同类调研。
>
> 面向使用者的说明请看 [README.md](../README.md)；面向模型的协议主体在 [SKILL.md](../SKILL.md)。

---

## 1. 版本状态矩阵

| 版本 | 定位 | 状态 |
|---|---|---|
| V0.1 | Interview Control（采访控制层） | ✅ 冻结 |
| V0.2 | Question Selection（问题选择层，§11.1–§11.7） | ✅ 冻结（2026-10-02；依据 35/35 + 兼容 15/15 + 五零指标） |
| **V0.3** | **Uncertainty Resolution Engine（不确定性消解层）** | ✅ **2026-10-01 冻结**（基线见 [freeze-v0.3.md](freeze-v0.3.md)） |
| V0.4 | Adaptive Interview（反馈适应层） | 🚧 进行中：**Phase 1 Gap Ledger v1 = ✅ Frozen**；**Phase 1.5 Interface v2 = ✅ Frozen**；**Phase 2 = Discovery ✅ 30 / Transition Design ✅ 20 / Language Mapping ✅ 30 / State Extension ✅ 30 / Responsibility Extension ✅ 30**；**Interface v3 = ✅ 已并入并冻结**；**V0.4.3 `pending_resolution` = Discovery ✅ 36 + Contract ✅ §10 并冻结**；**V0.4.4 Priority = Discovery ✅ 30 + Layer Contract v1 ✅ 独立成层并冻结**；**V0.4.5 端到端 replay = ✅ 12/12（0 违规）**；**V0.4.6 Priority Hint 语言/生命周期 = ✅ 30/30 + L1–L3 收口并冻结（PHC 8/8、K4=0、K5=0）**；**V0.4.7 Fairness & Starvation = ✅ Discovery 30/30（K4=0、K5=2 已裁决）**；**V0.4.8-A Scheduler Fairness Contract v1 = ✅ 建立并冻结（SFC 18/18、K5-1 关闭）**；**V0.4.8-B Notification Policy = ✅ Discovery 30/30 + Contract v1 建立并冻结（NPC 10/10、K4=0、K5=0）**；**O-3 整条债完成**；**V0.4.9 五层 E2E replay = ✅ 12/12（E1–E8 全通过、全部指标 0）**；下一步 **V0.4 Final Architecture README → 封版**（章程见 [v04/README.md](v04/README.md)） |
| V0.5 | 并行研究（不在当前发布范围） | 🔬 Discovery 64 cases → Clustering → MSC-01（6/6 ACCEPTED candidate）；Schema NOT STARTED |

> **冻结语义**：不是禁止修改，而是"**异常修改模式**"——发现冲突 → 建立失败案例 → 证明非改不可 → 最小修改 → 全量回归 → 重新冻结（五条件）。当前例外登记 **7 次**（§6.5、§3、#3–#7；见 [freeze-v0.3.md](freeze-v0.3.md) §4）。

**V0.1** 需求采访器 → **V0.2** Adaptive Interview System（问题选择）→ **V0.3 Uncertainty Resolution Engine**：不再只是"问对问题"，而是**选择正确的不确定性消解方式**。

---

## 2. 变更记录

### 2.1 V0.1 · 采访决策缺口修复 + 冻结收口

**批准的结构性范围例外：§6.5**

- 原授权范围为 **§3 / §6.3 / §6.4**。
- 但 **D1、D2、F1** 等**已失败案例**证明：Revision（明确修正）、兼容更新、局部重开（Incremental Requirement Update）需要**独立的状态更新规则**，塞进 §3/§6.3/§6.4 会造成规则职责混乱。
- 因此批准**新增 §6.5** 承载这三类状态更新。
- 这是**测试证据驱动的范围例外**，不代表以后可以自行扩展章节范围；后续任何章节级扩展都必须先有失败案例证明。

**冻结范围（V0.1）**

> **§3 / §6.3 / §6.4 / §6.5 已满足冻结条件。**

- §2.1（用户侧环境信息表达）此前已冻结，本轮未修改。
- 冻结含义：除出现**新的失败案例**（表现为既有裁定规则无法得出唯一答案）外，不再改动上述章节；改动必须先补失败案例、再改规则、再全量回归。
- 冻结保护与验收基线（含各节哈希）见 [../tests/acceptance.md](../tests/acceptance.md)。

### 2.2 V0.2 · 新增 §11 问题选择规则（未触碰冻结区）

**证据来源**：`tests/adversarial-question-selection.md` 的 23 例破坏性测试（6 类产物），12 例唯一、11 例不唯一，收敛为 7 类缺口 Q1～Q7。

**批准写入 §11（新增章节，追加在文件末尾）**

| 条目 | 内容 |
|---|---|
| §11.1（Q1） | 同层裁界：先比"答案排除多少下游分支"，仍无法区分再看可回答性与回答成本 |
| §11.2（Q2） | 高价值缺口难回答：先降维问法，**不换低价值问题**；降维后仍答不出再按 §3.2 决定默认／延后／跳过 |
| §11.3（Q3） | 表达深度：只依据**当前对话证据**，不建立永久"新手／专家"标签 |
| §11.4（Q4） | 选项质量：中立、尽量正交、具有代表性、始终保留自由表达通道（不要求绝对完备） |
| §11.5（Q5） | 提问形式：答案空间未形成 → 开放问；已明确且能降低表达成本 → 选择题；允许"开放问 + 少量示例" |
| §11.6（Q7） | 上游依赖优先：若 B 改变 A 的定义／选项集／判断标准，则 B 先于 A |
| §11.7（Q6） | 相关缺口的合并提问：六项条件须**同时**满足；跨簇仅限 ≤2、全低成本、无依赖、无外部信息；命中任一"必须拆开"条件即拆开；与 §11.6 冲突时 **§11.6 优先**；按实际子问题数计入 1～3。**未修改冻结 R2** |
| §11.7 补充判据 | **约束型依赖 vs 共同决策**：合并与否看**决策依赖**而非主题相关性——一答案若改变另一问题的可行取值／选项集合／判断标准／后续提问方式 → 约束型依赖 → 按 §11.6 不合并；仅属同一决策的不同表达维度 → 共同决策 → 可合并（只加边界说明，不新增编号／状态） |

**落盘后的范围声明**

- §11 是**新增章节**，追加在文件末尾；落盘当时**没有修改任何冻结章节**（§2.1／§3／§6.3／§6.4／§6.5），五节哈希 MATCH、行号未移动。**⚠️ 该结论后被 V0.3 取代**：V0.3.3 对 §3 登记了第 2 次范围例外（追加一行适用范围注、判据原文未改）并使行号位移；**以 [../tests/acceptance.md](../tests/acceptance.md) 的基线表为准**。
- Q1 与冻结 §3 的「同层排序」存在**互补重叠**：§3 已要求"优先问能排除方案最多的那一个"，§11.1 只是补上"仍无法区分时看可回答性"的二次口径，未改写 §3。
- Q6 复核结论：冻结 R2 **并未禁止合并提问**（合并 3 个子问题计 3，属合规）；R2 的不足是缺少"何时应该合并"的正向判据。相关过强解读已在 `tests/adversarial-question-selection.md` 内更正。Q6 已转正为 **§11.7**，R2 原文保持不动。
- §11.1 与 §3 的关系按裁决固定为**上位规则 + 二次裁界**：§3 为一级裁界（排除更多下游方案分支），§11.1 仅在 §3 无法继续区分时比较可回答性与回答成本；**不解冻、不修改 §3**。
- §11.6 与 §11.7 的边界：M3、M5、M9 证明"看似同簇但含约束型依赖"的合并必须让位于 §11.6 优先条款（回归记录见 `tests/adversarial-merge-questions.md`）。

**裁决收口：§11 进入冻结候选**

- **§11.1～§11.7 全部通过 35/35 回归**（Question Selection 23 + 合并提问 12），Question Selection 层达到冻结标准。
- 唯一保留理由是留出版本边界——需先完成 **§11 × Gap Ledger 兼容性测试**：验证一个问题在 `SHOW 过 / ASK 过 / CONFIRMED / 后续 CHALLENGED` 状态下，是否影响**合并判断、问题优先级、是否重复询问**。
- **版本状态（§11 已正式冻结，2026-10-02）**：V0.1 Interview Control = **已冻结**；V0.2 Question Selection（§11.1–§11.7）= **✅ 已冻结**；V0.3 Uncertainty Resolution = **已冻结**；V0.4 Adaptive Interview · **Phase 1 Gap Ledger = ✅ Frozen Interface v1**、**Phase 2 Feedback Semantics = 🚀 已启动**。
- **§11 冻结依据**：基础回归 **35/35**（23 + 12）＋ 兼容测试 **C-01～C-15 = 15/15 唯一**；关键指标 **重复询问 0 / 状态冲突 0 / §11 改动需求 0 / 新 Action 0 / 新 Type 0**。原保留理由（与 Gap Ledger 生命周期耦合风险）由**接口层**消解：Gap Ledger 是 §11 的**状态接口**，不是替代。

**交互层裁决（2026-10-02）：§11 × Gap Ledger 兼容性测试结果**

- **兼容性测试**：23 例 V0.2 + 12 例合并 + 15 例兼容 = 通过；§11 判据**未被证伪**，失败全部集中在**账本 → §11 的接口**。
- **裁决**：M1–M4 批准但**写入接口层，不写进 §11**（测试证明 §11 没错，缺的是接口）；M5（`validity_state` 中间概念）与 M6（重复询问以有效集合为准）批准。
- **产物**：[v04/gap-ledger-interface.md](v04/gap-ledger-interface.md)（Patch v1）+ [v04/gap-ledger-x-v11-compat.md](v04/gap-ledger-x-v11-compat.md)（C-01～C-15 重跑 15/15 唯一、I-01～I-12 新增回归 12/12 唯一）。
- **V0.2 冻结状态权威来源**：以 [../tests/acceptance.md](../tests/acceptance.md) 为准（用户裁决）；[freeze-v0.3.md](freeze-v0.3.md) 为版本冻结历史说明。

### 2.3 V0.3 · Uncertainty Resolution Engine

**定位变化**

| 版本 | 定位 |
|---|---|
| V0.1 | Prompt 增强器 |
| V0.2 | Adaptive Interview System |
| **V0.3** | **不确定性消解引擎（Uncertainty Resolution Engine）** |

从此竞争对象不再只是 prompt 工具，而更接近 **AI 产品经理 / 需求分析师 / Agent Orchestrator**。

**新增内容**

| 落点 | 内容 |
|---|---|
| `SKILL.md` §2.5 | **未知类型分类**：Type A（已知未知）/ B（不可描述但可判断）/ C（未意识到的风险）/ D（已说清）/ E（环境可查）；三条规定：**能查不问 / 能选不追 / 先教再问** |
| `SKILL.md` §11.0 | **动作选择优先于问题排序**：分类 → 选动作 → 定层级 → 同层裁界（四层不可颠倒）；含同轮顺序与容量、P0 语义例外 |
| `SKILL.md` §6.6 | **决策记录**：五状态 + `Resolution: asked/shown/inspected/taught/discovered`，六条填写约束 |
| `SKILL.md` §1 / §9 / §10 | 触发信号新增 5、6；反模式新增 7 行；版本边界改为 V0.1–V0.3 分段 |
| `core/uncertainty-classifier.md` | **接口契约**：五种类型、五种动作、动作优先级、决策树 Step 1–7、契约规则 **R1–R13**、决策记录字段、自检清单 |
| `strategies/*.md` ×5 | 每个动作的完整规范：适用对象 / 前置条件 / 执行步骤 / 用户可见模板 / 失败降级 / 反模式 |
| `tests/*.md` ×3 | **V0.3.4 增至 4 个专项文件**：unknown-known（11）、evidence-unknown（10）、blind-spot（9）、**high-risk-c（8）**，共 38 例 |
| `docs/failure-map.md` | 失败模式 → 规则映射；**显式标注测试盲区**，不假装全覆盖 |

**本轮新增规则（V0.3 / V0.3.1）**

| 规则 | 内容 | 来源 |
|---|---|---|
| 契约 **R11** | **P0 语义例外**：目标类槽位整类缺失时先 ASK 目标，SHOW 让位 | 消解 `tests/cases.md` **T-05** 与 §2.5 Step 3 的真冲突（"我要一个电影感的方案"） |
| 契约 **R12** | 被降为"备注"的 Type C **必须在 1–2 轮内 TEACH**，或显式标「暂不做」，不得静默丢弃 | 契约空白复盘：Step 3 短路可能把高风险 Type C 永久压后 |
| 契约 **R13** | INSPECT 多来源矛盾 → 标「部分核实」、并列出处、**不替用户择一、不转问用户** | 契约空白复盘：只写了"读不到"，没写"读到了但互相矛盾" |
| 契约 **R4 改写** | 同轮有容量**且有顺序**：`INSPECT → SHOW → TEACH → ASK`（依优先级，不依决策树 Step 序）；TEACH 恒先于 ASK | 队友提出的"树序 vs 优先级"歧义 |
| 契约 R11 细化 | **"整类缺失"必须先扣除可读环境证据**：环境查得到的目标 → 走 INSPECT，不得拿 P0 例外去问用户 | 队友发现的 **R11 × R1 新交叉**（契约空白，已补 EU-10 回归） |
| 契约 R11 **P0 分级**（V0.3.3） | **锚点 = 要什么产物**（缺失 → ASK 产物、SHOW 让位）；**修饰 = 给谁用/怎么算成功**（缺失**不冻结** SHOW，方向须中立） | 迁移回归发现 `契约 R11` 字面与 §3/§4/`show.md` 给出**相反首动作**（Case A / W6 有两个"唯一正确动作"） |
| 契约 **缺口 Type 归属**（V0.3.3） | 用户**未提及**的 P0/P1/P2 语义槽位一律 **Type A → ASK**；**Type C 只留风险/后果类** | W4/V3/A4/M11 的 P0 缺项在 Step 4 字面下会落到 C（→ TEACH），口径不统一 |
| 契约 R11 **与 R3 顺序**（V0.3.3） | 同时存在**高风险 Type C** → **先 TEACH**，同轮不叠 P0 ASK，**优先于 R11** | skeptic 自造输入"电影感 + 自动炒股"：R11 与 R3/R4 相反裁定 |
| 契约 **R14 高风险 Type C 前置**（V0.3.4/5） | **Type C 不默认优先**：`高风险 C > 普通 A`、`普通 C < 阻塞 A`、**`高风险 C = 阻塞 A`（同轮先 TEACH 紧接 ASK，不得推迟阻塞项）**。三闸门全过（高风险五类 / 用户未意识——三信号皆无 / 本项目有具体载体与后果）才前置；**只适用于风险类缺口**，语义槽位一律走 Type A；TEACH 后必须回到 ASK 或记「暂不做」；**禁止无限教学** | 迁移回归发现"ASK → 轮1纯 TEACH → 轮2 ASK"缺正文级判据（9 例）；随后证伪轮发现 `高风险 C × 阻塞项` 优先级为空（D1，`strategies/teach.md` 反模式与 R14 相反） |
| 契约 R12 细化 | 计时起点：备注出现在第 N 轮 → **第 N+1 轮必须 TEACH**（最迟 N+2 轮内完成或标「暂不做」） | R12 原计时起点未定义 |
| §11.4 补充 | **允许"有依据的推荐"**（依据须来自用户已说信息或成本/风险事实），仍禁"最新/最好/最流行" | 与"推荐项置首 + 「（推荐）」"口径对齐 |

**冻结基线复核（如实记录）**

- **内容零改动**：§2.1 / §3 / §6.3 / §6.4 / §6.5 哈希 **5/5 MATCH**（复算脚本 `.gh-search/freeze_check.py`）。
- **行号已位移**（§1 +4 行、§6.5 之后插入 §6.6 +61 行），旧基线声明的"未移动冻结区行号"在 V0.3 起不成立；`tests/acceptance.md` 已同步为实测行号 + 取块口径，并明确"以内容哈希为准"。
- **命名空间警示**：**契约 R1–R13** 与 **核心规则 R1–R8** 是两套独立编号，跨文件引用必须写全前缀，否则映射串行。

### 2.4 发布记录

| 版本 | 文档 |
|---|---|
| v0.4.0-rc.2 | [releases/v0.4.0-rc.2.md](releases/v0.4.0-rc.2.md) |
| SHIP-02 运行时冒烟协议 | [release-ship-02/protocol.md](release-ship-02/protocol.md) · [protocol-pin.md](release-ship-02/protocol-pin.md) |
| 证据记录模板 | [release-ship-02/record-template.md](release-ship-02/record-template.md) |

---

## 3. 逐文件清单

| 文件 | 作用 |
|---|---|
| [SKILL.md](../SKILL.md) | 主协议：触发条件 → 采访循环 → **§2.5 未知类型分类** → 优先级梯级 → 模糊词协议 → 对象七问 → 停止规则 → **§6.6 决策记录** → 双轨标记 → 出口组装 → 反模式 → 边界 → **§11.0 动作选择** + §11.1–§11.7 问题选择 |
| [core/uncertainty-classifier.md](../core/uncertainty-classifier.md) | **V0.3 接口契约**：五种 Type、五种动作、动作优先级、决策树 Step 1–7、契约规则 R1–R13、决策记录字段。与正文冲突时以本文件为准 |
| [strategies/ask.md](../strategies/ask.md) | 动作规范 · **ASK**：≤3 题、每题附影响说明与推荐默认值、优先调用宿主原生提问工具、合并提问的门槛 |
| [strategies/show.md](../strategies/show.md) | 动作规范 · **SHOW**：3 个正交方向 + 自由混搭；**不是交付**、不追问模糊词、两轮升级路径 |
| [strategies/inspect.md](../strategies/inspect.md) | 动作规范 · **INSPECT**：只读查证；读不到标"未核实"且**不转问用户**；只给项目内文件 + 行号 |
| [strategies/teach.md](../strategies/teach.md) | 动作规范 · **TEACH**：≤3 条隐藏缺口 + 各自后果；不制造焦虑；教完必须重跑决策树 |
| [strategies/discover.md](../strategies/discover.md) | 动作规范 · **DISCOVER**：写进 Prompt 的执行期验证步骤；**阻塞项不可用** |
| [docs/failure-map.md](failure-map.md) | 失败模式 → 规则映射表（V0.1–V0.3），并**标出测试盲区**（哪些规则还没有案例支撑） |
| [docs/migration-regression.md](migration-regression.md) | **V0.2 → V0.3 迁移回归报告**：23 例 + 12 例 + 5 个边界反例全部重跑，40 例 **M3 = 0**；含 SHOW 误抢 P0 结论与终局判定 |
| [docs/migration-framework.md](migration-framework.md) | 迁移回归方法学：三层架构、M1–M4 定义、判定协议、证据格式、统一报数口径 |
| [docs/freeze-v0.3.md](freeze-v0.3.md) | **V0.3 冻结基线**：冻结范围、24 个受保护文件的全量 SHA-256、5 个冻结章节哈希、异常修改模式五条件 |
| [docs/r14-rerun.md](r14-rerun.md) | **V0.3.4–7**：R14 副作用验证 —— 40 例逐例重跑（M3 = 0，影响 10/40） |
| [docs/v04/README.md](v04/README.md) | **V0.4 章程**：阶段界线、五个反馈方向（F1–F5）、破坏测试证据格式、本轮禁止项 |
| [docs/v04/failure-inventory.md](v04/failure-inventory.md) | **V0.4 第一轮破坏测试失效点总账**：七方向 38 例 / **34 个真失效点** / 三个结构性空白 |
| [docs/v04/gap-ledger-proposal.md](v04/gap-ledger-proposal.md) | **V0.4.1 设计提案**：Gap Entity、**七态生命周期**、依赖闭包（含边证据与未建模保留）、反馈账，及对失效点的统一解释力复评 |
| [docs/v04/gap-ledger-replay.md](v04/gap-ledger-replay.md) | **V0.4.1 十例重跑验证**：SHOW 沉默 / 目标突变 / 矛盾反馈 / 多轮压缩，逐例对照新旧动作链（SOLVED 3 / PARTIAL 4 / UNSOLVED 3） |
| [docs/v04/gap-ledger-coverage.md](v04/gap-ledger-coverage.md) | **V0.4.1 独立覆盖复核**：对 32 个受审点逐点判定，指出 **8 处 OVERCLAIM**、6 处应下调，并推翻"闭包可枚举"的承诺 |
| [docs/v04/gap-ledger-interface.md](v04/gap-ledger-interface.md) | **V0.4 Phase 1 · Gap Ledger Interface Patch v1**：有效/可问集合谓词、`validity_state` 三态、§11.2 三出口映射、重复询问定义、优先级声明、§11 消费契约（**独立于 §11，未改 §11／Model／V0.3**） |
| [docs/v04/gap-ledger-x-v11-compat.md](v04/gap-ledger-x-v11-compat.md) | **§11 × Gap Ledger 兼容性测试**：C-01～C-15 兼容案例（Patch v1 后 15/15 唯一）+ 新增固定回归 I-01～I-12 |
| [docs/v04/feedback-semantics-discovery.md](v04/feedback-semantics-discovery.md) | **V0.4.2 Phase 2 第一轮**：30 个反馈语句破坏测试（F1–F5，**未写规则**）——不可承接 **16** / 可承接 6 / 半承接 8；新语义 8 / 缺失转换 10；E1=8、E2=6、E3=10 |
| [docs/v04/feedback-transition-design.md](v04/feedback-transition-design.md) | **V0.4.2 Phase 2.1**：T2 风险门（Effective Authorization）/ T7 否定目标 / T1 授权作用域 + **20 个破坏案例**（TD-01～TD-20）；**只设计、不写 SKILL** |
| [docs/v04/feedback-language-map.md](v04/feedback-language-map.md) | **V0.4.2 Phase 2.2**：表达 → 意图槽位的最小映射契约（三层 + L-01～L-30）；唯一 25 / 不唯一 5（全部为已延期字段或语句复合）；**TD-01～TD-20 = 20/20 通过** |
| [docs/v04/feedback-state-extension-design.md](v04/feedback-state-extension-design.md) | **V0.4.2 Phase 2.3-A**：`reset_scope`／`revision_scope`／`reverted_to` + `reverts` 反向边 + 30 例；**Interface v3 候选** |
| [docs/v04/feedback-responsibility-extension-design.md](v04/feedback-responsibility-extension-design.md) | **V0.4.2 Phase 2.3-B**：责任边界 `pending_external`（10 例）+ 认知边界 `feedback.intent` 四态（20 例）；**30/30 唯一**；SUSPENDED 不新增状态 |
| [docs/v04/interface-v3-migration-manifest.md](v04/interface-v3-migration-manifest.md) | **Canonical Migration Manifest**：Raw **167**（含 B0 共 201）／精确别名簇 28（覆盖 59）／**唯一场景 136**／固定回归 5／canary 4；显式标注 ID 冲突与重叠，不静默去重 |
| [docs/v04/interface-v3-migration-test.md](v04/interface-v3-migration-test.md) | **Interface v3 迁移测试**：K1 48／K2 48／K3 71／**K4 = 0**／**K5 = 0**（修订后）；四条历史不变量 + suspend→resume 五问 + 跨轮 intent + UA-01～04 证伪集 + **raw release gate 201/201** |
| [docs/v04/pending-resolution-second-challenge-discovery.md](v04/pending-resolution-second-challenge-discovery.md) | **V0.4.3 破坏测试**：`pending_resolution` 二次质疑 **36 例**（六 intent 分支各 6）；**K4 = 0、K5 = 1**；证明"额度不是主变量"（误伤 14 / 无作用 22 / 必要 0）；**未写规则** |
| [docs/v04/pending-resolution-transition-contract.md](v04/pending-resolution-transition-contract.md) | **V0.4.3 Transition Contract（✅ 已并入 §10 并冻结）**：两段式模型（intent 选族 → risk/blocking/target/scope 定出口）；六分支骨架；`CLOSED(assumed)` 重进四类（**R-2 = 直接 `CONFIRMED`，不经 OPEN**）；G-1 质疑撤回、G-2 meta 反馈；**Gate：201/201｜PC 18/18｜RC 4/4｜canary PASS｜K4=0／K5=0** |
| [docs/v04/priority-model-discovery.md](v04/priority-model-discovery.md) | **V0.4.4 破坏测试**：Priority Layer **30 例**（显式优先级／blocker×降权／risk×priority／dependency×priority／多 action 竞争）；**职责边界 = 调度器非决策器**；`deprioritized` = **纯调度属性**；冲突 **0**；字段需求 = `priority_hint`（非数值，待裁）；**未写规则** |
| [docs/v04/priority-layer-contract.md](v04/priority-layer-contract.md) | **V0.4.4 Priority Layer Contract v1 + §9 V0.4.6 增量（✅ 冻结）**：四层架构位置；**P1–P6**；硬约束**四类白名单**；`priority_hint` 非数值偏序；**§9 L1–L3**（`scope` × `valid_until` 正交／`current_round` = action bundle 生命周期／`deprioritized` vs `delay` 按效果判）；**PCY-01～12 + PHC-01～08 全唯一** |
| [docs/v04/e2e-adaptive-replay.md](v04/e2e-adaptive-replay.md) | **V0.4.5 端到端 replay（✅ 12/12）**：12 个 4–8 轮真实会话（6 类 ×2），每轮 10 项 + Layer owner + Violation；**E1–E6 全部成立**；违规 0／重复询问 0／硬约束被越过 0／过期 hint 0／机制词泄漏 0／K5 0 |
| [docs/v04/priority-hint-language-discovery.md](v04/priority-hint-language-discovery.md) | **V0.4.6 破坏测试（✅ 30/30 + 收口）**：偏序解析 8／scope 8／生命周期 6／冲突复合 8；**H1–H5 成立**；**O-1/O-2 收口**；**B-03 K5 消失**（→ `whole_task + valid_until`）；**PHC-01～08 = 8/8**；K4=0／K5=0 |
| [docs/v04/scheduler-fairness-starvation-discovery.md](v04/scheduler-fairness-starvation-discovery.md) | **V0.4.7 破坏测试（✅ 30/30）**：真/假 starvation 各 6、×用户 priority 6、×hard constraints 6、通知 6；**F1 最小定义**（eligible ∧ 容量竞争 ∧ 无 hard ∧ 跨周期）；**F4 promotion ≠ notification**；**F5 debt 绑 identity+generation**；ineligible 误判 0／公平越硬门 0／delay 误判 0／失效继承债 0；K4=0、**K5=2（fairness vs user preference，已裁决）** |
| [docs/v04/scheduler-fairness-contract.md](v04/scheduler-fairness-contract.md) | **V0.4.8-A Scheduler Fairness Contract v1（✅ 建立并冻结）**：调度层次 `Hard > explicit active user priority > fairness > ordinary soft`；**F1–F6**；**Fairness Ledger**（scheduler-local 观测账，key = identity + generation，**计数是证据非阈值**）；fairness 恢复资格三条件；**SFC-01～18 = 18/18**；**K5-1 关闭**；**不可发通知**（属 V0.4.8-B） |
| [docs/v04/notification-policy-discovery.md](v04/notification-policy-discovery.md) | **V0.4.8-B Notification Policy Discovery（✅ 30/30 + 封口）**：`visibility_commitment{required, trigger, discharged}`；**必须提醒的唯一来源 = commitment**；一次足够；"知道了"解除义务；防骚扰五条；`delay` 默认不许提醒、叠加可见要求才许；**K5-1／K5-2 均已关闭** |
| [docs/v04/notification-policy-contract.md](v04/notification-policy-contract.md) | **V0.4.8-B Notification Policy Contract v1（✅ 建立并冻结）**：宪法条款（**不得改 ordered_actions／promotion／gap status／Action／创建 blocker·risk**）；`notify_now｜notify_later｜record_only｜never_notify`；**`fairness evidence ≠ notification obligation`**；**`next_relevant_checkpoint`**（时机解析顺序 1–5）；**one commitment → one notification**；**delay 四象限**；**NPC-01～10 = 10/10** |
| [docs/v04/full-adaptive-e2e-replay.md](v04/full-adaptive-e2e-replay.md) | **V0.4.9 五层端到端 replay（✅ 12/12）**：纯 starvation／`不急但别忘了`／explicit priority×fairness／delay 对照／external＋notification／generation／高负担冲突／**9 轮大混合**；**E1–E8 全通过**；错误主动提醒 0／承诺漏兑现 0／generation 债务泄漏 0／K4=0、K5=0 |
| [docs/v04/v04-defect-ledger.md](v04/v04-defect-ledger.md) | **V0.4 Defect Ledger（D/N 双账本）**：旧 **D01–D10** 编号保留（**D01** Final README 缺失＝OPEN BY DESIGN｜**D02** 无时机"别忘了"＝RESOLVED BY N08/N09｜**D03** PR-17＝**CLOSED BY N10**｜D04–D10 待扫）；**N01–N10** 本轮口径批次；**NR-01～NR-09** 最小回归 |
| [docs/v04/v05-architecture-candidates.md](v04/v05-architecture-candidates.md) | **V0.5 架构候选（只记录，不改 V0.4）**：**C1 Authority / Value Separation**（`Decision Authority ≠ Value Commitment`）｜**C2 Notification lifecycle decomposition**（`Commitment → Trigger → Delivery → Discharge`） |
| [docs/v04/release-evidence-closure.md](v04/release-evidence-closure.md) | **V0.4 Release Evidence Closure**：**ER-07** E2 ownership trace（M-01～M-11，final writer = Interface）｜**ER-08** E3/E5 修正索引（4 条错引用已改；E3-A/B ＋ E5-A/B）｜**ER-09** scenario-12 debt provenance；**EV-07/08/09 = 3/3** |
| [docs/v04/historical-discovery-governance.md](v04/historical-discovery-governance.md) | **D10 Historical Discovery Governance（5 条）**：append-only｜candidate findings｜后续合同权威｜取代者须标注｜**`30/30` 仅表历史执行覆盖**；含 **HG-10** 文档身份探针与应用实例（C-03／C-06／NB-01） |
| [docs/v04/v0.4-release-baseline.md](v04/v0.4-release-baseline.md) | **V0.4 Release Baseline（INITIAL → REBASELINE = `baseline-2`，✅ 只读验证 PASS）**：三层分类（normative 6／governance 3／evidence 11）；**SHA-256 raw bytes**（file 权威／section 诊断）；**prospective-only** 声明；machine source of truth = `v0.4-release-baseline.json`；校验器 `.gh-search/verify_v04_release_baseline.py`（**只读**；DIFF／MISSING／UNREGISTERED ⇒ 非零退出） |
| [tests/acceptance.md](../tests/acceptance.md) | 核心规则逐条可勾选验收清单 + **冻结基线与哈希**（V0.3 实测行号 / 5 节 MATCH） |
| [tests/cases.md](../tests/cases.md) | 可执行用例：输入 → 期望行为 → 通过/失败判据（含反例）；页首有 V0.3 命名空间说明 |
| [tests/adversarial-question-selection.md](../tests/adversarial-question-selection.md) | V0.2 破坏性测试：23 个"问什么"案例（6 类产物），12 例唯一、11 例不唯一，收敛为 7 类缺口 Q1～Q7；文末含 §11 落盘后的重跑复核 |
| [tests/adversarial-merge-questions.md](../tests/adversarial-merge-questions.md) | Q6 专项 + **§11.7 固定回归**：12 个合并提问案例（4 允许合并／7 必须拆开／1 不该问） |
| [tests/adversarial-interview-core.md](../tests/adversarial-interview-core.md) | 对抗测试：21 个采访核心案例，全部唯一裁定（§3.1 冲突/张力、§3.2 unresolved、§6.3 授权默认、§6.5 Revision/局部重开） |
| [tests/unknown-known.md](../tests/unknown-known.md) | **V0.3**：Type B / SHOW 专项 10 例（含"高级官网""requirements.txt""自动交易机器人"三个强制案例） |
| [tests/evidence-unknown.md](../tests/evidence-unknown.md) | **V0.3**：Type E / INSPECT 专项 10 例（含读不到标"未核实"、多来源冲突、**R11×R1 边界（EU-10）**） |
| [tests/blind-spot.md](../tests/blind-spot.md) | **V0.3**：Type C / TEACH 专项 9 例（含 AI 客服、自动交易机器人、教后重分类、「暂不做」出口） |
| [tests/high-risk-c.md](../tests/high-risk-c.md) | **V0.3.4**：高风险 Type C 前置（R14）固定回归 8 例（HR-01～HR-08，含 TEACH 后进 ASK、**阻塞项同轮并列**、粒度双条件、防膨胀闸门、R14 > R11） |
| [README.md](../README.md) | 面向使用者的说明与示例 |

---

## 4. 外部同类实现调研（GitHub，2026-10-01）

同类"需求采访 / 澄清后再生成"的 Skill 已是一条成熟赛道，本仓库与它们**无同源关系**（3-gram 最高重合 4.6%，属功能词底噪）：

- [Cunzhang0703/req-interview-skill](https://github.com/Cunzhang0703/req-interview-skill) —— 中文同题，支持 DSH；其"提问优先调用宿主原生工具""失败模式映射表""零依赖校验脚本"三项已被本次吸收
- [arjunlohan/sharpen](https://github.com/arjunlohan/sharpen) —— 四象限未知（known/unknown knowns/unknown unknowns），**SHOW 手法**的主要外部参照
- `ask-questions-if-underspecified` 家族（[MoizIbnYousaf](https://github.com/MoizIbnYousaf/Ai-Agent-Skills/blob/main/skills/ask-questions-if-underspecified/SKILL.md) 等 4 个镜像）—— "≤3 问 + 每问附默认值"的轻量版

调研全文与证据：`.gh-search/REPORT.md`。
