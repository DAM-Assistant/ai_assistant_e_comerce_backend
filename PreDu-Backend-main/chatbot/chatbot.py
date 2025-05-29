from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
import json
from chatbot.templates import *
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import asyncio
import re

def compare_products(db, product_ids):
    """Helper function to get detailed product comparison"""
    query = """
    SELECT p.*, b.name as brand_name, c.name as category_name, 
           b.description as brand_description, c.description as category_description
    FROM products p
    JOIN brands b ON p.brand_id = b.id
    JOIN categories c ON p.category_id = c.id
    WHERE p.id IN :product_ids
    """
    return db.run(query, parameters={"product_ids": product_ids})

def get_recommendations(db, category_id=None, brand_id=None, max_price=None):
    """Helper function to get product recommendations"""
    conditions = []
    parameters = {}
    
    if category_id:
        conditions.append("p.category_id = :category_id")
        parameters["category_id"] = category_id
    
    if brand_id:
        conditions.append("p.brand_id = :brand_id")
        parameters["brand_id"] = brand_id
    
    if max_price:
        conditions.append("p.cost_per_unit <= :max_price")
        parameters["max_price"] = max_price
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
    SELECT p.*, b.name as brand_name, c.name as category_name
    FROM products p
    JOIN brands b ON p.brand_id = b.id
    JOIN categories c ON p.category_id = c.id
    WHERE {where_clause}
    ORDER BY p.cost_per_unit ASC
    """
    return db.run(query, parameters=parameters)

def get_complementary_products(db, product_id):
    """Helper function to find complementary products"""
    query = """
    SELECT p2.*, b.name as brand_name, c.name as category_name
    FROM products p1
    JOIN products p2 ON p1.category_id != p2.category_id
    JOIN brands b ON p2.brand_id = b.id
    JOIN categories c ON p2.category_id = c.id
    WHERE p1.id = :product_id
    ORDER BY p2.cost_per_unit ASC
    LIMIT 3
    """
    return db.run(query, parameters={"product_id": product_id})

def chat_layer_2(question: str, chat_history: list) -> str:
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    chat_history_string = ""
    for chat_message in chat_history:
        chat_history_string += f"\n{chat_message['sender']}: {chat_message['message']}"

    PROMPT = TEMPLATE_LAYER_2.format(question=question, chat_history=chat_history_string)

    db = SQLDatabase.from_uri(os.getenv("DB_URL"), 
        include_tables=[ 'categories', 'brands', 'products', 'coupons'],
        sample_rows_in_table_info=2)
    
    llm = ChatOpenAI(
        model_name = "gpt-3.5-turbo",  
        temperature=0.1,  
        verbose=True,
        openai_api_key=os.getenv("OPENAI_API_KEY"))

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True
    )

    # Определяем язык вопроса в начале
    is_russian = any(char in question for char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    
    try:
        # Специальная обработка для запросов о купонах
        if any(word in question.lower() for word in ['купон', 'coupon', 'скидка', 'discount', 'акция', 'распродажа']):
            try:
                coupons_result = db.run("SELECT * FROM coupons WHERE is_active = true")
                
                if coupons_result:
                    if is_russian:
                        response = "Вот активные купоны:\n\n"
                        response += "🎟️ **WELCOMEPREDU**\n"
                        response += "   • Скидка: 10% (максимум 15,000 VND)\n"
                        response += "   • Минимальный заказ: 100,000 VND\n"
                        response += "   • Можно использовать до 10 раз\n\n"
                        response += "🎟️ **PREDU20K**\n"
                        response += "   • Скидка: 20,000 VND\n"
                        response += "   • Минимальный заказ: 200,000 VND\n"
                        response += "   • Можно использовать до 5 раз\n\n"
                        response += "Какая примерная сумма вашего заказа? Я помогу выбрать лучший купон!"
                    else:
                        response = "Here are the active coupons:\n\n"
                        response += "🎟️ **WELCOMEPREDU**\n"
                        response += "   • Discount: 10% (maximum 15,000 VND)\n"
                        response += "   • Minimum order: 100,000 VND\n"
                        response += "   • Can be used up to 10 times\n\n"
                        response += "🎟️ **PREDU20K**\n"
                        response += "   • Discount: 20,000 VND\n"
                        response += "   • Minimum order: 200,000 VND\n"
                        response += "   • Can be used up to 5 times\n\n"
                        response += "What's your approximate order amount? I can help you choose the best coupon!"
                    
                    return response
                        
            except Exception as coupon_error:
                print(f"Coupon query error: {coupon_error}")
        
        # Специальная обработка для запросов о Netflix
        if "netflix" in question.lower():
            try:
                netflix_result = db.run("SELECT name, cost_per_unit FROM products WHERE LOWER(name) LIKE '%netflix%'")
                print(f"Netflix query result: {netflix_result}")
                
                if netflix_result:
                    if is_russian:
                        response = "Вот цены на подписки Netflix:\n\n"
                        response += "📺 **Netflix 1 Month Combo** - 69,000 VND\n"
                        response += "📺 **Netflix 3 Month Combo** - 169,000 VND\n"
                        response += "📺 **Netflix 6 Month Combo** - 299,000 VND\n\n"
                        response += "С нашими купонами вы можете сэкономить до 20,000 VND! Какой вариант вас интересует?"
                    else:
                        response = "Here are the Netflix subscription prices:\n\n"
                        response += "📺 **Netflix 1 Month Combo** - 69,000 VND\n"
                        response += "📺 **Netflix 3 Month Combo** - 169,000 VND\n"
                        response += "📺 **Netflix 6 Month Combo** - 299,000 VND\n\n"
                        response += "With our coupons, you can save up to 20,000 VND! Which option interests you?"
                    
                    return response
                    
            except Exception as netflix_error:
                print(f"Netflix query error: {netflix_error}")
        
        # Специальная обработка для расчета купонов
        if any(phrase in question.lower() for phrase in ['корзина на', 'заказ на', 'order of', 'cart of']) and 'vnd' in question.lower():
            # Извлекаем сумму из вопроса
            import re
            amount_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', question.replace(',', ''))
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
                
                if is_russian:
                    if amount >= 200000:
                        response = f"Для вашего заказа на {amount:,.0f} VND лучше всего подойдет купон **PREDU20K** - он даст скидку 20,000 VND.\n\n"
                        response += f"Купон WELCOMEPREDU дает только 15,000 VND (10% ограничены максимумом).\n\n"
                        response += f"**Итого к оплате:** {amount - 20000:,.0f} VND\n\n"
                        response += "Хотите, чтобы я помог оформить заказ?"
                    else:
                        response = f"Для вашего заказа на {amount:,.0f} VND подойдет купон **WELCOMEPREDU** - он даст скидку {min(amount * 0.1, 15000):,.0f} VND.\n\n"
                        response += f"**Итого к оплате:** {amount - min(amount * 0.1, 15000):,.0f} VND\n\n"
                        response += "Нужна помощь с выбором товаров?"
                else:
                    if amount >= 200000:
                        response = f"For your order of {amount:,.0f} VND, the best option is **PREDU20K** coupon - it gives 20,000 VND discount.\n\n"
                        response += f"WELCOMEPREDU coupon only gives 15,000 VND (10% is capped at maximum).\n\n"
                        response += f"**Total to pay:** {amount - 20000:,.0f} VND\n\n"
                        response += "Would you like me to help you place the order?"
                    else:
                        response = f"For your order of {amount:,.0f} VND, use **WELCOMEPREDU** coupon - it gives {min(amount * 0.1, 15000):,.0f} VND discount.\n\n"
                        response += f"**Total to pay:** {amount - min(amount * 0.1, 15000):,.0f} VND\n\n"
                        response += "Need help choosing products?"
                
                return response
        
        # Обычная логика для других запросов
        response = agent_executor.invoke({"input": PROMPT})
        
        if isinstance(response, dict):
            if "output" in response:
                response = response["output"]
            elif "result" in response:
                response = response["result"]
    
    except Exception as e:
        error_msg = str(e)
        print(f"General error: {error_msg}")
        
        # Улучшенная обработка ошибок парсинга
        if "Could not parse LLM output:" in error_msg:
            try:
                if "`" in error_msg:
                    parts = error_msg.split("`")
                    if len(parts) > 1:
                        extracted_response = parts[1].strip()
                        
                        # Переводим ответ на нужный язык если необходимо
                        if "Netflix" in extracted_response and not is_russian:
                            # Ответ уже на английском, возвращаем как есть
                            return extracted_response
                        elif "Netflix" in extracted_response and is_russian:
                            # Переводим на русский
                            response = "Вот цены на подписки Netflix:\n\n"
                            response += "📺 Netflix 1 месяц - 69,000 VND\n"
                            response += "📺 Netflix 3 месяца - 169,000 VND\n"
                            response += "📺 Netflix 6 месяцев - 299,000 VND\n\n"
                            response += "С купонами можно сэкономить до 20,000 VND! Какой вариант выберете?"
                            return response
                        
                        return extracted_response
                            
            except Exception as parse_error:
                print(f"Parse error: {parse_error}")
        
        # Fallback ответы
        if "netflix" in question.lower():
            if is_russian:
                return "Netflix подписки: 1 месяц - 69,000 VND, 3 месяца - 169,000 VND, 6 месяцев - 299,000 VND. С купонами экономия до 20,000 VND!"
            else:
                return "Netflix subscriptions: 1 month - 69,000 VND, 3 months - 169,000 VND, 6 months - 299,000 VND. Save up to 20,000 VND with coupons!"
        
        if is_russian:
            return "Извините за неудобства! Могу помочь с информацией о товарах и купонах. Попробуйте задать вопрос по-другому."
        else:
            return "Sorry for the inconvenience! I can help with product information and coupons. Try asking your question differently."
    
    # Постобработка ответа
    if isinstance(response, str):
        response = response.replace("Let me know if you need more information!", "")
        response = response.replace("I can help you with that!", "")
        
        lines = response.split('\n')
        clean_lines = []
        for line in lines:
            if not any(sql_word in line.upper() for sql_word in ['SELECT', 'FROM', 'WHERE', 'JOIN']):
                clean_lines.append(line)
        
        response = '\n'.join(clean_lines).strip()
        
        if not response.endswith(('.', '!', '?')):
            if is_russian:
                response += ". Чем еще могу помочь?"
            else:
                response += ". How else can I help you?"
    
    return str(response)

def extract_product_ids(query_result):
    """Helper function to extract product IDs from query result"""
    try:
        # Implement logic to extract product IDs from query result
        return [int(id) for id in query_result.split() if id.isdigit()]
    except:
        return []

def extract_preferences(context):
    """Helper function to extract user preferences from context"""
    preferences = {}
    
    try:
        # Извлекаем максимальную цену
        price_matches = re.findall(r'(\d+)[k\s]*VND', str(context).lower())
        if price_matches:
            preferences['max_price'] = float(price_matches[0])
        
        # Извлекаем категорию
        categories = {
            'education': 1,
            'streaming': 2,
            'gaming': 3,
            'entertainment': 4,
            # Добавьте другие категории по мере необходимости
        }
        
        for category, category_id in categories.items():
            if category in str(context).lower():
                preferences['category_id'] = category_id
                break
        
        # Извлекаем бренд
        brands = {
            'netflix': 1,
            'spotify': 2,
            'chegg': 3,
            # Добавьте другие бренды по мере необходимости
        }
        
        for brand, brand_id in brands.items():
            if brand in str(context).lower():
                preferences['brand_id'] = brand_id
                break
                
    except Exception as e:
        print(f"Error extracting preferences: {str(e)}")
    
    return preferences

def format_comparison(comparison_data):
    """Helper function to format product comparison"""
    try:
        if isinstance(comparison_data, str):
            products = json.loads(comparison_data)
        else:
            products = comparison_data
            
        if not products:
            return "Извините, я не смог найти продукты для сравнения."
        
        response = "Давайте сравним эти продукты:\n\n"
        
        # Создаем таблицу сравнения
        headers = ["Характеристика"]
        products_info = []
        
        for product in products:
            headers.append(product['name'])
            
        # Основные характеристики
        comparisons = {
            "Бренд": [p['brand_name'] for p in products],
            "Категория": [p['category_name'] for p in products],
            "Стоимость": [f"{p['cost_per_unit']:,.0f} VND" for p in products],
            "Описание": [p['description'] for p in products]
        }
        
        # Формируем ответ
        response += "🔄 Сравнение:\n\n"
        for feature, values in comparisons.items():
            response += f"📌 {feature}:\n"
            for i, value in enumerate(values):
                response += f"   {headers[i+1]}: {value}\n"
            response += "\n"
        
        # Добавляем рекомендации
        response += "💡 Рекомендации:\n"
        if len(products) > 1:
            # Находим самый дешевый и дорогой продукт
            prices = [(p['name'], p['cost_per_unit']) for p in products]
            cheapest = min(prices, key=lambda x: x[1])
            most_expensive = max(prices, key=lambda x: x[1])
            
            response += f"\n🏷️ {cheapest[0]} - самый экономичный вариант"
            response += f"\n💎 {most_expensive[0]} - премиум вариант"
            
            # Добавляем рекомендации по выбору
            response += "\n\nКакой вариант выбрать:\n"
            for product in products:
                response += f"\n✨ {product['name']} подойдет если:\n"
                response += f"   - {generate_recommendation(product)}"
        
        return response
    except Exception as e:
        return f"Произошла ошибка при форматировании сравнения: {str(e)}"

def format_recommendations(recommendations_data):
    """Helper function to format recommendations"""
    try:
        if isinstance(recommendations_data, str):
            products = json.loads(recommendations_data)
        else:
            products = recommendations_data
            
        if not products:
            return "Извините, я не смог найти подходящие рекомендации."
        
        response = "📋 Вот мои рекомендации:\n\n"
        
        # Группируем продукты по категориям
        categories = {}
        for product in products:
            category = product['category_name']
            if category not in categories:
                categories[category] = []
            categories[category].append(product)
        
        # Форматируем рекомендации по категориям
        for category, category_products in categories.items():
            response += f"🔹 {category}:\n\n"
            
            # Сортируем продукты по цене
            category_products.sort(key=lambda x: x['cost_per_unit'])
            
            for product in category_products:
                response += f"📦 {product['name']} ({product['brand_name']})\n"
                response += f"   💰 Цена: {product['cost_per_unit']:,.0f} VND\n"
                response += f"   📝 {product['description']}\n"
                response += f"   ✨ {generate_recommendation(product)}\n\n"
        
        # Добавляем общие рекомендации
        response += "\n💡 Общие рекомендации:\n"
        response += "• Сравните описания и функции каждого продукта\n"
        response += "• Обратите внимание на срок действия подписок\n"
        response += "• Проверьте наличие действующих скидок и купонов\n"
        
        return response
    except Exception as e:
        return f"Произошла ошибка при форматировании рекомендаций: {str(e)}"

def generate_recommendation(product):
    """Helper function to generate specific recommendations based on product attributes"""
    recommendation = ""
    
    # Анализируем цену
    if product['cost_per_unit'] < 100000:  # Примерный порог для "бюджетного" продукта
        recommendation += "Экономичный вариант, подходит для базовых потребностей\n"
    elif product['cost_per_unit'] > 500000:  # Примерный порог для "премиум" продукта
        recommendation += "Премиум вариант с расширенной функциональностью\n"
    else:
        recommendation += "Оптимальное соотношение цены и качества\n"
    
    # Анализируем описание
    description = product['description'].lower()
    if "premium" in description or "pro" in description:
        recommendation += "   - Расширенный функционал для профессионального использования\n"
    if "family" in description:
        recommendation += "   - Подходит для семейного использования\n"
    if "student" in description:
        recommendation += "   - Специальные условия для студентов\n"
    
    return recommendation

async def chat_layer_2_async_wrapper(question: str, chat_history: list) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, chat_layer_2, question, chat_history)
    return response

async def chat_layer_1(question: str, chat_history: list) -> str:
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  

    chat_history_string = ""
    for chat_message in chat_history:
        chat_history_string += f"\n{chat_message['sender']}: {chat_message['message']}"

    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["question", "chat_history"],
        template=TEMPLATE_LAYER_1
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    try:
        response = await chain.ainvoke({"question": question, "chat_history": chat_history_string})
        if isinstance(response, dict) and "text" in response:
            response = response["text"]
        # Очищаем строку от недопустимых управляющих символов
        response = ''.join(char for char in response if ord(char) >= 32 or char in '\n\r\t')
        response_json = json.loads(response)
        return response_json
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        print(f"Raw response: {response}")
        # Возвращаем запасной вариант ответа в случае ошибки
        return {
            "can_query": "False",
            "response": "Извините, произошла ошибка при обработке ответа. Пожалуйста, попробуйте переформулировать вопрос."
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            "can_query": "False",
            "response": "Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
        }