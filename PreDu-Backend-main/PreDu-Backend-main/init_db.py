from database import init_db
from seed import seedCategories, seedBrands, seedProducts, seedUsers, seedCoupons
from database import create_session

def initialize_database():
    # Инициализация базы данных
    init_db()
    
    # Создание сессии
    session = create_session()
    
    try:
        # Заполнение базы данных начальными данными
        seedCategories(session)
        seedBrands(session)
        seedProducts(session)
        seedUsers(session)
        seedCoupons(session)
        print("База данных успешно инициализирована!")
    except Exception as e:
        print(f"Произошла ошибка при инициализации базы данных: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    initialize_database() 