#!/usr/bin/env python3
"""
分析wiki/sources/shared目录中的文件，推断其正确主题
"""
import os
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
        'deep-learning': ['deep', 'neural', 'pytorch', 'tensorflow', 'cnn', 'rnn', 'lstm', 'transformer', 'attention', 'gradient', 'backpropagation', 'activation', 'dropout', 'batch norm'],
        'llm': ['llm', 'language model', 'gpt', 'claude', 'llama', 'mistral', 'bert', 'transformer', 'tokenizer', 'embedding', 'finetuning', 'pretrain', 'rag', 'retrieval'],
        'machine-learning': ['machine learning', 'ml', 'regression', 'classification', 'clustering', 'svm', 'random forest', 'xgboost', 'lightgbm', 'decision tree', 'ensemble'],
        'timeseries': ['time series', 'forecast', 'arima', 'seasonal', 'trend', 'holt', 'exponential smoothing', 'time forecasting', 'temporal'],
        'computer-vision': ['computer vision', 'image', 'vision', 'yolo', 'detection', 'segmentation', 'classification', 'opencv', 'pillow', 'cnn', 'convolutional'],
        'operations-research': ['optimization', 'linear programming', 'lp', 'integer programming', 'ip', 'scheduling', 'routing', 'inventory', 'supply chain', 'or'],
        'data-analysis': ['data analysis', 'analytics', 'statistics', 'pandas', 'numpy', 'visualization', 'plot', 'chart', 'dashboard', 'bi'],
        'programming-tools': ['programming', 'tool', 'ide', 'editor', 'vscode', 'pycharm', 'git', 'docker', 'kubernetes', 'ci/cd', 'debug'],
        'tools': ['tool', 'utility', 'software', 'application', 'app', 'platform', 'framework'],
        'knowledge-base': ['knowledge', 'wiki', 'documentation', 'notes', 'obsidian', 'logseq', 'roam', 'second brain'],
        'vibe-coding': ['vibe', 'coding', 'workflow', 'productivity', 'efficiency', 'zen', 'flow'],
        'reinforcement-learning': ['reinforcement', 'rl', 'q-learning', 'policy gradient', 'ppo', 'dqn', 'actor-critic', 'reward', 'agent'],
        'nlp': ['nlp', 'natural language', 'text', 'sentiment', 'ner', 'named entity', 'parsing', 'syntax', 'semantic'],
        'control-algorithms': ['control', 'pid', 'feedback', 'system', 'robotics', 'automation', 'regulation'],
        'data-structure-algorithm': ['data structure', 'algorithm', 'sorting', 'searching', 'tree', 'graph', 'linked list', 'hash', 'dynamic programming'],
        'power-market-trading': ['power', 'electricity', 'energy', 'market', 'trading', 'grid', 'load', 'demand'],
        'agent-dev': ['agent', 'ai agent', 'autonomous', 'multi-agent', 'coordination', 'communication']
    }
    
    # 检查文件名中的关键词
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return topic
    
    return None

def infer_topic_from_content(content):
    """根据内容推断主题"""
    content_lower = content.lower()
    
    # 主题关键词映射（与上面相同）
    topic_keywords = {
        'deep-learning': ['deep learning', 'neural network', 'convolutional', 'recurrent', 'transformer', 'attention mechanism', 'gradient descent', 'backpropagation'],
        'llm': ['large language model', 'language model', 'llm', 'gpt', 'claude', 'llama', 'bert', 'roberta', 'tokenization', 'embedding'],
        'machine-learning': ['machine learning', 'supervised learning', 'unsupervised learning', 'regression', 'classification', 'clustering'],
        'timeseries': ['time series', 'forecasting', 'arima', 'seasonality', 'autocorrelation', 'stationary'],
        'computer-vision': ['computer vision', 'image processing', 'object detection', 'segmentation', 'yolo', 'open cv'],
        'operations-research': ['operations research', 'optimization', 'linear programming', 'integer programming', 'mixed integer'],
        'data-analysis': ['data analysis', 'data visualization', 'statistical analysis', 'exploratory data analysis'],
        'programming-tools': ['programming language', 'software development', 'version control', 'debugging', 'testing'],
        'tools': ['software tool', 'utility', 'application programming interface', 'api'],
        'knowledge-base': ['knowledge management', 'note taking', 'information organization', 'personal knowledge base'],
        'vibe-coding': ['workflow optimization', 'productivity tips', 'coding environment', 'developer experience'],
        'reinforcement-learning': ['reinforcement learning', 'markov decision process', 'q-learning', 'policy gradient'],
        'nlp': ['natural language processing', 'text mining', 'sentiment analysis', 'named entity recognition'],
        'control-algorithms': ['control theory', 'pid controller', 'feedback control', 'system dynamics'],
        'data-structure-algorithm': ['data structure', 'algorithm design', 'computational complexity', 'sorting algorithm'],
        'power-market-trading': ['electricity market', 'power trading', 'energy economics', 'grid operation'],
        'agent-dev': ['intelligent agent', 'multi-agent system', 'agent architecture', 'agent communication']
    }
    
    topic_scores = defaultdict(int)
    
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in content_lower:
                topic_scores[topic] += 1
    
    if topic_scores:
        # 返回得分最高的主题
        return max(topic_scores.items(), key=lambda x: x[1])[0]
    
    return None

def analyze_shared_files():
    """分析shared目录中的文件"""
    repo_root = Path(__file__).parent.parent.parent
    shared_dir = repo_root / 'wiki' / 'sources' / 'shared'
    
    if not shared_dir.exists():
        print(f"shared目录不存在: {shared_dir}")
        return
    
    files = list(shared_dir.glob('*.md'))
    print(f"找到 {len(files)} 个shared文件")
    
    results = []
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            fm, _ = extract_frontmatter(content)
            
            filename_topic = infer_topic_from_filename(file_path.name)
            content_topic = infer_topic_from_content(content[:5000])  # 只分析前5000字符
            
            # 决策逻辑
            final_topic = None
            if content_topic:
                final_topic = content_topic
            elif filename_topic:
                final_topic = filename_topic
            
            results.append({
                'file': str(file_path.relative_to(repo_root)),
                'filename': file_path.name,
                'filename_topic': filename_topic,
                'content_topic': content_topic,
                'final_topic': final_topic,
                'has_frontmatter': fm is not None,
                'current_topics': fm.get('topics', []) if fm else []
            })
            
        except Exception as e:
            print(f"分析文件 {file_path} 时出错: {e}")
    
    # 统计主题分布
    topic_distribution = defaultdict(int)
    for result in results:
        if result['final_topic']:
            topic_distribution[result['final_topic']] += 1
    
    print(f"\n推断的主题分布:")
    for topic, count in sorted(topic_distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"  {topic}: {count}")
    
    # 保存详细结果
    output_dir = Path(__file__).parent
    with open(output_dir / 'shared_files_analysis.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细分析结果已保存到: {output_dir / 'shared_files_analysis.json'}")
    
    # 显示一些示例
    print(f"\n示例分析结果 (前10个):")
    for i, result in enumerate(results[:10]):
        print(f"\n{i+1}. {result['filename']}")
        print(f"   文件名推断: {result['filename_topic']}")
        print(f"   内容推断: {result['content_topic']}")
        print(f"   最终主题: {result['final_topic']}")
        print(f"   现有topics: {result['current_topics']}")
    
    return results

def main():
    print("开始分析shared目录文件...")
    results = analyze_shared_files()
    
    # 生成迁移计划
    if results:
        print(f"\n生成迁移计划...")
        migration_plan = []
        for result in results:
            if result['final_topic'] and result['final_topic'] != 'shared':
                migration_plan.append({
                    'source': result['file'],
                    'target_topic': result['final_topic'],
                    'target_path': result['file'].replace('/shared/', f'/{result["final_topic"]}/')
                })
        
        print(f"需要迁移的文件数: {len(migration_plan)}")
        
        output_dir = Path(__file__).parent
        with open(output_dir / 'shared_migration_plan.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(migration_plan, f, ensure_ascii=False, indent=2)
        
        print(f"迁移计划已保存到: {output_dir / 'shared_migration_plan.json'}")
        
        # 显示按主题分组的统计
        topic_counts = defaultdict(int)
        for item in migration_plan:
            topic_counts[item['target_topic']] += 1
        
        print(f"\n按目标主题分组:")
        for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {topic}: {count} 个文件")

if __name__ == '__main__':
    main()