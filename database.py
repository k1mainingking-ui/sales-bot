"""
Database module for Telegram Sales Bot
Handles all database operations and schema management
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class Database:
    """Database manager for the sales bot"""
    
    def __init__(self, db_path: str = "sales_bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                preferences TEXT
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                emoji TEXT,
                image_url TEXT,
                rating REAL DEFAULT 0,
                reviews_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                delivery_address TEXT,
                phone_number TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                UNIQUE(user_id, product_id)
            )
        ''')
        
        # Q&A history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_history (
                qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                product_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    # User operations
    def add_or_update_user(self, user_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None) -> bool:
        """Add or update user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, last_interaction)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, username, first_name, last_name))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding/updating user: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def update_user_contact(self, user_id: int, phone: str = None, email: str = None) -> bool:
        """Update user contact information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if phone:
                cursor.execute('UPDATE users SET phone_number = ? WHERE user_id = ?', 
                             (phone, user_id))
            if email:
                cursor.execute('UPDATE users SET email = ? WHERE user_id = ?', 
                             (email, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating user contact: {e}")
            return False
    
    # Product operations
    def add_product(self, name: str, category: str, description: str, 
                   price: float, stock: int, emoji: str = "", image_url: str = "") -> bool:
        """Add a new product"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO products 
                (name, category, description, price, stock, emoji, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, category, description, price, stock, emoji, image_url))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            return False
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """Get product by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting product: {e}")
            return None
    
    def get_all_products(self) -> List[Dict]:
        """Get all products"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products ORDER BY category, name')
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all products: {e}")
            return []
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Get products by category"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE category = ? ORDER BY name', 
                         (category,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting products by category: {e}")
            return []
    
    def search_products(self, query: str) -> List[Dict]:
        """Search products by name or description"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute('''
                SELECT * FROM products 
                WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
                ORDER BY name
            ''', (search_term, search_term, search_term))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return []
    
    def update_product_stock(self, product_id: int, quantity: int) -> bool:
        """Update product stock"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE products SET stock = stock - ? WHERE product_id = ?', 
                         (quantity, product_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating product stock: {e}")
            return False
    
    # Cart operations
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> bool:
        """Add item to cart"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO cart (user_id, product_id, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + ?
            ''', (user_id, product_id, quantity, quantity))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding to cart: {e}")
            return False
    
    def get_cart(self, user_id: int) -> List[Dict]:
        """Get user's cart"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, p.name, p.price, p.emoji, p.stock
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = ?
            ''', (user_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting cart: {e}")
            return []
    
    def remove_from_cart(self, user_id: int, product_id: int) -> bool:
        """Remove item from cart"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cart WHERE user_id = ? AND product_id = ?', 
                         (user_id, product_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error removing from cart: {e}")
            return False
    
    def clear_cart(self, user_id: int) -> bool:
        """Clear user's cart"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
            return False
    
    # Order operations
    def create_order(self, order_id: str, user_id: int, total_amount: float, 
                    delivery_address: str = "", phone_number: str = "", 
                    notes: str = "") -> bool:
        """Create a new order"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO orders 
                (order_id, user_id, total_amount, delivery_address, phone_number, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order_id, user_id, total_amount, delivery_address, phone_number, notes))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return False
    
    def add_order_item(self, order_id: str, product_id: int, 
                      quantity: int, unit_price: float) -> bool:
        """Add item to order"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            subtotal = quantity * unit_price
            
            cursor.execute('''
                INSERT INTO order_items 
                (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, product_id, quantity, unit_price, subtotal))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding order item: {e}")
            return False
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting order: {e}")
            return None
    
    def get_order_items(self, order_id: str) -> List[Dict]:
        """Get items in an order"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT oi.*, p.name, p.emoji
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = ?
            ''', (order_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting order items: {e}")
            return []
    
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Get all orders for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM orders 
                WHERE user_id = ? 
                ORDER BY created_at DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting user orders: {e}")
            return []
    
    def update_order_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE orders 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
            ''', (status, order_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            return False
    
    # Q&A operations
    def save_qa(self, user_id: int, question: str, answer: str, 
               product_id: int = None) -> bool:
        """Save Q&A interaction"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO qa_history 
                (user_id, question, answer, product_id)
                VALUES (?, ?, ?, ?)
            ''', (user_id, question, answer, product_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error saving Q&A: {e}")
            return False
    
    def get_user_qa_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get Q&A history for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM qa_history 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting Q&A history: {e}")
            return []
