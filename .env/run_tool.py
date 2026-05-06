#!/usr/bin/env python3
"""
LLM Wiki 维护工具统一入口脚本

用法:
  python run_tool.py <工具类别> <脚本名> [参数...]
  python run_tool.py list                    # 列出所有可用工具
  python run_tool.py health check            # 运行统一检查工具 health/wiki_check.py --checks all
  python run_tool.py health lint             # 运行 health/wiki_check.py --checks lint
  python run_tool.py health health_check     # 运行 health/wiki_check.py --checks health
  python run_tool.py fix links --dry-run     # 运行 fix/fix_links.py --dry-run

支持的工具类别:
  health, fix, backfill, classify, assets, create

注意: 推荐使用统一检查工具 'python run_tool.py health check'
"""

import sys
import os
import subprocess
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

# 工具类别映射
CATEGORIES = {
    'health': '健康检查工具',
    'fix': '修复工具',
    'backfill': '回填工具',
    'classify': '分类工具',
    'assets': '资产管理工具',
    'create': '创建工具',
}

def list_tools():
    """列出所有可用工具"""
    print("LLM Wiki 维护工具列表")
    print("=" * 50)
    
    for category, description in CATEGORIES.items():
        category_dir = SCRIPT_DIR / category
        if not category_dir.exists():
            continue
            
        print(f"\n{category.upper()} - {description}")
        print("-" * 30)
        
        py_files = sorted(category_dir.glob("*.py"))
        for py_file in py_files:
            # 读取文件第一行注释获取简要描述
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#!/'):
                        second_line = f.readline().strip()
                        if second_line.startswith('"""'):
                            doc_start = second_line[3:]
                            if doc_start:
                                desc = doc_start
                            else:
                                # 读取下一行
                                third_line = f.readline().strip()
                                desc = third_line
                        else:
                            desc = second_line if second_line.startswith('#') else ""
                    else:
                        desc = first_line if first_line.startswith('#') else ""
                    
                    if desc.startswith('#'):
                        desc = desc[1:].strip()
                    
                    if len(desc) > 60:
                        desc = desc[:57] + "..."
            except:
                desc = ""
            
            print(f"  {py_file.stem:30} - {desc}")

def run_tool(category, script_name, args):
    """运行指定工具"""
    # 特殊脚本名映射和额外参数
    special_mappings = {
        ('health', 'check'): ('wiki_check.py', []),  # 默认使用 --checks all
        ('health', 'lint'): ('wiki_check.py', ['--checks', 'lint']),
        ('health', 'health_check'): ('wiki_check.py', ['--checks', 'health']),
    }
    
    # 检查是否有特殊映射
    key = (category, script_name)
    extra_args = []
    if key in special_mappings:
        actual_script, extra_args = special_mappings[key]
        script_path = SCRIPT_DIR / category / actual_script
        if script_path.exists():
            print(f"使用映射: {script_name} -> {actual_script} (额外参数: {' '.join(extra_args)})")
        else:
            # 如果映射的脚本不存在，回退到默认查找
            script_path = SCRIPT_DIR / category / f"{script_name}.py"
            extra_args = []  # 清除额外参数
    else:
        script_path = SCRIPT_DIR / category / f"{script_name}.py"
    
    if not script_path.exists():
        # 尝试查找匹配的脚本文件
        category_dir = SCRIPT_DIR / category
        matches = list(category_dir.glob(f"*{script_name}*.py"))
        if not matches:
            print(f"错误: 在 {category} 类别中未找到脚本 '{script_name}'")
            print(f"可用脚本:")
            for f in sorted(category_dir.glob("*.py")):
                print(f"  - {f.stem}")
            return 1
        
        if len(matches) > 1:
            print(f"错误: 找到多个匹配的脚本:")
            for m in matches:
                print(f"  - {m.stem}")
            return 1
        
        script_path = matches[0]
        print(f"找到脚本: {script_path.name}")
    
    # 构建完整命令（包含额外参数）
    cmd = [sys.executable, str(script_path)]
    
    # 添加额外参数（如果有）
    if extra_args:
        cmd.extend(extra_args)
    
    # 添加用户参数
    cmd.extend(args)
    
    print(f"运行: {' '.join(cmd)}")
    print(f"工作目录: {ROOT_DIR}")
    print("-" * 60)
    
    # 在仓库根目录执行，并设置环境变量
    try:
        # 设置环境变量，让脚本可以读取
        env = os.environ.copy()
        env['WIKI_ROOT'] = str(ROOT_DIR)
        
        # 检查脚本是否支持 --root 参数
        script_supports_root = False
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '--root' in content or 'argparse' in content:
                    script_supports_root = True
        except:
            pass
        
        # 如果脚本支持 --root 且用户没有提供 --root 参数，添加它
        if script_supports_root and '--root' not in cmd:
            # 在脚本路径后插入 --root 参数（索引2：在 sys.executable 和 script_path 之后）
            root_index = 2  # 在 sys.executable 和 script_path 之后
            cmd = cmd[:root_index] + ['--root', str(ROOT_DIR)] + cmd[root_index:]
        
        result = subprocess.run(cmd, cwd=ROOT_DIR, env=env)
        return result.returncode
    except KeyboardInterrupt:
        print("\n用户中断")
        return 130
    except Exception as e:
        print(f"运行错误: {e}")
        return 1

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    
    if sys.argv[1] == 'list':
        list_tools()
        return 0
    
    if len(sys.argv) < 3:
        print("错误: 需要指定工具类别和脚本名")
        print("用法: python run_tool.py <类别> <脚本名> [参数...]")
        print("       python run_tool.py list")
        return 1
    
    category = sys.argv[1].lower()
    script_name = sys.argv[2]
    args = sys.argv[3:]
    
    if category not in CATEGORIES:
        print(f"错误: 未知的工具类别 '{category}'")
        print(f"可用类别: {', '.join(CATEGORIES.keys())}")
        return 1
    
    return run_tool(category, script_name, args)

if __name__ == '__main__':
    sys.exit(main())
