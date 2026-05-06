#!/usr/bin/env python3
"""
诊断 raw 文件和 wiki/sources 之间的分类一致性
"""
import os
import re
import json
import yaml
from collections import defaultdict
from pathlib import Path

def extract_frontmatter(content):
    """提取frontmatter"""
    if not content.startswith('---'):
        return None
    end = content.find('---', 3)
    if end == -1:
        return None
    fm = content[3:end].strip()
    try:
        return yaml.safe_load(fm)
    except:
        return None

def analyze_raw_classification():
    """分析raw文件的分类"""
    repo_root = Path(__file__).parent.parent.parent
    raw_dirs = ['raw/web', 'raw/local-notes', 'raw/repos']
    
    stats = {
        'total_files': 0,
        'by_source': defaultdict(int),
        'by_topic': defaultdict(int),
        'files_with_topics': 0,
        'files_without_topics': 0,
        'topic_distribution': defaultdict(int),
        'files_by_path_topic': defaultdict(int)  # 根据路径推断的主题
    }
    
    # 路径到主题的映射
    path_to_topic = {
        'computer-vision': 'computer-vision',
        'deep-learning': 'deep-learning',
        'llm': 'llm',
        'llm-others': 'llm',
        'llm-pre-training': 'llm',
        'llm-post-training': 'llm',
        'machine-learning': 'machine-learning',
        'timeseries': 'timeseries',
        'operations-research': 'operations-research',
        'control-algorithms': 'control-algorithms',
        'data-analysis': 'data-analysis',
        'data-structure-algorithm': 'data-structure-algorithm',
        'programming': 'programming',
        'programming-tools': 'programming-tools',
        'agent-dev': 'agent-dev',
        'knowledge-base': 'knowledge-base',
        'knowledge-base-building': 'knowledge-base',
        'tools': 'tools',
        'vibe-coding': 'vibe-coding',
        'reinforcement-learning': 'reinforcement-learning',
        'nlp': 'nlp',
        'power-market-trading': 'power-market-trading',
        'learning-method': 'learning-method',
        'reports': 'reports',
        'collection': 'collection',
        'uncategorized': 'uncategorized'
    }
    
    for raw_dir in raw_dirs:
        raw_path = repo_root / raw_dir
        if not raw_path.exists():
            continue
            
        for md_file in raw_path.rglob('*.md'):
            stats['total_files'] += 1
            source = raw_dir.replace('raw/', '')
            stats['by_source'][source] += 1
            
            # 根据路径推断主题
            rel_path = md_file.relative_to(raw_path)
            path_parts = str(rel_path).split('/')
            inferred_topic = None
            for part in path_parts:
                if part in path_to_topic:
                    inferred_topic = path_to_topic[part]
                    break
            if inferred_topic:
                stats['files_by_path_topic'][inferred_topic] += 1
            
            # 读取frontmatter
            try:
                content = md_file.read_text(encoding='utf-8')
                fm = extract_frontmatter(content)
                if fm and 'topics' in fm:
                    stats['files_with_topics'] += 1
                    topics = fm['topics']
                    if isinstance(topics, str):
                        topics = [topics]
                    for topic in topics:
                        stats['topic_distribution'][topic] += 1
                else:
                    stats['files_without_topics'] += 1
            except:
                stats['files_without_topics'] += 1
    
    return stats

def analyze_wiki_sources():
    """分析wiki/sources的分类"""
    repo_root = Path(__file__).parent.parent.parent
    sources_dir = repo_root / 'wiki' / 'sources'
    
    stats = {
        'total_files': 0,
        'by_topic': defaultdict(int),
        'files_with_frontmatter': 0,
        'files_without_frontmatter': 0,
        'topic_files': defaultdict(list)
    }
    
    for topic_dir in sources_dir.iterdir():
        if not topic_dir.is_dir():
            continue
        topic = topic_dir.name
        if topic == 'autofix':
            continue
            
        md_files = list(topic_dir.glob('*.md'))
        stats['by_topic'][topic] = len(md_files)
        stats['total_files'] += len(md_files)
        
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                fm = extract_frontmatter(content)
                if fm:
                    stats['files_with_frontmatter'] += 1
                    stats['topic_files'][topic].append(str(md_file))
                else:
                    stats['files_without_frontmatter'] += 1
            except:
                stats['files_without_frontmatter'] += 1
    
    return stats

def analyze_wiki_concepts():
    """分析wiki/concepts的分类"""
    repo_root = Path(__file__).parent.parent.parent
    concepts_dir = repo_root / 'wiki' / 'concepts'
    
    stats = {
        'total_files': 0,
        'by_topic': defaultdict(int),
        'autofix_files': 0
    }
    
    for topic_dir in concepts_dir.iterdir():
        if not topic_dir.is_dir():
            continue
        topic = topic_dir.name
        
        md_files = list(topic_dir.glob('*.md'))
        if topic == 'autofix':
            stats['autofix_files'] = len(md_files)
        else:
            stats['by_topic'][topic] = len(md_files)
            stats['total_files'] += len(md_files)
    
    return stats

def compare_classifications():
    """比较raw路径分类和wiki/sources分类"""
    repo_root = Path(__file__).parent.parent.parent
    
    # 收集raw文件的路径主题映射
    raw_files_by_path = defaultdict(list)  # topic -> [file_paths]
    
    raw_dirs = ['raw/web', 'raw/local-notes', 'raw/repos']
    path_to_topic = {
        'computer-vision': 'computer-vision',
        'deep-learning': 'deep-learning',
        'llm': 'llm',
        'llm-others': 'llm',
        'llm-pre-training': 'llm',
        'llm-post-training': 'llm',
        'machine-learning': 'machine-learning',
        'timeseries': 'timeseries',
        'operations-research': 'operations-research',
        'control-algorithms': 'control-algorithms',
        'data-analysis': 'data-analysis',
        'data-structure-algorithm': 'data-structure-algorithm',
        'programming': 'programming',
        'programming-tools': 'programming-tools',
        'agent-dev': 'agent-dev',
        'knowledge-base': 'knowledge-base',
        'knowledge-base-building': 'knowledge-base',
        'tools': 'tools',
        'vibe-coding': 'vibe-coding',
        'reinforcement-learning': 'reinforcement-learning',
        'nlp': 'nlp',
        'power-market-trading': 'power-market-trading',
        'learning-method': 'learning-method',
        'reports': 'reports',
        'collection': 'collection',
        'uncategorized': 'uncategorized'
    }
    
    for raw_dir in raw_dirs:
        raw_path = repo_root / raw_dir
        if not raw_path.exists():
            continue
            
        for md_file in raw_path.rglob('*.md'):
            rel_path = md_file.relative_to(raw_path)
            path_parts = str(rel_path).split('/')
            inferred_topic = None
            for part in path_parts:
                if part in path_to_topic:
                    inferred_topic = path_to_topic[part]
                    break
            if inferred_topic:
                raw_files_by_path[inferred_topic].append(str(md_file))
            else:
                raw_files_by_path['uncategorized'].append(str(md_file))
    
    # 收集wiki/sources文件
    sources_files_by_topic = defaultdict(list)
    sources_dir = repo_root / 'wiki' / 'sources'
    
    for topic_dir in sources_dir.iterdir():
        if not topic_dir.is_dir():
            continue
        topic = topic_dir.name
        if topic == 'autofix':
            continue
            
        for md_file in topic_dir.glob('*.md'):
            sources_files_by_topic[topic].append(str(md_file))
    
    # 比较
    comparison = {
        'raw_topics': {k: len(v) for k, v in raw_files_by_path.items()},
        'sources_topics': {k: len(v) for k, v in sources_files_by_topic.items()},
        'mismatches': []
    }
    
    all_topics = set(list(raw_files_by_path.keys()) + list(sources_files_by_topic.keys()))
    
    for topic in all_topics:
        raw_count = len(raw_files_by_path.get(topic, []))
        sources_count = len(sources_files_by_topic.get(topic, []))
        
        if topic not in sources_files_by_topic and raw_count > 0:
            comparison['mismatches'].append({
                'topic': topic,
                'issue': f'Raw中有{topic}主题的文件({raw_count}个)，但wiki/sources中没有对应目录',
                'raw_count': raw_count,
                'sources_count': 0
            })
        elif topic not in raw_files_by_path and sources_count > 0:
            comparison['mismatches'].append({
                'topic': topic,
                'issue': f'wiki/sources中有{topic}主题目录({sources_count}个文件)，但Raw中没有对应主题的文件',
                'raw_count': 0,
                'sources_count': sources_count
            })
        elif abs(raw_count - sources_count) > max(raw_count, sources_count) * 0.5:
            # 数量差异超过50%
            comparison['mismatches'].append({
                'topic': topic,
                'issue': f'Raw和wiki/sources中{topic}主题文件数量差异大: Raw={raw_count}, Sources={sources_count}',
                'raw_count': raw_count,
                'sources_count': sources_count
            })
    
    return comparison

def main():
    print("开始诊断分类问题...")
    
    # 1. 分析raw文件
    print("\n1. Raw文件分析:")
    raw_stats = analyze_raw_classification()
    print(f"  总文件数: {raw_stats['total_files']}")
    print(f"  按来源分布: {dict(raw_stats['by_source'])}")
    print(f"  有topics字段的文件: {raw_stats['files_with_topics']}")
    print(f"  无topics字段的文件: {raw_stats['files_without_topics']}")
    print(f"  根据路径推断的主题分布: {dict(raw_stats['files_by_path_topic'])}")
    
    # 2. 分析wiki/sources
    print("\n2. wiki/sources分析:")
    sources_stats = analyze_wiki_sources()
    print(f"  总文件数: {sources_stats['total_files']}")
    print(f"  按主题分布:")
    for topic, count in sorted(sources_stats['by_topic'].items(), key=lambda x: x[1], reverse=True):
        print(f"    {topic}: {count}")
    print(f"  有frontmatter的文件: {sources_stats['files_with_frontmatter']}")
    print(f"  无frontmatter的文件: {sources_stats['files_without_frontmatter']}")
    
    # 3. 分析wiki/concepts
    print("\n3. wiki/concepts分析:")
    concepts_stats = analyze_wiki_concepts()
    print(f"  总文件数: {concepts_stats['total_files']}")
    print(f"  autofix目录文件数: {concepts_stats['autofix_files']}")
    print(f"  按主题分布:")
    for topic, count in sorted(concepts_stats['by_topic'].items(), key=lambda x: x[1], reverse=True):
        print(f"    {topic}: {count}")
    
    # 4. 比较分类
    print("\n4. Raw与wiki/sources分类比较:")
    comparison = compare_classifications()
    print(f"  Raw主题分布: {comparison['raw_topics']}")
    print(f"  Sources主题分布: {comparison['sources_topics']}")
    print(f"\n  发现的不匹配:")
    for mismatch in comparison['mismatches']:
        print(f"    - {mismatch['issue']}")
    
    # 保存结果
    output_dir = Path(__file__).parent
    result = {
        'raw_stats': raw_stats,
        'sources_stats': sources_stats,
        'concepts_stats': concepts_stats,
        'comparison': comparison
    }
    
    # 转换defaultdict为普通dict
    def convert_defaultdict(obj):
        if isinstance(obj, defaultdict):
            return dict(obj)
        elif isinstance(obj, dict):
            return {k: convert_defaultdict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_defaultdict(item) for item in obj]
        else:
            return obj
    
    result = convert_defaultdict(result)
    
    with open(output_dir / 'classification_diagnosis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n诊断结果已保存到: {output_dir / 'classification_diagnosis.json'}")

if __name__ == '__main__':
    main()