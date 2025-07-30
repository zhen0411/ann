#!/usr/bin/env python3
"""
数据库初始化脚本
创建初始用户和基础数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, User, UserRole
from app.core.security import get_password_hash

def init_database():
    """初始化数据库"""
    db = SessionLocal()
    try:
        # 检查是否已有用户
        existing_user = db.query(User).first()
        if existing_user:
            print("数据库已初始化，跳过...")
            return

        # 创建默认用户
        users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "admin123",
                "role": UserRole.ADMIN
            },
            {
                "username": "annotator",
                "email": "annotator@example.com",
                "password": "annotator123",
                "role": UserRole.ANNOTATOR
            },
            {
                "username": "reviewer",
                "email": "reviewer@example.com",
                "password": "reviewer123",
                "role": UserRole.REVIEWER
            },
            {
                "username": "project_manager",
                "email": "manager@example.com",
                "password": "manager123",
                "role": UserRole.PROJECT_MANAGER
            }
        ]

        for user_data in users:
            hashed_password = get_password_hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                role=user_data["role"]
            )
            db.add(user)

        db.commit()
        print("数据库初始化完成！")
        print("默认用户:")
        for user_data in users:
            print(f"  用户名: {user_data['username']}, 密码: {user_data['password']}, 角色: {user_data['role']}")

    except Exception as e:
        print(f"初始化数据库时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()