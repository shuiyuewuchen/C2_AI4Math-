# AI 协作日志（AI4Math 论文挑战）

> 挑战：C2 AI for Math 论文 ｜ 主题：AI4Math 可靠性框架 ｜ 周期：2 天（紧凑版）
> 日志用途：记录"AI 辅助学术研究"闭环中的每一次关键协作、AI 输出与人工核验，
> 使论文中所有"AI 生成结论"可追溯（对应 rubric：aiUsage / researchRigor）。

---

## Day 1 —— 选题、文献调研与框架构建

**目标**：理解挑战要求，确定选题，完成文献回源核验，把"语义规约层"落成可定义、可论证的框架。

**AI 协作过程**
- 阅读 `CHALLENGE.md`、`challenge.json`、`rubric.json`，确认交付物与红线（引用造假→0 分，不可编译→≤5 分）。
- 提取 `materials/` 两份 PDF 文本：《Lectures on AI for Mathematics.pdf》（112 页讲义）与《中文论文大纲（AI4Math）.pdf》（12 页中英对照大纲）。
- 让 AI 依据大纲归纳"三层模型"（生成 / 语义规约 / 验证）与核心论点：**可靠性不能只靠最终验证，必须引入语义规约层**。
- 让 AI 起草形式化定义 `(Gen, ρ, Ver)`（其中 `ρ : NL ⇀ IR` 为偏函数）、verifiability gap `g = 1 − |V|/|D|`，以及 sound verifier 的命题（含证明草图）。

**关键产出**
- 选题：*From Natural Language to Verifiable Reasoning: A Semantic-Reduction Framework for Reliable AI Mathematics*。
- 三层模型 + 缺口公式 + 命题。
- 原创贡献清单：① 显式提出"语义规约层为瓶颈"；② typed IR 四要素；③ verifiability gap；④ 可靠性清单。

**人工核验记录（Day 1）**
- 讲义的参考文献表本身是二手来源，**不能直接照抄进论文**。
- 对拟引用的每一条，逐个在 arXiv / Nature 官网检索确认：

| 引用 | 核验方式 | 结论 |
|---|---|---|
| Cobbe et al. 2021 (GSM8K) | arXiv:2110.14168 检索 | ✅ 真实 |
| Hendrycks et al. 2021 (MATH) | arXiv:2103.03874 检索 | ✅ 真实 |
| Lewkowycz et al. 2022 (Minerva) | NeurIPS 2022 / arXiv:2206.14858 | ✅ 真实 |
| de Moura & Ullrich 2021 (Lean 4) | CADE-28, LNCS 12699 | ✅ 真实 |
| Wu et al. 2022 (Autoformalization) | NeurIPS 2022 / arXiv:2205.12615 | ✅ 真实 |
| Zheng et al. (miniF2F) | ICLR 2022 / arXiv:2109.00110 | ✅ 真实 |
| Hubert et al. 2025 (AlphaProof, Nature) | Nature 651(8106):607–613 | ✅ 真实（Nature 官网可查） |
| Howard 1980 (formulae-as-types) | 学术出版社文集 pp.479–490 | ✅ 真实 |

- 纠正 AI 的**过度断言**：初稿把 verifiability gap 写成"绝对质量指标"，改为"仅在同一 pipeline 内作为**比较性诊断**，因 `ρ` 与 `D` 不同会改变 `g`"（写入论文 §6 Limitations（Threats to validity））。

---

## Day 2 —— 写作、LaTeX 排版、编译与全局核验

**目标**：完成正文写作与图表公式排版，产出可编译的 `paper.tex`，补齐 `references.bib`，终检并复盘。

**AI 协作过程**
- 让 AI 分节起草 Abstract / Introduction / Related Work / Discussion / Conclusion。
- 对 Related Work 要求"对比、找漏洞、找共识"，而非搬运摘要（对应学习目标 2）；多轮迭代，第 1 稿偏综述，第 2 稿加入 positioning 段。
- 让 AI 生成 `paper.tex`：`article` 类 + amsmath/amssymb/amsthm/booktabs/tikz/hyperref；TikZ 绘制四段 pipeline 图与三层模型示意图，booktabs 绘制分类表，推理规则用 `\frac` 排版。
- 补一个可复现的 20 题 micro-pilot（`pilot.py`）：用 typed DSL 实现 `ρ`，实测 verifiability gap。
- 参考文献采用**内联 thebibliography**，使单次 `pdflatex/xelatex` 即可编译（不依赖 bibtex），另附 `references.bib` 满足 BibTeX 交付要求。
- 生成 AI 日志与 AAR，逐条对照 `rubric.json` 自评并补齐。

**人工核验记录（Day 2）**
- 事实核查（重点，防止"凭空断言"）：
  - AlphaProof 在 IMO 2024 得 **28/42 分、银牌水平（4/6 题）**——AI 初稿写"完全解决 IMO"系**错误**，已改。✅
  - 不引用任何"听起来对但查无出处"的条目；所有 24 条均落入 `references.bib` 且与 `paper.tex` 内联参考文献一一对应。
- 编译验证（内置 Tectonic 编译器）：
  - 第 1 次：冷缓存首次下载格式/宏包**超时**（非源码错误）。
  - 第 2 次：**编译成功**。✅
- 键一致性核对（脚本）：`paper.tex` 内 24 个 `\cite` ↔ 24 个 `\bibitem` ↔ `references.bib` 24 条，全部一一对应。
- micro-pilot 实测核验：脚本运行得 `|D|=20、|V|=14、g=0.30`；14 个可规约推导全部验证正确（无假阳性），6 个静默错误全部落在 `D∖V`，与论文 Proposition 一致。✅
- 红线自查：无引用造假（全部经检索核验）✅；`paper.tex` 可编译 ✅。

---

## 关键 AI 误导案例（汇总，供 AAR 引用）

1. **事实夸大**：AI 初稿把 AlphaProof 说成"完全解决 IMO"，实际为 4/6 题、银牌水平。
   → 对策：凡涉及具体成绩/数字的断言，一律回源（Nature 原文 / 官方博客）核验后再写入。
2. **引用漂移**：AI 曾给出"看起来真实但格式/年份存疑"的文献条目。
   → 对策：每条引用必须能命中 arXiv ID 或 DOI 才算通过；未命中即删除，绝不用"大概真实"的条目。
3. **可执行代码风险**：AI 起初建议内嵌 Lean 代码证明片段；未经验证即内嵌有编译失败风险。
   → 对策：改为"归纳对象"的**示意性**推理规则展示，避免贴入未经 `#check`/编译验证的代码。

