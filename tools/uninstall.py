#!/usr/bin/env python3
"""一键还原 Antigravity 官方原版（从 .original.bak 快速回滚）。"""

import argparse
import os
import shutil
import sys
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def find_default_app_dir() -> Path | None:
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if local_app_data:
        official_path = Path(local_app_data) / 'Programs' / 'antigravity'
        if (official_path / 'resources' / 'app.asar.original.bak').is_file():
            return official_path

    user_profile = os.environ.get('USERPROFILE', '')
    if user_profile:
        ice_base = Path(user_profile) / 'Documents' / 'Antigravity-ICE-NativeTitlebar'
        if ice_base.is_dir():
            app_dirs = sorted(
                [d for d in ice_base.glob('app_v*') if (d / 'resources' / 'app.asar.original.bak').is_file()],
                key=lambda p: p.name,
                reverse=True
            )
            if app_dirs:
                return app_dirs[0]

    return None

def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity 原版还原卸载器")
    parser.add_argument('--app-dir', type=str, default=None, help="Antigravity 应用程序根目录")
    args = parser.parse_args()

    app_dir = Path(args.app_dir) if args.app_dir else find_default_app_dir()
    if not app_dir:
        print("❌ 未检测到包含备份的 Antigravity 目录！")
        return 1

    asar_file = app_dir / 'resources' / 'app.asar'
    bak_file = app_dir / 'resources' / 'app.asar.original.bak'

    if not bak_file.is_file():
        print(f"❌ 未找到原版备份文件: {bak_file}")
        return 1

    print(f"🔄 正在还原原版 asar: {bak_file} -> {asar_file}")
    shutil.copy2(bak_file, asar_file)
    print("✅ 还原成功！已恢复为官方纯净英文原版。")
    return 0

if __name__ == '__main__':
    sys.exit(main())
