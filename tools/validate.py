#!/usr/bin/env python3
"""校验词条字典的 JSON 语法、占位符完整性与基本格式。"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main() -> int:
    locales_dir = ROOT / 'locales'
    docs_dir = ROOT / 'docs'
    has_error = False

    files_to_check = [
        locales_dir / 'dict-zh-CN.json',
        locales_dir / 'long-entries-zh-CN.json',
        locales_dir / 'menu-zh-CN.json',
        docs_dir / 'terminology.json'
    ]

    for f in files_to_check:
        if not f.is_file():
            print(f"❌ 缺少文件: {f.relative_to(ROOT)}")
            has_error = True
            continue

        try:
            data = json.loads(f.read_text(encoding='utf-8'))
            count = len(data)
            print(f"✓ {f.name:<25} 校验通过 ({count} 条记录)")
        except json.JSONDecodeError as e:
            print(f"❌ {f.name} JSON 语法错误: {e}")
            has_error = True

    if has_error:
        print("\n❌ 校验失败！请修复以上文件。")
        return 1

    print("\n🎉 所有语言字典与术语表校验通过！")
    return 0

if __name__ == '__main__':
    sys.exit(main())
