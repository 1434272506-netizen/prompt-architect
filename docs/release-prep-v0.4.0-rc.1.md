# V0.4 Release Preparation（2026-10-03）

> **范围**：今晚只做 4 个发布 Gate（**架构不动**）。
> **版本判定原则（用户给定）**：真实 Skill load ＋ runtime smoke 都过 → `v0.4.0`；**只完成文档/架构验证** → **`v0.4.0-rc.1`**；**不得把"Architecture Release Ready"包装成"Runtime 已验证"**。

---

## SHIP-01 · Package / Load Smoke（静态）

| 检查 | 结果 |
|---|---|
| `SKILL.md` 存在 | ✅ 681 行 / 44 978 B |
| front matter 合法（`name` / `description`） | ✅ `name: prompt-architect`；description 完整（含 "Use when…" 触发条件） |
| 入口文件正常 | ✅ 无缺失 |
| **全仓 markdown 链接完整性** | 修前 **338 链接 / 97 断链**；其中 **92 条位于 `.gh-search/raw/**`**（抓取的参考资料，**不属发布物**） |
| **scope 内断链** | **5 条 → 已修复为 0** |

**已修复的 5 条（非语义修复，冻结政策明确允许）**

```
docs/v04/break-tests/{low-quality-answer,multi-round-compaction,show-silence,teach-rejection}.md
    ../freeze-v0.3.md            → ../../freeze-v0.3.md      （4 处）
docs/migration-regression.md
    tests/acceptance.md          → ../tests/acceptance.md    （1 处）
```

**未处理（明确 out of scope）**：`.gh-search/raw/**` 92 条断链 —— 那是**抓取原料**，不是 Skill 发布物；不修、不入 git（见 SHIP-04 的 `.gitignore`）。

---

## SHIP-02 · 三组 Runtime Smoke　⚠ **未执行（诚实声明）**

> **本会话无法运行真实模型**。因此下面做的是**契约级静态 replay**（引用已冻结条款），
> **明确不是 runtime evidence**。按用户给定的版本规则，这**不足以**支持 `v0.4.0`。

### A · `还是你来定吧` → Authorization → **NOT automatically CONFIRMED**
```
契约链：pending-resolution-transition-contract §3.5（N10 边界）
        "你来定 / 还是你来定吧 / 你看着办" = Authorization ≠ Value Acceptance
        → 该句不确认具体值、不产生 CONFIRMED
静态判定：唯一 ✅（NR-08 negative 已有文档级证据）
```

### B · `别忘了` vs `现在告诉我` → timing 正确
```
契约链：notification-policy-contract §6.2
        规则 4：任何不含时机的可见请求（含裸"别忘了"）→ condition = next_relevant_checkpoint
        规则 6：用户明确要求当场（"现在告诉我"）→ trigger = now
静态判定：唯一 ✅（NR-01／NR-02 已有文档级证据）
```

### C · priority ＋ fairness ＋ notification 混合 → ownership 不串层
```
契约链：Priority Layer Contract（只排序）｜Scheduler Fairness Contract（只调软竞争）｜
        Notification Policy Contract 第 1 条（不改调度／Gap／Action）
静态判定：唯一 ✅（E7／E8 ＋ 剧本 5/6 已有文档级证据）
```

**结论**：三组**契约级**判定均唯一；但**缺真实运行证据** ⇒ 版本封顶 **`v0.4.0-rc.1`**。
**升 `v0.4.0` 的唯一条件**：在真实模型上跑完 A/B/C 三组并记录输出。

---

## SHIP-03 · Release Verification

| Gate | 命令 | 结果 |
|---|---|---|
| **FRG-01** | `python .gh-search/freeze_v03.py` | ✅ `MATCH 24 / DIFF 0 / UNREGISTERED 0`（exit 0） |
| **FRG-02** | `python .gh-search/verify_v04_release_baseline.py` | ✅ `MATCH 21 / DIFF 0 / MISSING 0 / UNREGISTERED 0`（exit 0） |
| **FRG-07** | `python .gh-search/verify_readme_reverse_refs.py` | ✅ `28/28 claims 可追`（exit 0） |

---

## SHIP-04 · Tag / Rollback

| 项 | 修前状态 | 结果 |
|---|---|---|
| 是否 git 仓库 | ✅ 是（`.git` 存在） | — |
| 已有 commit | ❌ **0 个 commit**（`master` 分支无任何提交） | → **已建立首个 release commit `43f3901`**（105 文件） |
| 已有 tag | ❌ 无 | → **已打 annotated tag `v0.4.0-rc.1`** |
| 回滚点 | ❌ 不存在 | → 见下方"回滚方式"（git 之外另有 `docs/freeze-v0.3.md.bak`） |
| 排除项 | — | → 新增 `.gitignore`：`.gh-search/raw/`（20 个抓取原料文件）· `*.bak` · `*.tmp` · `__pycache__/`；**均未入库** |

**回滚方式**

```
git reset --hard v0.4.0-rc.1        # 回到发布点
git checkout v0.4.0-rc.1            # 只读查看
# 文档层面另有：docs/freeze-v0.3.md.bak（V0.3 哈希表重写前快照）
```

---

## 版本判定

```
真实 Skill load + runtime smoke 都过  →  v0.4.0
只完成文档 / 架构验证（当前情况）      →  v0.4.0-rc.1   ← 本次
```

**⇒ 今晚发布版本：`Prompt Architect v0.4.0-rc.1`**

**升 `v0.4.0` 的待办（唯一）**：在真实模型上执行 SHIP-02 的 A/B/C 三组，记录实际输出与判定。

**发布后仍属允许的变更**（V0.4 frozen 政策）：implementation bug 修复 · 文档链接/拼写等非语义修复 · 走正式 exception governance 的必要变更。
**仍禁止**：新行为规则 · 新 ontology · 新 Action／Gap semantics · 为需求继续扩 V0.4。
