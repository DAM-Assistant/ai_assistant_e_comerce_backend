# PreDu Backend

Backend сервис для онлайн-магазина подписок PreDu, реализованный на FastAPI.

## Функциональность

- Мультиязычный чатбот с поддержкой русского, английского и казахского языков
- Управление продуктами и категориями
- Система купонов и скидок
- API для работы с подписками (Netflix, Spotify, Chegg и др.)
- Аутентификация и авторизация пользователей

## Технологии

- FastAPI
- SQLAlchemy
- PyJWT
- LangChain
- SQLite

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/AlexPreDu/PreDu-Backend.git
cd PreDu-Backend
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
pip install -r requirements.txt
```

3. Инициализируйте базу данных:
```bash
python seed.py
```

4. Запустите сервер:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Чатбот
- `POST /api/chatbot/layer-1` - Базовый уровень чатбота
- `POST /api/chatbot/layer-2` - Продвинутый уровень чатбота

### Продукты
- `GET /api/products` - Получить список продуктов
- `GET /api/products/{id}` - Получить информацию о продукте
- `POST /api/products` - Создать новый продукт
- `PUT /api/products/{id}` - Обновить продукт
- `DELETE /api/products/{id}` - Удалить продукт

### Купоны
- `GET /api/coupons` - Получить список активных купонов
- `POST /api/coupons/apply` - Применить купон к заказу

## Структура проекта

```
PreDu-Backend/
├── app.py              # Основной файл приложения
├── database.py         # Конфигурация базы данных
├── models.py           # SQLAlchemy модели
├── dependencies.py     # Зависимости FastAPI
├── requirements.txt    # Зависимости проекта
├── seed.py            # Скрипт инициализации БД
├── chatbot/           # Модуль чатбота
├── routers/           # API роутеры
├── services/          # Бизнес-логика
└── dtos/              # Data Transfer Objects
```

## Лицензия

MIT 