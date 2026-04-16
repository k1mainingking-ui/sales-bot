#!/usr/bin/env python3
"""
Database initialization script
Loads sample products into the database
"""

import sys
from database import Database
from sample_products import load_sample_products

def main():
    """Initialize database with sample data"""
    print("🚀 Initializing Sales Bot Database...")
    print("-" * 50)
    
    try:
        # Create database instance
        db = Database()
        print("✅ Database schema created successfully")
        
        # Load sample products
        print("\n📦 Loading sample products...")
        if load_sample_products(db):
            print("✅ Sample products loaded successfully")
        else:
            print("❌ Failed to load sample products")
            return False
        
        # Verify products were loaded
        all_products = db.get_all_products()
        print(f"\n📊 Database Statistics:")
        print(f"   Total Products: {len(all_products)}")
        
        # Count by category
        categories = {}
        for product in all_products:
            cat = product['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"   Categories:")
        for cat, count in sorted(categories.items()):
            print(f"      - {cat}: {count} products")
        
        print("\n" + "=" * 50)
        print("✅ Database initialization completed successfully!")
        print("=" * 50)
        print("\n📝 Next steps:")
        print("   1. Configure your .env file with TELEGRAM_BOT_TOKEN")
        print("   2. Run: python bot.py")
        print("\n🎉 Your bot is ready to go!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
