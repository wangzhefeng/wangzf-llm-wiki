#!/usr/bin/env python3
"""
分析wiki/concepts/autofix目录中的文件，推断其正确主题
"""
import re
import yaml
from collections import defaultdict
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

def infer_topic_from_filename(filename):
    """根据文件名推断主题"""
    filename_lower = filename.lower()
    
    # 主题关键词映射
    topic_keywords = {
        'deep-learning': ['deep', 'neural', 'pytorch', 'tensorflow', 'cnn', 'rnn', 'lstm', 'transformer', 'attention', 'gradient', 'backpropagation', 'activation', 'dropout', 'batch norm', 'distributed data parallel', 'ddp', 'autograd', 'convolutional', 'recurrent'],
        'llm': ['llm', 'language model', 'gpt', 'claude', 'llama', 'mistral', 'bert', 'transformer', 'tokenizer', 'embedding', 'finetuning', 'pretrain', 'rag', 'retrieval', 'large language', 'chatbot'],
        'machine-learning': ['machine learning', 'ml', 'regression', 'classification', 'clustering', 'svm', 'random forest', 'xgboost', 'lightgbm', 'decision tree', 'ensemble', 'gradient boosting', 'gbm'],
        'timeseries': ['time series', 'forecast', 'arima', 'seasonal', 'trend', 'holt', 'exponential smoothing', 'time forecasting', 'temporal'],
        'computer-vision': ['computer vision', 'image', 'vision', 'yolo', 'detection', 'segmentation', 'classification', 'opencv', 'pillow', 'cnn', 'convolutional', 'clip', 'chexnet', 'darknet'],
        'operations-research': ['optimization', 'linear programming', 'lp', 'integer programming', 'ip', 'scheduling', 'routing', 'inventory', 'supply chain', 'or', 'cplex', 'gurobi', 'solver', 'basinhopping'],
        'data-analysis': ['data analysis', 'analytics', 'statistics', 'pandas', 'numpy', 'visualization', 'plot', 'chart', 'dashboard', 'bi'],
        'programming-tools': ['programming', 'tool', 'ide', 'editor', 'vscode', 'pycharm', 'git', 'docker', 'kubernetes', 'ci/cd', 'debug', 'api', 'rest', 'grpc'],
        'tools': ['tool', 'utility', 'software', 'application', 'app', 'platform', 'framework'],
        'knowledge-base': ['knowledge', 'wiki', 'documentation', 'notes', 'obsidian', 'logseq', 'roam', 'second brain'],
        'vibe-coding': ['vibe', 'coding', 'workflow', 'productivity', 'efficiency', 'zen', 'flow'],
        'reinforcement-learning': ['reinforcement', 'rl', 'q-learning', 'policy gradient', 'ppo', 'dqn', 'actor-critic', 'reward', 'agent'],
        'nlp': ['nlp', 'natural language', 'text', 'sentiment', 'ner', 'named entity', 'parsing', 'syntax', 'semantic'],
        'control-algorithms': ['control', 'pid', 'feedback', 'system', 'robotics', 'automation', 'regulation'],
        'data-structure-algorithm': ['data structure', 'algorithm', 'sorting', 'searching', 'tree', 'graph', 'linked list', 'hash', 'dynamic programming', 'sliding window'],
        'power-market-trading': ['power', 'electricity', 'energy', 'market', 'trading', 'grid', 'load', 'demand'],
        'agent-dev': ['agent', 'ai agent', 'autonomous', 'multi-agent', 'coordination', 'communication']
    }
    
    # 检查文件名中的关键词
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return topic
    
    return 'uncategorized'

def analyze_autofix_files():
    """分析autofix目录中的文件"""
    repo_root = Path(__file__).parent.parent.parent
    autofix_dir = repo_root / 'wiki' / 'concepts' / 'autofix'
    
    if not autofix_dir.exists():
        print(f"autofix目录不存在: {autofix_dir}")
        return
    
    files = list(autofix_dir.glob('*.md'))
    print(f"找到 {len(files)} 个autofix文件")
    
    results = []
    topic_distribution = defaultdict(int)
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            fm, _ = extract_frontmatter(content)
            
            inferred_topic = infer_topic_from_filename(file_path.name)
            
            current_topics = []
            if fm and 'topics' in fm:
                current_topics = fm['topics'] if isinstance(fm['topics'], list) else [fm['topics']]
            
            results.append({
                'file': str(file_path.relative_to(repo_root)),
                'filename': file_path.name,
                'inferred_topic': inferred_topic,
                'current_topics': current_topics,
                'has_frontmatter': fm is not None,
                'should_move': inferred_topic != 'uncategorized' and 'autofix' in current_topics
            })
            
            topic_distribution[inferred_topic] += 1
            
        except Exception as e:
            print(f"分析文件 {file_path} 时出错: {e}")
    
    print(f"\n推断的主题分布:")
    for topic, count in sorted(topic_distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"  {topic}: {count}")
    
    # 保存详细结果
    output_dir = Path(__file__).parent
    import json
    with open(output_dir / 'autofix_files_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细分析结果已保存到: {output_dir / 'autofix_files_analysis.json'}")
    
    # 统计需要移动的文件
    should_move_count = sum(1 for r in results if r['should_move'])
    print(f"\n需要移动的文件数: {should_move_count}")
    
    # 生成迁移计划
    migration_plan = []
    for result in results:
        if result['should_move']:
            source = result['file']
            target_topic = result['inferred_topic']
            # 目标路径：从autofix移动到对应主题目录
            target_path = source.replace('/autofix/', f'/{target_topic}/')
            migration_plan.append({
                'source': source,
                'target_topic': target_topic,
                'target_path': target_path
            })
    
    print(f"生成的迁移计划包含 {len(migration_plan)} 个文件")
    
    with open(output_dir / 'autofix_migration_plan.json', 'w', encoding='utf-8') as f:
        json.dump(migration_plan, f, ensure_ascii=False, indent=2)
    
    print(f"迁移计划已保存到: {output_dir / 'autofix_migration_plan.json'}")
    
    # 显示示例
    print(f"\n示例分析结果 (前10个):")
    for i, result in enumerate(results[:10]):
        print(f"\n{i+1}. {result['filename']}")
        print(f"   推断主题: {result['inferred_topic']}")
        print(f"   当前topics: {result['current_topics']}")
        print(f"   需要移动: {result['should_move']}")
    
    return results, migration_plan

def main():
    print("开始分析autofix目录文件...")
    analyze_autofix_files()
    print("\n完成!")

if __name__ == '__main__':
    main()