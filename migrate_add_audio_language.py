#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本 - 添加音频语言字段到 stories 表
Database Migration Script - Add audio language fields to stories table
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

        # 检查音频语言字段是否已存在
        print("检查音频语言字段...")
        audio_language_columns = ['audio_language', 'audio_language_name']
        existing_columns = []
        missing_columns = []

        for column in audio_language_columns:
            if check_column_exists(cursor, 'stories', column):
                existing_columns.append(column)
            else:
                missing_columns.append(column)

        if existing_columns:
            print(f"[OK] 以下字段已存在: {', '.join(existing_columns)}")

        if not missing_columns:
            print("\n[OK] 所有音频语言字段都已存在，无需迁移！")
            return True

        print(f"! 需要添加以下字段: {', '.join(missing_columns)}\n")

        # 执行迁移
        print("开始执行数据库迁移...")

        # 构建 ALTER TABLE 语句
        alter_statements = []

        if 'audio_language' in missing_columns:
            alter_statements.append("ADD COLUMN audio_language VARCHAR(20) DEFAULT NULL COMMENT '音频录制语言代码 (如: cmn-Hans-CN, en-US)'")

        if 'audio_language_name' in missing_columns:
            alter_statements.append("ADD COLUMN audio_language_name VARCHAR(100) DEFAULT NULL COMMENT '音频录制语言名称 (如: Chinese (Mandarin), English)'")

        if alter_statements:
            migration_sql = f"ALTER TABLE stories {', '.join(alter_statements)}"
            cursor.execute(migration_sql)
            connection.commit()
            print("[OK] ALTER TABLE 执行成功！\n")

        # 验证迁移结果
        print("验证迁移结果...")
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'stories'
            AND COLUMN_NAME IN ('audio_language', 'audio_language_name')
            ORDER BY COLUMN_NAME
        """)

        results = cursor.fetchall()

        if len(results) == 2:
            print("[OK] 迁移验证成功！新增字段详情：\n")
            print(f"{'字段名':<25} {'数据类型':<15} {'注释':<50}")
            print("-" * 90)
            for row in results:
                print(f"{row[0]:<25} {row[1]:<15} {row[2]:<50}")
            print("\n[SUCCESS] 数据库迁移完成！")
            print("\n提示：现有故事的音频语言字段为NULL，展示时将不显示语言信息")
            return True
        else:
            print(f"[ERROR] 验证失败！预期 2 个字段，但只找到 {len(results)} 个")
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
    print("数据库迁移脚本 - 添加音频语言字段")
    print("Database Migration - Add Audio Language Fields")
    print("=" * 90)
    print()

    success = migrate_database()

    if success:
        sys.exit(0)
    else:
        print("\n迁移失败，请检查错误信息")
        sys.exit(1)
