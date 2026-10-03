# 验收清单 · Prompt Architect V0.1

**用途**：核对 V0.1 是否真正建立了"需求采访机制"。
**方式**：把本文件当作人工（或 agent）逐条核对表；每条都必须给出**文本证据**（引用被检输出的原句），不接受"感觉符合"。
**范围**：只验收采访机制。不验收 Prompt 成品质量、不做 UI/性能验收。

---

## 一、8 条核心规则逐条验收

### R1 · 需求明显不完整时不立即生成最终 Prompt

- [ ] 对"帮我做个高级的咖啡海报"这类输入，**第 1 轮回复中不包含**编号为 1～5 的 5 段组装内容
- [ ] 第 1 轮明确说明"还缺什么"
- [ ] 判定方式：检索首轮输出是否出现 `1. 角色与目标` / `2. 输入` / `3. 约束` / `4. 输出格式` / `5. 验收标准` 中任意 2 项以上

**证据**：＿＿＿＿＿＿＿＿

---

### R2 · 每轮最多 1～3 个问题

- [ ] 统计每一轮的问题条目数，**全部 ≤3**，且 ≥1
- [ ] 不存在"一个问题里塞三个子问题"的规避写法（如"尺寸、时长、平台分别是？"算 3 个，若写成一段仍计 3 个）

**判定**：轮次表

| 轮次 | 问题数 | 是否合规 |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

**证据**：＿＿＿＿＿＿＿＿

---

### R3 · 优先询问显著影响最终方案的问题

- [ ] 当输入同时缺 P0（目标/产物/成功标准）与 P3（风格）时，**首轮问的是 P0**
- [ ] 每个问题都附有「影响：<哪个决策>」说明
- [ ] 不存在"只影响措辞"却被优先提出的问题排在 P0 之前

**证据**：＿＿＿＿＿＿＿＿

---

### R4 · 不擅自把 AI 的建议当成用户需求

- [ ] 最终输出中，「需求」区（1～5 段）**不含**任何用户未明确说过的选择
- [ ] 所有 AI 推测出现在「待确认假设」区，并带"若不符请指出"类说明
- [ ] 不存在把建议表述成用户原话（如"你说过要…"而用户并未说过）
- [ ] 用户对某建议**沉默**时，该建议仍只能留在假设区

**判定**：逐条比对「用户原话」与「需求区」是否一一对应。

**证据**：＿＿＿＿＿＿＿＿

---

### R5 · 模糊词不被照抄

- [ ] 输入含"高级/自然/漂亮/震撼/舒服/真实/科技感/电影感"时，最终「约束」区**不出现未澄清的该词**
- [ ] 该词被替换为可执行描述，或（若用户明确要求保留原词作风格指令）保留但已附澄清说明
- [ ] 澄清动作使用了协议三法之一：目的反推 / 参照物法 / 方向择选

**判定**：在最终输出的约束区检索 8 个模糊词原文；命中即为问题，除非同段有澄清定义。

**证据**：＿＿＿＿＿＿＿＿

---

### R6 · 提供 2～4 个明显不同方向，且允许自由描述

- [ ] 给出的方向数在 **2～4** 之间
- [ ] 方向**正交**：把每个方向归入一个维度标签（如 视觉质感 / 运镜语言 / 布光 / 目的类型），若 ≥2 个方向落在同一维度且仅程度不同 → **不通过**
- [ ] 每次都明确写出"也可以不按这些，直接描述你想要的"或等价句
- [ ] 用户选定后，选择结果原样进入需求区（未被改写、未被"优化"）

**正交性检查表**：

| 方向 | 我归的维度 | 与其它方向是否仅程度差异 |
|---|---|---|
| A | | |
| B | | |
| C | | |

**证据**：＿＿＿＿＿＿＿＿

---

### R7 · 核心对象按需分析七问

- [ ] 对核心对象（产物中最被在意的可描述事物）**按需**问及：是什么 / 在哪 / 什么状态 / 会做什么 / 什么触发 / 影响什么 / 动作后如何恢复
- [ ] **不机械问满 7 问**：对一次性产物，"恢复"可判为可默认并跳过
- [ ] 缺失且会改变结构的维度**确实被问到**了（不是全跳过）

**七问覆盖表**：

| 维度 | 是否问到 | 是否可合理默认 | 判定 |
|---|---|---|---|
| 是什么 | | | |
| 在哪里 | | | |
| 什么状态 | | | |
| 会做什么 | | | |
| 什么触发 | | | |
| 影响什么 | | | |
| 如何恢复 | | | |

**证据**：＿＿＿＿＿＿＿＿

---

### R8 · 信息足够时不继续追问

- [ ] 出现"谁用 / 要什么产物 / 怎么算成功 / 硬约束"齐备后，**无追加问题**，直接出口
- [ ] 无重复提问（同一信息问两次，或换措辞再问同一点）
- [ ] 用户连续 2 轮"随便/不知道"后，停止提问并出稿
- [ ] 用户说"别问了/直接给"后，**立即出稿**，未再提问

**证据**：＿＿＿＿＿＿＿＿

---

## 二、机制完整性验收

- [ ] **触发判定存在**：明显完整的请求（如已给产物/受众/字数/语气/语言）会得到 0 问直接出口
- [ ] **出口结构完整**：5 段齐全 + 独立的「待确认假设」区 + 结尾确认句（"哪一条不对告诉我编号"）
- [ ] **不编造**：需求区不确定处留空或标注，未凭空生成事实
- [ ] **反模式零命中**：对照 `SKILL.md` §9 表格与 §6.4 禁止清单逐条检查，命中数 = 0
- [ ] **对外语言无泄露**：用户可见文本中无机制词（`SKILL.md`/触发信号/`P0`/七问/采访循环/槽位/停止规则）、无与交付无关的工具或环境状态、不预告内部步骤（对照 §2.1；检索方式：在每轮用户可见段落中检索上述词表）
- [ ] **环境信息裁定唯一**：按 §2.1「裁定顺序」5 步核对 `tests/adversarial-2.1.md` 的 A1～A12，12 例均得出唯一答案（该节已冻结）
- [ ] **采访决策裁定唯一**：`tests/adversarial-interview-core.md` 的 21 例（B/C/D/E/F + 4 微型判例）全部唯一裁定
- [ ] **unresolved 口径统一**："不知道 / 不确定 / 答非所问 / 明显回避"统一进入 §3.2 计数；连续 2 次后按阻塞/非阻塞分流
- [ ] **授权默认不被误判**："随便 / 你决定 / 按你想的来 / 直接给"不计入 unresolved，也不再追问
- [ ] **Tension 与 Conflict 可区分**：先按 Tension 试解，解不掉才判 Conflict；Tension 不要求二选一
- [ ] **Revision 与 Conflict 可区分**：有明确修正信号 → Revision（覆盖）；无信号且互斥 → Conflict（不覆盖）
- [ ] **局部重开生效**：出稿后收到新信息只重开受影响分支，不重开整轮
- [ ] **§2.1 零修改**：见下方「冻结范围与保护基线」
- [ ] **"停止追问"未被误读为"拒收新信息"**：§6.3 末注与 §6.5C 均体现该边界
- [ ] **同层裁界（§11.1）**：同层多缺口先比"答案排除多少下游分支"，仍无法区分再看可回答性与回答成本（核对 W3、S1）
- [ ] **难回答的高价值缺口（§11.2）**：先降维问法，**不换成低价值问题**；降维后仍答不出才按 §3.2 决定默认／延后／跳过（核对 I3、A3）
- [ ] **表达深度只依据当前证据（§11.3）**：不建立永久"新手／专家"标签，逐轮重判（核对 W4、V3）
- [ ] **选项质量（§11.4）**：中立、尽量正交、具有代表性、保留自由表达通道；不要求绝对完备（核对 W6、A2）
- [ ] **提问形式（§11.5）**：答案空间未形成 → 开放问；已明确且能降低表达成本 → 选择题；允许开放问 + 少量示例（核对 W7）
- [ ] **上游依赖优先（§11.6）**：若 B 改变 A 的定义／选项集／判断标准，则 B 先于 A（核对 T2、S1、A3）
- [ ] **合并提问（§11.7）**：六项条件须**同时**满足才可合并；跨簇仅限 ≤2、全低成本、无依赖、无外部信息；命中任一"必须拆开"条件即拆开；与 §11.6 冲突时 **§11.6 优先**；按**实际子问题数**计入 1～3，不得语言包装绕过 R2（核对 M1～M12）
- [ ] **合并边界判据（§11.7 补充判据）**：合并与否看**决策依赖**而不是主题相关性——若一个答案会改变另一个问题的**可行取值／选项集合／判断标准／后续提问方式**，即属**约束型依赖**，须按 §11.6 上游优先、**不合并**（约束型依赖反例核对 **M3 / M5 / M9**）；若只是同一决策中的**不同表达维度**（目标、受众、核心任务），属**共同决策**，可以合并（共同决策跨簇合并例核对 **M12**）
- [ ] **R2 保持原文**：合并提问按实际子问题计数，R2 未修改（结论见 `tests/adversarial-merge-questions.md`）
- [ ] **【V0.4·接口层】候选集合 = `askable_set`**：`OPEN ∪ CHALLENGED(pending_resolution) ∪ CLOSED(partial)`；`SUSPENDED` 与 `CLOSED(assumed)` 不进候选；合并的子问题也必须取自该集合（核对 `docs/v04/gap-ledger-interface.md` §1.2；案例 C-06、I-06、I-08）
- [ ] **【V0.4·接口层】有效集合 = `CONFIRMED ∩ stable`**：只有有效集合内的值可作为已确认事实进入出口与裁界（核对 §1.1；案例 C-01、I-04）
- [ ] **【V0.4·接口层】重复询问以有效集合为准**：`INVALIDATED → OPEN` 后重新消解不算重复询问；被 `supersedes` 替代的旧值不得进候选（核对 §4；案例 C-07、I-05、I-09、I-10）
- [ ] **【V0.4·接口层】`validity_state` 三态**：`stable` 可用；`challenged` 可继续输出但须标注、不得扩散确认；`pending_resolution` 阻断该值交付并进 `askable_set`（核对 §2；案例 C-11、I-01～I-03）
- [ ] **【V0.4·接口层】停止判据的点例外仅限 `pending_resolution`**：允许一次确认，不得连续第二次（核对 §2.5；案例 I-02）
- [ ] **【V0.4·接口层】§11.2 三出口映射**：default→`CLOSED(assumed)`／delay→`OPEN+deferred`／skip→`CLOSED(partial)`，且出口必须渲染（核对 §3；案例 C-08）
- [ ] **【V0.4·接口层】优先级：账本状态约束 > §11.5 形式选择**：动作闸门禁用同一动作后，形式选择只在允许动作内生效（核对 §5；案例 C-09、C-10、I-11）
- [ ] **【V0.4·接口层】裁界基数 = 有效下游**：历史 `CLOSED` 不参与计数；`CLOSED(partial)` 可问但不得作为已确认依据（核对 §1.3、§1.4；案例 C-03、C-12、C-14、I-07）
- [ ] **【V0.4·接口层】合并出口渲染未建模依赖**：`unmodeled_dependencies ≠ []` 时必须输出"未建模的潜在依赖：X（建议你确认）"（核对 §6；案例 C-13、I-12）
- [ ] **【V0.3】未知分类存在（§2.5）**：给出缺口先能说清是 Type A/B/C/D/E 之一；混合性质按主导类型执行一个动作（契约 R5）
- [ ] **【V0.3】能查不问（契约 R1 / §2.5 规则 1）**：可读环境中的事实（版本 / 技术栈 / 既有约定 / 历史决策）用 INSPECT，不得问用户；读不到标"未核实"且**不转问用户**（核对 `tests/evidence-unknown.md` EU-01～EU-09）
- [ ] **【V0.3】能选不追（契约 R2 / §2.5 规则 2）**：命中模糊词后**同轮不得追问定义**，改为 SHOW 3 个正交方向（核对 `tests/unknown-known.md` UB-01～UB-10）
- [ ] **【V0.3】先教再问（契约 R3 / §2.5 规则 3）**：未意识到的风险缺口先 TEACH **≤3 条且每条讲后果**，不得跳过直接问（核对 `tests/blind-spot.md` BS-01～BS-08）
- [ ] **【V0.3】SHOW 不是交付**：SHOW 阶段只给"够判断"的粗略草案，不得完成主交付物
- [ ] **【V0.3】阻塞项不可 DISCOVER（契约 R6）**：目标 / 范围 / 权限 / 费用 / 数据用途 / 不可逆操作必须用户拍板
- [ ] **【V0.3】P0 语义例外（契约 R11 / §11.0 规则 8）**：目标类槽位整类缺失时先 ASK 目标、SHOW 让位（核对 `tests/cases.md` **T-05**）；P0 有部分依据时只补缺项，不扩大解释
- [ ] **【V0.3.3】P0 分级**：锚点（产物）缺失 → ASK 产物；**修饰（受众/成功）缺失不冻结 SHOW**（核对 Case A / W6）
- [ ] **【V0.3.4】高风险 C 前置（契约 R14）**：三闸门全过才占位；`高风险 C > 普通 A`、`普通 C < 阻塞 A`、**`高风险 C = 阻塞 A`（同轮先 TEACH 紧接 ASK，不得推迟阻塞项）**；"指向同一件事"须满足双条件（槽位 ∈ R6 **且** 不拿到无法知情拍板）；TEACH 后必须回到 ASK 或有「暂不做」出口；禁止无限教学（核对 `tests/high-risk-c.md` HR-01～HR-08，8/8 唯一裁定）
- [ ] **【V0.3】备注中的 Type C 不搁置（契约 R12）**：被降为备注的 Type C 须在 1–2 轮内 TEACH 或显式标「暂不做」
- [ ] **【V0.3】多来源冲突如实处理（契约 R13）**：并列出处 + 标「部分核实」+ 不替用户择一 + 不转问用户
- [ ] **【V0.3】同轮容量与顺序（契约 R4）**：≤1 TEACH 块 + 1 SHOW + 1 ASK；顺序依优先级 `INSPECT → SHOW → TEACH → ASK`，TEACH 恒先于 ASK
- [ ] **【V0.3】决策记录完整（§6.6）**：每条关键缺口有 `类型 / 动作 / 状态 / 依据 / 结果`；`shown` 未收到选择前不得写成「已确认」；写了动作不等于用户授权
- [ ] **【V0.3】用户侧零机制词**：ASK/SHOW/INSPECT/TEACH/DISCOVER、Type A–E、unknown known、决策树均不得出现在用户可见文本
- [ ] **【V0.3】旧案例已完成 V0.3 重跑评估**：`tests/adversarial-question-selection.md`（23 例）与 `tests/adversarial-merge-questions.md`（12 例）在 V0.3 下是否换动作已评估并记录（当前状态见 `docs/failure-map.md` 盲区 B13）
- [ ] **边界守住**：未引入任何脚本、框架、API、外部依赖、CLI/GUI、持久化状态（技能本体仅由 `.md` 构成，`SKILL.md` 不依赖任何脚本）
  - 注：`.gh-search/`（GitHub 调研与冻结哈希复算脚本）与 `scripts/check-skill.*` 属**维护者工具**，不参与技能运行；技能运行时只读 `.md`。

---

## 二·A 冻结范围与保护基线（V0.1）

**冻结范围**

> **§2.1 / §3 / §6.3 / §6.4 / §6.5 已满足冻结条件。**
> **§11.1 / §11.2 / §11.3 / §11.4 / §11.5 / §11.6 / §11.7 已满足冻结条件（V0.2，2026-10-02 裁决）。**

- §2.1 冻结于更早一轮；§3 / §6.3 / §6.4 / §6.5 于"采访决策缺口修复"轮验收通过后冻结。
- **V0.2 §11（问题选择）为独立章节，追加在 `SKILL.md` 文件末尾；自 2026-10-02 起正式冻结。**
- **V0.2 冻结依据**：① 基础回归 **35/35**（Question Selection 23 + 合并提问 12）；② §11 × Gap Ledger 兼容测试 **C-01～C-15 = 15/15 唯一**；③ 关键指标 **重复询问 0 / 状态冲突 0 / §11 改动需求 0 / 新 Action 0 / 新 Type 0**；④ 合并边界验证（M1～M12）与状态生命周期验证（I-01～I-12）完成。原先不予冻结的唯一原因（与 Gap Ledger 状态生命周期可能耦合冲突）已由**接口层**消解：Gap Ledger 成为 §11 的**状态接口**，而非替代 §11。
- **版本状态（本轮）**：V0.1 = **已冻结**；V0.2 §11 = **已冻结**；V0.3 = **已冻结**；V0.4 · **Phase 1 Gap Ledger v1 = ✅ Frozen**、**Phase 1.5 Interface v2 = ✅ Frozen**、**Phase 2 = Discovery ✅ 30 / Transition Design ✅ 20 / Language Mapping ✅ 30 + TD 20/20 / State Extension ✅ 30（A 类三字段）**、**Phase 2.3-B ✅ 30（责任 10 + 认知 20）**、**Interface v3 = 🟡 落盘候选（不冻结，待迁移测试）**。
- **Phase 2.3 设计产物**：[`docs/v04/feedback-state-extension-design.md`](../docs/v04/feedback-state-extension-design.md)（A 类：`reset_scope`／`revision_scope`／`reverted_to` + `reverts` 反向边）与 [`docs/v04/feedback-responsibility-extension-design.md`](../docs/v04/feedback-responsibility-extension-design.md)（B 类：`pending_external` + `suspension_reason` + `feedback.intent` 四态）。**均未落盘到接口正文**（v2 冻结正文未改）。
- **Interface v3 状态**：**✅ 已并入接口正文并冻结（2026-10-02）**。迁移测试见 [`docs/v04/interface-v3-migration-test.md`](../docs/v04/interface-v3-migration-test.md)（K1 48／K2 48／K3 71／**K4 = 0**／**K5 = 0**）；Manifest 见 [`docs/v04/interface-v3-migration-manifest.md`](../docs/v04/interface-v3-migration-manifest.md)（**Raw 201**／**唯一场景 170**／**固定回归 5**／**canary 4**／**证伪集 UA-01～04**）。规范落点：[`docs/v04/gap-ledger-interface.md`](../docs/v04/gap-ledger-interface.md) **§9（v2 章节逐字保留）**。
- **v3 收口记录**：唯一阻塞项 `unaware` 判据已按裁决修订为 `unaware ⟺ ¬topic_presented ∧ ¬user_evidences_awareness`（派生证据，不新增 Gap 状态／持久字段）；UA-01～04 **4/4 唯一**、V3-C4 **PASS**、**K5 = 0**；**Release regression 201/201**（raw 口径），`170 unique` 仅作覆盖统计。
- **流程纪律**：本次按"**先登记、后执行**"（例外 **#13 预登记**）——预登记 → 修订判据 → 跑 UA/回归 → 并入正文 → 重冻结；**未修改 §11／§6.3／v2 冻结章节／V0.3／Gap Model 正文**。
- **V0.4.3 `pending_resolution` Second-Challenge Discovery 状态**：**✅ 36/36 有明确分析结果**，**K4 = 0**、**K5 = 1**（PR-17，根因＝`CLOSED(assumed)` 重开入口未定义）；产物 [`docs/v04/pending-resolution-second-challenge-discovery.md`](../docs/v04/pending-resolution-second-challenge-discovery.md)。
  - **核心假设判定**：**"第二次质疑不是次数问题，而是反馈意图问题"成立**——旧"一次确认额度"在 **14/36** 例上会**误伤合法反馈**（Revision 链／Challenge 链／阻塞项多轮降维／外部恢复），在 **22/36** 例上**无作用**，在 **0** 例上**必要**；六个 intent 分支出口互不相同。
  - **Q4 结论**：**没有**一例迫使新增 Gap 生命周期状态；发现 3 个 **intent 子型**缺口（质疑撤回／meta 反馈／条件性放弃），均可用既有状态表达。
  - **纪律**：**未写规则**、未改 `SKILL.md`／§6.3／§11／v2／v3／V0.3、未新增 Type／Action／Gap 状态。
  - **下一步（待批准）**：**Pending Resolution Transition Contract**（用 intent 替换额度；补 `CLOSED(assumed)` 重开入口、`Challenge` 撤回子型、`meta` 不触状态机）。
- **Pending Resolution Transition Contract 状态**：**✅ 已并入接口正文（§10）并冻结（2026-10-02）**；产物 [`docs/v04/pending-resolution-transition-contract.md`](../docs/v04/pending-resolution-transition-contract.md)、规范落点 [`docs/v04/gap-ledger-interface.md`](../docs/v04/gap-ledger-interface.md) **§10**（v2 §1–§8、v3 §9 **逐字保留**）。
  - **核心模型（按裁决收紧）**：`intent dispatch`（选跃迁族）→ `target/scope/risk/blocking/provenance/resume_condition`（定具体出口）；**不是 `intent → state` 一跳映射**。**废弃**"剩余确认次数"局部模型。
  - **计数口径**：Contract **不自带计数器**；`pending_resolution` 不新增独立额度；既有 `unable/evaded/no_signal` 计数**仍归其原冻结规则**，未改写。
  - **R-2 封口修正（预登记 #16）**：原写"保持 `CLOSED(assumed)` 仅升 `confidence`"与 **v1 冻结谓词 `effective_set = CONFIRMED ∩ valid`** 冲突（且造成 `status` 与 `confidence` 争夺权威）。改为**直接确认跃迁** `CLOSED(assumed) → CONFIRMED`（**不经 OPEN**）+ `confidence := confirmed` + `provenance += user_confirmed_after_assumed`；**未改任何冻结谓词**。原则确立：**`status` 决定生命周期；`confidence`／`provenance` 只描述"为何成立"**。
  - **G-1**：`Challenge withdrawal` 三条件 + 恢复原有效值 + 历史保留 `challenged → withdrawal`。**G-2**：`meta feedback` = `target=interaction_process`，状态不变，**不是第七种业务 Intent**。
  - **验收（分栏 Release Gate）**：Base raw **201/201**｜Pending Contract **18/18**｜R-2 probes **4/4**（RC-01～04）｜V3 canaries **PASS**｜**K4 = 0、K5 = 0**（**PR-17 K5 消失**）。
  - **⚠ N10 更正（2026-10-03）**：该条目的 **PR-17 归因已更正** —— `算了，还是你来定吧。` **= Authorization（决定权转移 ≠ 值接受）**，**不是** R-2，**该句不产生 `CONFIRMED`**；**R-2 定义未改**，仅更正分类。因此：
    - **旧 `K5 = 0` 不作为最终证据**（其归因基于过宽读法）；
    - **K5 = REOPENED FOR N10 → 已重确认 = 0**（新归因：分类唯一 ⇒ 无第二合法读法）；
    - 探针：**RC-01～RC-03 重跑唯一**；**NR-08 negative**（仅授权 → NOT CONFIRMED）／**NR-09 positive control**（"就按 X" → R-2 → CONFIRMED）**成对唯一**；
    - 落盘：[`pending-resolution-transition-contract.md`](../docs/v04/pending-resolution-transition-contract.md) §3.4 更正框／**§3.5 N10 边界**／**§8.1 重确认**；[`gap-ledger-interface.md`](../docs/v04/gap-ledger-interface.md) §10.5；账本 **N10**。
    - **状态**：**原审计 D03 = ✅ CLOSED BY N10**（旧 D02 = RESOLVED BY N08/N09；旧 D01 = OPEN BY DESIGN）。
- **D04–D06 closure sweep 状态（第一批 · 语义澄清组）**：**✅ 全部 CLOSED（2026-10-03）**；传播修复编号 **CS-04／CS-05／CS-06**；账本见 [`docs/v04/v04-defect-ledger.md`](../docs/v04/v04-defect-ledger.md) §七。
  - **D04（CS-04）**：**原子性 = per-Gap 完整门链**（`≠ whole-feedback transaction ≠ whole-cluster transaction`）；"禁止部分执行"指**单个 Gap 一次完整门链不得部分提交**，同 feedback／cluster 其他 Gap **独立过各自门链、不整体回滚**；**G-8.3c（逐 gap 过 T2 门）改为此原则的正例**。落盘 Interface **§8.1 原子性作用域**。**不加 rollback、不加 cluster transaction、不加状态。**
  - **D05（CS-05）**：**`External` 描述依赖来源；`SUSPENDED(external_owner)` 描述决策权是否真的离开"用户—系统"闭环** → `reason = information_source` **依 X-4 保持 `OPEN`、用户仍为决策者**；仅 `reason = external_owner` 进入既有 SUSPENDED。落盘 Interface **§10.2 External 行**（引用 X-4，**不新增第七分支／子类型**）。
  - **D06（CS-06）**：**`askable` 成员资格 ≠ 当前调度资格** → `OPEN + deferred`：state `OPEN`／**`askable_set` = YES**／**normal scheduling = NO**；`delay ≠ remove_from_askable_set`。落盘 V0.4.9 剧本 7 措辞（**正式 `askable_set` predicate 未改**）。
  - **8 个 closure probes**：**AR-01／AR-02**（per-Gap 原子性正/负例）｜**EX-01／EX-02／EX-03**（信息源 vs 决策权；外部信息不自动 CONFIRMED）｜**DL-01／DL-02／DL-03**（askable 仍 YES、调度 NO；解除无需重建；delay 与 commitment 并行且 Notification 不得取消 deferred）＝ **8/8 唯一**；**K4 = 0、K5 = 0**；未新增字段／状态／计数。
  - **新洞见入 V0.5 候选（未编号，不改 V0.4 ontology）**：`participation / information provision / decision authority` 是三个不同维度——**不要从"谁参与"推导"谁拥有决定权"**。
  - **下一批**：**D07–D09 evidence repair**（D07 E2 ownership｜D08 E3/E5 错引用｜D09 scenario 12 debt provenance），随后 **D10** 历史治理。
- **D07–D09 evidence repair 状态（第二批 · 只修证据链）**：**✅ 全部 CLOSED（2026-10-03）**；编号 **ER-07／ER-08／ER-09**；产物 [`docs/v04/release-evidence-closure.md`](../docs/v04/release-evidence-closure.md)。
  - **ER-07（D07）E2 ownership trace**：**要证明的是"每一次实际 Gap-state mutation 的 final write owner 都能追到 Interface"**。六行 ownership trace（V0.3 选 Action｜§11 选问题｜Priority 排序｜Fairness 调调度竞争｜Notification 本层 `visibility`·`discharged`——**五者皆不写 Gap state**｜**Gap state commit = Interface**）＋ **M-01～M-11 逐 mutation 完整链**（含负例 **M-10**：`discharged` 仅 Notification 内部 → Interface 无 mutation）。
  - **ER-08（D08）E3/E5 corrected index**：旧汇总 **4 条引用错误**已逐条打开确认并替换 —— `剧本 2 轮2` 称 SHOW 实为 **ASK**；`剧本 9 轮2` 称"不落 SUSPENDED"实为**该轮即 SUSPENDED**；`剧本 3 轮2`／`剧本 5 轮2` 并非 SHOW 轮。重建：**E3-A** 剧本 1 轮2（SHOW）｜**E3-B** 剧本 1 轮1（ASK）｜**E5-A（negative control）** 剧本 1 轮2 ＋ 剧本 12 轮2（SHOW → §11 不参与）｜**E5-B（positive control）** 剧本 1 轮1／轮3（ASK 被调度 → §11 才选问法）；`information_source` 正例改用 **V0.4.5 `E2E-08` 轮2**。**无 `NOT EVIDENCED`、未补造轮次**。
  - **ER-09（D09）scenario-12 debt provenance**：逐轮可推出 —— 轮3 `soft_competition` **0→1**｜轮4 `soft_competition`（显式 hint A≻C）**1→2**｜轮5 起 `user_deprioritization` **increment = 0**｜轮8 `generation replacement` 旧债终止。明确两个命题：**`deprioritized` 不清零已有债、也不新增债**（**⛔ 不是 reset to 0**）；同源补证剧本 10 轮2／轮3。
  - **证据一致性探针 EV-07／EV-08／EV-09 = 3/3 通过**：EV-07 **11/11 mutation final writer = Interface**（无越权 writer）｜EV-08 **修正后 4/4 一致**｜EV-09 **每次 +1 有合法 skip reason、`deprioritized` 后 increment = 0、`debt=2` 可由前序完整推出（O-5 未被混合场景违反）**。
  - **本阶段边界**：**只修证据链，未改任何行为规则／字段／状态／计数**；**未为保住 PASS 找"差不多"的轮次**。
  - **账本进度**：D01 OPEN BY DESIGN｜D02 RESOLVED BY N08/N09（待最终 linkback）｜**D03–D09 全部 CLOSED**｜D10 待正式闭合。
  - **下一步**：**D10**（历史治理）→ **D02 最终 evidence linkback** → **V0.4 freeze governance baseline** → **D01 Final Architecture README** → **Release Ready**。
- **D10 历史治理 ＋ D02 证据回链状态（第三批 · 收口）**：**✅ 两项全部 CLOSED（2026-10-03）**；产物 [`docs/v04/historical-discovery-governance.md`](../docs/v04/historical-discovery-governance.md)。
  - **D10 · Historical Discovery Governance（5 条）**：① Discovery artifact 为 **append-only 历史证据**，不得覆写；② Discovery 结论是 **candidate findings**，不自动成为规范合同；③ 后续已批准合同对同一语义问题裁决不同时，**以后续合同为现行行为权威**；④ 被取代结论**保持可见**并须标注**历史状态／取代者／现行解释**；⑤ **`30/30` 只表示历史执行／覆盖成功**，**不得**读作"30 个历史结论今天仍是现行规范行为"。
  - **证据层次**：`治理规则 → N06 实际应用 → 历史 artifact（C-03／C-06）`。**N06 是实例修复，D10 是治理规则闭合**（**未重复修改 C-03／C-06**）。
  - **HG-10 文档身份探针 = PASS**：C-03／C-06 历史证据仍在、superseded 已标注、现行来源已指明、**无静默改写**；并刻意纳入**未被取代的对照 NB-01**（治理条款**不得**降级仍有效的历史结论）。
  - **D02 · closure chain**：`root conflict（NPC-02 now vs V0.4.9/O-4 checkpoint）→ adjudication（N08 无时机→checkpoint；N09 明确当场→now）→ contract propagation（规则 4 扩围／规则 6 新增／NPC-02 修正）→ regression（NR-01～07 = 7/7；NPC = 10/10；剧本 3／4／11 对齐）→ structural check（no new Action／Gap state／counter·debt）`。
  - **EL-02 链路完整性探针 = PASS**：`D02 → N08/N09 → contract change → NPC-02 → NR-01～NR-07 → 现行解释` **全链无断链**；**已移除 `RESOLVED ... pending linkback`**。
  - **账本终局**：**D02–D10 全部 CLOSED**；**D01 OPEN BY DESIGN（唯一仍 OPEN，且本就是设计如此）**。
  - **项目状态**：**V0.4 architecture + defect closure complete; release governance and final documentation remain.**
- **V0.4 Release Baseline（BL-01～BL-10）状态**：**✅ 已建立并只读验证通过（2026-10-03）**；例外 **#33**。
  - **产物**：`docs/v04/v0.4-release-baseline.json`（machine source of truth）＋ `docs/v04/v0.4-release-baseline.md`（human record）；工具 `.gh-search/generate_v04_baseline.py`（可写，仅初始化／经批准 rebaseline）＋ `.gh-search/verify_v04_release_baseline.py`（**永远只读**）。
  - **三层分类（BL-01）**：**A normative** 6（gap-ledger-proposal／interface／pending-resolution-transition／priority-layer／scheduler-fairness／notification-policy）｜**B governance** 3（historical-discovery-governance／v04-defect-ledger／freeze-v0.3）｜**C evidence** 10（interface-v3-migration-manifest／test、pending-resolution discovery、priority 3 份、fairness discovery、notification discovery、e2e-adaptive-replay、full-adaptive、release-evidence-closure）。**`release-evidence-closure` 身份 = release evidence ≠ normative source**。
  - **哈希规格（BL-03）**：**file hash = SHA256(raw bytes) 权威**（不做 trim／换行归一化／排序／语义归一化）；**section hash = 诊断定位**；**禁止** `file DIFF + section MATCH ⇒ 整体通过`。
  - **V0.3 关系**：只**引用**既有 V0.3 baseline（`freeze-v0.3.md` ＋ `freeze_v03.py`），**不复制 24 个 hash**；校验为**组合执行**（V0.3 ＋ V0.4）。
  - **分权**：generator（可写）≠ verifier（**永远只读、无写入参数**）；`--init` **一次性**；rebaseline 须 `--reason`（治理例外 ＋ 批准变更集）。
  - **bootstrap 五阶段**：enumerate（只读、**不声称 MATCH**）→ approval → init（`INITIAL BASELINE` ＋ `effective_at`）→ immediate verify → future verify。
  - **prospective-only 声明**（写入 JSON ＋ Markdown 首页）："**本基线是在 V0.4 架构与缺陷闭合完成后建立的首个可追溯发布基线，自所记录的生效时刻起具有冻结验证效力；它不构成这些文件在此前历史时点始终保持相同内容的证明。**"
  - **退出码**：`0 PASS`／`1 DRIFT`／`2 manifest 不可读`／`3 V0.3 校验失败`（**修复 D12 的"显示 DIFF 但仍像成功"**）。
  - **BL-04**：候选 **20**（normative 6／governance 3／evidence 11），inventory OK（路径唯一、全部存在、scope 与 out-of-scope 无交集）。
  - **BL-06/07**：JSON ＋ Markdown 已写；只读校验 **V0.3 MATCH 24 DIFF 0 UNREGISTERED 0** ＋ **V0.4 MATCH 20 DIFF 0 MISSING 0 UNREGISTERED 0 = PASS**。
  - **Phase C 迭代（诚实记录）**：**尝试 #1 在 Phase D 被否决** —— verifier 检出 **2 个 UNREGISTERED**（`docs/v04/failure-inventory.md` 未分类 ＋ baseline 自身 Markdown 未列入 out-of-scope）⇒ **撤回该次初始化**（不构成 baseline）；修正 scope 后重初始化（20 个 artifact）；其后因**本轮记录文案修正（19→20）**触发一次**经批准的 rebaseline（`--reason`）** → 最终 **baseline-2**。三次动作均证明 **D12 修复后的治理工具正常工作**（DIFF／MISSING／UNREGISTERED ⇒ 非零退出；初始化与验证分权）。
  - **BL-08 反向探针**：`probe_baseline_drift.py` —— 临时副本 pristine **exit 0 PASS** → 注入 drift **exit 1 ＋ DIFF 1 行** → 恢复 **exit 0 PASS**（证明 checker 不是摆设）。
  - **工具是否入册（scope 决策）**：`.gh-search/` 三个治理脚本（generator／verifier／probe）**有意不列入 baseline artifact**（它们是治理基础设施，按 git 版本管理）；D12 的闭合依据是**行为探针**（BL-08）而非工具哈希。若需把工具也钉进 baseline，走 `--rebaseline --reason`。
  - **D12 残余（诚实记录）**：**新路径**（generator／verifier 分权 ＋ verifier 永远只读 ＋ DIFF·MISSING·UNREGISTERED ⇒ 非零退出）已闭合；**旧 `freeze_v03.py --write` 的哨兵重复缺陷仍在**（本轮两次出现，均手工清理，未授权改脚本）。**缓解措施**：`docs/freeze-v0.3.md` 本身是 **V0.4 baseline 的 governance artifact**，因此**该旧脚本若再次损坏它的哨兵区，V0.4 verifier 会立刻报 DIFF**（已成为可独立复核的护栏）。
  - **baseline 迭代记录**：`baseline-1`（20 artifacts，INITIAL）→ `baseline-2` → `baseline-3`（V0.3 哈希表刷新）→ `baseline-4`（**21 artifacts**：D01 Final README 纳入 governance 类）→ `baseline-6` → **`baseline-7`（公开发布版 README 重写，例外 #35；reason 写入 manifest）**。**每次 rebaseline 的 reason 都可反查，且均无运行时语义变更**。**基线版本的唯一权威来源 = manifest 的 `baseline_id`**（文档不再硬编码版本号，避免"改文档→再基线化"的循环耦合）。
  - **公开发布整理（例外 #35，2026-10-03，用户裁定 A）**：**README 非规范性重写**（403→224 行，面向使用者；内部工程信息**迁移不删除**至新建 `docs/project-status.md`）＋ 新增 MIT `LICENSE` ＋ 修正过时编号 `R1–R13`→**`R1–R14`**（权威＝`core/uncertainty-classifier.md`）＋ 补章节锚点（§1／§2.5／§6.6／§11.0）与证据入口（freeze／V0.4 baseline／架构 README）。**未改**任何判据／契约条款／Action·Gap·Notification 规则；**未移动任何 tag**。V0.3 重冻结（README 哈希）＋ V0.4 **rebaseline-7**（`docs/freeze-v0.3.md` 属 governance artifact，登记例外必然使其漂移）。**工具纪律**：未用 `freeze_v03.py --write`（该脚本哨兵重复缺陷仍在，见下方 D12 residual），改为**手工最小替换** §2 中受影响行。
- **D01 Final Architecture README ＋ Final Release Gate（FRG-01～08）状态**：**✅ D01 CLOSED（2026-10-03）**；产物 [`docs/v04/README.md`](../docs/v04/README.md)（取代早期章程）＋ 审计器 `.gh-search/verify_readme_reverse_refs.py`；例外 **#34**。
  - **规格**：按 17 节落盘 —— 首页状态块（三层 closure complete ＋ traceable baseline）｜System Purpose｜Architecture at a Glance（主链 ＋ 旁路 visibility path，明确"架构视图非新状态机"）｜**Ownership Matrix**（六层：输入／输出／**唯一写权限**／明确禁止）｜Interface（锚 ＋ **D04/D05/D06** 三条 clarified boundaries）｜Resolution & Value（**N10** ＋ "不要从参与关系推导事实承诺"）｜Priority｜Fairness（**O-5** 两命题 ＋ N04 表述）｜Notification（四出口 ＋ timing 表 ＋ **B2** ＋ "条件已成立 ≠ 改触发类型"）｜**Notification vs Fairness**｜ASK/§11 边界｜**E1–E8**（Architecture definition CLOSED／Evidence index repaired & verified）｜Historical Governance｜Release Evidence（仅索引）｜Freeze & Release Governance｜**Known Non-goals**（N04／N07／D12 residual，均**非 Release blocker**）｜V0.5 Candidates｜**Final Release Gate**｜**Appendix A · 28 条 Claim Index**。
  - **早期章程**：**显式标注 Superseded**（不静默改写；原文可由 git 历史查回）。
  - **FRG-07 抓到的真实缺陷（已修）**：**CS-06 的传播修复不完整** —— D06 澄清此前只落在**缺陷账本**与 **E2E 措辞**，**从未落进 Interface 正文**（`askable_set` 定义处缺 `OPEN + deferred` 成员资格说明）。**已补 normative home**：Interface **§1.2** 新增该说明 ＋ `delay ≠ remove_from_askable_set`。另 2 条为 README 引用错误（`CL-10` 调度层次实际落在 fairness §1；`CL-11` anchor 改指 `current_round :=`），均已修。
  - **Gate 结果**：**FRG-01** V0.3 `MATCH 24/DIFF 0/UNREGISTERED 0` ✅｜**FRG-02** V0.4 `MATCH 21/DIFF 0/MISSING 0/UNREGISTERED 0` ✅｜**FRG-03** EV-07/08/09 PASS ✅｜**FRG-04** HG-10 PASS ✅｜**FRG-05** EL-02 PASS ✅｜**FRG-06** D02–D12 CLOSED＋D01 complete ✅｜**FRG-07** **28/28 claims 可追，无 README-only rule** ✅｜**FRG-08** README 入 baseline → rebaseline-4 → verifier PASS ✅。
  - **D01 闭合条件**：Final README written ✅｜无历史阶段表述充当当前架构 ✅｜无 README-only 规范 ✅｜合同链接全部有效 ✅｜Known Non-goals 明确分离 ✅｜baseline/evidence 引用正确 ✅｜FRG-01～08 全 PASS ✅。
  - **终局**：**D01–D12 ALL CLOSED**；**Architecture／Evidence／Governance closure PASS**；**Release baseline PASS**；**Final Architecture README PASS**；**Final Release Gate PASS** → **V0.4 RELEASE READY**。
  - **BL-08 反向探针**：临时副本改一字符 ⇒ **DIFF 1 ＋ exit 1**；恢复 ⇒ **DIFF 0 ＋ exit 0**。
  - **BL-09 闭合**：**D11 ✅ CLOSED BY V0.4 INITIAL RELEASE BASELINE**｜**D12 ✅ CLOSED BY GOVERNANCE CHECKER REPAIR**。
  - **账本终局**：**D02–D12 全部 CLOSED；D01 OPEN BY DESIGN 为唯一未闭合项**。
  - **剩余**：**D01 Final Architecture README → Final Release Gate → V0.4 RELEASE READY**。
  - **下一刀（已锁定）**：**V0.4 freeze governance baseline** —— 方向为"确定最终 approved V0.4 contract set → 登记**从此刻起生效**的 baseline → 记录 hash／manifest／approval provenance → 修 governance checker → 未来 drift 可独立验证"；**⛔ 不得写成"这些 hash 证明过去它们一直就是冻结版本"，而应写"这是 closure 完成以后建立的首个可追溯 V0.4 release baseline"**。
  - **禁止项遵守**：未改 `SKILL.md`／§6.3／§11／Interface v2／v3 冻结正文／V0.3／`effective_set` 谓词；未新增 Type／Action／Gap 状态／字段；**未新设 transition path**（PR-17 后续跃迁交由既有 Authorization／T1／T2 合同）。
- **V0.4.4 Priority Model Discovery 状态**：**✅ 30/30 有明确分析结果**；产物 [`docs/v04/priority-model-discovery.md`](../docs/v04/priority-model-discovery.md)。
  - **职责边界（结论 A）**：**Priority 层是"调度器"，不是"决策器"**——输入 = active gaps（state／blocking／risk／dependency）＋ 已由 V0.3 §11.0 选出并经 R4／R6／R14 过滤的动作集合 ＋ 用户显式优先级 ＋ 同轮容量；输出 = **有序 action 队列**。**不得**决定"做不做"、不得覆盖 R4／R6／R14、**不得改写 gap 状态**、**不设计数值评分**。
  - **`deprioritized` 定位（结论 B）**：**是纯调度属性**——但必须与"延后（delay → `OPEN+deferred`）"和"放弃（Refused→assumed）"严格区分。三条边界：① 降权**不能作用于阻塞／R6／高风险 C**（被硬约束吸收，不改状态）；② 上游降权后的下游重评由 Interface §9 负责，**不属 Priority 层**；③ `deprioritized` **不参与"是否继续提问"**（由 Interface §5 闸门／§10 Contract 决定）。
  - **冲突检查**：与冻结规则冲突 **0 例**（三处疑点判明非冲突：P3-06 授权默认 vs 先教再问 → TEACH 非追问、可共存；P4-01/03 用户显式序 vs 上游依赖 → 依赖胜；P5-03/05 用户偏好 vs R4/R6 → 硬约束吸收）。
  - **字段需求**：**需要 1 个非数值承载位** `priority_hint`（表达"先 A 后 B"的相对序；`deprioritized` 的 bool 表达不了）；**不设计分值/权重**。其余复用现有字段，无新增。
  - **禁止项遵守**：未改 §11／V0.3／Interface v1–v3／§10；未新增 Action／Type／Gap state；未设计数值评分。
  - **待裁决**：① 是否建立 `priority_hint`（非数值、纯序）；② 确认 `deprioritized` = 纯调度属性；③ Priority Layer 职责边界是否独立成层（暂不并入冻结正文）。
- **Priority Layer Contract v1 状态**：**✅ 独立成层并冻结（2026-10-02）**；产物 [`docs/v04/priority-layer-contract.md`](../docs/v04/priority-layer-contract.md)（**独立层文档，未并入任何冻结正文**）。
  - **职责**：**只对已经合法的 active actions 做调度；不产生动作、不改变 Gap 状态、不覆盖冻结规则**。架构位置：Gap Ledger → V0.3 Resolution Engine → **Priority Layer** → §11 Question Selection。
  - **六条原则**：P1 硬约束 > 用户提示｜P2 提示只排序合法候选｜P3 `deprioritized` 只降调度优先级｜P4 只排序 V0.3 已选动作（不重选）｜P5 一旦调度到 ASK，§11 独占问题选择与合并判断｜P6 每轮派生排序不持久化，仅 `priority_hint` 在其 scope 内保留。
  - **硬调度约束（收紧）**：**仅四类白名单**——当前 blocker／R6、**R14 三闸门全过的** high-risk C、**§11.6 约束型依赖**、R4 既有顺序与容量。**⛔ 不扩大**成"所有 Type C"（PCY-02）或"所有 dependency"（PCY-03）。
  - **`priority_hint`（新增，本层自有）**：非数值偏序 `{source, scope: current_cluster|current_round|whole_task, relations: [{before: [A,B]}]}`；三条边界 `≠ gap state`／`≠ action selection`／`≠ hard dependency`；顺序可持久化至 scope 失效，**每轮最终排序不持久化**。
  - **`deprioritized`（确认）**：**纯调度属性**；不能导致 `CLOSED`／`INVALIDATED`／`assumed`／停止询问／改 `effective_set`／改动作选择。措辞按裁决修正为 **`expressed_priority` vs `effective_priority`**——"用户可以表达降权，但**硬调度约束可使该降权在当前轮不生效**"（偏好照记）。
  - **`deferred_by_capacity` ≠ Interface `deferred`**：前者是"本轮塞不下"的纯调度事实，**绝不写回 gap 状态**（PCY-04）。
  - **回归与 Canary**：原 **P1～P5 30/30**｜**§11 35/35**｜**V0.3 priority-sensitive 11/11**（HR-01～08 ＋ UB-05 ＋ BS-07 ＋ EU-10）｜**Priority canary PCY-01～12 = 12/12 唯一**（含 4 个硬 canary）。
  - **禁止项遵守**：未改 §11／V0.3／Interface v1／v2／v3／§10；未新增 Action／Type／Gap state；**未设计数值评分**。
- **V0.4.5 End-to-End Adaptive Replay 状态**：**✅ 12/12 跑到底，全部 gate 通过、0 违规**；产物 [`docs/v04/e2e-adaptive-replay.md`](../docs/v04/e2e-adaptive-replay.md)。
  - **12 个 4–8 轮真实会话**（6 类各 2）：正常收敛（E2E-01/02）／中途 Revision（03/04）／授权+风险门（05/06）／外部依赖（07/08）／Priority 与依赖冲突（09/10）／反复质疑与回退（11/12）。每轮记录 10 项 + `Layer owner` + `Violation?`。
  - **六条系统不变量 E1–E6 全部成立**：E1 单一 authoritative｜**E2 只有 Interface 改 Gap 状态**｜**E3 只有 V0.3 决定 Action 类型**｜**E4 Priority 只排序合法 Action**｜**E5 §11 只在 ASK 被调度后工作**｜**E6 用户可见输出无内部机制词**。
  - **通过指标**：Layer ownership violation **0**｜错误重复询问 **0**｜硬约束被 `priority_hint` 越过 **0**｜过期 hint 泄漏 **0**｜authoritative 冲突 **0**｜机制词泄漏 **0**｜K5 **0**。
  - **未发现任何"某层越权／缺接口"实例**；**未为全绿补规则**。
  - **残留观察（移交 V0.4.6，非失败）**：O-1 `priority_hint.scope=current_round` 的"一轮"边界未定义；O-2 "顺序偏好 + 延后"同句需分解（本轮用 §10 复合语句分解契约处理）；O-3 `deferred_by_capacity` 连续容量不足的累积可见性。
- **V0.4.6 Priority Hint Language & Lifecycle Discovery 状态**：**✅ 30/30 有明确解析结果**；产物 [`docs/v04/priority-hint-language-discovery.md`](../docs/v04/priority-hint-language-discovery.md)。
  - **规模**：**30 例** —— A 顺序表达解析 8／B scope 判定 8／C 生命周期与 Revision 6／D 冲突·条件·复合 8；每例记录 11 项（含 **Reason for expiry**，仅允许 `scope ended`／`target removed`／`superseded by newer hint`／`Revision invalidated referent`／`explicit cancellation`）。
  - **解析契约验证**：只产出**能确定的偏序边**（`A ≻ {others}` **不脑补** B 与 C 之间；`A 做完再处理 B` **不生成 dependency**；"你判断" **不产出 relation**）。
  - **五条不变量 H1–H5 全部成立**：H1 hint 只表达偏序｜H2 scope 不泄漏（cluster 外项不受影响）｜**H3 Revision 不无脑删 hint**（C-01 目标变更后 keep、C-04 值失效但 gap 活跃 keep、C-05 target removed 才 expire）｜**H4 supersede/shadow 可解释**（D-05/D-06 supersede、C-06 shadow 且 cluster 结束自动恢复）｜**H5 不制造 dependency/blocker/risk**（A-07、D-01、D-02）。
  - **O-1 收口**：**Interpretation B 胜出**——`current_round` 应绑定**一次调度周期（action bundle）**而非"某条消息"（证据 B-08：按 A 解释同一 bundle 后半段会丢 hint）。（**结论仅记录，未落规则**。）
  - **O-2 收口**：`先 A，B 以后再说` **必须拆两事件** = `priority_hint(A≻B)` ＋ `delay(B)`（状态由 Interface §3 承担）；并确立 `deprioritized` vs `delay` 判定口径（"不管/不处理/以后再决定"→delay；"排后面/不急/优先级低"→deprioritized）。
  - **通过标准**：错误状态写回 0｜错误 Action 改写 0｜硬约束被越过 0｜scope 泄漏 0｜delay/refused 当 priority 0｜priority 当 dependency 0｜**K4 = 0**｜**K5 = 1**（**B-03**，定位到 **scope 歧义**：时间窗表达在 `{current_round, current_cluster, whole_task}` 无对应项）。
  - **K5 处置**：**未自动补字段**——现有 `source/scope/relations` **结构足够**，缺的是**判定契约**（时间窗 → 最近似 scope 映射 + 到期语义）；**待裁决**。
  - **禁止项遵守**：未改 Priority Contract v1／§11／V0.3／Interface v1–v3／§10；未新增规则／字段／Action／Type／Gap state；未设计数值评分；O-3 未进入本轮。
- **V0.4.6 收口（L1–L3 落盘）状态**：**✅ V0.4.6 Priority Hint Language & Lifecycle 正式冻结（2026-10-02）**；规范落点 [`docs/v04/priority-layer-contract.md`](../docs/v04/priority-layer-contract.md) **§9（v1.1 增量，§1–§8 未动）**。
  - **L1**：`scope` 与 temporal lifetime **正交** —— `scope ∈ {current_round, current_cluster, whole_task}` ＋ 可附 **`valid_until`**／expiry condition；**不新增 `timed` scope**；结构作用域无更窄证据时取 `whole_task`，由 `valid_until` 限生命周期。
  - **L2**：`current_round` = **一次 scheduler action bundle 的完整生命周期**（起于 bundle 生成；止于全部完成／被取消／失效并触发重排）；**单条 user/assistant 消息不自动结束它**（`ASK(q1)+ASK(q2)` 中答 q1 后 hint 对 q2 仍有效）。
  - **L3**：`deprioritized` vs `delay` 按**效果**区分，**不按关键词**；机械判据＝"**还能不能在当前处理窗口里顺手处理？**"；关键词仅作 cue，不足时一次最小澄清。
  - **重跑结果**：**B-03 K5 消失**（→ `whole_task + valid_until`）｜原 **30/30 保持**｜**PHC-01～08 = 8/8 唯一**｜**K4 = 0、K5 = 0**｜scope leakage **0**｜delay/prioritization 混淆 **0**。
  - **未新增**：`timed` scope／Gap 状态／Action／Type／数值权重。
  - **O-3**（连续多轮 `deferred_by_capacity` 的 starvation / fairness / 可见性）：**仍单列下一阶段**。
- **V0.4.7 Scheduler Fairness & Starvation Discovery 状态**：**✅ 30/30 有明确分析结果**；产物 [`docs/v04/scheduler-fairness-starvation-discovery.md`](../docs/v04/scheduler-fairness-starvation-discovery.md)。
  - **规模**：**30 例** —— A 真 starvation 6／B 假 starvation 6／C starvation×用户 priority 6／D fairness×hard constraints 6／E notification·可见性 6；每例 11 项（④ 连续次数为**观测数据，非规则**）。
  - **F1 最小定义**：`starvation candidate ⟺ eligible ∧ 真实原因是容量／软排序竞争 ∧ 无 hard 阻断 ∧ 跨调度周期计数 > 0`（**同一 bundle 内未轮到不算**：A-04）。"连续没执行"太宽（B 组 6 例证伪）；**不设阈值**（2 轮与 3 轮均仅作观测）。
  - **F2**：fairness 可修正**软排序竞争**；**绝不可越过** R6／R14／R4／§11.6（D 组 6/6）；用户显式 soft hint 属**未决**（K5）。
  - **F3**：`deprioritized`（"C 不急"）连 10 轮未做 ⇒ **不是 starvation**（忠实执行用户偏好）；但"不急，**但别忘了**"产生 **`must_not_starve` 需求证据**（效果＝通知义务，非自动提升）；**本轮禁止新增该字段**。
  - **F4**：**promotion 与 notification 必须分开**——"应提醒但不应提升"（E-01/03/04）与"可提升但无需提醒"（A-02、C-05、D 组）同时存在。
  - **F5**：**debt 绑 `gap identity + 当前 resolution generation`，不绑 action 类型**——同 gap 动作 `ASK→SHOW` **继承**（A-05）；全新 gap 同动作类型 **不继承**（A-06）；失效 action **不继承**（B-05）。
  - **通过标准**：ineligible 误判 starvation **0**｜fairness 越过 hard constraint **0**｜delay 误当 starvation **0**｜失效 action 继承等待债 **0**｜**K4 = 0**｜**K5 = 2（同一类：`fairness vs user preference` → C-01／C-04，待裁）**。
  - **K5 处置**：**未自动补字段**——现有 `priority_hint`／`deprioritized`／hard constraints **表达力足够**，缺的是**判定契约**（用户 soft hint 与 fairness 的优先关系）。
  - **fairness ledger 证据（不设计）**：跨轮观测需**跨轮留存**（A-01/02/03/05）＋ identity·generation 清零（A-06/B-05）→ 支持"可能需要"；`must_not_starve` 属 **notification policy**。**本轮未新增任何字段**。
  - **禁止项遵守**：未改 Priority Contract v1.1／Interface／§11／V0.3；未新增 Gap state／Action／Type／priority score；未规定"连续 3 轮必须提升"。
- **V0.4.8-A Scheduler Fairness Contract 状态**：**✅ 独立合同 v1 建立并冻结（2026-10-02）**；产物 [`docs/v04/scheduler-fairness-contract.md`](../docs/v04/scheduler-fairness-contract.md)。**O-3 正式关闭** → 分裂为 **A. Scheduler Fairness**（本合同）／**B. Notification Policy**（V0.4.8-B）。
  - **调度层次（仅调度层）**：`Hard scheduling constraints > explicit active user priority > fairness adjustment > ordinary soft scheduling preference`；**用户明确偏好可被硬约束覆盖，但不被 fairness 偷偷覆盖**。
  - **六条原则 F1–F6**：只有 eligible-but-unscheduled 且原因属 capacity／soft competition 才累积 debt｜hard 永不因 fairness 被越｜仍有效的 explicit user priority 不被自动覆盖｜无显式用户排序时 fairness 可修正普通软排序｜debt 绑 `gap identity + resolution generation`｜ineligible 周期不增债、generation 变化旧债终止。
  - **Fairness Ledger（scheduler-local 观测账）**：`gap_id / resolution_generation / eligible_unscheduled_cycles / last_skip_reason / last_eligible_cycle / starvation_candidate`；key = `gap identity + resolution generation`（**不绑 action 类型**）。`resolution_generation` = 当 gap 的当前 resolution problem 被 Revision／invalidation／replacement 实质重建时前进的 **Scheduler 派生 epoch**，**不进 Gap 生命周期正文**，且**不影响** current_value／confidence／validity／Action／§11。
  - **计数是证据不是政策**：`eligible_unscheduled_cycles` 可记录，**不产生"N → 必须 promotion"**；不引入数字评分。
  - **fairness 恢复资格的三种情形**：hint scope 到期（含 `valid_until`）／用户取消或修改 hint／C 不再被该 relation 覆盖。
  - **职责边界**：fairness 可识别 starvation candidate、修正普通软排序、在无有效用户 relation 时 promotion；**不可**越 hard、不可越有效用户显式排序、不可改 Gap 状态、**不可发用户通知**（属 B）。
  - **验收**：V0.4.7 **30/30 保持**｜新证伪集 **SFC-01～18 = 18/18 唯一**｜**K5-1（C-01/C-04）关闭**｜公平越硬约束 **0**｜偷偷覆盖有效用户排序 **0**｜ineligible 累积 debt **0**｜失效/新 identity 继承旧债 **0**｜通知越权 **0**｜**K4=0、K5=0**。
  - **禁止项遵守**：未改 Priority Contract v1.1／Interface／§11／V0.3；未新增 Gap state／Action／Type／数值评分；`visibility_commitment` **未放入 Scheduler**（留 V0.4.8-B）。
  - **下一步**：**V0.4.8-B Notification Policy**（引入 `visibility_commitment`）。
- **V0.4.8-B Notification Policy Discovery 状态**：**✅ 30/30 有明确分析结果**；产物 [`docs/v04/notification-policy-discovery.md`](../docs/v04/notification-policy-discovery.md)。
  - **职责**：Notification Policy **只回答**"有哪些长期未处理事项现在应该让用户知道？"；可读取 `starvation candidate`／`visibility_commitment`／用户显式 `delay`／`deprioritized`／交互负担；**不可**改调度、promotion、改 Gap、改 Action（30/30 例"改调度=否""改 Gap=否"）。
  - **候选模型**：输出 `notify_now｜notify_later｜record_only｜never_notify`；字段 `visibility_commitment{required, trigger: now｜condition｜time_window, discharged}`（**本层字段，不进 Scheduler**）。
  - **Q1 必须提醒**：⟺ `visibility_commitment.required=true` ∧ 触发条件成立 ∧ 事项仍存在且合法；**`starvation candidate` 单独不足以**主动提醒（NA-06／NE-01）。
  - **Q2 一次够不够**：**一次足够**——未回应不得逐轮复催；同承诺去重；已提醒 2 次进静默。
  - **Q3 "知道了"是否解除**：**解除**（`discharged=true → never_notify`，历史保留痕迹）；`先放着吧` → 降级 record_only；`那你现在做吧` → 承诺达成并解除；新 generation → 旧承诺结束。
  - **Q4 防骚扰五条**：一承诺一次／合并进既有输出／负担优先（高负担延后或仅记录）／冷静期／不催已明确 delay 且未要求可见的事。
  - **Q5 `delay` 是否允许提醒**：`delay` 且**无** commitment → **不允许**；`delay` **＋** `别漏掉`／`但别忘` → **允许且一次为限**（delay 决定"现在不处理"，不决定"是否可以提"）。
  - **架构验证**：`promotion ≠ notification` 成立（Fairness 只提供输入）；调度公平／用户优先权／用户可见性**三维度分离**（同一事项可 `deprioritized=true` ＋ `visibility_commitment=true` ＋ 调度序不变）。
  - **K4 = 0**；**K5 = 2 类**：**K5-1 `notification boundary`**（纯 starvation candidate＋零用户表达时是否应主动提醒）、**K5-2 `timing`**（`这个以后提醒我` 的"以后"未指定时机）。
  - **K5 处置**：**未自动补字段**——`visibility_commitment{required, trigger, discharged}` **结构够用**，缺的是**判定契约**（时机 + 零表达边界）。
  - **禁止项遵守**：未改 Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3；未新增 Gap state／Action／Type／数值化通知频率评分。
- **V0.4.8-B Notification Policy Contract v1 状态**：**✅ 正式 sibling contract 建立并冻结（2026-10-03）**；产物 [`docs/v04/notification-policy-contract.md`](../docs/v04/notification-policy-contract.md)（与 Scheduler Fairness **共享证据、互不写权**）。
  - **第 1 条（宪法条款）**：Notification Policy **不得**改变 `ordered_actions`／promotion／gap status／Action／创建 blocker·risk；只回答"有哪些长期未处理事项现在应该让用户知道？"。
  - **输出词表（封闭）**：`notify_now｜notify_later｜record_only｜never_notify`。
  - **K5-1 封口**：**零表达的 `starvation_candidate` 默认 `record_only`**；钉成 **`fairness evidence ≠ notification obligation`**；例外保住——**任务结束前披露未完成内容属既有交付完整性责任**，不由 starvation 触发。
  - **K5-2 封口**：`以后提醒我` → **`condition = next_relevant_checkpoint`**（**不是**"下一轮"、**不是**"有空位"）；含机械定义、典型/非 checkpoint 清单、**时机解析顺序 1–5**（时间→条件→复用既有恢复条件→checkpoint→仅在错误时机有明显损失时最小澄清）；**默认不立刻反问"什么时候"**。
  - **`visibility_commitment` 定位**：**用户可见性义务 ≠ 需求状态 ≠ 调度优先级** → `true` **不意味着** priority↑／starvation debt↑／action eligibility↑。
  - **一次足够**：**one commitment → at most one proactive notification**；仅三种情形可重建（用户明确重建／新 resolution generation／用户明确要求重复或条件性提醒）；**禁止**"第 1 次／第 2 次／冷静期"式次数债。
  - **delay 四象限**：否·否＝正常无义务｜否·是＝正常但须满足可见承诺｜**是·否＝延后且不催**｜**是·是＝延后但 trigger 后允许提醒一次**。
  - **验收**：原 Discovery **30/30 保持**｜**NPC-01～10 = 10/10 唯一**｜**K4 = 0、K5 = 0**｜Notification 改调度 **0**｜Notification 改 Gap **0**｜starvation 自动生成通知义务 **0**｜delay 无授权被催 **0**｜重复主动提醒 **0**｜**sibling boundary regression 通过**。
  - **O-3 整条债完成**：Fairness ✅／starvation observation ✅／user explicit priority ✅／notification visibility ✅。
  - **禁止项遵守**：未改 Priority Contract v1.1／Scheduler Fairness Contract v1／Interface／§11／V0.3；未新增 Gap state／Action／Type／通知计数器。
- **V0.4.9 Full Adaptive E2E Replay 状态**：**✅ 12/12 跑到底，E1–E8 全通过，全部 gate 指标为 0（K4 = 0、K5 = 0）**；产物 [`docs/v04/full-adaptive-e2e-replay.md`](../docs/v04/full-adaptive-e2e-replay.md)。
  - **被测链**：`Feedback → Interface → V0.3 → Priority → Fairness → Action Bundle → §11 → User-visible`＋旁路 `Fairness Ledger → Notification`。
  - **12 剧本（5–9 轮）**：纯 starvation 无义务 ×2｜`不急但别忘了`×2（含高负担延后）｜显式 priority × fairness ×2（含取消 hint 后恢复资格）｜delay 对照 A/B ×2｜external dependency ＋ notification｜resolution generation｜notification 与高负担冲突｜**9 轮大混合压力剧本**。
  - **E1–E6 沿用＋新增 E7／E8**：**E7 = Fairness 不得改变 Gap 状态／Action 类型／显式用户 priority relation** ✅；**E8 = Notification 不得改变调度／Gap／Action，只影响可见性** ✅。
  - **关键结论**：① **fairness 全程未偷偷翻转用户序**（剧本 5/6，debt 累积而 A ≻ C 不动）；② **同一结果两条链不可混**——"有承诺时重新暴露"走 Notification，不走 fairness（剧本 6）；③ `deprioritized` 的项**不累积 debt**，故"长期没排上"与"用户要往后排"在**证据层**即分开（O-5）；④ 关键拍板**不被提醒打断**（`notify_later`，剧本 4/11）。
  - **Release Gate（全 0）**：Layer ownership violation｜错误重复询问｜hard constraint 被越过｜explicit priority 被 fairness 偷偷覆盖｜starvation 自动变提醒｜visibility commitment 漏兑现｜重复主动提醒｜**错误主动提醒**｜**承诺触发后漏提醒**｜过期 generation 债务泄漏｜机制词泄漏｜**K4／K5**。
  - **观察**：**O-4**（`别忘了`＝无时机可见请求 → 按 §6.2 规则 4 归 `next_relevant_checkpoint`，属规则语义覆盖，README 澄清项）；**O-5**（`deprioritized` 不累积 debt 是 E7 成立的前提，README 应写明）。
  - **下一步（用户已定顺序）**：全绿 → **停止继续加 V0.4 行为规则** → 写 **V0.4 Final Architecture README** → **V0.4 正式封版**。
- **V0.4 Defect Ledger（D 账本）状态**：**✅ 建立（2026-10-03）**；产物 [`docs/v04/v04-defect-ledger.md`](../docs/v04/v04-defect-ledger.md)。
  - **D02 已裁决（用户确认按 B 生效）**：裸"别忘了。"**取 B** —— 不产生 `notify_now`；建立 `visibility_commitment{required:true, trigger:condition, condition:next_relevant_checkpoint}`。
  - **净化表述（消除矛盾的关键）**：**`notify_now` 是"兑现形态"，不是独立触发条件**；`trigger=now` 收窄为"**用户明确要求现在就提**"（例："现在告诉我还差什么"）；裸"别忘了"走 `condition`，若解析时刻本身即自然检查点则**当场兑现**（机制上仍非 `trigger=now`）。
  - **D03 已裁决**：`trigger=now` = **用户指定当场**；判定表 7 行（now／time_window／condition／复用恢复条件／"以后"→checkpoint／**裸"别忘了"→checkpoint**／最小澄清）；三条边界——**B1** `now` 不是"更紧急"（不改调度/Gap）｜**B2** **只有系统自选时机（checkpoint）适用 burden 延后；用户指定时机（now／time_window／明确 condition）不因 burden 延后**（同构于"用户明确偏好不被内部软机制偷偷覆盖"）｜**B3** `now` 仍须"事项仍存在且合法"。
  - **D04–D10 拟裁（待一次性确认）**：**D04** `discharged` = Notification 层内部状态（非 Gap 写回）｜**D05** `notify_later` 只推迟到**下一个 checkpoint**，每 checkpoint 至多尝试一次｜**D06** `cycle` 与 `current_round` **同义**（＝action bundle 生命周期），不另立定义｜**D07** `starvation_candidate=true` ⟺ F1/F6 成立 ∧ `eligible_unscheduled_cycles ≥ 1`，**该门槛只决定"候选观测"资格，不触发任何调度或通知动作**｜**D08** commitment 随 `gap identity + generation` 存在，**不随 cluster 结束失效**，仅 generation 变化才终止｜**D09** Discovery C-03／C-06 与 D02 同判（无时机→checkpoint）｜**D10** "用户再次提到"＝**兑现**（非重建），故不产生第二次主动提醒。
  - **冲突证据（三处）**：Discovery NA-01（`trigger=now`→`notify_now`）vs Contract §6.2 规则 4／NPC-02（行内 trigger 与文字自相矛盾）vs V0.4.9 剧本 3（checkpoint）／O-4。
  - **传播修复清单（待后续步骤，本步未执行）**：F1 改 NPC-02 trigger／F2 规则 4 扩为"任何不含时机的可见请求"＋**新增规则 6（明确要求当场→now）**／F3 Discovery **不覆写历史**（追加封口更正，覆盖 NA-01／C-03／C-06）／F4 O-4 升为判定契约／F5 剧本 3·4·11 仅标注引用／**F6 Contract 第 6·7 条补 burden 只作用于系统自选时机 ＋ notify_later 落点**／**F7** Fairness §3 补 cycle 括注与 `≥1` 候选资格／**F8** Contract 第 4 条补 `discharged` 写权限／**F9** E2E `W` 行标注"Notification 内部状态"。
  - **最小回归**：`D02-A～D`（裸"别忘了"→checkpoint／"现在说"→now／"以后"→checkpoint 防回归／裸"别忘了"＋当前即检查点→当场兑现）＋`D03-A～C`（"现在说"遇 R6 仍立即兑现／无 R6 同样 now／"以后"遇 R6→notify_later 对照）；重跑 NPC-02／NPC-03 ＋ 剧本 3／4／11；门槛 K4=0、K5=0、错误主动提醒 0、漏兑现 0。
  - **处理顺序**：D02 ✅ → D03 ✅ → D04–D10（拟裁待确认）→ 修 E2E 证据 → 最小回归 → K4/K5 重确认 → 冻结治理 → Final README → 封版。
  - **本步边界**：**未改任何冻结正文、未新增字段**（账本为新建文件；仓内此前**无** D 账本，仅有 `O-1`～`O-5`）。
- **暂缓**：`deprioritized`（移交 Priority Layer）／`pending_resolution` 二次质疑计数（待 `feedback.intent` 落地）。
- **新增固定回归（用户裁决）**：**L-20（reset）／L-23（revert）／L-24（revision scope）／L-25（split feedback）／L-30（revision+conflict）**——今后任何字段改动必须让这 5 例继续通过；本轮已全部关闭（唯一裁定）。
- **工程纪律（本轮确立）**：映射层出问题时**不改 Interface v2**，先判定是**字段不足**还是**语义解析不足**。本轮结论：不唯一 5 例全部为**已延期字段缺失（4）**或**语句复合（1）**，语义解析不足 **0 例**。
- **V0.2 冻结状态的权威来源 = 本文件**（用户裁决 2026-10-02）：`docs/freeze-v0.3.md` 是版本冻结历史说明，若与其表述冲突，以本文件的"当前验收状态"为准。
- **接口层独立于 §11**：`docs/v04/gap-ledger-interface.md`（Gap Ledger → Question Selection 接口）与 §11 分离；§11 未被修改，接口层不得改写 §11 判据（用户裁决：测试已证明 §11 没错）。
- **V0.3 定位：§2.5 / §11.0 / §6.6 为新增章节**（未知类型分类 / 动作选择优先 / 决策记录），追加在各自位置；**V0.3 未修改任何冻结段落的文字**（哈希复核 5/5 MATCH，见下）。
- **⚠️ V0.3.3 冻结例外（2026-10-01，测试证据驱动）**：迁移回归发现 **Case A / W6**（产物已锚定、受众缺失、含模糊审美词）与**契约 R11 字面读法**给出**相反首动作**，导致同一输入有两个"唯一正确动作"。按冻结语义"改动必须先补失败案例"，此属**已失败案例**，故对 **§3 追加一行范围注（不改判据）**：
  - 追加内容仅说明"P0 缺失 → 先问目标"在 V0.3 下细化为**锚点缺失**触发；**§3 原判据文字一字未改**。
  - 因 §3 哈希随之变化（**MATCH → 新基线**），旧基线 `b21c73bf…` 作废，以「保护基线（哈希）」表内新值为准。
  - 这是**第二次冻结区范围例外**（第一次是 V0.1 的 §6.5）。不代表以后可以自行扩展冻结章节。
- **冻结区修改协议（V0.3.4 确立，五条件缺一不可）**：冻结区的意义是**防止无证据改动**，不是绝对不可改。任何对 §2.1 / §3 / §6.3 / §6.4 / §6.5 的修改必须**同时**满足：
  1. **有新测试证明冲突**（可复现的失败案例，不是"感觉可以更好"）
  2. **非修改不可解决**（无法通过新增章节 / 契约条款 / 优先级声明解决）
  3. **修改范围最小**（只加必要说明或限定词；能加"适用范围注"就不改判据原文）
  4. **全量回归**（该节相关用例 + V0.3 专项 + 迁移回归全部重跑）
  5. **新哈希重新建立**（旧基线作废，新值写入本表并注明变更原因）
  - 记录义务：每次例外都要在本节登记**序号 / 日期 / 触发案例 / 改动内容 / 新旧哈希 / 回归结果**。
  - 当前例外登记：**#1 §6.5（V0.1，"采访决策缺口修复"轮，D1/D2/F1 失败案例）**、**#2 §3（V0.3.3，Case A/W6 与契约 R11 冲突）**。
- **⚠️ 行号已因 V0.3 插入而位移**（§1 追加 4 行 → +4；§6.5 之后插入 §6.6 → §6.3 起 +61）。基线文档此前声明的"未移动冻结区行号"在 V0.3 起**不再成立**；按下方口径，**以内容哈希为准**，行号仅作定位参考。
- 冻结语义：除出现**新的失败案例**（既有裁定规则无法得出唯一答案）外，不再改动；任何改动必须先补失败案例 → 再改规则 → 再全量回归。

**保护基线（哈希）**

计算口径：取章节**标题行**到下一个分隔（`---`）或**下一个同级 / 更高级标题**之间、**去掉尾部空行**后的原文，以 `\n` 连接后按 UTF-8 计算 `sha256`。

- **§3 的口径例外**：§3 是 `##` 级标题，其冻结范围**包含子节 §3.1 / §3.2**，因此取到下一个 `---` 为止（不因遇到 `###` 而截断）。
- **§2.1 / §6.3 / §6.4 / §6.5 均为 `###` 级**，取到下一个 `###` 或 `---` 为止；§6.5 的下一个 `###` 即 §6.6。

| 章节 | 行区间（V0.3 实测） | sha256 | 与基线 |
|---|---|---|---|
| §2.1 | 87～155 | `26e207d736b0ad747fa3bb69bded41fb1720b2fbf8b109a6634f96e8b4ad3d38` | **MATCH** |
| §3（含 3.1 / 3.2） | 159～221 | `24efa40f9b64f335ba2b4dd5c2d053cadadef22a73bb1e697703cb25a122d1cd` | **V0.3.3 新基线**（附加一行范围注，判据未改） |
| §6.3 | 359～372 | `8571705186f487b20712c2d8e2f25d96d9b799acf3be45d4248dfbb1d5c04b52` | **MATCH** |
| §6.4 | 374～382 | `60315aa5681c0814193e1575c4b4792a22512c922944a465cf9d1212740d3e47` | **MATCH** |
| §6.5 | 384～421 | `aef796ad3a5bda6a5c2fc00480be083b33dbb02e5eb54a8780090511819792b0` | **MATCH** |

> 基线值（V0.1/V0.2 记录）：§2.1 83～151、§3 155～215、§6.3 288～301、§6.4 303～311、§6.5 313～350。
> **V0.3 → V0.3.3 变化**：§2.1 / §6.3 / §6.4 / §6.5 四节哈希仍与基线相同（**内容零改动**，仅行号位移）；**§3 因 V0.3.3 追加一行范围注而变更哈希**，旧值 `b21c73bfadeee8a96a1a6bba4c4b54b5458d359e38430002a92a9d7663656bf3` 作废，新值见上表。

> 基线值（V0.1/V0.2 记录）：§2.1 83～151、§3 155～215、§6.3 288～301、§6.4 303～311、§6.5 313～350，哈希与上表逐一相同 → **内容零改动，仅行号位移**。
> 复算脚本：`.gh-search/freeze_check.py`（按上述口径自动取块并比对基线）。
>
> 校验脚本（pwsh，以 §2.1 为例，行号需按上表更新）：
> ```powershell
> $l = Get-Content -LiteralPath SKILL.md -Encoding UTF8
> $blk = ($l[86..154]) -join "`n"   # 行 87～155（0 基索引 86～154）
> ([System.Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes($blk)) | ForEach-Object { $_.ToString('x2') }) -join ''
> ```
> 行号会随其他章节编辑而移动；若行号与哈希不一致，以**按上述口径取到的内容哈希**为准。

## 三、验收结论

| 项 | 结果 | 说明 |
|---|---|---|
| R1～R8 全部通过 | ☐ 通过 ☐ 不通过 | |
| 机制完整性 5 项 | ☐ 通过 ☐ 不通过 | |
| 反模式命中数 | ____ 处 | |
| 冻结基线哈希一致（5 节） | ☐ 一致 ☐ 不一致 | |
| 结论 | ☐ 验收通过 ☐ 需修改后复验 | |

**验收人**：＿＿＿＿　**日期**：＿＿＿＿
