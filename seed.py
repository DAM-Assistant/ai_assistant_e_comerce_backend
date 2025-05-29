"code": "WELCOMEDAM",
"code": "DAM20K", 

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Category, Brand, Product, Coupon
import datetime

# Создаем таблицы
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    try:
        # Создаем категории
        categories = [
            Category(name="entertainment", description="Streaming services and entertainment platforms"),
            Category(name="education", description="Educational platforms and study tools"),
            Category(name="professional", description="Professional tools and services")
        ]
        for category in categories:
            db.add(category)
        db.commit()

        # Создаем бренды
        brands = [
            Brand(name="Netflix", description="Streaming service for movies and TV shows"),
            Brand(name="Spotify", description="Music streaming service"),
            Brand(name="Chegg", description="Study platform with homework help"),
            Brand(name="Bartleby", description="Study platform with textbook solutions"),
            Brand(name="Canva", description="Graphic design platform")
        ]
        for brand in brands:
            db.add(brand)
        db.commit()

        # Создаем продукты
        products = [
            # Netflix products
            Product(
                name="Netflix 1 Month Combo",
                description="For 1 User, 1 Month",
                cost_per_unit=69000,
                stock_quantity=195,
                brand_id=1,
                category_id=1
            ),
            Product(
                name="Netflix 3 Month Combo",
                description="For 1 User, 3 Months",
                cost_per_unit=199000,
                stock_quantity=150,
                brand_id=1,
                category_id=1
            ),
            # Spotify products
            Product(
                name="Spotify Premium Combo",
                description="For 1 User, 1 Month",
                cost_per_unit=49000,
                stock_quantity=200,
                brand_id=2,
                category_id=1
            ),
            Product(
                name="Spotify Family Combo",
                description="Family Plan for 6 Users",
                cost_per_unit=299000,
                stock_quantity=100,
                brand_id=2,
                category_id=1
            ),
            # Chegg products
            Product(
                name="Chegg 1 Month Combo",
                description="Study Pack for 1 Month",
                cost_per_unit=49000,
                stock_quantity=150,
                brand_id=3,
                category_id=2
            ),
            Product(
                name="Chegg 3 Month Combo",
                description="Study Pack for 3 Months",
                cost_per_unit=139000,
                stock_quantity=100,
                brand_id=3,
                category_id=2
            ),
            # Bartleby products
            Product(
                name="Bartleby 1 Month Combo",
                description="Study Pack for 1 Month",
                cost_per_unit=39000,
                stock_quantity=180,
                brand_id=4,
                category_id=2
            ),
            Product(
                name="Bartleby 3 Month Combo",
                description="Study Pack for 3 Months",
                cost_per_unit=109000,
                stock_quantity=120,
                brand_id=4,
                category_id=2
            ),
            # Canva products
            Product(
                name="Canva Pro Combo",
                description="Professional design tools for 1 Month",
                cost_per_unit=79000,
                stock_quantity=200,
                brand_id=5,
                category_id=3
            )
        ]
        for product in products:
            db.add(product)
        db.commit()

        # Создаем купоны
        coupons = [
            Coupon(
                code="WELCOMEPREDU",
                type="percentage",
                value=10,
                min_purchase=100000,
                max_discount=50000,
                start_date=datetime.datetime.now(),
                end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                is_active=True
            ),
            Coupon(
                code="PREDU20K",
                type="fixed",
                value=20000,
                min_purchase=150000,
                max_discount=20000,
                start_date=datetime.datetime.now(),
                end_date=datetime.datetime.now() + datetime.timedelta(days=15),
                is_active=True
            )
        ]
        for coupon in coupons:
            db.add(coupon)
        db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 