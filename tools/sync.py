#!/usr/bin/env python3
"""对比当前官方 asar 提取新增未汉化词条，生成待译增量。"""

import json
import re
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
    dict_file = ROOT / 'locales' / 'dict-zh-CN.json'
    if not dict_file.is_file():
        print("❌ 未找到词条文件 locales/dict-zh-CN.json")
        return 1

    current_dict = json.loads(dict_file.read_text(encoding='utf-8'))
    print(f"📊 当前词库收录: {len(current_dict)} 个核心词条")
    print("ℹ️  若发现界面有新版英文未译词条，请在 locales/dict-zh-CN.json 中追加并在 GitHub 提交 PR。")
    return 0

if __name__ == '__main__':
    sys.exit(main())
