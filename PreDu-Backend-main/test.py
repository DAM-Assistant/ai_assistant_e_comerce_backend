from database import create_session
from models import Product, Category, Brand

def check_categories():
    db = create_session()
    try:
        # Проверяем категории
        categories = db.query(Category).all()
        print("\n=== Categories ===")
        for cat in categories:
            print(f"ID: {cat.id}, Name: {cat.name}, Description: {cat.description}")
        
        # Проверяем продукты с их категориями и брендами
        products = db.query(Product).all()
        print("\n=== Products with Categories and Brands ===")
        for prod in products:
            category = db.query(Category).filter(Category.id == prod.category_id).first()
            brand = db.query(Brand).filter(Brand.id == prod.brand_id).first()
            print(f"Product: {prod.name}")
            print(f"Category: {category.name if category else 'None'}")
            print(f"Brand: {brand.name if brand else 'None'}")
            print(f"Price: {prod.cost_per_unit} VND")
            print("---")
    finally:
        db.close()

if __name__ == "__main__":
    check_categories() 

