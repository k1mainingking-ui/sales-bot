# 🤖 Telegram Sales AI Agent Bot

A fully-featured intelligent sales assistant bot for Telegram that handles product catalog management, customer inquiries, shopping cart operations, and order processing.

## ✨ Features

### 🎯 Core Functionality
- **Intelligent Greeting & Navigation**: Warm welcome with clear menu options
- **Product Catalog**: 15+ sample products across 4 categories with emojis and pricing
- **Smart Search & Filtering**: Find products by category or search terms
- **Product Details**: Comprehensive descriptions, pricing, stock status, and ratings
- **Shopping Cart**: Add/remove items, view cart, manage quantities
- **Order Processing**: Step-by-step checkout with order confirmation and tracking
- **Q&A System**: Intelligent answers to common questions about shipping, returns, payments, etc.
- **Order History**: Users can view their past orders and status

### 📊 Product Categories
1. **Electronics** - Headphones, chargers, power banks, mice, keyboards
2. **Fashion** - T-shirts, jeans, jackets, shoes
3. **Home & Kitchen** - Coffee makers, blenders, cookware, water bottles
4. **Books & Media** - Programming guides, business handbooks

### 💾 Database Features
- User management with contact information
- Product inventory with stock tracking
- Shopping cart management
- Order history with status tracking
- Q&A interaction logging
- Timestamps for all transactions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Telegram Bot Token (from BotFather)
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
cd "d:\VS Code\CLINE pogect1"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your Telegram Bot Token
# TELEGRAM_BOT_TOKEN=your_token_here
```

4. **Initialize the database with sample products**
```bash
python init_db.py
```

5. **Run the bot**
```bash
python bot.py
```

## 📁 Project Structure

```
├── bot.py                 # Main bot implementation
├── database.py            # Database operations and schema
├── sample_products.py     # Sample product data and Q&A knowledge base
├── init_db.py            # Database initialization script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_BOT_USERNAME=your_bot_username

# Database Configuration
DATABASE_PATH=sales_bot.db

# Bot Settings
BOT_NAME=Sales AI Agent
BOT_DESCRIPTION=Smart sales assistant for product inquiries and orders

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=bot.log

# Delivery Settings
DEFAULT_DELIVERY_TIME=2-3 business days
DELIVERY_COST=5.00

# Admin Settings
ADMIN_USER_ID=your_admin_user_id
SUPPORT_EMAIL=support@example.com
```

## 📚 Database Schema

### Users Table
- `user_id`: Telegram user ID (Primary Key)
- `username`: Telegram username
- `first_name`: User's first name
- `last_name`: User's last name
- `phone_number`: Contact phone
- `email`: Contact email
- `created_at`: Account creation timestamp
- `last_interaction`: Last activity timestamp

### Products Table
- `product_id`: Unique product identifier (Primary Key)
- `name`: Product name
- `category`: Product category
- `description`: Detailed product description
- `price`: Product price
- `stock`: Available quantity
- `emoji`: Product emoji icon
- `image_url`: Product image URL
- `rating`: Product rating (0-5)
- `reviews_count`: Number of reviews

### Orders Table
- `order_id`: Unique order identifier (Primary Key)
- `user_id`: Customer user ID (Foreign Key)
- `total_amount`: Order total
- `status`: Order status (pending, processing, shipped, completed)
- `delivery_address`: Shipping address
- `phone_number`: Contact phone
- `notes`: Special instructions
- `created_at`: Order creation timestamp
- `updated_at`: Last update timestamp

### Order Items Table
- `item_id`: Unique item identifier (Primary Key)
- `order_id`: Associated order (Foreign Key)
- `product_id`: Product ordered (Foreign Key)
- `quantity`: Quantity ordered
- `unit_price`: Price per unit
- `subtotal`: Line item total

### Cart Table
- `cart_id`: Unique cart item identifier (Primary Key)
- `user_id`: User ID (Foreign Key)
- `product_id`: Product ID (Foreign Key)
- `quantity`: Quantity in cart
- `added_at`: When item was added

### Q&A History Table
- `qa_id`: Unique Q&A identifier (Primary Key)
- `user_id`: User ID (Foreign Key)
- `question`: User's question
- `answer`: Bot's answer
- `product_id`: Related product (if applicable)
- `created_at`: Timestamp

## 🎮 Bot Commands & Usage

### Main Menu
- **📦 View Catalog** - Browse products by category
- **🛒 View Cart** - See items in shopping cart
- **❓ Ask a Question** - Get answers about products, shipping, returns, etc.
- **📋 My Orders** - View order history and status

### Workflow Example

1. User sends `/start`
2. Bot displays welcome menu
3. User clicks "📦 View Catalog"
4. Bot shows product categories
5. User selects a category (e.g., "Electronics")
6. Bot displays products in that category
7. User clicks on a product to see details
8. User clicks "➕ Add to Cart"
9. User clicks "🛒 View Cart"
10. User clicks "✅ Checkout"
11. Bot creates order and shows confirmation with Order ID
12. User can view order history anytime

## 🤖 Q&A Knowledge Base

The bot can answer questions about:
- **Shipping**: Delivery times and express options
- **Returns**: 30-day return policy
- **Payment**: Accepted payment methods
- **Warranty**: Product warranty information
- **Bulk Orders**: Discounts for large orders
- **Tracking**: Order tracking capabilities
- **Support**: How to contact customer service
- **Exchanges**: Product exchange policy

## 🛠️ Customization

### Adding New Products

Edit `sample_products.py`:

```python
{
    "name": "Product Name",
    "category": "Category Name",
    "description": "Detailed description",
    "price": 99.99,
    "stock": 50,
    "emoji": "🎯",
    "image_url": "https://example.com/image.jpg"
}
```

Then run `init_db.py` to load products.

### Adding Q&A Responses

Edit `sample_products.py` in the `QA_KNOWLEDGE_BASE` dictionary:

```python
"custom_key": {
    "question": "What is your question?",
    "answer": "This is the answer"
}
```

### Modifying Bot Behavior

Edit `bot.py` to customize:
- Welcome messages
- Button layouts
- Order processing logic
- Error handling
- Logging levels

## 📊 Sample Products

The bot comes with 15 pre-loaded products:

**Electronics (5 products)**
- Wireless Headphones - $199.99
- USB-C Fast Charger - $49.99
- Portable Power Bank - $34.99
- Wireless Mouse - $29.99
- Mechanical Keyboard - $129.99

**Fashion (4 products)**
- Cotton T-Shirt - $24.99
- Denim Jeans - $59.99
- Leather Jacket - $249.99
- Running Shoes - $119.99

**Home & Kitchen (4 products)**
- Coffee Maker - $79.99
- Blender - $89.99
- Non-Stick Cookware Set - $99.99
- Stainless Steel Water Bottle - $34.99

**Books & Media (2 products)**
- Python Programming Guide - $39.99
- Business Strategy Handbook - $44.99

## 🔐 Security Considerations

- Store sensitive data (tokens, keys) in `.env` file
- Never commit `.env` to version control
- Use environment variables for all configuration
- Implement rate limiting for production
- Add user authentication if needed
- Validate all user inputs
- Use HTTPS for external API calls

## 📝 Logging

The bot logs all activities to `bot.log`:
- User interactions
- Database operations
- Errors and exceptions
- Order processing
- Q&A interactions

Configure logging level in `.env`:
```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🐛 Error Handling

The bot includes comprehensive error handling for:
- Missing environment variables
- Database connection errors
- Invalid user inputs
- Product not found errors
- Cart operation failures
- Order processing errors

## 🚀 Deployment

### Local Testing
```bash
python bot.py
```

### Production Deployment

1. **Use a process manager** (systemd, supervisor, PM2)
2. **Set up logging** to files
3. **Configure error notifications**
4. **Use a database backup strategy**
5. **Monitor bot performance**
6. **Implement rate limiting**

Example systemd service file:
```ini
[Unit]
Description=Telegram Sales Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 /path/to/bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 📞 Support

For issues or questions:
1. Check the logs in `bot.log`
2. Verify `.env` configuration
3. Ensure database is initialized
4. Check Telegram Bot Token validity
5. Review error messages in console

## 📄 License

This project is provided as-is for educational and commercial use.

## 🎯 Future Enhancements

- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications for orders
- [ ] Admin dashboard for order management
- [ ] Product recommendations based on purchase history
- [ ] Discount codes and promotional campaigns
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Customer reviews and ratings
- [ ] Wishlist functionality
- [ ] Real-time inventory updates

## 📊 Statistics

- **Products**: 15 sample products
- **Categories**: 4 categories
- **Q&A Responses**: 8 pre-configured answers
- **Database Tables**: 6 tables
- **Code Lines**: ~600+ lines of production code

---

**Built with ❤️ for Telegram Bot Developers**

For more information about the Telegram Bot API, visit: https://core.telegram.org/bots
