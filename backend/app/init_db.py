#!/usr/bin/env python3
"""
Database initialization script for the Clothing Swap Platform
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from main import engine, Base, User, Category, get_password_hash
from sqlalchemy.orm import sessionmaker

load_dotenv()

def init_database():
    """Initialize the database with sample data"""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@swapapp.com").first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                id=str(uuid.uuid4()),
                email="admin@swapapp.com",
                password_hash=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                is_admin=True,
                is_verified=True,
                points_balance=1000
            )
            db.add(admin_user)
            print("✅ Admin user created: admin@swapapp.com / admin123")
        
        # Create sample categories
        categories_data = [
            {"name": "Top", "description": "Shirts, blouses, t-shirts, sweaters"},
            {"name": "Bottom", "description": "Pants, jeans, skirts, shorts"},
            {"name": "Dress", "description": "Casual and formal dresses"},
            {"name": "Shoes", "description": "Sneakers, heels, boots, sandals"},
            {"name": "Accessory", "description": "Bags, jewelry, scarves, belts"},
            {"name": "Outerwear", "description": "Jackets, coats, blazers"},
            {"name": "Activewear", "description": "Sports and fitness clothing"},
            {"name": "Vintage", "description": "Vintage and retro clothing"}
        ]
        
        for cat_data in categories_data:
            existing_cat = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not existing_cat:
                category = Category(
                    id=str(uuid.uuid4()),
                    name=cat_data["name"],
                    description=cat_data["description"]
                )
                db.add(category)
                print(f"✅ Category created: {cat_data['name']}")
        
        db.commit()

        # Create admin user if not exists
        admin_email = "admin@example.com"
        admin_password = "adminpassword123"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin = User(
                id=str(uuid.uuid4()),
                email=admin_email,
                password_hash=pwd_context.hash(admin_password),
                first_name="Admin",
                last_name="User",
                is_admin=True,
                is_verified=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin user created: {admin_email} / {admin_password}")
        
        print("\n🎉 Database initialized successfully!")
        print("\n📋 Login Credentials:")
        print("   Admin: admin@swapapp.com / admin123")
        print("\n🚀 Start the server with: uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import uuid
    init_database() 