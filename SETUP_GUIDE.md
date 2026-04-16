# 🚀 Telegram Sales AI Agent - Setup Guide

Complete step-by-step guide to get your sales bot up and running.

## 📋 Prerequisites

Before you start, make sure you have:
- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Telegram account** (to create a bot)
- **Text editor** (VS Code, Notepad++, etc.)
- **Command line/Terminal** access

## 🤖 Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a conversation with BotFather
3. Send the command: `/newbot`
4. Follow the prompts:
   - Enter a name for your bot (e.g., "Sales AI Agent")
   - Enter a username (must end with "bot", e.g., "sales_ai_agent_bot")
5. **Copy the API token** provided by BotFather
   - It looks like: `123456789:ABCdefGHIjklmnoPQRstuvWXYZ`
6. Save this token securely - you'll need it next

## 📁 Step 2: Set Up Project Files

1. **Navigate to project directory**
   ```bash
   cd "d:\VS Code\CLINE pogect1"
   ```

2. **Verify all files are present**
   ```
   ✓ bot.py
   ✓ database.py
   ✓ sample_products.py
   ✓ init_db.py
   ✓ requirements.txt
   ✓ .env.example
   ✓ README.md
   ✓ SETUP_GUIDE.md
   ```

## 🔧 Step 3: Install Dependencies

1. **Open command prompt/terminal** in the project directory

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `python-telegram-bot==20.3` - Telegram Bot API
   - `python-dotenv==1.0.0` - Environment variable management
   - `requests==2.31.0` - HTTP library
   - `aiohttp==3.9.1` - Async HTTP client

3. **Wait for installation to complete**
   ```
   Successfully installed python-telegram-bot-20.3 ...
   ```

## ⚙️ Step 4: Configure Environment Variables

1. **Copy the example file**
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux: `cp .env.example .env`)

2. **Open `.env` file** in your text editor

3. **Add your Telegram Bot Token**
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ
   TELEGRAM_BOT_USERNAME=sales_ai_agent_bot
   ```

4. **Optional: Customize other settings**
   ```env
   BOT_NAME=My Sales Bot
   LOG_LEVEL=INFO
   SUPPORT_EMAIL=your_email@example.com
   ```

5. **Save the file**

## 💾 Step 5: Initialize Database

1. **Run the initialization script**
   ```bash
   python init_db.py
   ```

2. **Expected output**
   ```
   🚀 Initializing Sales Bot Database...
   --------------------------------------------------
   ✅ Database schema created successfully
   
   📦 Loading sample products...
   ✅ Sample products loaded successfully
   
   📊 Database Statistics:
      Total Products: 15
      Categories:
         - Books & Media: 2 products
         - Electronics: 5 products
         - Fashion: 4 products
         - Home & Kitchen: 4 products
   
   ==================================================
   ✅ Database initialization completed successfully!
   ==================================================
   ```

3. **Verify database file created**
   - You should see `sales_bot.db` in your project directory

## 🤖 Step 6: Run the Bot

1. **Start the bot**
   ```bash
   python bot.py
   ```

2. **Expected output**
   ```
   2024-04-15 23:30:00,123 - telegram.ext._application - INFO - Application started
   2024-04-15 23:30:00,456 - __main__ - INFO - Bot started successfully
   ```

3. **Bot is now running!** ✅

## 📱 Step 7: Test the Bot

1. **Open Telegram**

2. **Search for your bot** by username (e.g., @sales_ai_agent_bot)

3. **Send `/start` command**

4. **You should see the welcome menu**
   ```
   🎉 Welcome to Sales AI Agent!
   
   I'm your intelligent shopping assistant...
   
   [📦 View Catalog] [🛒 View Cart] [❓ Ask a Question] [📋 My Orders]
   ```

5. **Test the features**
   - Click "📦 View Catalog" to browse products
   - Select a category to see products
   - Click on a product to view details
   - Add items to cart
   - Proceed to checkout
   - Ask questions about shipping, returns, etc.

## 🎯 Common Test Scenarios

### Scenario 1: Browse and Purchase
1. Click "📦 View Catalog"
2. Select "Electronics"
3. Click "View Wireless Headphones"
4. Click "➕ Add to Cart"
5. Click "🛒 View Cart"
6. Click "✅ Checkout"
7. See order confirmation with Order ID

### Scenario 2: Ask Questions
1. Type: "How long does shipping take?"
2. Bot responds with shipping information
3. Type: "What's your return policy?"
4. Bot responds with return policy

### Scenario 3: View Orders
1. Click "📋 My Orders"
2. See your previous orders
3. Click on an order to see details

## 🐛 Troubleshooting

### Issue: "TELEGRAM_BOT_TOKEN not found"
**Solution:**
- Check `.env` file exists in project directory
- Verify `TELEGRAM_BOT_TOKEN=` line is present
- Ensure token is correct (no spaces, full token)
- Restart the bot

### Issue: "ModuleNotFoundError: No module named 'telegram'"
**Solution:**
```bash
pip install python-telegram-bot==20.3
```

### Issue: "Database is locked"
**Solution:**
- Close any other instances of the bot
- Delete `sales_bot.db` and run `python init_db.py` again

### Issue: Bot doesn't respond to messages
**Solution:**
- Check bot is running (no errors in console)
- Verify token is correct
- Try `/start` command again
- Check logs in `bot.log`

### Issue: "Connection refused" or "Network error"
**Solution:**
- Check internet connection
- Verify Telegram API is accessible
- Check firewall settings
- Try restarting the bot

## 📊 Database Files

After initialization, you'll have:
- `sales_bot.db` - SQLite database with all data
- `bot.log` - Bot activity logs (created on first run)

## 🔐 Security Tips

1. **Never share your bot token**
   - Keep `.env` file private
   - Don't commit `.env` to version control

2. **Use environment variables**
   - All sensitive data should be in `.env`
   - Never hardcode tokens or keys

3. **Validate user input**
   - Bot already validates inputs
   - Add more validation if needed

4. **Monitor logs**
   - Check `bot.log` regularly
   - Look for suspicious activity

## 📈 Next Steps

### Customize the Bot
1. **Add more products** - Edit `sample_products.py`
2. **Modify Q&A responses** - Update `QA_KNOWLEDGE_BASE`
3. **Change welcome message** - Edit `bot.py` start() method
4. **Add new features** - Extend `bot.py` with new handlers

### Deploy to Production
1. **Use a process manager** (systemd, supervisor, PM2)
2. **Set up logging** to files
3. **Configure backups** for database
4. **Monitor performance** and errors
5. **Use a VPS or cloud server** for 24/7 operation

### Integrate Payment
1. **Add Stripe integration** for payments
2. **Implement payment verification**
3. **Update order status** after payment
4. **Send payment confirmations**

## 📞 Getting Help

### Check Logs
```bash
# View recent logs
tail -f bot.log

# On Windows, use:
type bot.log
```

### Verify Configuration
```bash
# Check if .env file exists
ls -la .env

# Check if database exists
ls -la sales_bot.db
```

### Test Bot Token
```python
# Create a test script to verify token
import requests
token = "YOUR_TOKEN_HERE"
url = f"https://api.telegram.org/bot{token}/getMe"
response = requests.get(url)
print(response.json())
```

## 🎓 Learning Resources

- **Telegram Bot API**: https://core.telegram.org/bots
- **python-telegram-bot**: https://python-telegram-bot.readthedocs.io/
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **Python Async/Await**: https://docs.python.org/3/library/asyncio.html

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Python 3.8+ installed
- [ ] All project files present
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with bot token
- [ ] Database initialized (`python init_db.py`)
- [ ] Bot runs without errors (`python bot.py`)
- [ ] Bot responds to `/start` command
- [ ] Can browse products
- [ ] Can add items to cart
- [ ] Can complete checkout
- [ ] Can ask questions
- [ ] Can view order history

## 🎉 Success!

If you've completed all steps and the bot is working, congratulations! 🎊

Your Telegram Sales AI Agent is now ready to:
- ✅ Greet customers warmly
- ✅ Display product catalog
- ✅ Answer customer questions
- ✅ Process orders
- ✅ Track order history

---

**Need help?** Check the README.md for more detailed information about features and customization.

**Happy selling!** 🚀
python init_db.py