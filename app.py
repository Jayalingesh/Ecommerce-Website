from flask import (Flask, render_template, request, redirect, url_for, session, jsonify, flash)

from database import(
    init_db, get_all_products, get_product, get_related_products, create_user, get_user_by_id, verify_user, create_order, get_order, get_orders_by_user, get_wishlist, db_toggle_wishlist, get_wishlist_ids, is_in_wishlist,
)

"""
import json
import os

"""

app = Flask(__name__)
app.secret_key = "ecommerce_secret_key_2026"



CATEGORIES = [
    "All", 
    "Electronics", 
    "Wearables", 
    "Furniture", 
    "Accessories", 
    "Smart Home"
]

# USERS = {} # email: {name, password, orders}

with app.app_context():
    init_db()


def get_current_user():
    uid = session.get("user_id")
    return get_user_by_id(uid) if uid else None

def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart

def cart_count():
    return sum(item["qty"] for item in get_cart().values())

def cart_total():
    cart = get_cart()
    total = 0.0
    for pid, item in cart.items():
        product = get_product(int(pid))

        if product:
            total += product["price"] * item["qty"]
    return round(total, 2)

""" def get_user():
    email = session.get("user_email")
    if email and email in USERS:
        return USERS[email]
    return None
"""

def build_cart_items():
    items = []
    for pid, item in get_cart().items():
        product = get_product(int(pid))
        if product:
            items.append({**product,
                          "qty": item["qty"],
                          "subtotal": round(product["price"] * item["qty"], 2)})
    return items



@app.route("/")
def index():
    featured = [p for p in get_all_products() if p.get("badge") in ("Best Seller", "Hot")][:4]

    new_arrivals = [p for p in get_all_products() if p.get("badge") == "New"][:3]

    return render_template("index.html",featured = featured, new_arrivals = new_arrivals, cart_count = cart_count(), user = get_current_user())


@app.route("/products")
def products():
    category = request.args.get("category", "All")
    sort = request.args.get("sort", "default")
    search = request.args.get("search", "").strip().lower()
    min_price = request.args.get("min_price", 0, type=float)
    max_price = request.args.get("max_price", 100000, type=float)

    filtered = get_all_products(
        category = category,
        search = search, 
        sort = sort,
        min_price = min_price,
        max_price = max_price
    )

    """
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
    """

    return render_template("products.html",
                           products=filtered,
                           categories=CATEGORIES,
                           selected_category=category,
                           selected_sort=sort,
                           search=search,
                           cart_count=cart_count(),
                           user=get_current_user())

@app.route("/product/<int:product_id>")
def product_details(product_id):

    """
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    """

    product = get_product(product_id)
    if not product:
        return redirect(url_for("products"))
    
    """
    related = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != product_id][:4]
    """

    related = get_related_products(product_id, product["category"])
    user = get_current_user()
    in_wish = is_in_wishlist(user["id"], product_id) if user else False

    in_cart = str(product_id) in get_cart()

    return render_template("product_details.html",
                           product=product,
                           related=related,
                           in_cart=in_cart,
                           in_wish = in_wish,
                           cart_count=cart_count(),
                           user=user)

@app.route("/cart")
def cart():
    # cart_data = get_cart()

    items = build_cart_items()

    """
    for pid, item in cart_data.items():
            product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
            if product:
                items.append({**product, "qty": item["qty"],
                                "subtotal": round(product["price"] * item["qty"], 2)})

    """


    return render_template("cart.html",
                           items=items,
                           total=cart_total(),
                           cart_count=cart_count(),
                           user=get_current_user())


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
    flash("Item added to cart!", "success")
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
    
    items = build_cart_items()
    subtotal = cart_total()
    shipping = 0.0 if subtotal >= 1000 else 100
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + shipping + tax, 2)

    """
    for pid, item in cart_data.items():
            product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
            if product:
                items.append({**product, "qty": item["qty"],
                              "subtotal": round(product["price"] * item["qty"], 2)})
    """

    if request.method == "POST":
        """
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
        """

        user = get_current_user()
        user_id = user["id"] if user else None
        name = request.form.get("name", "Guest")
        address = request.form.get("address", "")
        city = request.form.get("city", "")

        # email = session.get("user_email")

        order = create_order(
            user_id = user_id,
            name = name,
            address = address,
            city = city,
            items = items,
            subtotal = subtotal,
            shipping = shipping,
            tax = tax,
            total = total,
        )

        """
        if email and email in USERS:
                    USERS[email].setdefault("orders", []).append(order)
        """

        session["last_order_id"] = order["id"]
        session["cart"] = {}
        return redirect(url_for("order_success"))
    return render_template("checkout.html",
                           items=items,
                           subtotal=subtotal,
                           shipping=shipping,
                           tax=tax,
                           total=total,
                           cart_count=cart_count(),
                           user=get_current_user())


@app.route("/order/success")
def order_success():
    # order = session.get("last_order")

    order_id = session.get("last_order_id")
    if not order_id:
        return redirect(url_for("index"))

    order = get_order(order_id)
    if not order:
            return redirect(url_for("index"))
    
    return render_template("order_success.html",
                           order=order,
                           cart_count=cart_count(),
                           user=get_current_user())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password", "")
        user = verify_user(email, password)

        if user:
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['name'].split()[0]}!", "success")
            return redirect(url_for("index"))
        flash("Invalid email or password.", "error")
    return render_template("login.html",
                           cart_count = cart_count(),
                           user=get_current_user())

@app.route("/register", methods=["GET", "POST"])            
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        """
        if email in USERS:
                    flash("Email already registered.", "error")
                else:
                    USERS[email] = {"name": name, "email": email, "password": password, "orders": []}
                    session["user_email"] = email
                    flash("Account created successfully!", "success")
                    return redirect(url_for("index"))
        """

        if not name or not email or not password:
            flash("All fields are required.", "error")
        elif len(password) <8:
            flash("Password must be at least 8 characters.", "error")
        else:
            user = create_user(name, email, password)
            if user:
                session["user_id"] = user["id"]
                flash("Account created successfully!", "success")
                return redirect(url_for("index"))
            else:
                flash("Email already registered.", "error")        

    return render_template("register.html",
                           cart_count=cart_count(),
                           user=get_current_user())

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been signed out.", "success")
    return redirect(url_for("index"))

@app.route("/account")
def account():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    orders = get_orders_by_user(user["id"])
    return render_template("account.html",
                           user=user,
                           orders = orders,
                           cart_count=cart_count())

@app.route("/wishlist")
def wishlist():
    # wishlist_ids = session.get("wishlist", [])
    user = get_current_user()
    items = get_wishlist(user["id"]) if user else []
    return render_template("wishlist.html",
                           items=items,
                           cart_count=cart_count(),
                           user=get_current_user())

@app.route("/wishlist/toggle/<int:product_id>")
def toggle_wishlist(product_id):
    """
    wishlist = session.get("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    else:
        wishlist.append(product_id)
    session["wishlist"] = wishlist

    return redirect(request.referrer or url_for("wishlist"))
    """

    user = get_current_user()
    if not user:
        flash("Please sign in to use the wishlist.", "error")
        return redirect(url_for("login"))
    db_toggle_wishlist(user["id"], product_id)
    return redirect(request.referrer or url_for("wishlist"))


@app.route("/api/wishlist")
def api_wishlist():

    user = get_current_user()
    ids = get_wishlist_ids(user["id"]) if user else []
    return jsonify({"wishlist": ids})

if __name__ == "__main__":
    app.run(debug=True, port=5000)