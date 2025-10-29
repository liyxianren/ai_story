#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本 - 添加显示元数据字段到 stories 表
Database Migration Script - Add display metadata fields to stories table
"""

import pymysql
import sys
from config import Config

def check_column_exists(cursor, table_name, column_name):
    """检查列是否存在"""
    cursor.execute("""
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s
        AND TABLE_NAME = %s
        AND COLUMN_NAME = %s
    """, (Config.DB_CONFIG['database'], table_name, column_name))

    result = cursor.fetchone()
    return result[0] > 0

def migrate_database():
    """执行数据库迁移"""
    connection = None

    try:
        # 连接数据库
        print("正在连接到数据库...")
        print(f"数据库地址: {Config.DB_CONFIG['host']}:{Config.DB_CONFIG['port']}")
        print(f"数据库名称: {Config.DB_CONFIG['database']}")

        connection = pymysql.connect(
            host=Config.DB_CONFIG['host'],
            port=Config.DB_CONFIG['port'],
            user=Config.DB_CONFIG['user'],
            password=Config.DB_CONFIG['password'],
            database=Config.DB_CONFIG['database'],
            charset=Config.DB_CONFIG['charset']
        )

        cursor = connection.cursor()
        print("[OK] 数据库连接成功！\n")

        # 检查 display_author 字段是否已存在
        print("检查显示元数据字段...")

        if check_column_exists(cursor, 'stories', 'display_author'):
            print(f"[OK] display_author 字段已存在，无需迁移！")
            return True

        print(f"! 需要添加 display_author 字段\n")

        # 执行迁移
        print("开始执行数据库迁移...")

        # 添加 display_author 字段
        migration_sql = """
            ALTER TABLE stories
            ADD COLUMN display_author VARCHAR(100) DEFAULT NULL
            COMMENT '自定义显示的作者名（如果为NULL则显示真实用户名）'
        """

        cursor.execute(migration_sql)
        connection.commit()
        print("[OK] ALTER TABLE 执行成功！\n")

        # 验证迁移结果
        print("验证迁移结果...")
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'stories'
            AND COLUMN_NAME = 'display_author'
        """)

        result = cursor.fetchone()

        if result:
            print("[OK] 迁移验证成功！新增字段详情：\n")
            print(f"{'字段名':<25} {'数据类型':<15} {'注释':<50}")
            print("-" * 90)
            print(f"{result[0]:<25} {result[1]:<15} {result[2]:<50}")
            print("\n[SUCCESS] 数据库迁移完成！")
            print("\n提示：现有故事的 display_author 字段为NULL，将自动显示真实用户名")
            return True
        else:
            print(f"[ERROR] 验证失败！未找到新增字段")
            return False

    except pymysql.Error as e:
        print(f"\n[ERROR] 数据库错误: {e}")
        if connection:
            connection.rollback()
        return False

    except Exception as e:
        print(f"\n[ERROR] 发生错误: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\n数据库连接已关闭")

if __name__ == '__main__':
    print("=" * 90)
    print("数据库迁移脚本 - 添加显示元数据字段")
    print("Database Migration - Add Display Metadata Fields")
    print("=" * 90)
    print()

    success = migrate_database()

    if success:
        sys.exit(0)
    else:
        print("\n迁移失败，请检查错误信息")
        sys.exit(1)
