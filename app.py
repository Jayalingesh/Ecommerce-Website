from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json
import os

app = Flask(__name__)
app.secret_key = "ecommerce_secret_key_2026"

PRODUCTS = [
    {"id": 1,"name": "Wireless Noise-Cancelling Headphones", "price": 2392.99, "original_price": 3192.99, "category": "Electronics", "rating": 4.8, "reviws": 1240, "stock": 15, "badge": "Best Seller", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80", "description": "Premium wireless headphones with 40-hour battery life, active noise cancellation, and studio-quality sound. Foldable design with carrying case included.", "features": ["40-hour battery", "Active Noise Cancellation", "Bluetooth 5.0", "Fast charge (10min = 3hrs)"]},

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

CATEGORIES = [
    "All", 
    "Electronics", 
    "Wearables", 
    "Furniture", 
    "Accessories", 
    "Smart Home"
]

USERS = {} # email: {name, password, orders}

def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart

def cart_count():
    return sum(item["qty"] for item in get_cart().values())

def cart_total():
    cart = get_cart()
    total = 0
    for pid, item in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            total += product["price"] * item["qty"]
    return round(total, 2)

def get_user():
    email = session.get("user_email")
    if email and email in USERS:
        return USERS[email]
    return None

@app.route("/")
def index():
    featured = [p for p in PRODUCTS if p.get("badge") in ["Best Seller", "Hot"]][:4]

    new_arrivals = [p for p in PRODUCTS if p.get("badge") == "New"][:3]

    return render_template("index.html",
    featured = featured,new_arrivals = new_arrivals, cart_count = cart_count(), user = get_user())


@app.route("/products")
def products():
    category = request.args.get("category", "All")
    sort = request.args.get("sort", "default")
    search = request.args.get("search", "").strip().lower()
    min_price = request.args.get("min_price", 0, type=float)
    max_price = request.args.get("max_price", 10000, type=float)

    filtered = PRODUCTS[:]

    if search:
        filtered = [p for p in filtered if search in p["name"].lower() or search in p["category"].lower()]

    if category != "All":
        filtered = [p for p in filtered if p["category"] == category]
        
    filtered = [p for p in filtered if min_price <= p["price"] <= max_price]

    if sort == "price_asc":
        filtered.sort(key=lambda x: x["price"])
    elif sort == "price_desc":
        filtered.sort(key=lambda x: x["price"], reverse = True)
    elif sort == "rating":
        filtered.sort(key=lambda x: x["rating"], reverse =True)
    elif sort == "name":
        filtered.sort(key=lambda x: x["name"])

    return render_template("products.html",
                           products=filtered,
                           categories=CATEGORIES,
                           selected_category=category,
                           selected_sort=sort,
                           search=search,
                           cart_count=cart_count(),
                           user=get_user())

@app.route("/product/<int:product_id>")
def product_details(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return redirect(url_for("products"))
    related = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != product_id][:4]

    in_cart = str(product_id) in get_cart()
    return render_template("product_details.html",
                           product=product,
                           related=related,
                           in_cart=in_cart,
                           cart_count=cart_count(),
                           user=get_user())

@app.route("/cart")
def cart():
    cart_data = get_cart()
    items =[]
    for pid, item in cart_data.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            items.append({**product, "qty": item["qty"],
                          "subtotal": round(product["price"] * item["qty"], 2)})
    return render_template("cart.html",
                           items=items,
                           total=cart_total(),
                           cart_count=cart_count(),
                           user=get_user())

@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    qty = int(request.form.get("qty", 1))
    cart = get_cart()
    pid = str(product_id)
    if pid in cart:
        cart[pid]["qty"] += qty
    else:
        cart[pid] = {"qty": qty}
    save_cart(cart)
    flash(f"Item added to cart!", "success")
    return redirect(request.referrer or url_for("cart"))

@app.route("/cart/update", methods=["POST"])
def update_cart():
    pid = request.form.get("product_id")
    qty = int(request.form.get("qty", 1))
    cart = get_cart()
    if pid in cart:
        if qty <= 0:
            del cart[pid]
        else:
            cart[pid]["qty"] = qty
    save_cart(cart)
    return redirect(url_for("cart"))

@app.route("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)
    return redirect(url_for("cart"))

@app.route("/api/cart/count")
def api_cart_count():
    return jsonify({"count": cart_count()})

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not get_cart():
        return redirect(url_for("cart"))
    cart_data = get_cart()
    items = []
    for pid, item in cart_data.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            items.append({**product, "qty": item["qty"],
                          "subtotal": round(product["price"] * item["qty"], 2)})

    subtotal = cart_total()
    shipping = 0 if subtotal >= 100 else 9.99
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + shipping +tax, 2)

    if request.method == "POST":
        order = {
            "id": f"ORD-{len(USERS.get(session.get('user_email', ''), {}).get('orders', [])) + 1001}",
            "items": items,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "name": request.form.get("name"),
            "address": request.form.get("city"),
            "status": "Processing"
        }
        email = session.get("user_email")
        if email and email in USERS:
            USERS[email].setdefault("orders", []).append(order)

        session["last_order"] = order
        session["cart"] = {}
        return redirect(url_for("order_success"))
    return render_template("checkout.html",
                           items=items,
                           subtotal=subtotal,
                           shipping=shipping,
                           tax=tax,
                           total=total,
                           cart_count=cart_count(),
                           user=get_user())

@app.route("/order/success")
def order_success():
    order = session.get("last_order")
    if not order:
        return redirect(url_for("index"))
    return render_template("order_success.html",
                           order=order,
                           cart_count=cart_count(),
                           user=get_user())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = USERS.get(email)
        if user and user["password"] == password:
            session["user_email"] = email
            flash("Welcome back!", "success")
            return redirect(url_for("index"))
        flash("Invalid email or password.", "error")
    return render_template("login.html", cart_count=cart_count(), user=get_user())

@app.route("/register", methods=["GET", "POST"])            
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if email in USERS:
            flash("Email already registered.", "error")
        else:
            USERS[email] = {"name": name, "email": email, "password": password, "orders": []}
            session["user_email"] = email
            flash("Account created successfully!", "success")
            return redirect(url_for("index"))
    return render_template("register.html", cart_count=cart_count(), user=get_user())

@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect(url_for("index"))

@app.route("/account")
def account():
    user = get_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("account.html",
                           user=user,
                           cart_count=cart_count())

@app.route("/wishlist")
def wishlist():
    wishlist_ids = session.get("wishlist", [])
    items = [p for p in PRODUCTS if p["id"] in wishlist_ids]
    return render_template("wishlist.html",
                           items=items,
                           cart_count=cart_count(),
                           user=get_user())

@app.route("/wishlist/toggle/<int:product_id>")
def toggle_wishlist(product_id):
    wishlist = session.get("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    else:
        wishlist.append(product_id)
    session["wishlist"] = wishlist
    return redirect(request.referrer or url_for("wishlist"))

@app.route("/api/wishlist")
def api_wishlist():
    return jsonify({"wishlist": session.get("wishlist", [])})

if __name__ == "__main__":
    app.run(debug=True, port=5000)