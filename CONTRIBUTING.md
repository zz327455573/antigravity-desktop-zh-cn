# 参与贡献指南 (Contributing)

感谢您关注并愿意参与 Google Antigravity 简体中文本地化项目！

## 1. 词条翻译原则

1. **术语统一**：所有核心术语必须严格遵守 [`docs/terminology.json`](docs/terminology.json)，如：
   - `Agent` -> **智能体**（勿翻成“代理”、“特工”）
   - `Workspace` -> **工作区**
   - `Artifact` -> **交付件**
   - `Skill` -> **技能**
   - `Customization` -> **个性化定制**
2. **代码禁区绝对不碰**：严禁翻译任何编程代码、函数名、API 路由、HTML 标签名、命令行参数。
3. **保留格式**：保留所有占位符（如 `{count}`, `%s`）、Markdown 符号及首尾空格。

## 2. 提交流程

1. Fork 本仓库并克隆到本地；
2. 在 `locales/dict-zh-CN.json` 或 `locales/menu-zh-CN.json` 中追加/修正词条；
3. 运行本地校验工具确保没有语法错误：
   ```bash
   python tools/validate.py
   ```
4. 提交 Pull Request，简要说明修正的词条及界面截屏证据。
