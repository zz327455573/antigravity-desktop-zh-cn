<div align="center">

# Google Antigravity 简体中文语言包 & 云电脑适配增强套件

**专为 Google Antigravity 桌面端量身定制的全量简体中文汉化与云电脑 ICE 优化补丁**

[![GitHub release](https://img.shields.io/badge/release-v2.19.1-blue.svg)](https://github.com/zz327455573/antigravity-desktop-zh-cn/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](README.md)

[使用说明](#-使用说明) · [核心特性](#-核心特性) · [移动云电脑-ice-适配](#-移动云电脑-ice-适配) · [常见问题](#-常见问题) · [更新日志](CHANGELOG.md) · [参与翻译](CONTRIBUTING.md)

</div>

---

## 🌟 核心特性

- 🎯 **全量深度本地化**：覆盖应用顶部原生菜单（Menu）、任务栏托盘（Tray）、版本更新交互窗口（Updater）及前端渲染界面（DOM）；
- 🖥️ **独家移动云电脑 ICE 适配**：内置原生 Windows 标题栏补丁，根治移动云电脑（Elink ICE 协议）下无边框窗口按钮（放大、缩小、关闭）失效的顽疾；
- 🛡️ **物理隔离安全引擎 (V12.0)**：基于容器向上回溯算法，严格识别并规避代码编辑器（Monaco）、终端、Diff 视窗及 Markdown 代码块，**绝不污染或误译任何用户代码**；
- ⚡ **零运行时代价**：采用原生 ASAR 静态重构机制，无需常驻后台代理、无端口监听、极速秒开；
- 🔄 **完善的回滚保障**：首次安装自动将官方原版备份为 `app.asar.original.bak`，支持随时一键无损还原。

---

## 🚀 使用说明

### 方式一：脚本一键安装（推荐）

克隆本项目并运行安装脚本，脚本会自动探测当前系统的 Antigravity 安装路径并注入补丁：

```bash
git clone https://github.com/zz327455573/antigravity-desktop-zh-cn.git
cd antigravity-desktop-zh-cn
python tools/install.py
```

> **常用参数**：
> - `python tools/install.py`：自动寻径并开启移动云电脑原生标题栏适配（默认开启）；
> - `python tools/install.py --no-ice`：仅进行汉化，保留官方默认的无边框自定义标题栏；
> - `python tools/install.py --app-dir "C:\你的路径\antigravity"`：手动指定自定义安装目录；
> - `python tools/install.py --dry-run`：预览将要修改的文件，不产生实际写入。

安装完成后，**彻底退出 Antigravity（托盘右键 -> 退出）**，重新打开即可享受全中文体验。

### 方式二：一键还原官方纯净版

如需卸载汉化或恢复官方英文纯净版，运行还原脚本即可：

```bash
python tools/uninstall.py
```

---

## 🖥️ 移动云电脑 ICE 适配

在移动云电脑 / 华为云电脑等虚拟桌面环境（特别是采用 Elink ICE 远程画面推流）中，Electron 应用的无边框标题栏经常出现右上角按钮无法被远程鼠标捕获的问题。

本项目通过修改主进程窗口参数：
```javascript
titleBarStyle: 'default',
titleBarOverlay: false,
frame: true // 启用系统原生窗口边框
```
让操作系统接管窗口的拉伸、缩放与最小化，彻底恢复流畅的多任务操作。

---

## 📁 目录结构

```
antigravity-desktop-zh-cn/
├── locales/
│   ├── dict-zh-CN.json          # 前端 DOM 汉化核心词典 (1,080+ 词条)
│   ├── long-entries-zh-CN.json  # 复杂说明段落与长文本词典
│   └── menu-zh-CN.json          # 主菜单、系统托盘、更新弹窗字典
├── patch/
│   └── engine.js                # V12.0 物理隔离 DOM 动态翻译引擎
├── tools/
│   ├── install.py               # 一键安装脚本（自动备份/解包/打补丁/重打包）
│   ├── uninstall.py             # 一键卸载与还原脚本
│   ├── sync.py                  # 增量词条提取与同步
│   └── validate.py              # 词典 JSON 格式与占位符完整性校验
├── docs/
│   ├── terminology.json         # 统一术语规范表
│   └── architecture.md          # 架构设计与云电脑技术细节说明
├── .github/
│   └── ISSUE_TEMPLATE/          # 词条反馈与报错模板
├── CHANGELOG.md                 # 版本迭代记录
├── CONTRIBUTING.md              # 贡献与翻译指南
└── LICENSE                      # MIT 开源协议
```

---

## ❓ 常见问题

<details>
<summary><b>为什么软件自动更新后汉化失效了？</b></summary>
Antigravity 官方在自动升级时会从云端下载全新的官方安装包并重写程序目录，导致本地修改被官方原版覆盖。此时只需重新运行一次 <code>python tools/install.py</code> 即可再次注入。
</details>

<details>
<summary><b>汉化会泄露我的代码或对话记录吗？</b></summary>
<b>完全不会。</b>本补丁纯离线运行，所有的词条字典和注入引擎均位于本地 ASAR 包内，不含任何外部网络请求、端口监听或数据遥测代码。
</details>

<details>
<summary><b>代码区域或者终端命令会被翻译成中文吗？</b></summary>
<b>不会。</b>内置的 V12.0 引擎在遇到节点时会执行 DOM 容器树向上回溯，凡是处于 Monaco 编辑器、终端（xterm/terminal）、Diff 视窗或 <code>&lt;pre&gt;</code>、<code>&lt;code&gt;</code> 容器内的内容均被物理隔离保护，严格保持原汁原味。
</details>

---

## 📄 开源许可

本项目遵循 [MIT License](LICENSE) 开源。  
Google Antigravity 客户端版权归 Google 所有，本项目仅提供非侵入式的本地化辅助补丁与开源脚本。
