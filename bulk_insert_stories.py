#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量插入故事脚本
Bulk Insert Stories Script

用法：
1. 将故事内容和图片准备好
2. 修改下面的SAMPLE_STORIES数据
3. 运行脚本: python bulk_insert_stories.py
"""

import pymysql
import os
import shutil
from datetime import datetime
from config import Config

# 示例故事数据 - 你需要替换为实际内容
SAMPLE_STORIES = [
    {
        'title': '月光下的秘密花园',
        'content': '在一个宁静的夜晚，小女孩莉莉发现了后院里一个神秘的花园。月光洒在花瓣上，每一朵花都散发着银白色的光芒...',
        'description': '一个关于勇气和发现的温暖故事',
        'language': 'zh-CN',
        'language_name': 'Chinese',
        'image_name': 'story1.jpg',  # 需要放在脚本同目录下
        'user_id': 1,  # 默认用户ID，需要确保用户存在
        'status': 'published'
    },
    {
        'title': 'The Magic Library',
        'content': 'Every night at midnight, the old library transforms into something extraordinary. Books float in the air, and characters step out from their pages...',
        'description': 'A magical adventure about the power of imagination',
        'language': 'en-US',
        'language_name': 'English',
        'image_name': 'story2.jpg',
        'user_id': 1,
        'status': 'published'
    },
    {
        'title': '星空咖啡馆',
        'content': '在城市的角落有一家特别的咖啡馆，只在午夜后营业。这里的咖啡师会根据客人的心情调制独特的饮品...',
        'description': '一个治愈系的都市奇幻故事',
        'language': 'zh-CN',
        'language_name': 'Chinese',
        'image_name': 'story3.jpg',
        'user_id': 1,
        'status': 'published'
    },
    # 添加更多故事...
]

def calculate_reading_time(content):
    """计算阅读时间（分钟）- 基于中文200字/分钟，英文250词/分钟"""
    word_count = len(content)
    if any('\u4e00' <= char <= '\u9fff' for char in content):  # 包含中文
        reading_time = max(1, round(word_count / 200))
    else:  # 英文
        word_count = len(content.split())
        reading_time = max(1, round(word_count / 250))
    return reading_time, len(content)

def copy_image_to_uploads(image_name, story_id):
    """复制图片到本地static/uploads目录（区别于云端/image路径）"""
    if not image_name:
        return None, None
        
    # 获取当前脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查story_images目录下的图片
    story_images_dir = os.path.join(script_dir, 'story_images')
    source_path = os.path.join(story_images_dir, image_name)
    
    if not os.path.exists(source_path):
        # 如果story_images目录不存在，尝试脚本同级目录
        source_path = os.path.join(script_dir, image_name)
        if not os.path.exists(source_path):
            print(f"⚠️  图片文件不存在: {source_path}")
            return None, None
    
    # 生成新的文件名
    file_ext = os.path.splitext(image_name)[1]
    new_filename = f"local_story_{story_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
    
    # 使用static/uploads目录（本地路径）
    uploads_dir = os.path.join(script_dir, 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    dest_path = os.path.join(uploads_dir, new_filename)
    
    try:
        shutil.copy2(source_path, dest_path)
        print(f"✅ 图片复制成功: {new_filename}")
        # 返回本地路径（与云端/image路径区分）
        return f"/static/uploads/{new_filename}", image_name
    except Exception as e:
        print(f"❌ 图片复制失败 {image_name}: {e}")
        return None, None

def get_db_connection():
    """获取数据库连接"""
    try:
        return pymysql.connect(**Config.DB_CONFIG)
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        raise

def insert_stories():
    """批量插入故事"""
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        print("🚀 开始批量插入故事...")
        
        inserted_count = 0
        
        for i, story_data in enumerate(SAMPLE_STORIES, 1):
            try:
                print(f"\n📖 处理故事 {i}/{len(SAMPLE_STORIES)}: {story_data['title']}")
                
                # 计算阅读时间和字数
                reading_time, word_count = calculate_reading_time(story_data['content'])
                
                # 插入故事数据
                story_query = """
                    INSERT INTO stories (user_id, title, content, language, language_name, description, 
                                       image_path, image_original_name, reading_time, word_count, status, published_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                published_at = datetime.now() if story_data['status'] == 'published' else None
                
                cursor.execute(story_query, (
                    story_data['user_id'],
                    story_data['title'],
                    story_data['content'],
                    story_data['language'],
                    story_data['language_name'],
                    story_data['description'],
                    None,  # 先插入，后面更新图片路径
                    None,  # 先插入，后面更新原始文件名
                    reading_time,
                    word_count,
                    story_data['status'],
                    published_at
                ))
                
                story_id = cursor.lastrowid
                print(f"✅ 故事插入成功，ID: {story_id}")
                
                # 处理图片
                if story_data.get('image_name'):
                    image_path, original_name = copy_image_to_uploads(story_data['image_name'], story_id)
                    if image_path:
                        # 更新图片路径
                        cursor.execute("""
                            UPDATE stories 
                            SET image_path = %s, image_original_name = %s 
                            WHERE id = %s
                        """, (image_path, original_name, story_id))
                        print(f"✅ 图片路径更新成功")
                
                connection.commit()
                inserted_count += 1
                print(f"✅ 故事 '{story_data['title']}' 处理完成")
                
            except Exception as e:
                print(f"❌ 处理故事失败 '{story_data['title']}': {e}")
                connection.rollback()
                continue
        
        print(f"\n🎉 批量插入完成！成功插入 {inserted_count}/{len(SAMPLE_STORIES)} 个故事")
        
    except Exception as e:
        print(f"❌ 批量插入失败: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()

def preview_stories():
    """预览即将插入的故事"""
    print("📋 预览即将插入的故事:")
    print("=" * 50)
    
    for i, story in enumerate(SAMPLE_STORIES, 1):
        print(f"{i}. 标题: {story['title']}")
        print(f"   语言: {story['language_name']}")
        print(f"   描述: {story['description']}")
        print(f"   内容长度: {len(story['content'])} 字符")
        print(f"   图片: {story.get('image_name', '无')}")
        print(f"   状态: {story['status']}")
        print("-" * 30)

if __name__ == "__main__":
    print("🌟 故事批量插入工具")
    print("=" * 50)
    print("📁 图片存放路径: ./story_images/")
    print("💾 本地图片将保存到: /static/uploads/ (区别于云端的/image/)")
    print()
    
    # 预览故事
    preview_stories()
    
    # 确认插入
    confirm = input("\n❓ 确定要插入这些故事吗？(y/N): ").strip().lower()
    if confirm == 'y':
        insert_stories()
    else:
        print("❌ 取消插入操作")