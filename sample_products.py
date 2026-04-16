"""
Sample product data for the Telegram Sales Bot
This file contains sample products that can be loaded into the database
"""

SAMPLE_PRODUCTS = [
    # Electronics Category
    {
        "name": "Wireless Headphones",
        "category": "Electronics",
        "description": "Premium noise-cancelling wireless headphones with 30-hour battery life. Features active noise cancellation, touch controls, and premium sound quality.",
        "price": 199.99,
        "stock": 45,
        "emoji": "🎧",
        "image_url": "https://example.com/headphones.jpg"
    },
    {
        "name": "USB-C Fast Charger",
        "category": "Electronics",
        "description": "65W USB-C fast charger compatible with laptops, tablets, and smartphones. Compact design with multiple ports.",
        "price": 49.99,
        "stock": 120,
        "emoji": "🔌",
        "image_url": "https://example.com/charger.jpg"
    },
    {
        "name": "Portable Power Bank",
        "category": "Electronics",
        "description": "20000mAh portable power bank with fast charging. Supports multiple devices simultaneously.",
        "price": 34.99,
        "stock": 85,
        "emoji": "🔋",
        "image_url": "https://example.com/powerbank.jpg"
    },
    {
        "name": "Wireless Mouse",
        "category": "Electronics",
        "description": "Ergonomic wireless mouse with precision tracking and 18-month battery life.",
        "price": 29.99,
        "stock": 150,
        "emoji": "🖱️",
        "image_url": "https://example.com/mouse.jpg"
    },
    {
        "name": "Mechanical Keyboard",
        "category": "Electronics",
        "description": "RGB mechanical keyboard with customizable switches and programmable keys. Perfect for gaming and typing.",
        "price": 129.99,
        "stock": 60,
        "emoji": "⌨️",
        "image_url": "https://example.com/keyboard.jpg"
    },
    
    # Fashion Category
    {
        "name": "Cotton T-Shirt",
        "category": "Fashion",
        "description": "100% organic cotton t-shirt available in multiple colors. Comfortable and breathable for everyday wear.",
        "price": 24.99,
        "stock": 200,
        "emoji": "👕",
        "image_url": "https://example.com/tshirt.jpg"
    },
    {
        "name": "Denim Jeans",
        "category": "Fashion",
        "description": "Classic blue denim jeans with comfortable fit. Available in various sizes and styles.",
        "price": 59.99,
        "stock": 95,
        "emoji": "👖",
        "image_url": "https://example.com/jeans.jpg"
    },
    {
        "name": "Leather Jacket",
        "category": "Fashion",
        "description": "Premium genuine leather jacket with classic design. Perfect for any season.",
        "price": 249.99,
        "stock": 30,
        "emoji": "🧥",
        "image_url": "https://example.com/jacket.jpg"
    },
    {
        "name": "Running Shoes",
        "category": "Fashion",
        "description": "Professional running shoes with advanced cushioning technology. Lightweight and durable.",
        "price": 119.99,
        "stock": 75,
        "emoji": "👟",
        "image_url": "https://example.com/shoes.jpg"
    },
    
    # Home & Kitchen Category
    {
        "name": "Coffee Maker",
        "category": "Home & Kitchen",
        "description": "Programmable coffee maker with thermal carafe. Makes up to 12 cups of coffee.",
        "price": 79.99,
        "stock": 40,
        "emoji": "☕",
        "image_url": "https://example.com/coffeemaker.jpg"
    },
    {
        "name": "Blender",
        "category": "Home & Kitchen",
        "description": "High-power blender with 6 preset programs. Perfect for smoothies, soups, and more.",
        "price": 89.99,
        "stock": 35,
        "emoji": "🥤",
        "image_url": "https://example.com/blender.jpg"
    },
    {
        "name": "Non-Stick Cookware Set",
        "category": "Home & Kitchen",
        "description": "10-piece non-stick cookware set with heat-resistant handles. Dishwasher safe.",
        "price": 99.99,
        "stock": 25,
        "emoji": "🍳",
        "image_url": "https://example.com/cookware.jpg"
    },
    {
        "name": "Stainless Steel Water Bottle",
        "category": "Home & Kitchen",
        "description": "Insulated water bottle keeps drinks hot for 12 hours or cold for 24 hours. Eco-friendly design.",
        "price": 34.99,
        "stock": 110,
        "emoji": "🧊",
        "image_url": "https://example.com/waterbottle.jpg"
    },
    
    # Books & Media Category
    {
        "name": "Python Programming Guide",
        "category": "Books & Media",
        "description": "Comprehensive guide to Python programming for beginners and intermediate developers.",
        "price": 39.99,
        "stock": 50,
        "emoji": "📚",
        "image_url": "https://example.com/python_book.jpg"
    },
    {
        "name": "Business Strategy Handbook",
        "category": "Books & Media",
        "description": "Essential strategies for modern business success. Written by industry experts.",
        "price": 44.99,
        "stock": 40,
        "emoji": "📖",
        "image_url": "https://example.com/business_book.jpg"
    },
]

def load_sample_products(db):
    """
    Load sample products into the database
    
    Args:
        db: Database instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        for product in SAMPLE_PRODUCTS:
            db.add_product(
                name=product["name"],
                category=product["category"],
                description=product["description"],
                price=product["price"],
                stock=product["stock"],
                emoji=product["emoji"],
                image_url=product["image_url"]
            )
        print(f"✅ Successfully loaded {len(SAMPLE_PRODUCTS)} sample products")
        return True
    except Exception as e:
        print(f"❌ Error loading sample products: {e}")
        return False


# Product categories for filtering
PRODUCT_CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Books & Media"
]

# Common questions and answers for Q&A system
QA_KNOWLEDGE_BASE = {
    "shipping": {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 2-3 business days. Express shipping is available for 1-day delivery at an additional cost."
    },
    "returns": {
        "question": "What is your return policy?",
        "answer": "We offer 30-day returns on all products. Items must be in original condition with all packaging."
    },
    "payment": {
        "question": "What payment methods do you accept?",
        "answer": "We accept all major credit cards, PayPal, and bank transfers."
    },
    "warranty": {
        "question": "Do products come with warranty?",
        "answer": "Most electronics come with a 1-year manufacturer's warranty. Check product details for specific warranty information."
    },
    "bulk_orders": {
        "question": "Do you offer discounts for bulk orders?",
        "answer": "Yes! Orders of 10+ items receive a 10% discount. Contact our support team for larger orders."
    },
    "tracking": {
        "question": "Can I track my order?",
        "answer": "Yes, you'll receive a tracking number via email once your order ships. You can use it to monitor delivery status."
    },
    "contact": {
        "question": "How can I contact customer support?",
        "answer": "You can reach our support team via email at support@example.com or through this chat. We respond within 24 hours."
    },
    "exchange": {
        "question": "Can I exchange a product?",
        "answer": "Yes, we offer free exchanges within 30 days of purchase for defective items or if you received the wrong product."
    }
}

# Product recommendations based on user interests
RECOMMENDATIONS = {
    "electronics_lover": [1, 2, 3, 4, 5],  # All electronics
    "fashion_enthusiast": [6, 7, 8, 9],    # All fashion items
    "home_cook": [10, 11, 12, 13],         # Home & Kitchen items
    "student": [14, 15, 2, 4],             # Books, charger, mouse, keyboard
    "professional": [1, 4, 5, 14],         # Headphones, mouse, keyboard, books
}
