
import os
from datetime import datetime
from flask import Flask, render_template, send_from_directory, Blueprint, jsonify, request
import flask_cors

# Resolve absolute paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(BASE_DIR, 'build')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

app = Flask(
    __name__,
    static_folder=BUILD_DIR,
    static_url_path='',
    template_folder=BUILD_DIR
)

flask_cors.CORS(app)

api = Blueprint("api", __name__, url_prefix="/api")

# ----------------------------
# Mock In-Memory Data (Demo)
# ----------------------------
DB = {
    "customers": {
        "CUST001": {"name": "John David", "membership": "Golden"},
        "CUST002": {"name": "Jane Doe", "membership": "Standard"},
        "CUST003": {"name": "Leo Lee", "membership": "Silver"},
    },
    "shoes": {
        "SHOE001": {
            "name": "Classic Running Shoes",
            "brand": "ShoeHub",
            "image": "/images/Shoe 1.jfif",
            "base_price": 8999,
            "discount_percent": 10,
            "rating": 4.5,
            "colors": ["red", "white", "black"],
            "sizes": [7, 8, 9, 10],
            "materials": ["Breathable mesh", "EVA midsole"],
            "advantages": ["Lightweight", "Good ventilation", "Comfort fit"],
            "description": "Lightweight and comfortable shoes perfect for daily runs."
        },
        "SHOE002": {
            "name": "Urban Casual Sneakers",
            "brand": "ShoeHub",
            "image": "/images/Shoe 2.jfif",
            "base_price": 7999,
            "discount_percent": 15,
            "rating": 4.3,
            "colors": ["white", "black", "navy"],
            "sizes": [6, 7, 8, 9, 10],
            "materials": ["Canvas upper", "Rubber outsole"],
            "advantages": ["Stylish", "Durable", "Versatile"],
            "description": "Stylish sneakers ideal for casual everyday wear."
        },
        "SHOE003": {
            "name": "Professional Formal Shoes",
            "brand": "ShoeHub",
            "image": "/images/Shoe 3.jfif",
            "base_price": 12999,
            "discount_percent": 8,
            "rating": 4.6,
            "colors": ["black", "brown"],
            "sizes": [6, 7, 8, 9, 10, 11],
            "materials": ["Genuine leather", "Leather insole"],
            "advantages": ["Professional look", "Comfortable", "Premium material"],
            "description": "Elegant formal shoes for business and special occasions."
        },
        "SHOE004": {
            "name": "Athletic Sports Shoes",
            "brand": "ShoeHub",
            "image": "/images/Shoe 4.jfif",
            "base_price": 11999,
            "discount_percent": 12,
            "rating": 4.4,
            "colors": ["black", "white", "blue"],
            "sizes": [7, 8, 9, 10, 11],
            "materials": ["Synthetic mesh", "Cushioned sole"],
            "advantages": ["High performance", "Good support", "Breathable"],
            "description": "High-performance shoes designed for intense sports activities."
        },
        "SHOE005": {
            "name": "Comfort Walking Shoes",
            "brand": "ShoeHub",
            "image": "/images/Shoe 5.jfif",
            "base_price": 7499,
            "discount_percent": 5,
            "rating": 4.2,
            "colors": ["beige", "gray", "navy"],
            "sizes": [6, 7, 8, 9, 10, 11],
            "materials": ["Memory foam", "Breathable fabric"],
            "advantages": ["All-day comfort", "Ergonomic", "Lightweight"],
            "description": "Ergonomic design for all-day comfort and support."
        },
        "SHOE006": {
            "name": "Marathon Running Shoes",
            "brand": "ShoeHub",
            "image": "/images/Shoe 6.jfif",
            "base_price": 13999,
            "discount_percent": 18,
            "rating": 4.7,
            "colors": ["red", "white", "black"],
            "sizes": [7, 8, 9, 10, 11],
            "materials": ["Advanced foam", "Responsive sole"],
            "advantages": ["Long-distance comfort", "Excellent cushioning", "Lightweight"],
            "description": "Advanced cushioning for long-distance running performance."
        },
        "SHOE007": {
            "name": "Casual Slip-On Shoes",
            "brand": "ShoeHub",
            "image": "/images/Shoe 7.avif",
            "base_price": 5999,
            "discount_percent": 10,
            "rating": 4.0,
            "colors": ["black", "white", "gray"],
            "sizes": [6, 7, 8, 9, 10],
            "materials": ["Canvas", "Flexible sole"],
            "advantages": ["Easy to wear", "Casual style", "Convenient"],
            "description": "Easy-to-wear slip-on shoes for quick and convenient styling."
        },
        "SHOE008": {
            "name": "Casual Black Sneaker with Red Stripes",
            "brand": "ShoeHub",
            "image": "/images/Shoe 8.avif",
            "base_price": 8999,
            "discount_percent": 20,
            "rating": 4.1,
            "colors": ["black", "white"],
            "sizes": [6, 7, 8, 9, 10],
            "materials": ["Synthetic leather", "Rubber sole"],
            "advantages": ["Stylish design", "Comfortable", "Trendy"],
            "description": "Stylish sneakers ideal for casual everyday wear."
        },
        "SHOE009": {
            "name": "Limited Edition Shoe",
            "brand": "ShoeHub",
            "image": "/images/Shoe 9.jfif",
            "base_price": 14999,
            "discount_percent": 15,
            "rating": 4.8,
            "colors": ["gold", "silver", "black"],
            "sizes": [7, 8, 9, 10, 11],
            "materials": ["Premium leather", "Cushioned insole"],
            "advantages": ["Exclusive design", "Premium quality", "Collectible"],
            "description": "Limited edition shoe with premium materials and design."
        }
    },
    "inventory": {
        "SHOE001": {
            "red":    {7: True, 8: True, 9: True, 10: True},
            "white":  {7: True, 8: False, 9: True, 10: True},
            "black":  {7: True, 8: True, 9: True, 10: False}
        },
        "SHOE002": {
            "white":  {6: True, 7: True, 8: True, 9: True, 10: True},
            "black":  {6: True, 7: True, 8: False, 9: True, 10: True},
            "navy":   {6: False, 7: True, 8: True, 9: True, 10: True}
        },
        "SHOE003": {
            "black":  {6: True, 7: True, 8: True, 9: True, 10: True, 11: True},
            "brown":  {6: True, 7: True, 8: True, 9: False, 10: True, 11: True}
        },
        "SHOE004": {
            "black":  {7: True, 8: True, 9: True, 10: True, 11: True},
            "white":  {7: True, 8: True, 9: False, 10: True, 11: True},
            "blue":   {7: False, 8: True, 9: True, 10: True, 11: True}
        },
        "SHOE005": {
            "beige":  {6: True, 7: True, 8: True, 9: True, 10: True, 11: True},
            "gray":   {6: True, 7: True, 8: True, 9: True, 10: False, 11: True},
            "navy":   {6: True, 7: True, 8: True, 9: True, 10: True, 11: True}
        },
        "SHOE006": {
            "red":    {7: True, 8: True, 9: True, 10: True, 11: True},
            "white":  {7: True, 8: True, 9: True, 10: True, 11: False},
            "black":  {7: True, 8: False, 9: True, 10: True, 11: True}
        },
        "SHOE007": {
            "black":  {6: True, 7: True, 8: True, 9: True, 10: True},
            "white":  {6: True, 7: True, 8: True, 9: False, 10: True},
            "gray":   {6: True, 7: True, 8: True, 9: True, 10: True}
        },
        "SHOE008": {
            "black":  {6: True, 7: True, 8: True, 9: True, 10: True},
            "white":  {6: True, 7: False, 8: True, 9: True, 10: True}
        },
        "SHOE009": {
            "gold":   {7: True, 8: True, 9: False, 10: True, 11: True},
            "silver": {7: True, 8: True, 9: True, 10: True, 11: True},
            "black":  {7: True, 8: True, 9: True, 10: False, 11: True}
        }
    },
    "orders": {
        "ORD1001": {
            "customer_id": "CUST001",
            "shoe_id": "SHOE001",
            "size": 9,
            "color": "red",
            "status": "PLACED",
            "shipping_address": {
                "name": "John David",
                "line1": "123 Shoe Street",
                "line2": "Near City Mall",
                "city": "Greenwich",
                "state": "London",
                "pincode": "SE10 9NN",
                "phone": "+44 7911 123456"
            },
            "created_at": datetime.now().isoformat()
        }
    },
    "pending": {}
}

def price_after_discount(shoe):
    return round(shoe["base_price"] * (100 - shoe["discount_percent"]) / 100)

def is_golden_member(customer_id):
    cust = DB["customers"].get(customer_id)
    return cust and cust.get("membership", "").lower() == "golden"

def check_availability(shoe_id, color, size):
    inv = DB["inventory"].get(shoe_id, {})
    sizes = inv.get(color, {})
    return bool(sizes.get(size, False))

# ----------------------------
# Static/Image & SPA Routes
# ----------------------------
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    requested_path = os.path.join(BUILD_DIR, path) if path else None
    if path and os.path.isfile(requested_path):
        return send_from_directory(BUILD_DIR, path)
    return render_template('index.html')

# ----------------------------
# Basic sample API (existing)
# ----------------------------
@api.route('/simple-get', methods=['GET'])
def get_item():
    return jsonify({"name": 'Hai'})

# ----------------------------
# (1–4 Combined) Order Change Flow (Automatic)
# ----------------------------
@api.route('/order-change', methods=['POST'])
def order_change():
    """
    Automatically handles the complete color change flow in sequence:
    1. Validates membership & checks color availability
    2. Applies the color change if available
    3. Confirms shipping address with the new color
    
    Customer only provides: order_id and new_color
    The API automatically executes all three stages and returns final status.
    """
    data = request.get_json(force=True) or {}
    order_id = data.get("order_id")
    new_color = (data.get("new_color") or "").strip().lower()
    new_address = data.get("new_address")  # Optional: for address update during change

    # Validate inputs
    if not order_id:
        return jsonify({"ok": False, "error": "order_id is required"}), 400
    if not new_color:
        return jsonify({"ok": False, "error": "new_color is required"}), 400

    # Fetch order and shoe
    order = DB["orders"].get(order_id)
    if not order:
        return jsonify({"ok": False, "error": "Order not found"}), 404

    shoe = DB["shoes"].get(order["shoe_id"])
    if not shoe:
        return jsonify({"ok": False, "error": "Shoe not found for this order"}), 404

    # Stage 1: Check membership eligibility
    if not is_golden_member(order["customer_id"]):
        return jsonify({
            "ok": False,
            "error": "Only Golden Membership card holders can change the color after ordering.",
            "customer_id": order["customer_id"],
            "membership": DB["customers"].get(order["customer_id"], {}).get("membership", "Unknown")
        }), 403

    # Stage 2: Check color availability
    if new_color not in shoe["colors"]:
        return jsonify({
            "ok": False,
            "error": f"Color '{new_color}' is not available for this shoe",
            "available_colors": shoe["colors"]
        }), 400

    if not check_availability(order["shoe_id"], new_color, order["size"]):
        return jsonify({
            "ok": False,
            "error": f"{new_color} not available in size {order['size']}",
            "requested_size": order["size"],
            "requested_color": new_color
        }), 409

    # Stage 3: Apply the color change
    old_color = order["color"]
    order["color"] = new_color

    # Stage 4: Handle shipping address
    current_address = order["shipping_address"]
    if new_address and isinstance(new_address, dict):
        # Update with new address if provided
        order["shipping_address"] = new_address
        address_status = "updated"
        final_address = new_address
    else:
        # Keep existing address
        address_status = "confirmed"
        final_address = current_address

    # Return complete success response
    message = (
        f"Color change completed successfully!\n"
        f"Order ID: {order_id}\n"
        f"Shoe: {shoe['name']}\n"
        f"Color changed from {old_color} to {new_color}\n"
        f"Size: {order['size']}\n"
        f"Shipping address {address_status}:\n"
        f"{final_address['name']}, {final_address['line1']}, {final_address['line2']}, "
        f"{final_address['city']}, {final_address['state']} - {final_address['pincode']}, "
        f"{final_address['phone']}"
    )

    return jsonify({
        "ok": True,
        "order_id": order_id,
        "shoe_id": order["shoe_id"],
        "shoe_name": shoe["name"],
        "old_color": old_color,
        "new_color": new_color,
        "size": order["size"],
        "address_status": address_status,
        "shipping_address": final_address,
        "message": message
    })

# ----------------------------
# (5 single) Direct Address Update
# ----------------------------
@api.route('/address-update', methods=['POST'])
def address_update_direct():
    data = request.get_json(force=True) or {}
    order_id = data.get("order_id")
    new_address = data.get("new_address")
    if not order_id or not new_address:
        return jsonify({"ok": False, "error": "order_id and new_address are required"}), 400
    order = DB["orders"].get(order_id)
    if not order:
        return jsonify({"ok": False, "error": "Order not found"}), 404
    order["shipping_address"] = new_address
    return jsonify({
        "ok": True,
        "order_id": order_id,
        "message": "Shipping address changed successfully.",
        "new_address": new_address
    })

# ----------------------------
# (6 single) Shoes Search
# ----------------------------
@api.route('/shoes/search', methods=['GET'])
def search_shoes():
    query = (request.args.get('query') or "").strip().lower()
    if not query:
        return jsonify({"ok": False, "error": "query parameter is required"}), 400
    results = []
    for shoe_id, shoe in DB["shoes"].items():
        if query in shoe["name"].lower() or query in shoe["brand"].lower():
            results.append({"shoe_id": shoe_id, **shoe})
    return jsonify({"ok": True, "results": results})

# ----------------------------
# (7 single) Shoe Details
# ----------------------------
@api.route('/shoes/<shoe_id>', methods=['GET'])
def shoe_details(shoe_id):
    shoe = DB["shoes"].get(shoe_id)
    if not shoe:
        return jsonify({"ok": False, "error": "Shoe not found"}), 404
    
    # Get base price in USD (convert from INR by dividing by ~83)
    base_price_usd = round(shoe["base_price"] / 83, 2)
    discounted_price_usd = round(base_price_usd * (100 - shoe["discount_percent"]) / 100, 2)
    
    # Return shoe details without image
    return jsonify({
        "ok": True,
        "shoe_id": shoe_id,
        "name": shoe["name"],
        "brand": shoe["brand"],
        "description": shoe["description"],
        "materials": shoe["materials"],
        "advantages": shoe["advantages"],
        "colors": shoe["colors"],
        "sizes": shoe["sizes"],
        "rating": shoe["rating"],
        "base_price": f"${base_price_usd:.2f}",
        "discount_percent": shoe["discount_percent"],
        "price_after_discount": f"${discounted_price_usd:.2f}"
    })

# ----------------------------
# (8 & 9 combined) Compare or Order
# ----------------------------
@api.route('/compare-or-order', methods=['POST'])
def compare_or_order():
    """
    Combines:
    - action='compare' : compare two shoes
    - action='order'   : create an order (COD)
    """
    data = request.get_json(force=True) or {}
    action = (data.get("action") or "").strip().lower()

    if action == "compare":
        a_id = data.get("shoe_id_a")
        b_id = data.get("shoe_id_b")
        if not a_id or not b_id:
            return jsonify({"ok": False, "error": "shoe_id_a and shoe_id_b are required"}), 400

        a = DB["shoes"].get(a_id)
        b = DB["shoes"].get(b_id)
        if not a or not b:
            return jsonify({"ok": False, "error": "Shoe ID(s) not found"}), 404

        a_price = price_after_discount(a)
        b_price = price_after_discount(b)
        price_benefit = {
            "cheaper_shoe": a_id if a_price < b_price else b_id if b_price < a_price else "equal",
            "difference": abs(a_price - b_price)
        }
        advantages = {
            "unique_to_a": [adv for adv in a["advantages"] if adv not in b["advantages"]],
            "unique_to_b": [adv for adv in b["advantages"] if adv not in a["advantages"]],
            "common": [adv for adv in a["advantages"] if adv in b["advantages"]]
        }
        return jsonify({
            "ok": True,
            "shoe_a": {
                "shoe_id": a_id, "name": a["name"], "price": a["base_price"],
                "discount_percent": a["discount_percent"], "price_after_discount": a_price,
                "rating": a["rating"], "advantages": a["advantages"]
            },
            "shoe_b": {
                "shoe_id": b_id, "name": b["name"], "price": b["base_price"],
                "discount_percent": b["discount_percent"], "price_after_discount": b_price,
                "rating": b["rating"], "advantages": b["advantages"]
            },
            "comparison": {
                "price_benefit": price_benefit,
                "rating_diff": round(a["rating"] - b["rating"], 2),
                "advantages": advantages
            }
        })

    elif action == "order":
        order_id = data.get("order_id")  # If provided, use existing order; else create new
        shoe_id = data.get("shoe_id")
        color = (data.get("color") or "").lower()
        size = data.get("size")
        shipping_address = data.get("shipping_address")
        payment_method = (data.get("payment_method") or "COD").upper()

        if not all([shoe_id, color, size, shipping_address]):
            return jsonify({"ok": False, "error": "shoe_id, color, size, shipping_address are required"}), 400
        if payment_method not in ["COD", "CARD"]:
            return jsonify({"ok": False, "error": "Payment method must be COD or CARD"}), 400

        shoe = DB["shoes"].get(shoe_id)
        if not shoe:
            return jsonify({"ok": False, "error": "Shoe not found"}), 404
        if color not in shoe["colors"]:
            return jsonify({"ok": False, "error": f"Color '{color}' is not available for this shoe"}), 400
        if size not in shoe["sizes"]:
            return jsonify({"ok": False, "error": f"Size '{size}' is not available for this shoe"}), 400
        if not check_availability(shoe_id, color, size):
            return jsonify({"ok": False, "error": f"{color} not available in size {size}"}), 409

        # If no order_id provided, create a new one
        if not order_id:
            next_id_num = 1000 + len(DB["orders"]) + 1
            order_id = f"ORD{next_id_num}"
        
        # Use CUST001 (Golden Member) by default for demo
        customer_id = data.get("customer_id", "CUST001")
        
        DB["orders"][order_id] = {
            "customer_id": customer_id,
            "shoe_id": shoe_id,
            "size": size,
            "color": color,
            "status": "PLACED",
            "shipping_address": shipping_address,
            "payment_method": payment_method,
            "created_at": datetime.now().isoformat()
        }

        message = (
            f"Order placed successfully with {payment_method}.\n"
            f"Order ID: {order_id}, Product: {shoe['name']}, Size: {size}, Color: {color}.\n"
            f"Payment Method: {payment_method}.\n"
            f"Shipping to: {shipping_address.get('name')}, {shipping_address.get('line1')}, {shipping_address.get('line2')}, "
            f"{shipping_address.get('city')}, {shipping_address.get('state')} - {shipping_address.get('pincode')}, "
            f"{shipping_address.get('phone')}."
        )
        return jsonify({"ok": True, "order_id": order_id, "message": message})

    else:
        return jsonify({"ok": False, "error": "Invalid or missing 'action'. Use compare|order"}), 400

# Register blueprint
app.register_blueprint(api)

if __name__ == '__main__':
    print("Server started on http://127.0.0.1:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)
