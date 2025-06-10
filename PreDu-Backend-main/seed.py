from models import *
from services.auth import get_password_hash
from sqlalchemy.orm import Session
from database import create_session
from datetime import datetime, timedelta

session = create_session()

# ===== CATEGORIES ===== #
categories = [
    {
        "name": "education",
        "description": "Educational Products"
    },
    {
        "name": "entertainment",
        "description": "Entertainment Products"
    },
    {
        "name": "professional",
        "description": "Professional Tools and Services"
    },
    {
        "name": "gaming",
        "description": "Gaming Subscriptions and Services"
    },
    {
        "name": "productivity",
        "description": "Productivity and Work Tools"
    }
]

def seedCategories(session: Session):
    for category in categories:
        existed_category = session.query(Category).filter_by(name=category["name"]).first()
        if not existed_category:
            new_category = Category(name=category["name"], description=category["description"])
            session.add(new_category)
    session.commit()



# ===== BRANDS ===== #
brands = [
    {
        "name": "netflix",
        "description": "Popular Streaming Service"
    },
    {
        "name": "spotify",
        "description": "The best Music Subscription"
    },
    {
        "name": "chegg",
        "description": "Educational Platform"
    },
    {
        "name": "bartleby",
        "description": "Study Help Platform"
    },
    {
        "name": "canva",
        "description": "Design Platform"
    },
    {
        "name": "xbox",
        "description": "Microsoft Gaming Platform"
    },
    {
        "name": "playstation",
        "description": "Sony Gaming Platform"
    },
    {
        "name": "notion",
        "description": "All-in-one Workspace"
    }
]

def seedBrands(session: Session):
    for brand in brands:
        existed_brand = session.query(Brand).filter_by(name=brand["name"]).first()
        if not existed_brand:
            new_brand = Brand(name=brand["name"], description=brand["description"])
            session.add(new_brand)
    session.commit()



# ===== PRODUCTS ===== #
products = [
    # Netflix products
    {
        "category_id": 2,  # entertainment
        "brand_id": 1,     # netflix
        "name": "Netflix 1 Month Combo",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 69000,
        "image": "https://drive.google.com/file/d/1Z0prCuvqYZc0DDrradtDoNGrieW9pirf/view?usp=sharing",
        "stock_quantity": 195
    },
    {
        "category_id": 2,
        "brand_id": 1,
        "name": "Netflix 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 169000,
        "image": "https://drive.google.com/file/d/1uMkj9R8VKFAHF-kMv5dJGdP60lW-PG2z/view?usp=sharing",
        "stock_quantity": 197
    },
    {
        "category_id": 2,
        "brand_id": 1,
        "name": "Netflix 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 299000,
        "image": "https://drive.google.com/file/d/1xLyo9wJzUcX34_osyeV3V1wFPxInQWK9/view?usp=sharing",
        "stock_quantity": 200
    },
    # Chegg products
    {
        "category_id": 1,
        "brand_id": 3,
        "name": "Chegg 1 Month Combo",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 49000,
        "image": "https://drive.google.com/file/d/1Jg3NtHdA5cYGEeHutU95YTy4n0zR034r/view?usp=sharing",
        "stock_quantity": 150
    },
    {
        "category_id": 1,
        "brand_id": 3,
        "name": "Chegg 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 129000,
        "image": "https://drive.google.com/file/d/1CNLEYm_fRm9aqFTBgl2vFhH2RcXPAPiz/view?usp=sharing",
        "stock_quantity": 150
    },
    {
        "category_id": 1,
        "brand_id": 3,
        "name": "Chegg 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 239000,
        "image": "https://drive.google.com/file/d/1Et_liRwG6raohaWyQ3dPsK0mVTZnD_ZB/view?usp=sharing",
        "stock_quantity": 200
    },
    # Spotify products
    {
        "category_id": 2,
        "brand_id": 2,
        "name": "Spotify 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 69000,
        "image": "https://drive.google.com/file/d/1EjcdfH6vPMR9UNjYwqsRc3aBHo3TycVa/view?usp=sharing",
        "stock_quantity": 200
    },
    {
        "category_id": 2,
        "brand_id": 2,
        "name": "Spotify 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 119000,
        "image": "https://drive.google.com/file/d/1S7DTMI9RXQpyCzfZfi4czKDkPIDzxSY_/view?usp=sharing",
        "stock_quantity": 200
    },
    {
        "category_id": 2,
        "brand_id": 2,
        "name": "Spotify Family Combo",
        "description": "For 3 User, 6 Month",
        "cost_per_unit": 299000,
        "image": "https://drive.google.com/file/d/1M8mesbrw-v39x1hTJki9Uo3H0psjQkAE/view?usp=sharing",
        "stock_quantity": 100
    },
    # Bartleby products
    {
        "category_id": 1,
        "brand_id": 4,
        "name": "Bartleby 1 Month Combo",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 59000,
        "image": "https://drive.google.com/file/d/1ZjdzVO_jy9I_FZEDIszLWB7IfoVnuhcF/view?usp=sharing",
        "stock_quantity": 100
    },
    {
        "category_id": 1,
        "brand_id": 4,
        "name": "Bartleby 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 159000,
        "image": "https://drive.google.com/file/d/1coeMkz28PEYeDTXyUyEEvF_0FzTZM43X/view?usp=sharing",
        "stock_quantity": 100
    },
    {
        "category_id": 1,
        "brand_id": 4,
        "name": "Bartleby 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 259000,
        "image": "https://drive.google.com/file/d/1Pqk4cuD149NdrZHTIxS8PurRKVymhlmg/view?usp=sharing",
        "stock_quantity": 100
    },
    # Canva products
    {
        "category_id": 3,
        "brand_id": 5,
        "name": "Canva 1 Month",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 49000,
        "image": "https://drive.google.com/file/d/1xSUNFkNjSmPnoik2IqYPz3DbBxcw951S/view?usp=sharing",
        "stock_quantity": 100
    },
    {
        "category_id": 3,
        "brand_id": 5,
        "name": "Canva 2 Month",
        "description": "For 1 User, 2 Month",
        "cost_per_unit": 49000,
        "image": "https://drive.google.com/file/d/16C3w1QYtuNOV3WVXOxkNGW4oKMvHyTZX/view?usp=sharing",
        "stock_quantity": 200
    },
    {
        "category_id": 3,
        "brand_id": 5,
        "name": "Canva 3 Month",
        "description": "For 1 User, 4 Month",
        "cost_per_unit": 59000,
        "image": "https://drive.google.com/file/d/1dv_FNvEUI0PNfMY5UInOvNMsPRHKzkbg/view?usp=sharing",
        "stock_quantity": 100
    },
    # Xbox products
    {
        "category_id": 4,
        "brand_id": 6,
        "name": "Xbox Game Pass Ultimate 1 Month",
        "description": "Access to 100+ games, Xbox Live Gold, and EA Play",
        "cost_per_unit": 79000,
        "image": "https://drive.google.com/file/d/1rZEj_ONf8_oLk74Xy_s_e2zaT5xEknPP/view?usp=sharing",
        "stock_quantity": 150
    },
    {
        "category_id": 4,
        "brand_id": 6,
        "name": "Xbox Game Pass Ultimate 3 Months",
        "description": "Access to 100+ games, Xbox Live Gold, and EA Play",
        "cost_per_unit": 199000,
        "image": "https://drive.google.com/file/d/1DrE0Y99KPlYy4mhGyp5cZEWw5A9IQEER/view?usp=sharing",
        "stock_quantity": 150
    },
    # PlayStation products
    {
        "category_id": 4,
        "brand_id": 7,
        "name": "PlayStation Plus 1 Month",
        "description": "Online gaming, monthly games, and exclusive discounts",
        "cost_per_unit": 69000,
        "image": "https://drive.google.com/file/d/1Srtwxq-OTDXSwnVaBb1YOF9-UZOda9kO/view?usp=sharing",
        "stock_quantity": 150
    },
    {
        "category_id": 4,
        "brand_id": 7,
        "name": "PlayStation Plus 3 Months",
        "description": "Online gaming, monthly games, and exclusive discounts",
        "cost_per_unit": 169000,
        "image": "https://drive.google.com/file/d/1QRMyAhkuB2AkGR1BXuTe_VparXSaKVlb/view?usp=sharing",
        "stock_quantity": 150
    },
    # Notion products
    {
        "category_id": 5,
        "brand_id": 8,
        "name": "Notion Personal Pro 1 Month",
        "description": "Unlimited blocks, file uploads, and version history",
        "cost_per_unit": 49000,
        "image": "https://drive.google.com/file/d/13btgknhjMf_dgqk03UNmOCbLRpjoENM-/view?usp=sharing",
        "stock_quantity": 200
    },
    {
        "category_id": 5,
        "brand_id": 8,
        "name": "Notion Personal Pro 6 Months",
        "description": "Unlimited blocks, file uploads, and version history",
        "cost_per_unit": 249000,
        "image": "https://drive.google.com/file/d/1kzJDhfQyzfaNeFqdjdSjDzFZy25JI1xw/view?usp=sharing",
        "stock_quantity": 200
    }
]

def seedProducts(session: Session):
    for product in products:
        existed_product = session.query(Product).filter_by(name=product["name"]).first()
        if not existed_product:
            new_product = Product(**product)
            session.add(new_product)
    session.commit()



# ===== USERS ===== #
users = [
    {
        "username": "admin",
        "password": "admin123",
        "firstname": "Admin",
        "lastname": "User",
        "phone": "1234567890",
        "email": "admin@predumarket.com",
        "location": "Admin Location",
        "role": "admin",
        "is_email_verified": True
    },
    {
        "username": "user1",
        "password": "user123",
        "firstname": "Regular",
        "lastname": "User",
        "phone": "9876543210",
        "email": "user@predumarket.com",
        "location": "User Location",
        "role": "user",
        "is_email_verified": True
    }
]

def seedUsers(session: Session):
    for user in users:
        existed_user = session.query(User).filter_by(email=user["email"]).first()
        if not existed_user:
            new_user = User(
                username=user["username"],
                password=get_password_hash(user["password"]),
                firstname=user["firstname"],
                lastname=user["lastname"],
                phone=user["phone"],
                email=user["email"],
                location=user["location"],
                role=user["role"],
                is_email_verified=user["is_email_verified"]
            )
            session.add(new_user)
    session.commit()



# ===== COUPONS ===== #
coupons = [
    {
        "code": "WELCOME10",
        "type": "percentage",
        "value": 10.0,
        "min_order_required": 100000,
        "max_discount_applicable": 50000,
        "stock_quantity": 100,
        "is_active": True,
        "limit_per_user": 1
    },
    {
        "code": "SUMMER20",
        "type": "percentage",
        "value": 20.0,
        "min_order_required": 200000,
        "max_discount_applicable": 100000,
        "stock_quantity": 50,
        "is_active": True,
        "limit_per_user": 1
    }
]

def seedCoupons(session: Session):
    for coupon in coupons:
        existed_coupon = session.query(Coupon).filter_by(code=coupon["code"]).first()
        if not existed_coupon:
            new_coupon = Coupon(
                code=coupon["code"],
                type=coupon["type"],
                value=coupon["value"],
                min_order_required=coupon["min_order_required"],
                max_discount_applicable=coupon["max_discount_applicable"],
                stock_quantity=coupon["stock_quantity"],
                is_active=coupon["is_active"],
                limit_per_user=coupon["limit_per_user"]
            )
            session.add(new_coupon)
    session.commit()



def seed_database():
    try:
        seedCategories(session)
        seedBrands(session)
        seedProducts(session)
        seedUsers(session)
        seedCoupons(session)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
