#!/usr/bin/env python3
"""
验证 LLM Wiki 维护系统设置是否正确
"""

import os
import sys
from pathlib import Path

def check_directory_structure():
    """检查目录结构"""
    print("检查目录结构...")
    scripts_dir = Path(__file__).parent
    
    required_dirs = ['tools']
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = scripts_dir / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"  ❌ 缺少目录: {missing_dirs}")
        return False
    else:
        print("  ✅ 目录结构完整")
        return True

def check_virtual_environment():
    """检查虚拟环境"""
    print("检查虚拟环境...")
    root_dir = Path(__file__).parent.parent
    venv_dir = root_dir / '.venv'
    
    if not venv_dir.exists():
        print("  ❌ 虚拟环境目录不存在")
        return False
    
    required_files = [
        '.venv/bin/activate',
        '.venv/bin/python',
        '.venv/pyvenv.cfg'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (root_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"  ⚠ 虚拟环境可能不完整，缺少文件: {missing_files}")
        return True
    else:
        print("  ✅ 虚拟环境存在")
        return True

def check_key_scripts():
    """检查关键脚本"""
    print("检查关键脚本...")
    scripts_dir = Path(__file__).parent
    
    key_scripts = [
        'tools/wiki_lint.py',
        'run.py'
    ]
    
    missing_scripts = []
    for script_path in key_scripts:
        if not (scripts_dir / script_path).exists():
            missing_scripts.append(script_path)
    
    if missing_scripts:
        print(f"  ❌ 缺少关键脚本: {missing_scripts}")
        return False
    else:
        print("  ✅ 关键脚本存在")
        return True

def check_config_files():
    """检查配置文件"""
    print("检查配置文件...")
    root_dir = Path(__file__).parent.parent
    
    required_configs = ['pyproject.toml', '.python-version']
    missing_configs = []
    
    for config_file in required_configs:
        if not (root_dir / config_file).exists():
            missing_configs.append(config_file)
    
    if missing_configs:
        print(f"  ⚠ 缺少配置文件: {missing_configs}")
        return False
    else:
        print("  ✅ 配置文件存在")
        return True

def test_run():
    """测试 run.py 基本功能"""
    print("测试 run.py...")
    scripts_dir = Path(__file__).parent
    
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, str(scripts_dir / 'run.py'), 'list'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        
        if result.returncode == 0:
            print("  ✅ run.py list 命令正常")
            output = result.stdout
            if 'wiki_lint' in output and 'backfill' in output:
                print("  ✅ 找到预期工具")
                return True
            else:
                print("  ⚠ 输出中未找到预期工具名")
                return True
        else:
            print(f"  ❌ run.py list 失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ 运行 run.py 时出错: {e}")
        return False

def main():
    print("=" * 60)
    print("LLM Wiki 维护系统验证")
    print("=" * 60)
    
    checks = [
        ("目录结构", check_directory_structure),
        ("虚拟环境", check_virtual_environment),
        ("关键脚本", check_key_scripts),
        ("配置文件", check_config_files),
        ("运行工具", test_run),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print(f"  ❌ 检查过程中出错: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("验证结果摘要:")
    print("=" * 60)
    
    all_passed = True
    for check_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{check_name:20} {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有检查通过！维护系统已正确设置。")
        print("\n下一步建议:")
        print("1. 激活虚拟环境: source .venv/bin/activate")
        print("2. 运行健康检查: uv run scripts/run.py lint")
        print("3. 查看工具列表: uv run scripts/run.py list")
    else:
        print("⚠ 部分检查未通过，系统可能需要进一步配置。")
        print("\n建议操作:")
        print("1. 检查缺失的文件或目录")
        print("2. 确保虚拟环境完整")
        print("3. 重新运行验证脚本")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())