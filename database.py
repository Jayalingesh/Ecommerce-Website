import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "nexashop.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

SCHEMA ="""

    CREATE TABLE IF NOT EXISTS users(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT NOT NULL,
        email           TEXT NOT NULL UNIQUE,
        password_hash   TEXT NOT NULL,
        create_at       DATETIME DEFAULT CURRENT_TIMESTAMP);
        
    CREATE TABLE IF NOT EXISTS products(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT NOT NULL,
        price           REAL NOT NULL,
        original_price  REAL,
        category        TEXT NOT NULL,
        rating          REAL DEFAULT 0,
        reviews         INTEGER DEFAULT 0,
        stock           INTEGER DEFAULT 0,
        badge           TEXT,
        image           TEXT,
        description     TEXT,
        features        TEXT,
        created_at      DATETIME DEFAULT CURRENT_TIMESTAMP);
        
    CREATE TABLE IF NOT EXISTS orders(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER REFERENCES users(id) ON DELETE SET NULL,
        order_ref   TEXT NOT NULL UNIQUE,
        name        TEXT NOT NULL,
        address     TEXT NOT NULL,
        city        TEXT NOT NULL,
        subtotal    REAL NOT NULL,
        shipping    REAL NOT NULL,
        tax         REAL NOT NULL,
        total       REAL NOT NULL,
        status      TEXT DEFAULT 'Processing',
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    );
        
    CREATE TABLE IF NOT EXISTS order_items (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id    INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
        product_id  INTEGER REFERENCES products(id) ON DELETE SET NULL,
        name        TEXT    NOT NULL,
        price       REAL    NOT NULL,
        qty         INTEGER NOT NULL,
        subtotal    REAL    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS wishlist (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        UNIQUE(user_id, product_id)
    );
"""
PRODUCTS = [
    {"id": 1,"name": "Wireless Noise-Cancelling Headphones", "price": 2392.99, "original_price": 3192.99, "category": "Electronics", "rating": 4.8, "reviews": 1240, "stock": 15, "badge": "Best Seller", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80", "description": "Premium wireless headphones with 40-hour battery life, active noise cancellation, and studio-quality sound. Foldable design with carrying case included.", "features": ["40-hour battery", "Active Noise Cancellation", "Bluetooth 5.0", "Fast charge (10min = 3hrs)"]},

    {"id": 2, "name": "Mechanical Gaming Keyboard", "price": 1192.99, "original_price": 1512.99, "category": "Electronics", "rating": 4.7, "reviews": 876, "stock": 30,
    "badge": "Hot",
    "image": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400&q=80",
    "description": "RGB backlit mechanical keyboard with tactile switches, n-key rollover, and aluminum frame. Perfect for gaming and productivity.",
    "features": ["Cherry MX switches", "Per-key RGB", "Aluminum frame", "Detachable USB-C cable"]},

    {"id": 3, 
        "name": "4K Ultra HD Monitor 27\"", "price": 39920.99, 
        "original_price": 51920.99,
        "category": "Electronics", 
        "rating": 4.9, 
        "reviews": 543, 
        "stock": 8,
        "badge": "Sale",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&q=80",
        "description": "27-inch 4K IPS display with 144Hz refresh rate, HDR400, and ultra-thin bezels. Ideal for creative professionals and gamers.",
        "features": ["4K 3840x2160", "144Hz refresh", "HDR400", "USB-C 65W charging"]
    },

    {
        "id": 4, 
        "name": "Smart Fitness Watch", 
        "price": 1992.99, 
        "original_price": 2392.99,
        "category": "Wearables", 
        "rating": 4.6, 
        "reviews": 2100, 
        "stock": 50,
        "badge": "New",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80",
        "description": "Advanced fitness tracker with GPS, heart rate monitor, sleep tracking, and 7-day battery. Water resistant to 50 meters.",
        "features": ["Built-in GPS", "Heart rate & SpO2", "7-day battery", "50m water resistance"]
    },

    {
        "id": 5, 
        "name": "Ergonomic Office Chair", "price": 13920.99, 
        "original_price": 23920.99,
        "category": "Furniture", 
        "rating": 4.5, 
        "reviews": 389, 
        "stock": 12,
        "badge": "Sale",
        "image": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400&q=80",
        "description": "Full lumbar support ergonomic chair with adjustable armrests, seat depth, and tilt tension. Breathable mesh back for all-day comfort.",
        "features": ["Lumbar support", "Adjustable armrests", "Breathable mesh", "5-year warranty"]
    },

    {
        "id": 6, 
        "name": "Professional Camera Drone", "price": 63920.99, 
        "original_price": 79920.99,
        "category": "Electronics", 
        "rating": 4.8, 
        "reviews": 234, 
        "stock": 5,
        "badge": "Limited",
        "image": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400&q=80",
        "description": "4K camera drone with 3-axis gimbal, obstacle avoidance, 30-min flight time, and 7km transmission range.",
        "features": ["4K/60fps video", "3-axis gimbal", "30-min flight", "Obstacle avoidance"]
    },

    {
        "id": 7, 
        "name": "Portable Bluetooth Speaker", "price": 712.99, 
        "original_price": 952.99,
        "category": "Electronics", 
        "rating": 4.4, 
        "reviews": 1567, 
        "stock": 45,
        "badge": "Best Seller",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&q=80",
        "description": "360-degree sound, 20-hour playtime, IPX7 waterproof. Pair two speakers for stereo sound. Built-in mic for calls.",
        "features": ["360° sound", "20-hour battery", "IPX7 waterproof", "Dual speaker pairing"]
    },

    {
        "id": 8, 
        "name": "Standing Desk 60\"", 
        "price": 4392.99, 
        "original_price": 5592.99,
        "category": "Furniture", 
        "rating": 4.7, 
        "reviews": 712, 
        "stock": 7,
        "badge": "Popular",
        "image": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&q=80",
        "description": "Electric height-adjustable standing desk with memory presets, anti-collision, and cable management. Supports up to 300 lbs.",
        "features": ["Electric adjustment", "4 memory presets", "Anti-collision", "300 lb capacity"]
    },

    {
        "id": 9, 
        "name": "Wireless Charging Pad", "price": 3120.99, 
        "original_price": 4720.99,
        "category": "Accessories", 
        "rating": 4.3, 
        "reviews": 3200, 
        "stock": 100,
        "badge": "New",
        "image": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&q=80",
        "description": "15W fast wireless charger compatible with all Qi devices. Charges through cases up to 5mm thick. LED indicator.",
        "features": ["15W fast charge", "Qi universal", "Charges through cases", "Anti-slip surface"]
    },

    {
        "id": 10, 
        "name": "Noise-Cancelling Earbuds", "price": 1432.99, 
        "original_price": 1832.99,
        "category": "Electronics", 
        "rating": 4.7, 
        "reviews": 4521, 
        "stock": 60,
        "badge": "Hot",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&q=80",
        "description": "True wireless earbuds with ANC, 8hr battery + 24hr case, IPX4, and multipoint connection to 2 devices simultaneously.",
        "features": ["Active Noise Cancellation", "32hr total battery", "IPX4 splash proof", "Multipoint connection"]
    },

    {
        "id": 11, 
        "name": "Smart Home Hub", 
        "price": 10320.99, 
        "original_price": 12720.99,
        "category": "Smart Home", 
        "rating": 4.5, 
        "reviews": 890, 
        "stock": 25,
        "badge": "New",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80",
        "description": "Control all your smart devices from one hub. Compatible with Alexa, Google, and HomeKit. Supports 300+ device types.",
        "features": ["300+ device support", "Voice assistant ready", "Auto scenes", "Energy monitoring"]
    },

    {
        "id": 12, 
        "name": "Laptop Stand Adjustable", "price": 472.99, 
        "original_price": 632.99,
        "category": "Accessories", 
        "rating": 4.6, 
        "reviews": 2340, 
        "stock": 80,
        "badge": "Best Seller",
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&q=80",
        "description": "Aluminum laptop stand with 6 height angles, foldable design, and universal compatibility for 10-17 inch laptops.",
        "features": ["6 height settings", "Aluminum build", "Foldable portable", "10-17\" compatible"]
    },
]


def init_db():
    conn = get_db()
    
    try:
        conn.executescript(SCHEMA)

        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            for p in PRODUCTS:
                conn.execute(
                    """INSERT INTO products (name, price, original_price, category, rating, reviews, stock, badge, image, description, features) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (p["name"], p["price"], p.get("original_price"), p["category"], p["rating"], p["reviews"], p["stock"], p.get("badge"), p.get("image"), p.get("description"), json.dumps(p.get("features", []))) 
                )        
        conn.commit()  
    finally:
        conn.close()                           

def row_to_product(row):
    d = dict(row)
    try:
        d["features"] = json.loads(d.get("features") or "[]")
    except (json.JSONDecodeError, TypeError):
        d["features"] = []
    return d

def get_all_products(category=None, search=None, sort = "default", min_price=0, max_price=999999):
    conn = get_db()

    try:
        query = "SELECT * FROM products WHERE price BETWEEN ? AND ?"
        params = [min_price, max_price]

        if category and category != "All":
            query += " AND category = ?"
            params.append(category)

        if search:
            query += " AND (LOWER(name) LIKE ? OR LOWER(category) LIKE ?)"
            params += [f"%{search.lower()}%", f"%{search.lower()}%"]

        sort_map = {
            "price_asc": "price ASC",
            "price_desc": "price DESC",
            "rating": "rating DESC",
            "name": "name ASC",
        }

        query += f" ORDER BY {sort_map.get(sort, 'id ASC')}"

        rows = conn.execute(query, params).fetchall()
        return [row_to_product(r) for r in rows]

    finally:
        conn.close()

def get_product(product_id):
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        return row_to_product(row) if row else None
    finally:
        conn.close()

def get_related_products(product_id, category, limit=4):
    conn = get_db()
    try:
        rows = conn.execute("SELECT * FROM products WHERE category = ? AND id != ? LIMIT ?",(category, product_id, limit)).fetchall()

        return [row_to_product(r) for r in rows]
    finally:
        conn.close()

def create_user(name, email, password):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", (name, email, generate_password_hash(password))
        )
        conn.commit()
        return get_user_by_email(email)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db()

    try:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = get_db()

    try:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None

def create_order(user_id, name, address, city, items, subtotal, shipping, tax, total):
    conn = get_db()

    try:
        count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

        order_ref = f"ORD-{1001 + count}"

        cur = conn.execute(
            """INSERT INTO orders (user_id, order_ref, name, address, city, subtotal, shipping, tax, total, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (user_id, order_ref, name, address, city, subtotal, shipping, tax, total, "Processing")
        )
        order_id = cur.lastrowid

        for item in items:
            conn.execute(
                """INSERT INTO order_items (order_id, product_id, name, price, qty, subtotal) VALUES (?, ?, ?, ?, ?, ?)""", (order_id, item.get("id"), item["name"], item["price"], item["qty"], item["subtotal"])
            )
        conn.commit()
        return get_order(order_id)
    finally:
        conn.close()

def get_order(order_id):
    conn = get_db()
    try:
        order = conn.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if not order:
            return None
        order = dict(order)
        order["items"] = [dict(r) for r in conn.execute(
            "SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()]
        return order
    finally:
        conn.close()

def get_orders_by_user(user_id):
    conn = get_db()
    try:
        orders = conn.execute(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",(user_id,)).fetchall()

        result = []
        for o in orders:
            od = dict(o)
            od["items"] = [dict(r) for r in conn.execute(
            "SELECT * FROM order_items WHERE order_id = ?", (o["id"],)).fetchall()]
            result.append(od)
        return result
    finally:
        conn.close()


def get_wishlist(user_id):
    conn = get_db()
    try:
        rows = conn.execute(
            """SELECT p.* FROM products p JOIN wishlist w ON p.id = w.product_id WHERE w.user_id = ?""", (user_id,)).fetchall()
        return [row_to_product(r) for r in rows]
    finally:
        conn.close()


def db_toggle_wishlist(user_id, product_id):
    conn = get_db()

    try:
        exists = conn.execute(
            "SELECT 1 FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id)
        ).fetchone()
        if exists:
            conn.execute(
                "DELETE FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id)
            )
            conn.commit()
            return False
        else:
            conn.execute(
                "INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)", (user_id, product_id)
            )
            conn.commit()
            return True
    finally:
        conn.close()

def is_in_wishlist(user_id, product_id):
    conn = get_db()

    try:
        return bool(conn.execute(
            "SELECT 1 FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id)).fetchone())
    finally:
        conn.close()

def get_wishlist_ids(user_id):
    conn = get_db()

    try:
        rows = conn.execute(
            "SELECT product_id FROM wishlist WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [r["product_id"] for r in rows]
    finally:
        conn.close()
