from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, categories, brands, products, coupons, users, orders, chatbot
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://yourdomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Используем все определенные origins
    allow_credentials=True,  # Разрешаем credentials
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Явно указываем методы
    allow_headers=["*"],  # Разрешаем все заголовки
    expose_headers=["*"],  # Добавляем expose_headers
    max_age=3600,  # Кэшируем preflight запросы на 1 час
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(brands.router)
app.include_router(products.router)
app.include_router(coupons.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(chatbot.router)

@app.on_event("startup")
async def startup():
    print("\n # ========== DAM ========== #")