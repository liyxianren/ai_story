#!/usr/bin/env python3
"""
简化标签系统 - 只保留一个简单的故事类型分类
Update to simple tag system with just story types
"""

import pymysql

# Database configuration
DB_CONFIG = {
    'host': 'tpe1.clusters.zeabur.com',
    'port': 32149,
    'user': 'root',
    'password': '69uc42U0oG7Js5Cm831ylixRqHODwXLI',
    'database': 'zeabur'
}

def get_db_connection():
    """Get database connection"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def update_to_simple_tags():
    """更新为简化的标签系统"""
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        print("🔄 正在简化标签系统...")
        
        # 1. 清空现有数据
        print("📝 清空现有标签数据...")
        cursor.execute("DELETE FROM story_tags")
        cursor.execute("DELETE FROM tags")
        cursor.execute("DELETE FROM tag_categories")
        
        # 2. 插入简化的分类（只有一个分类：故事类型）
        print("📝 插入故事类型分类...")
        cursor.execute("""
            INSERT INTO tag_categories (id, name, description, color, icon) 
            VALUES (1, '故事类型', '选择最适合您故事的类型', '#007bff', 'fas fa-bookmark')
        """)
        
        # 3. 插入简化的标签（8个常见故事类型）
        print("📝 插入简化标签...")
        simple_tags = [
            ('家庭故事', 1, '温馨的家庭生活和亲情故事'),
            ('生活故事', 1, '日常生活中的感悟和经历'),
            ('爱情故事', 1, '浪漫的爱情和感情故事'),
            ('友情故事', 1, '友谊和朋友间的故事'),
            ('成长故事', 1, '个人成长和人生感悟'),
            ('冒险故事', 1, '刺激有趣的冒险经历'),
            ('幻想故事', 1, '奇幻和想象力丰富的故事'),
            ('其他故事', 1, '不属于以上分类的其他故事')
        ]
        
        cursor.executemany("""
            INSERT INTO tags (name, category_id, description) 
            VALUES (%s, %s, %s)
        """, simple_tags)
        
        # 4. 重置自增ID
        cursor.execute("ALTER TABLE tag_categories AUTO_INCREMENT = 2")
        cursor.execute("ALTER TABLE tags AUTO_INCREMENT = 9")
        
        connection.commit()
        print("✅ 标签系统简化完成！")
        
        # 5. 显示新的标签结构
        print("\n📊 新的标签结构：")
        cursor.execute("""
            SELECT tc.name as category, t.name as tag, t.description 
            FROM tag_categories tc 
            JOIN tags t ON tc.id = t.category_id 
            ORDER BY t.id
        """)
        
        results = cursor.fetchall()
        for category, tag, description in results:
            print(f"   🏷️  {tag}: {description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating tags: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def verify_simple_tags():
    """验证简化后的标签系统"""
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        print("\n" + "="*50)
        print("🔍 验证简化标签系统")
        print("="*50)
        
        # 检查分类数量
        cursor.execute("SELECT COUNT(*) FROM tag_categories")
        category_count = cursor.fetchone()[0]
        print(f"📁 标签分类数量: {category_count} (期望: 1)")
        
        # 检查标签数量
        cursor.execute("SELECT COUNT(*) FROM tags")
        tag_count = cursor.fetchone()[0]
        print(f"🏷️  标签数量: {tag_count} (期望: 8)")
        
        # 显示所有标签
        cursor.execute("""
            SELECT t.id, t.name, t.description 
            FROM tags t 
            JOIN tag_categories tc ON t.category_id = tc.id 
            ORDER BY t.id
        """)
        
        tags = cursor.fetchall()
        print(f"\n📋 所有标签列表:")
        for tag_id, name, description in tags:
            print(f"   {tag_id}. {name} - {description}")
        
        print(f"\n✅ 标签系统验证完成！")
        
    except Exception as e:
        print(f"❌ Error verifying tags: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    """主执行函数"""
    print("🚀 AI故事平台 - 标签系统简化")
    print("="*40)
    
    # 更新为简化标签
    if update_to_simple_tags():
        # 验证更新结果
        verify_simple_tags()
        print("\n🎉 标签系统简化成功！")
        print("💡 现在用户只需要选择一个故事类型即可")
    else:
        print("\n❌ 标签系统简化失败！")

if __name__ == "__main__":
    main()