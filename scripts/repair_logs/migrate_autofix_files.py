#!/usr/bin/env python3
"""
迁移autofix目录中的文件到正确的主题目录
"""
import json
import shutil
import yaml
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

def migrate_autofix_files():
    """迁移autofix文件"""
    repo_root = Path(__file__).parent.parent.parent
    migration_plan_path = repo_root / 'scripts/repair_logs/autofix_migration_plan.json'
    
    if not migration_plan_path.exists():
        print(f"迁移计划文件不存在: {migration_plan_path}")
        return
    
    with open(migration_plan_path, 'r', encoding='utf-8') as f:
        migration_plan = json.load(f)
    
    print(f"找到 {len(migration_plan)} 个需要迁移的文件")
    
    migrated_count = 0
    failed_count = 0
    skipped_count = 0
    
    for item in migration_plan:
        source_path = repo_root / item['source']
        target_path = repo_root / item['target_path']
        target_topic = item['target_topic']
        
        if not source_path.exists():
            print(f"源文件不存在: {source_path}")
            failed_count += 1
            continue
        
        # 检查目标目录是否存在
        target_dir = target_path.parent
        if not target_dir.exists():
            target_dir.mkdir(parents=True)
            print(f"创建目标目录: {target_dir}")
        
        # 如果目标文件已存在，跳过
        if target_path.exists():
            print(f"目标文件已存在，跳过: {target_path}")
            skipped_count += 1
            continue
        
        try:
            # 读取文件内容
            content = source_path.read_text(encoding='utf-8')
            fm, rest = extract_frontmatter(content)
            
            if fm is None:
                # 没有frontmatter，直接移动
                shutil.move(str(source_path), str(target_path))
                migrated_count += 1
                print(f"移动: {source_path.name} -> {target_topic}/")
            else:
                # 更新frontmatter中的topics
                if 'topics' in fm:
                    # 确保topics是列表
                    if isinstance(fm['topics'], str):
                        fm['topics'] = [fm['topics']]
                    
                    # 移除autofix和shared，添加目标主题
                    for topic_to_remove in ['autofix', 'shared']:
                        if topic_to_remove in fm['topics']:
                            fm['topics'].remove(topic_to_remove)
                    if target_topic not in fm['topics']:
                        fm['topics'].append(target_topic)
                else:
                    fm['topics'] = [target_topic]
                
                # 生成新的frontmatter
                fm_text = yaml.dump(fm, allow_unicode=True, default_flow_style=False)
                new_content = f"---\n{fm_text}---\n\n{rest}"
                
                # 写入目标文件
                target_path.write_text(new_content, encoding='utf-8')
                
                # 删除源文件
                source_path.unlink()
                
                migrated_count += 1
                print(f"迁移: {source_path.name} -> {target_topic}/ (更新frontmatter)")
                
        except Exception as e:
            failed_count += 1
            print(f"迁移失败 {source_path.name}: {e}")
    
    print(f"\n迁移完成:")
    print(f"  成功迁移: {migrated_count}")
    print(f"  跳过: {skipped_count}")
    print(f"  失败: {failed_count}")
    
    # 统计剩余的autofix文件
    autofix_dir = repo_root / 'wiki' / 'concepts' / 'autofix'
    remaining_files = list(autofix_dir.glob('*.md')) if autofix_dir.exists() else []
    print(f"  autofix目录剩余文件: {len(remaining_files)}")

def main():
    print("开始迁移autofix文件...")
    migrate_autofix_files()
    print("\n完成!")

if __name__ == '__main__':
    main()