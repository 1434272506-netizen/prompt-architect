# GitHub 同类 Skill 调研报告

> 目标：找 GitHub 上是否存在与 `prompt-architect`（需求采访 / 模糊词澄清 → 结构化 Prompt）同类的提示词 Skill。
> 调研时间：2026-10-01 · 方法：GitHub REST API（api.github.com，仓库检索） + raw.githubusercontent.com 拉取原文，本地 3-gram 相似度比对。
> ⚠️ 本机 VPN（fake-ip 198.18.0.0/16）劫持 github.com，`web_fetch` 不可用；**未登录的 GitHub 代码全文搜索已返回 401（GitHub 现已要求认证）**，因此"全站逐字比对"未做。

---

## 0. 结论速览

| 结论 | 判断 | 依据 |
|---|---|---|
| GitHub 上有没有**和本仓库相同/同源**的 skill？ | **没有** | 直接复制类没有：repo 检索无同名副本；3-gram 最高重合仅 4.6%（功能词底噪水平） |
| 有没有**同题（需求采访/澄清后再生成）**的 skill？ | **有，而且是一条成熟赛道** | 至少 8 个独立实现，含 2 个中文实现、1 个明确支持 DeepSeek Harness |
| 你的实现是否落后？ | **不在"有没有"，在"工程化"** | 机制覆盖度与生态最强者（sharpen / req）基本持平；差距在**可验证性、提问工具原生调用、交付物形态、迭代证据链** |

---

## 1. 最接近的三个对象

### 1.1 [Cunzhang0703/req-interview-skill](https://github.com/Cunzhang0703/req-interview-skill) —— 中文同题，重叠度最高

- 4 stars / MIT / 建仓 2026-09-19 / 最后推送 2026-09-30，**纯提示词、无脚本无依赖**
- 口号几乎与你的 README 同构：**"先把'想做什么'问清楚，再动手写。"**
- 明确支持 **WorkBuddy / OpenAI Codex / DeepSeek Harness** 三平台（有 `install-deepseek-harness.md`）
- 结构与你的 §1–§11 高度对应：`§1 先增强提示词再判断范围` / `§3 分轮追问 1—3 题` / `§4 查漏视角 8 个` / `§5 谁来决定` / `§7 收口标准 7 条` / `§8 需求简报` / `§9 交接退出`
- **它有而你没有的**：
  1. **提问优先调用宿主的原生结构化提问工具**（DSH 的 `ask_user_question` 式弹窗），并给出参数规范（1—3 题、2—4 项、推荐项置首、禁止手写"其他"）；无工具才降级为正文提问
  2. **需求可视化交付**：思维导图 + 功能架构图（Mermaid → SVG 落盘 → 读回验证）
  3. **`docs/design-notes.md` 失败模式表**：每条规则对应一个真实失败模式（"改规则前先判断能不能删"）
  4. **`scripts/check-skill.sh` 零依赖完整性校验** + CI + CONTRIBUTING 要求"改一个词要附改动前后实测对比"
  5. 决策记录五状态：`用户已确认／证据已核实／AI 建议／待决定／暂不做`
- **你有而它没有的**：§3.1 Conflict/Tension 分离、§3.2 unresolved 计数、§6.5 Revision/局部重开、§11 问题选择（同层裁界、上游依赖优先、降维问法）、双轨标记的出口强制分区、对抗测试集（`tests/*`）
- 它的设计笔记明确**拒绝**了"需求成熟度 95%"这类不可验证指标 —— 与你的"可验证优先于好看数字"同向

### 1.2 [arjunlohan/sharpen](https://github.com/arjunlohan/sharpen) —— 机制最精巧

- `skills/sharpen/SKILL.md` + `skills/sharpen/interviewing.md`
- **四象限未知**（本仓库独有视角）：known knowns→同事测试 / known unknowns→采访 / unknown knowns→**展示选项而非追问** / unknown unknowns→**blind-spot pass**
- 硬约束与我方一致：**每轮 ≤3–4 问、每问附推荐默认值、架构影响最大的先问、两轮封顶后写入 `Assumptions:` 块、问题能自己查证就不要问**
- **它有而你没有的**："unknown knowns 用选项扇/一次性原型去逼近品味"（适合设计类模糊需求，正是你 §4 模糊词表的短板：你靠问，它靠**给 4 个截然不同的方向让用户反应**）、"把答不出的问题转成 discovery step 写进 Prompt"（你归为 unresolved/延后，它更进一步落到产物里）

### 1.3 [MoizIbnYousaf/Ai-Agent-Skills](https://github.com/MoizIbnYousaf/Ai-Agent-Skills/blob/main/skills/ask-questions-if-underspecified/SKILL.md) 系列 —— `ask-questions-if-underspecified` 家族（最流行的轻量版）

同名 skill 至少有 4 个独立副本：MoizIbnYousaf / sickn33 / hanzo / oimiragieo，原始作者为 [@thsottiaux](https://x.com/thsottiaux)。共同骨架：

- 触发判据：objective / done（验收）/ scope / constraints / environment / safety-reversibility 六项缺任一即 underspecified
- 每轮 1–3 问（Moiz 版 1–5 问），**必附推荐默认值**，支持 `defaults` 快通道与 `1b 2a 3c` 紧凑作答
- 明确"**不要问你能靠低风险只读检查查到的**"
- **一律 ≤3 问**（agent-studio 版列为 Iron Law：>3 问导致决策瘫痪）
- 局限：面向**软件实现**（scope/tech），不做模糊词拆解、不做双轨标记、不产出 Prompt 成品 —— 定位比你的窄

---

## 2. 其他相关（不同定位，供参考）

| 仓库/包 | 定位 | 与你的关系 |
|---|---|---|
| [@ckelsoe/prompt-architect](https://www.npmjs.com/package/@ckelsoe/prompt-architect)（npm v3.5.1） | 名字撞车：31 个提示词框架 × 7 类意图，分析并改写 Prompt | **同为"改 Prompt"但无采访循环**，走"诊断+重写"路线 |
| [HenrikBrehm/prompt-refiner-skill](https://github.com/HenrikBrehm/prompt-refiner-skill) | 提示词**静态检查器**（lint 规则、确定性 pass + 模型 pass） | 互补：可做你出稿后的质量闸门 |
| [Q00/ouroboros](https://github.com/Q00/ouroboros) `skills/interview/SKILL.md` | 50KB 重流程采访：版本检查、MCP 前置、Path A/B 双模式、不可跳过门禁 | 工程化最重，**不适合口语化模糊需求**，但对"门禁/证据"可借鉴 |
| [obra/superpowers](https://github.com/obra/superpowers) `brainstorming/SKILL.md` | 头脑风暴式发散（req 仓库的工程规范也参考了它） | 与你的收敛式采访正相反 |
| [theultimate-dev/skills](https://github.com/theultimate-dev/skills) | 插件化 skill 集：`improving-prompts` / `guiding-product-discovery` / `shaping-product-briefs` | 与你最近的是 `shaping-product-briefs`（产出需求简报） |
| [trailofbits/ask-questions-if-underspecified](https://github.com/trailofbits/ask-questions-if-underspecified) | 检索命中最多的原始出处，**仓库 API 返回 404（已改名/删除）** | 仅存镜像 |

---

## 3. 生态位判断

```
                     轻量（1 个 SKILL.md）                          重（多文件+交付物+CI）
 面向软件实现   ask-questions-if-underspecified 家族  ──────────►  req-interview-skill
 面向任意产物   prompt-refiner（检查）/ improving-prompts        sharpen（四象限+采访）
 面向任务设计   ────────────────────────────────────────►  ouroboros/interview
 面向需求采访 → Prompt  ★ prompt-architect（本仓库）  ──缺口──►  （尚无：采访机制 × 对抗测试 × 跨产物）
```

**本仓库的差异化优势**（GitHub 上没看到同类同时具备）：

1. **对抗测试驱动的规则冻结**：`tests/adversarial-*.md`（12 + 23 + 12 + 21 例）+ 哈希冻结基线 —— 所有候选里**没有一家**把 skill 当规范来测
2. **§3.1 Conflict vs Tension 分离**、**unresolved 计数与授权默认的区别**（"随便/你决定"≠未解决）
3. **§6.5 Revision / 局部重开**（出稿后新信息不从头重来）
4. **§11 问题选择**（同层裁界、上游依赖优先 Q7、高价值缺口降维问法 Q2）—— 比"≤3 问 + 给默认值"深一层
5. **§2.1 用户侧语言规范**（机制词不出现在用户可见文本）

**明确短板**（对照得出的、可补的）：

1. **没有原生提问工具的调用规范** —— DSH 有 `ask_user_question`（弹窗选项），你目前靠正文提问；req 明确要求"工具在就必须实际调用"
2. **没有交付物形态** —— 你出口是"5 段 Prompt"，req 额外给 SVG 图 + `docs/需求简报.md` 落盘
3. **模糊词只有"问"一条路** —— sharpen 的"选项扇/一次性原型"是低成本高信息量的补充通道
4. **规则与失败模式没有映射表** —— req 的 `design-notes.md` 让"哪条规则能删"可判定；你的依据散在 `tests/`
5. **无 CI/校验脚本** —— 有冻结哈希基线，但没有 `check-skill.sh` 式一键校验

---

## 4. 建议的下一步（按性价比排序）

1. **补一节"提问工具优先"**：DSH 下优先调用 `ask_user_question`（1—3 题、推荐项置首、不手写"其他"），无工具再降级 —— 直接对标 req §3
2. **补"选项扇"通道**：把 sharpen 的 unknown-knowns 手法并入 §4 模糊词协议（给出 4 个正交方向让用户反应，而非继续追问）
3. **把 `tests/` 的失败模式抽成 `docs/design-notes.md` 映射表**：每条规则 ← 一个失败案例，兼容你已有的冻结哈希基线
4. **出口增加落盘选项**：`需求简报.md` / `任务 Prompt.md`（用户要求时），保持"建议 vs 需求"分区
5. 可选：写一个零依赖 `scripts/check-skill.mjs` 跑冻结哈希 + 章节存在性校验

---

## 附：证据文件

原始抓取与相似度数据在 `.gh-search/`：

- `raw/*.md`：15 份候选原文（含 req 全套、sharpen 两份、askq 四份镜像、ouroboros 50KB）
- `compare.json` / `analyze.py`：3-gram 重合度与 12 项机制命中矩阵
- `repos.csv`：仓库检索原始结果
