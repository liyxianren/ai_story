#!/usr/bin/env python3
"""
统计项目代码行数的脚本
Count lines of code in the project
"""

import os
import glob
from pathlib import Path

def count_lines_in_file(file_path):
    """统计单个文件的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except Exception:
        return 0

def get_file_stats():
    """获取项目文件统计信息"""
    
    # 项目根目录
    project_dir = Path(__file__).parent
    
    # 要统计的文件类型
    file_types = {
        'Python': ['*.py'],
        'HTML': ['*.html'],
        'CSS': ['*.css'],
        'JavaScript': ['*.js'],
        'JSON': ['*.json'],
        'Text': ['*.txt', '*.md'],
        'Config': ['*.cfg', '*.ini', '*.toml'],
        'Other': ['*.sql', '*.sh', '*.bat']
    }
    
    # 忽略的目录
    ignore_dirs = {
        '__pycache__', '.git', 'node_modules', 'venv', 'env', 
        '.pytest_cache', 'dist', 'build', '.vscode', '.idea'
    }
    
    # 忽略的文件
    ignore_files = {
        '.gitignore', '.env', 'requirements.txt', 'Procfile'
    }
    
    stats = {}
    total_lines = 0
    total_files = 0
    
    print("📊 项目代码行数统计")
    print("=" * 60)
    
    for category, patterns in file_types.items():
        category_lines = 0
        category_files = 0
        files_info = []
        
        for pattern in patterns:
            for file_path in project_dir.rglob(pattern):
                # 检查是否在忽略目录中
                if any(ignore_dir in file_path.parts for ignore_dir in ignore_dirs):
                    continue
                    
                # 检查是否是忽略文件
                if file_path.name in ignore_files:
                    continue
                
                lines = count_lines_in_file(file_path)
                if lines > 0:
                    category_lines += lines
                    category_files += 1
                    relative_path = file_path.relative_to(project_dir)
                    files_info.append((str(relative_path), lines))
        
        if category_files > 0:
            stats[category] = {
                'files': category_files,
                'lines': category_lines,
                'files_info': sorted(files_info, key=lambda x: x[1], reverse=True)
            }
            total_lines += category_lines
            total_files += category_files
    
    return stats, total_lines, total_files

def print_detailed_stats(stats, total_lines, total_files):
    """打印详细统计信息"""
    
    print(f"📁 总文件数: {total_files}")
    print(f"📝 总行数: {total_lines:,}")
    print("=" * 60)
    
    for category, data in stats.items():
        print(f"\n📂 {category} 文件:")
        print(f"   文件数: {data['files']}")
        print(f"   行数: {data['lines']:,}")
        print(f"   平均每文件: {data['lines'] // data['files'] if data['files'] > 0 else 0} 行")
        
        # 显示前5个最大的文件
        if len(data['files_info']) > 0:
            print("   📄 主要文件:")
            for file_path, lines in data['files_info'][:5]:
                print(f"      {file_path:<40} {lines:>6} 行")
            if len(data['files_info']) > 5:
                print(f"      ... 还有 {len(data['files_info']) - 5} 个文件")

def print_summary_table(stats, total_lines, total_files):
    """打印汇总表格"""
    print("\n" + "=" * 60)
    print("📊 汇总统计表")
    print("=" * 60)
    print(f"{'文件类型':<15} {'文件数':<10} {'行数':<12} {'占比':<10}")
    print("-" * 60)
    
    for category, data in sorted(stats.items(), key=lambda x: x[1]['lines'], reverse=True):
        percentage = (data['lines'] / total_lines * 100) if total_lines > 0 else 0
        print(f"{category:<15} {data['files']:<10} {data['lines']:<12,} {percentage:>6.1f}%")
    
    print("-" * 60)
    print(f"{'总计':<15} {total_files:<10} {total_lines:<12,} {'100.0%':>10}")

def find_largest_files(project_dir, top_n=10):
    """找出最大的文件"""
    print(f"\n📈 项目中最大的 {top_n} 个文件:")
    print("=" * 60)
    
    all_files = []
    ignore_dirs = {'__pycache__', '.git', 'node_modules', 'venv', 'env'}
    
    for file_path in project_dir.rglob('*'):
        if file_path.is_file():
            # 检查是否在忽略目录中
            if any(ignore_dir in file_path.parts for ignore_dir in ignore_dirs):
                continue
                
            lines = count_lines_in_file(file_path)
            if lines > 0:
                relative_path = file_path.relative_to(project_dir)
                all_files.append((str(relative_path), lines))
    
    # 按行数排序
    all_files.sort(key=lambda x: x[1], reverse=True)
    
    for i, (file_path, lines) in enumerate(all_files[:top_n], 1):
        print(f"{i:>2}. {file_path:<50} {lines:>6} 行")

def main():
    project_dir = Path(__file__).parent
    
    print(f"🔍 分析项目: {project_dir.name}")
    print(f"📂 项目路径: {project_dir}")
    
    # 获取统计信息
    stats, total_lines, total_files = get_file_stats()
    
    # 打印详细统计
    print_detailed_stats(stats, total_lines, total_files)
    
    # 打印汇总表格
    print_summary_table(stats, total_lines, total_files)
    
    # 找出最大的文件
    find_largest_files(project_dir)
    
    print("\n" + "=" * 60)
    print("✅ 统计完成!")
    
    # 保存到文件
    output_file = project_dir / "project_stats.txt"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"项目代码统计 - {project_dir.name}\n")
            f.write(f"生成时间: {os.popen('date').read().strip()}\n")
            f.write(f"总文件数: {total_files}\n")
            f.write(f"总行数: {total_lines:,}\n\n")
            
            for category, data in stats.items():
                f.write(f"{category}: {data['files']} 文件, {data['lines']:,} 行\n")
        
        print(f"📄 统计结果已保存到: {output_file}")
    except Exception as e:
        print(f"⚠️  保存文件时出错: {e}")

if __name__ == "__main__":
    main()