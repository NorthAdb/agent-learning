# 0027 过关

用户确认课 0027（North s07 Skill Loading：`SkillLoader` 启动扫描、YAML frontmatter、技能 registry、`catalog()` 目录与 `load(name)` 正文加载、按需注入 system / messages、缓存与路径边界、`load_skill` 的 schema / handler 接线）已按过关标准完成。

已掌握：

- 能区分技能目录与技能全文：system prompt 只放 name + description，完整 `SKILL.md` 通过 `load_skill` 作为 `tool_result` 进入 messages。
- 能说明 `scan()` 的完整职责：扫描 `skills/*/SKILL.md`、解析 metadata、为 name / description 提供回退、缓存完整 `content`。
- 能辨析 `body` 是去掉 frontmatter 后的正文，但当前 registry 保存的是包含 frontmatter 的原始 `content`。
- 能解释 `catalog()` 是技能菜单，`load(name)` 是按 registry 键返回缓存全文；未知名称返回错误字符串。
- 能说明当前“按需加载”是按需注入模型上下文，不是每次调用才从磁盘读取；启动后修改文件不会自动热更新。
- 能解释 `resolve()`、`is_relative_to()` 与 `continue` 的路径边界作用，并区分它们与权限审批。
- 能区分普通实例方法的 `self`、类方法的 `cls` 和 `staticmethod`；理解 `parse_frontmatter()` 不依赖实例状态，所以使用静态方法。
- 能区分 Function Calling、Tool Calling、Anthropic 的 `tool_use` / `tool_result`，以及模型发出的工具请求和 Harness 本地执行 Python handler 的两层调用。
- 能真跑 `s07_skill_loading/code.py`，观察技能目录、`load_skill` 工具结果和未知技能错误。

本课不要求：

- 自动技能路由、技能依赖与冲突解决、技能版本和热更新、远程技能仓库、技能权限隔离、向量检索及生产级插件发现。
- 深入学习 `code-review` / `pdf` 技能本身；它们在本课主要作为 Skill Loading 的示例。

## Implications

- 下一课是 **0028**：North `s08_context_compact`（上下文压缩，处理工具结果与技能正文不断累积的问题）
- 阶段 2 讲法不变：当章 README + `code.py`，按块拆到和 0021–0027 同密度；非必要不另写 playground
- 已钉边界：技能是知识文档，不是执行器；加载正文不等于执行其中命令；缓存中的完整正文与模型当前可见的上下文不是同一层
