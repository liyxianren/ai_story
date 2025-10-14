#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建演示用户脚本
Create Demo User Script
"""

import pymysql
import bcrypt
from datetime import datetime
from config import Config

def create_demo_user():
    """获取admin用户ID用于批量插入故事"""
    try:
        connection = pymysql.connect(**Config.DB_CONFIG)
        cursor = connection.cursor()
        
        # 检查是否已存在admin用户
        cursor.execute("SELECT id FROM users WHERE username = %s", ('admin',))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"✅ Admin用户已存在，ID: {existing_user[0]}")
            return existing_user[0]
        
        # 如果admin不存在，创建admin用户
        password = 'admin123456'  # admin密码
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, phone_number, bio)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            'admin',
            'admin@example.com',
            password_hash,
            '1234567890',
            'Admin user for story management'
        ))
        
        user_id = cursor.lastrowid
        connection.commit()
        
        print(f"✅ Admin用户创建成功！")
        print(f"   用户名: admin")
        print(f"   邮箱: admin@example.com") 
        print(f"   密码: admin123456")
        print(f"   用户ID: {user_id}")
        
        return user_id
        
    except Exception as e:
        print(f"❌ 创建演示用户失败: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_demo_user_id():
    """获取admin用户ID"""
    try:
        connection = pymysql.connect(**Config.DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = %s", ('admin',))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # 如果不存在，自动创建
            return create_demo_user()
            
    except Exception as e:
        print(f"❌ 获取演示用户ID失败: {e}")
        return None
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    create_demo_user()