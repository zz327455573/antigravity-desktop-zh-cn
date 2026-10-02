#!/usr/bin/env python3
"""Antigravity 桌面端全量简体中文汉化与云电脑适配一键安装器。

用法:
    python tools/install.py                  # 自动识别安装路径并一键安装
    python tools/install.py --ice            # 显式开启云电脑原生标题栏适配（默认开启）
    python tools/install.py --no-ice         # 仅汉化，保持官方无边框标题栏
    python tools/install.py --app-dir <path> # 指定 Antigravity 安装目录
    python tools/install.py --dry-run        # 模拟运行，仅检查不修改文件
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def find_default_app_dir() -> Path | None:
    # 1. 优先检查官方标准目录
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if local_app_data:
        official_path = Path(local_app_data) / 'Programs' / 'antigravity'
        if (official_path / 'resources' / 'app.asar').is_file():
            return official_path

    # 2. 检查云电脑 ICE 修改版目录
    user_profile = os.environ.get('USERPROFILE', '')
    if user_profile:
        ice_base = Path(user_profile) / 'Documents' / 'Antigravity-ICE-NativeTitlebar'
        if ice_base.is_dir():
            app_dirs = sorted(
                [d for d in ice_base.glob('app_v*') if (d / 'resources' / 'app.asar').is_file()],
                key=lambda p: p.name,
                reverse=True
            )
            if app_dirs:
                return app_dirs[0]

    return None

def find_asar_cmd() -> list[str]:
    # 查找 asar 工具
    hermes_npx = Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes' / 'node' / 'npx.cmd'
    if hermes_npx.is_file():
        return [str(hermes_npx), 'asar']

    npx_which = shutil.which('npx')
    if npx_which:
        return [npx_which, 'asar']

    asar_which = shutil.which('asar')
    if asar_which:
        return [asar_which]

    return ['npx', 'asar']

def run_cmd(cmd: list[str], cwd: Path | None = None) -> None:
    res = subprocess.run(cmd, cwd=cwd, shell=True if os.name == 'nt' else False)
    if res.returncode != 0:
        raise RuntimeError(f"命令执行失败 (退出代码 {res.returncode}): {' '.join(cmd)}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity 桌面版全量汉化与 ICE 修复安装器")
    parser.add_argument('--app-dir', type=str, default=None, help="Antigravity 应用程序根目录")
    parser.add_argument('--ice', action='store_true', default=True, help="开启云电脑 ICE 原生标题栏适配（默认开启）")
    parser.add_argument('--no-ice', dest='ice', action='store_false', help="关闭云电脑原生标题栏适配")
    parser.add_argument('--dry-run', action='store_true', help="模拟执行，不实际修改")
    args = parser.parse_args()

    app_dir = Path(args.app_dir) if args.app_dir else find_default_app_dir()
    if not app_dir or not (app_dir / 'resources' / 'app.asar').is_file():
        print("❌ 未检测到 Antigravity 安装目录！请通过 --app-dir 显式指定。")
        print(r"示例: python tools/install.py --app-dir C:\Users\Admin\AppData\Local\Programs\antigravity")
        return 1

    asar_file = app_dir / 'resources' / 'app.asar'
    bak_file = app_dir / 'resources' / 'app.asar.original.bak'
    temp_dir = Path(os.environ.get('TEMP', '.')) / 'antigravity_zh_extract'

    print(f"📦 目标安装路径: {app_dir}")
    print(f"🖥️  云电脑原生标题栏补丁: {'开启' if args.ice else '关闭'}")

    if args.dry_run:
        print("🔍 [dry-run] 模拟执行完毕，未写入任何文件。")
        return 0

    asar_cmd = find_asar_cmd()

    # 1. 备份原版
    if not bak_file.exists():
        print(f"🛡️  备份原版 asar: {bak_file}")
        shutil.copy2(asar_file, bak_file)
    else:
        print(f"ℹ️  原版备份已存在: {bak_file}")

    # 2. 解包 asar
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("⏳ 正在解包 app.asar ...")
    run_cmd([*asar_cmd, 'extract', str(asar_file), str(temp_dir)])

    # 3. 打入 ICE 原生标题栏补丁
    if args.ice:
        utils_js = temp_dir / 'dist' / 'utils.js'
        if utils_js.is_file():
            content = utils_js.read_text(encoding='utf-8')
            target_utils = """        titleBarStyle: 'hidden',
        titleBarOverlay: isMacOS()
            ? false
            : {
                color: backgroundColor,
                symbolColor: foregroundColor,
                height: 30,
            },"""
            replacement_utils = """        titleBarStyle: isMacOS() ? 'hidden' : undefined,
        titleBarOverlay: false,
        frame: true,"""
            if target_utils in content:
                content = content.replace(target_utils, replacement_utils, 1)
                utils_js.write_text(content, encoding='utf-8')
                print("  ✓ 已注入 utils.js (开启原生标题栏)")

        ipc_js = temp_dir / 'dist' / 'ipcHandlers.js'
        if ipc_js.is_file():
            content = ipc_js.read_text(encoding='utf-8')
            target_ipc = """        if (win && process.platform === 'win32') {
            win.setTitleBarOverlay({
                color: options.color,
                symbolColor: options.symbolColor,
                height: 30,
            });
        }"""
            replacement_ipc = """        if (win && process.platform === 'win32') {
            try {
                win.setTitleBarOverlay({
                    color: options.color,
                    symbolColor: options.symbolColor,
                    height: 30,
                });
            } catch (e) {}
        }"""
            if target_ipc in content:
                content = content.replace(target_ipc, replacement_ipc, 1)
                ipc_js.write_text(content, encoding='utf-8')
                print("  ✓ 已注入 ipcHandlers.js (标题栏异常保护)")

    # 4. 打入应用菜单与托盘汉化
    menu_js = temp_dir / 'dist' / 'menu.js'
    if menu_js.is_file():
        content = menu_js.read_text(encoding='utf-8')
        target_menu = "    electron_1.Menu.setApplicationMenu(menu);"
        replacement_menu = """    const translations = {
        'File': '文件', 'Edit': '编辑', 'View': '视图', 'Window': '窗口', 'Help': '帮助',
        'New Window': '新建窗口', 'Create Project': '创建项目', 'Command Palette': '命令面板',
        'Docs': '文档', 'Check for Updates': '检查更新', 'Toggle Developer Tools': '切换开发者工具',
        'Undo': '撤销', 'Redo': '重做', 'Cut': '剪切', 'Copy': '复制', 'Paste': '粘贴',
        'Select All': '全选', 'Minimize': '最小化', 'Maximize': '最大化', 'Close': '关闭',
        'Zoom': '缩放', 'Reset Zoom': '重置缩放', 'Zoom In': '放大', 'Zoom Out': '缩小',
        'Toggle Full Screen': '切换全屏', 'Split Terminal': '拆分终端',
        'Split Conversation Horizontally': '水平拆分会话', 'Split Conversation Vertically': '垂直拆分会话',
        'Find in conversation': '在会话中查找', 'Version': '版本',
        'Connect to WSL': '连接到 WSL', 'Reopen Locally': '在本地重新打开'
    };
    function translateMenu(items) {
        for (const item of items) {
            let label = item.label || '';
            let mnemonic = '';
            let cleanLabel = label;
            const m = label.match(/&([a-zA-Z])/);
            if (m) { mnemonic = '(&' + m[1] + ')'; cleanLabel = label.replace('&', ''); }
            if (translations[cleanLabel]) item.label = translations[cleanLabel] + mnemonic;
            else if (translations[label]) item.label = translations[label];
            else if (/^Version\\s*([\\d\\.]*)$/i.test(cleanLabel)) {
                item.label = cleanLabel.replace(/^Version\\s*([\\d\\.]*)$/i, (match, v) => v ? '版本 ' + v : '版本');
            }
            if (item.submenu && item.submenu.items) translateMenu(item.submenu.items);
        }
    }
    translateMenu(menu.items);
    electron_1.Menu.setApplicationMenu(menu);"""
        if target_menu in content and "Antigravity Native Menu" not in content:
            content = content.replace(target_menu, replacement_menu, 1)
            menu_js.write_text(content, encoding='utf-8')
            print("  ✓ 已注入 menu.js (应用主菜单汉化)")

    tray_js = temp_dir / 'dist' / 'tray.js'
    if tray_js.is_file():
        content = tray_js.read_text(encoding='utf-8')
        target_tray_actions = "function createTray(actions, onClick) {"
        replacement_tray_actions = """function createTray(actions, onClick) {
    const translations = {
        'No agents running': '无运行中的智能体',
        'Open Antigravity': '打开反重力智能编程',
        'Quit': '退出'
    };
    for (const item of actions) {
        if (translations[item.label]) item.label = translations[item.label];
    }"""
        target_tray_count = """            countItem.label =
                (count > 0 ? `${count}` : 'No') +
                    ' agent' +
                    (count === 1 ? '' : 's') +
                    ' running';"""
        replacement_tray_count = """            countItem.label = count > 0 ? `${count} 个智能体运行中` : '无运行中的智能体';"""
        if target_tray_actions in content and target_tray_count in content:
            content = content.replace(target_tray_actions, replacement_tray_actions, 1)
            content = content.replace(target_tray_count, replacement_tray_count, 1)
            tray_js.write_text(content, encoding='utf-8')
            print("  ✓ 已注入 tray.js (任务栏托盘菜单汉化)")

    updater_js = temp_dir / 'dist' / 'updater.js'
    if updater_js.is_file():
        content = updater_js.read_text(encoding='utf-8')
        target_updater = """            const options = {
                type: 'info',
                title: 'Check for Updates',
                message: 'No updates available',
                buttons: ['OK'],
            };"""
        replacement_updater = """            const options = {
                type: 'info',
                title: '检查更新',
                message: '暂无可用更新',
                buttons: ['确定'],
            };"""
        if target_updater in content:
            content = content.replace(target_updater, replacement_updater, 1)
            updater_js.write_text(content, encoding='utf-8')
            print("  ✓ 已注入 updater.js (更新弹窗汉化)")

    # 5. 打入 DOM 动态汉化引擎 (preload.js)
    preload_js = temp_dir / 'dist' / 'preload.js'
    engine_file = ROOT / 'patch' / 'engine.js'
    if preload_js.is_file() and engine_file.is_file():
        content = preload_js.read_text(encoding='utf-8')
        engine_code = engine_file.read_text(encoding='utf-8')
        if "ANTIGRAVITY CHINESE LOCALIZATION START" not in content:
            content = content + "\n\n" + engine_code + "\n"
            preload_js.write_text(content, encoding='utf-8')
            print("  ✓ 已注入 preload.js (DOM 动态物理隔离汉化引擎)")

    # 6. 重新打包 asar
    print("⏳ 正在重新打包 app.asar ...")
    run_cmd([*asar_cmd, 'pack', str(temp_dir), str(asar_file)])

    # 清理临时目录
    shutil.rmtree(temp_dir, ignore_errors=True)

    print("🎉 汉化补丁安装成功！请彻底关闭 Antigravity 并重新打开验证。")
    return 0

if __name__ == '__main__':
    sys.exit(main())
