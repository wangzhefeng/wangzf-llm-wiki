#!/usr/bin/env python3
"""
修复raw文件的frontmatter错误（缺少created_at和source_type）
"""
import os
import re
import yaml
from datetime import datetime
from pathlib import Path

def extract_frontmatter(content):
    """提取frontmatter"""
    if not content.startswith('---'):
        return None, content
    end = content.find('---', 3)
    if end == -1:
        return None, content
    fm_text = content[3:end].strip()
    rest = content[end+3:].lstrip('\n')
    try:
        fm = yaml.safe_load(fm_text)
        return fm, rest
    except:
        return None, content

def infer_source_type(file_path):
    """根据文件路径推断source_type"""
    str_path = str(file_path)
    if 'raw/web/' in str_path:
        return 'web'
    elif 'raw/local-notes/' in str_path:
        return 'local-notes'
    elif 'raw/repos/' in str_path:
        return 'repos'
    elif 'raw/codex_threads/' in str_path:
        return 'codex_threads'
    else:
        return 'unknown'

def infer_created_at(file_path):
    """根据文件名推断created_at"""
    # 从文件名中提取日期（YYYY-MM-DD格式）
    filename = file_path.name
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        return date_match.group(1)
    else:
        # 使用文件的修改时间
        mtime = file_path.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

def fix_frontmatter(file_path):
    """修复单个文件的frontmatter"""
    try:
        content = file_path.read_text(encoding='utf-8')
        fm, rest = extract_frontmatter(content)
        
        if fm is None:
            # 没有frontmatter，创建新的
            source_type = infer_source_type(file_path)
            created_at = infer_created_at(file_path)
            title = file_path.stem.replace('-', ' ').replace('_', ' ')
            
            new_fm = {
                'title': title,
                'created_at': created_at,
                'source_type': source_type,
                'status': 'raw'
            }
            
            # 如果文件有topics字段，保留它
            # 检查内容中是否有topics关键词
            if 'topics:' in content[:500]:
                # 尝试解析现有的YAML
                lines = content.split('\n')
                for line in lines[:20]:
                    if line.startswith('topics:'):
                        topics = line.replace('topics:', '').strip()
                        if topics:
                            new_fm['topics'] = topics
                            break
            
            fm_text = yaml.dump(new_fm, allow_unicode=True, default_flow_style=False)
            new_content = f"---\n{fm_text}---\n\n{rest}"
        else:
            # 有frontmatter，检查缺失字段
            source_type = infer_source_type(file_path)
            created_at = infer_created_at(file_path)
            
            updated = False
            if 'source_type' not in fm:
                fm['source_type'] = source_type
                updated = True
            if 'created_at' not in fm:
                fm['created_at'] = created_at
                updated = True
            if 'status' not in fm:
                fm['status'] = 'raw'
                updated = True
            
            if updated:
                fm_text = yaml.dump(fm, allow_unicode=True, default_flow_style=False)
                new_content = f"---\n{fm_text}---\n\n{rest}"
            else:
                return False  # 无需修复
        
        # 写入文件
        backup_path = file_path.with_suffix(file_path.suffix + '.frontmatter_fix_bak')
        file_path.rename(backup_path)
        file_path.write_text(new_content, encoding='utf-8')
        return True
        
    except Exception as e:
        print(f"修复文件 {file_path} 时出错: {e}")
        return False

def get_files_with_missing_frontmatter():
    """获取健康检查中报告的缺少frontmatter的文件列表"""
    # 从诊断结果中获取文件列表
    # 这里我们手动列出从健康检查中看到的文件
    files = [
        'raw/web/computer-vision/2026-04-06-Joseph Redmon - Survival Strategies for the Robot Rebellion.md',
        'raw/web/computer-vision/2026-04-06-What is the Sliding Window Algorithm - Programmathically.md',
        'raw/web/deep-learning/2026-04-06-(35 封私信  12 条消息) 猛猿 - 知乎.md',
        'raw/web/deep-learning/2026-04-06-Assignment1&2 - 小角龙的学习记录.md',
        'raw/web/knowledge-base-building/2026-04-05-卡帕西引爆硅谷！公开「第二大脑」黑科技，1250万人围观.md',
        'raw/web/knowledge-base-building/2026-04-06-Obsidian 使用指南：从零开始搭建你的个人知识库-腾讯云开发者社区-腾讯云.md',
        'raw/web/knowledge-base-building/2026-04-06-YouMind---AI-创作智能体.md',
        'raw/web/llm-pre-training/2026-04-06-Paper page - Spectrum Targeted Training on Signal to Noise Ratio.md',
        'raw/web/llm-pre-training/2026-04-06-Quickstart - Distilabel Docs.md',
        'raw/web/llm-pre-training/2026-04-06-The Ultra-Scale Playbook - a Hugging Face Space by nanotron.md',
        'raw/web/llm-pre-training/2026-04-06-可重复代码和模型方法 - AAAMLP 中译版.md',
        'raw/web/llm-pre-training/2026-04-06-大模型参数量和占的显存怎么换算？ - 看图学 的回答.md',
        'raw/web/machine-learning/2026-04-06-(34 封私信  12 条消息) 为什么我用lstm，svm，ann来预测股价，效果都非常好？ - 知乎.md',
        'raw/web/machine-learning/2026-04-06-(34 封私信  12 条消息) 机器学习中如何处理缺失数据？ - 知乎.md',
        'raw/web/machine-learning/2026-04-06-(35 封私信  12 条消息) 连续特征的离散化：在什么情况下将连续的特征离散化之后可以获得更好的效果？ - 知乎.md',
        'raw/web/machine-learning/2026-04-06-glmnet package - RDocumentation.md',
        'raw/web/operations-research/2026-04-06-Basic tour of the Bayesian Optimization package - Bayesian Optimization.md',
        'raw/web/operations-research/2026-04-06-GIFT Eval - a Hugging Face Space by Salesforce.md',
        'raw/web/operations-research/2026-04-06-PDFMathTranslate - PDF Translation with preserved formats.md',
        'raw/web/operations-research/2026-04-06-Pillow 1.md',
        'raw/web/operations-research/2026-04-06-TPT.md',
        'raw/web/operations-research/2026-04-06-Training extremely large neural networks across thousands of GPUs.md',
        'raw/web/operations-research/2026-04-06-gtbookrobotics Notebook-based book Introduction to Robotics and Perception by Frank Dellaert and Seth Hutchinson.md',
        'raw/web/operations-research/2026-04-06-optunaoptuna A hyperparameter optimization framework.md',
        'raw/web/operations-research/2026-04-11-1  引言和动机 – S&DS 431631 — 优化与计算 --- 1  Introduction and Motivation – S&DS 431631 — Optimization and Computation.md',
        'raw/web/programming/2026-04-06-Shell 编程范例 - 泰晓科技.md',
        'raw/web/reinforcement-learning/2026-04-06-马尔可夫决策过程 - 动手学强化学习.md',
        'raw/web/timeseries/2026-04-06-(34 封私信  12 条消息) 为什么基于深度学习的时间序列预测方向很少有动态预测的方法？ - 知乎.md',
        'raw/web/timeseries/2026-04-06-(34 封私信  12 条消息) 时序数据预测有哪些好方法？ - 知乎.md',
        'raw/web/timeseries/2026-04-06-(34 封私信  12 条消息) 时间序列预测还能在进步吗？ - 知乎.md',
        'raw/web/timeseries/2026-04-06-(35 封私信  12 条消息) 为什么基于深度学习的时间序列预测方向很少有动态预测的方法？ - 知乎.md',
        'raw/web/timeseries/2026-04-06-Chebyshev polynomials - Wikipedia.md',
        'raw/web/timeseries/2026-04-06-GIFT Eval - a Hugging Face Space by Salesforce.md',
        'raw/web/timeseries/2026-04-06-Intro to Forecasting - Skforecast Docs.md',
        'raw/web/timeseries/2026-04-06-Introduction - TimeGPT Foundational model for time series forecasting and anomaly detection.md',
        'raw/web/timeseries/2026-04-06-Paper page - Time-MoE Billion-Scale Time Series Foundation Models with Mixture of  Experts.md',
        'raw/web/timeseries/2026-04-06-Welcome to skforecast - Skforecast Docs.md',
        'raw/web/timeseries/2026-04-06-时间序列预测的层次分类辅助网络 --- Hierarchical Classification Auxiliary Network for Time Series Forecasting.md',
        'raw/web/timeseries/2026-04-11-‍​﻿​⁢​⁡⁡‍‬﻿​​​‌⁢‍⁤‌⁡‬​⁢‌⁤⁣‍⁢​﻿​⁤​⁣﻿⁢⁢‬⁢⁡‌⁢​﻿⁤‌﻿⁣​⁤超短期负荷预测算法方案设计 - 飞书云文档.md',
        'raw/web/tools/2026-04-06-PDFMathTranslate - PDF Translation with preserved formats.md'
    ]
    
    repo_root = Path(__file__).parent.parent.parent
    file_paths = []
    for f in files:
        path = repo_root / f
        if path.exists():
            file_paths.append(path)
        else:
            # 尝试用连字符替换空格
            f_fixed = f.replace(' ', '-')
            path = repo_root / f_fixed
            if path.exists():
                file_paths.append(path)
            else:
                print(f"警告: 文件不存在: {f}")
    
    return file_paths

def main():
    print("开始修复raw frontmatter错误...")
    
    # 获取需要修复的文件列表
    files_to_fix = get_files_with_missing_frontmatter()
    print(f"找到 {len(files_to_fix)} 个需要修复的文件")
    
    # 修复每个文件
    fixed_count = 0
    failed_count = 0
    
    for file_path in files_to_fix:
        print(f"处理: {file_path.relative_to(file_path.parent.parent.parent.parent)}")
        try:
            if fix_frontmatter(file_path):
                fixed_count += 1
                print("  ✓ 修复成功")
            else:
                print("  ✓ 无需修复（字段已存在）")
        except Exception as e:
            failed_count += 1
            print(f"  ✗ 修复失败: {e}")
    
    print(f"\n修复完成:")
    print(f"  成功修复: {fixed_count}")
    print(f"  修复失败: {failed_count}")
    
    # 运行健康检查验证
    print("\n运行健康检查验证...")
    import subprocess
    result = subprocess.run(
        ['python', '.env/health/wiki_check.py', '--output', 'detailed'],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent.parent.parent)
    )
    
    # 提取raw frontmatter错误数量
    lines = result.stdout.split('\n')
    for line in lines:
        if 'raw frontmatter' in line:
            print(f"当前raw frontmatter错误: {line}")
            break

if __name__ == '__main__':
    main()