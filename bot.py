#!/usr/bin/env python3
"""
Telegram Sales AI Agent Bot
Main bot implementation with all handlers and functionality
"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from database import Database
from sample_products import load_sample_products, PRODUCT_CATEGORIES, QA_KNOWLEDGE_BASE

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()

# Conversation states
SELECTING_CATEGORY, VIEWING_PRODUCT, ADDING_TO_CART, CHECKOUT, PAYMENT = range(5)

class SalesBot:
    def __init__(self):
        self.db = db
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        self.db.add_or_update_user(user.id, user.username, user.first_name, user.last_name)
        
        welcome_text = f"""
✨ Добро пожаловать, {user.first_name}!

Вас приветствует бутик красоты Factura 💅

Ваш личный помощник для записи на процедуры.

Я могу помочь вам:
✅ Просмотреть список наших услуг
✅ Записаться на приём
✅ Получить консультацию
✅ Узнать цены и акции

Выберите что вас интересует:
        """
        
        keyboard = [
            [InlineKeyboardButton("💆‍♀️ Наши услуги", callback_data='services')],
            [InlineKeyboardButton("📞 Записаться на приём", callback_data='book')],
            [InlineKeyboardButton("❓ Задать вопрос", callback_data='qa')],
            [InlineKeyboardButton("📍 Наши контакты", callback_data='contacts')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def catalog(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show product catalog"""
        query = update.callback_query
        await query.answer()
        
        keyboard = []
        for category in PRODUCT_CATEGORIES:
            keyboard.append([InlineKeyboardButton(f"📂 {category}", callback_data=f'cat_{category}')])
        keyboard.append([InlineKeyboardButton("🔍 Поиск", callback_data='search')])
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='back')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите категорию:", reply_markup=reply_markup)
    
    async def show_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show products in category"""
        query = update.callback_query
        category = query.data.replace('cat_', '')
        await query.answer()
        
        products = self.db.get_products_by_category(category)
        
        if not products:
            await query.edit_message_text(f"Товары в категории {category} не найдены")
            return
        
        text = f"📦 Товары категории {category}:\n\n"
        keyboard = []
        
        for product in products:
            stock_status = "✅ В наличии" if product['stock'] > 0 else "❌ Нет в наличии"
            text += f"{product['emoji']} {product['name']}\n💰 {product['price']:.2f} ₽ {stock_status}\n\n"
            keyboard.append([InlineKeyboardButton(f"Посмотреть {product['name']}", callback_data=f'prod_{product["product_id"]}')])
        
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='catalog')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_product(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show product details"""
        query = update.callback_query
        product_id = int(query.data.replace('prod_', ''))
        await query.answer()
        
        product = self.db.get_product(product_id)
        if not product:
            await query.edit_message_text("Товар не найден")
            return
        
        stock_status = "✅ В наличии" if product['stock'] > 0 else "❌ Нет в наличии"
        text = f"""
{product['emoji']} {product['name']}

💰 Цена: {product['price']:.2f} ₽
📊 На складе: {product['stock']} шт.
⭐ Рейтинг: {product['rating']}/5 (отзывов: {product['reviews_count']})

📝 Описание:
{product['description']}

{stock_status}
        """
        
        keyboard = []
        if product['stock'] > 0:
            keyboard.append([InlineKeyboardButton("➕ В корзину", callback_data=f'addcart_{product_id}')])
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='catalog')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def add_to_cart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Add product to cart"""
        query = update.callback_query
        product_id = int(query.data.replace('addcart_', ''))
        user_id = update.effective_user.id
        await query.answer()
        
        product = self.db.get_product(product_id)
        self.db.add_to_cart(user_id, product_id, 1)
        
        await query.edit_message_text(f"✅ {product['name']} добавлен в корзину!")
        
        keyboard = [
            [InlineKeyboardButton("🛒 Посмотреть корзину", callback_data='cart')],
            [InlineKeyboardButton("📦 Продолжить покупки", callback_data='catalog')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)
    
    async def view_cart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View shopping cart"""
        query = update.callback_query
        user_id = update.effective_user.id
        await query.answer()
        
        cart = self.db.get_cart(user_id)
        
        if not cart:
            await query.edit_message_text("Ваша корзина пуста")
            keyboard = [[InlineKeyboardButton("📦 Смотреть товары", callback_data='catalog')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
            return
        
        text = "🛒 Ваша корзина:\n\n"
        total = 0
        keyboard = []
        
        for item in cart:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            text += f"{item['emoji']} {item['name']}\n"
            text += f"   {item['price']:.2f} ₽ x {item['quantity']} = {subtotal:.2f} ₽\n\n"
            keyboard.append([InlineKeyboardButton(f"❌ Удалить {item['name']}", callback_data=f'remove_{item["product_id"]}')])
        
        text += f"\n💰 Итого: {total:.2f} ₽"
        
        keyboard.append([InlineKeyboardButton("✅ Оформить заказ", callback_data='checkout')])
        keyboard.append([InlineKeyboardButton("📦 Продолжить покупки", callback_data='catalog')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def checkout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start checkout process"""
        query = update.callback_query
        user_id = update.effective_user.id
        await query.answer()
        
        cart = self.db.get_cart(user_id)
        if not cart:
            await query.edit_message_text("Ваша корзина пуста")
            return
        
        # Create order
        order_id = f"ORD-{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        total = sum(item['price'] * item['quantity'] for item in cart)
        
        self.db.create_order(order_id, user_id, total)
        
        for item in cart:
            self.db.add_order_item(order_id, item['product_id'], item['quantity'], item['price'])
            self.db.update_product_stock(item['product_id'], item['quantity'])
        
        self.db.clear_cart(user_id)
        
        confirmation = f"""
✅ Заказ подтверждён!

📋 Номер заказа: {order_id}
💰 Сумма: {total:.2f} ₽
📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Ваш заказ успешно оформлен!
Мы скоро обработаем его и отправим вам информацию для отслеживания.

Спасибо за покупку! 🎉
        """
        
        keyboard = [
            [InlineKeyboardButton("📦 Продолжить покупки", callback_data='catalog')],
            [InlineKeyboardButton("📋 Посмотреть заказы", callback_data='orders')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(confirmation, reply_markup=reply_markup)
    
    async def view_orders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View user's orders"""
        query = update.callback_query
        user_id = update.effective_user.id
        await query.answer()
        
        orders = self.db.get_user_orders(user_id)
        
        if not orders:
            await query.edit_message_text("У вас пока нет заказов")
            keyboard = [[InlineKeyboardButton("📦 Начать покупки", callback_data='catalog')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
            return
        
        text = "📋 Ваши заказы:\n\n"
        keyboard = []
        
        for order in orders:
            if order['status'] == 'completed':
                status_emoji = "✅"
                status_text = "Выполнен"
            elif order['status'] == 'pending':
                status_emoji = "⏳"
                status_text = "В обработке"
            elif order['status'] == 'cancelled':
                status_emoji = "❌"
                status_text = "Отменён"
            else:
                status_emoji = "⏳"
                status_text = order['status']
                
            text += f"{status_emoji} {order['order_id']}\n"
            text += f"   Сумма: {order['total_amount']:.2f} ₽\n"
            text += f"   Статус: {status_text}\n"
            text += f"   Дата: {order['created_at']}\n\n"
            keyboard.append([InlineKeyboardButton(f"Детали: {order['order_id']}", callback_data=f'orderdet_{order["order_id"]}')])
        
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages for Q&A"""
        user_id = update.effective_user.id
        message = update.message.text.lower()
        
        # Search for matching Q&A
        answer = None
        for key, qa in QA_KNOWLEDGE_BASE.items():
            if any(word in message for word in qa['question'].lower().split()):
                answer = qa['answer']
                break
        
        if not answer:
            answer = "Я не уверен в этом. Пожалуйста, свяжитесь с нашей службой поддержки по адресу support@example.com"
        
        self.db.save_qa(user_id, update.message.text, answer)
        await update.message.reply_text(f"💬 {answer}")
    
    async def services(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show beauty salon services"""
        query = update.callback_query
        await query.answer()
        
        services_list = [
            {"name": "Маникюр классический", "price": 1500, "emoji": "💅"},
            {"name": "Маникюр с покрытием гель-лак", "price": 2500, "emoji": "💅"},
            {"name": "Маникюр с дизайном", "price": 3000, "emoji": "💅"},
            {"name": "Наращивание ногтей", "price": 3500, "emoji": "💅"},
            {"name": "Педикюр классический", "price": 1800, "emoji": "🦶"},
            {"name": "Педикюр с покрытием гель-лак", "price": 2800, "emoji": "🦶"},
            {"name": "Стрижка женская", "price": 2500, "emoji": "✂️"},
            {"name": "Стрижка мужская", "price": 1500, "emoji": "✂️"},
            {"name": "Окрашивание волос", "price": 4500, "emoji": "🎨"},
            {"name": "Окрашивание в один тон", "price": 3500, "emoji": "🎨"},
            {"name": "Мелирование волос", "price": 5000, "emoji": "🎨"},
            {"name": "Укладка волос", "price": 1500, "emoji": "💇‍♀️"},
            {"name": "Выпрямление волос кератином", "price": 7000, "emoji": "💇‍♀️"},
            {"name": "Макияж дневной", "price": 2000, "emoji": "💄"},
            {"name": "Макияж вечерний", "price": 3500, "emoji": "💄"},
            {"name": "Макияж свадебный", "price": 5000, "emoji": "💄"},
            {"name": "Чистка лица", "price": 3000, "emoji": "✨"},
            {"name": "Пилинг лица", "price": 2500, "emoji": "✨"},
            {"name": "Массаж лица", "price": 2500, "emoji": "😌"},
            {"name": "Ламинирование бровей", "price": 1800, "emoji": "👁️"},
            {"name": "Окрашивание бровей и ресниц", "price": 1200, "emoji": "👁️"},
            {"name": "Биоревитализация лица", "price": 8000, "emoji": "✨"},
            {"name": "Депиляция воском (руки/ноги)", "price": 2000, "emoji": "🌸"},
            {"name": "Депиляция сахарная", "price": 2500, "emoji": "🌸"},
            {"name": "SPA-программа для тела", "price": 5000, "emoji": "🧖‍♀️"},
            {"name": "Массаж общий", "price": 3500, "emoji": "💆"},
            {"name": "Обёртывание антицеллюлитное", "price": 4000, "emoji": "🧖‍♀️"},
        ]
        
        text = "✨ Услуги студии красоты Factura:\n\n"
        keyboard = []
        
        for service in services_list:
            text += f"{service['emoji']} {service['name']}\n   💰 {service['price']} ₽\n\n"
        
        keyboard.append([InlineKeyboardButton("📞 Записаться на услугу", callback_data='book')])
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='back')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def book_appointment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Book appointment"""
        query = update.callback_query
        await query.answer()
        
        text = """
📞 Для записи на приём:

Позвоните нам по телефону: +7 (383) 303-41-42
Или напишите администратору в WhatsApp

Мы с радостью подберём для вас удобное время!

⏰ График работы:
Пн-Пт: 09:00 - 21:00
Сб-Вс: 10:00 - 19:00
        """
        
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_contacts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show contact information"""
        query = update.callback_query
        await query.answer()
        
        text = """
📍 Студия красоты Factura

🏠 Адрес: г. Новосибирск, Красный проспект, 123, офис 45
📞 Телефон: +7 (383) 303-41-42
📱 WhatsApp: +7 (913) 123-45-67
📧 Email: info@factura-beauty.ru
🌐 Сайт: factura-beauty.ru

⏰ График работы:
Понедельник - Пятница: 09:00 - 21:00
Суббота: 10:00 - 19:00
Воскресенье: 10:00 - 18:00
        """
        
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        data = query.data
        
        if data == 'services':
            await self.services(update, context)
        elif data == 'book':
            await self.book_appointment(update, context)
        elif data == 'contacts':
            await self.show_contacts(update, context)
        elif data == 'qa':
            await query.answer()
            await query.edit_message_text("💬 Напишите ваш вопрос и мы с радостью ответим!")
        elif data == 'back':
            await self.start(update, context)
    
    async def welcome_new_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message when user writes first message"""
        await update.message.reply_text("Добро пожаловать, Вас приветствует бутик красоты Factura, для начала работы нажмите /start")
    
    def run(self):
        """Run the bot"""
        app = Application.builder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CallbackQueryHandler(self.button_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.welcome_new_user))
        
        logger.info("Bot started successfully")
        app.run_polling()

if __name__ == '__main__':
    bot = SalesBot()
    bot.run()
