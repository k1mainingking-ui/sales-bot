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
🎉 Welcome to Sales AI Agent, {user.first_name}!

I'm your intelligent shopping assistant. I can help you:
✅ Browse our product catalog
✅ Answer questions about products
✅ Process your orders
✅ Track deliveries

What would you like to do today?
        """
        
        keyboard = [
            [InlineKeyboardButton("📦 View Catalog", callback_data='catalog')],
            [InlineKeyboardButton("🛒 View Cart", callback_data='cart')],
            [InlineKeyboardButton("❓ Ask a Question", callback_data='qa')],
            [InlineKeyboardButton("📋 My Orders", callback_data='orders')]
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
        keyboard.append([InlineKeyboardButton("🔍 Search", callback_data='search')])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select a category:", reply_markup=reply_markup)
    
    async def show_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show products in category"""
        query = update.callback_query
        category = query.data.replace('cat_', '')
        await query.answer()
        
        products = self.db.get_products_by_category(category)
        
        if not products:
            await query.edit_message_text(f"No products found in {category}")
            return
        
        text = f"📦 {category} Products:\n\n"
        keyboard = []
        
        for product in products:
            stock_status = "✅ In Stock" if product['stock'] > 0 else "❌ Out of Stock"
            text += f"{product['emoji']} {product['name']}\n💰 ${product['price']:.2f} {stock_status}\n\n"
            keyboard.append([InlineKeyboardButton(f"View {product['name']}", callback_data=f'prod_{product['product_id']}')])
        
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='catalog')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_product(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show product details"""
        query = update.callback_query
        product_id = int(query.data.replace('prod_', ''))
        await query.answer()
        
        product = self.db.get_product(product_id)
        if not product:
            await query.edit_message_text("Product not found")
            return
        
        stock_status = "✅ In Stock" if product['stock'] > 0 else "❌ Out of Stock"
        text = f"""
{product['emoji']} {product['name']}

💰 Price: ${product['price']:.2f}
📊 Stock: {product['stock']} units
⭐ Rating: {product['rating']}/5 ({product['reviews_count']} reviews)

📝 Description:
{product['description']}

{stock_status}
        """
        
        keyboard = []
        if product['stock'] > 0:
            keyboard.append([InlineKeyboardButton("➕ Add to Cart", callback_data=f'addcart_{product_id}')])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='catalog')])
        
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
        
        await query.edit_message_text(f"✅ {product['name']} added to cart!")
        
        keyboard = [
            [InlineKeyboardButton("🛒 View Cart", callback_data='cart')],
            [InlineKeyboardButton("📦 Continue Shopping", callback_data='catalog')]
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
            await query.edit_message_text("Your cart is empty")
            keyboard = [[InlineKeyboardButton("📦 Browse Products", callback_data='catalog')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
            return
        
        text = "🛒 Your Cart:\n\n"
        total = 0
        keyboard = []
        
        for item in cart:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            text += f"{item['emoji']} {item['name']}\n"
            text += f"   ${item['price']:.2f} x {item['quantity']} = ${subtotal:.2f}\n\n"
            keyboard.append([InlineKeyboardButton(f"❌ Remove {item['name']}", callback_data=f'remove_{item['product_id']}')])
        
        text += f"\n💰 Total: ${total:.2f}"
        
        keyboard.append([InlineKeyboardButton("✅ Checkout", callback_data='checkout')])
        keyboard.append([InlineKeyboardButton("📦 Continue Shopping", callback_data='catalog')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def checkout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start checkout process"""
        query = update.callback_query
        user_id = update.effective_user.id
        await query.answer()
        
        cart = self.db.get_cart(user_id)
        if not cart:
            await query.edit_message_text("Your cart is empty")
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
✅ Order Confirmed!

📋 Order ID: {order_id}
💰 Total: ${total:.2f}
📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Your order has been placed successfully!
We'll process it shortly and send you tracking information.

Thank you for your purchase! 🎉
        """
        
        keyboard = [
            [InlineKeyboardButton("📦 Continue Shopping", callback_data='catalog')],
            [InlineKeyboardButton("📋 View Orders", callback_data='orders')]
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
            await query.edit_message_text("You have no orders yet")
            keyboard = [[InlineKeyboardButton("📦 Start Shopping", callback_data='catalog')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
            return
        
        text = "📋 Your Orders:\n\n"
        keyboard = []
        
        for order in orders:
            status_emoji = "✅" if order['status'] == 'completed' else "⏳"
            text += f"{status_emoji} {order['order_id']}\n"
            text += f"   Amount: ${order['total_amount']:.2f}\n"
            text += f"   Status: {order['status']}\n"
            text += f"   Date: {order['created_at']}\n\n"
            keyboard.append([InlineKeyboardButton(f"Details: {order['order_id']}", callback_data=f'orderdet_{order['order_id']}')])
        
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back')])
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
            answer = "I'm not sure about that. Please contact our support team at support@example.com"
        
        self.db.save_qa(user_id, update.message.text, answer)
        await update.message.reply_text(f"💬 {answer}")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        data = query.data
        
        if data == 'catalog':
            await self.catalog(update, context)
        elif data.startswith('cat_'):
            await self.show_category(update, context)
        elif data.startswith('prod_'):
            await self.show_product(update, context)
        elif data.startswith('addcart_'):
            await self.add_to_cart(update, context)
        elif data == 'cart':
            await self.view_cart(update, context)
        elif data == 'checkout':
            await self.checkout(update, context)
        elif data == 'orders':
            await self.view_orders(update, context)
        elif data == 'back':
            await self.start(update, context)
    
    def run(self):
        """Run the bot"""
        app = Application.builder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CallbackQueryHandler(self.button_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("Bot started successfully")
        app.run_polling()

if __name__ == '__main__':
    bot = SalesBot()
    bot.run()
