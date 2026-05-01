from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Cart, Product
from app.routes.auth import get_current_user

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user = get_current_user()
    data = request.get_json()

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Product not found"}), 404

    item = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()

    if item:
        item.quantity += quantity
    else:
        item = Cart(user_id=user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)

    db.session.commit()

    return jsonify({"msg": "Added to cart"})


@cart_bp.route("/cart", methods=["GET"])
@jwt_required()
def view_cart():
    user = get_current_user()

    items = Cart.query.filter_by(user_id=user.id).all()

    result = []
    total = 0

    for item in items:
        product = Product.query.get(item.product_id)

        if product:
            subtotal = product.price * item.quantity
            total += subtotal

            result.append({
                "cart_id": item.id,
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

    return jsonify({
        "items": result,
        "total": total
    })


@cart_bp.route("/cart/remove/<int:cart_id>", methods=["DELETE"])
@jwt_required()
def remove_cart_item(cart_id):
    user = get_current_user()

    item = Cart.query.get(cart_id)

    if not item:
        return jsonify({"msg": "Cart item not found"}), 404

    if item.user_id != user.id:
        return jsonify({"msg": "You can remove only your cart item"}), 403

    db.session.delete(item)
    db.session.commit()

    return jsonify({"msg": "Cart item removed"})

from app.models import Order, Delivery

@cart_bp.route("/cart/checkout", methods=["POST"])
@jwt_required()
def checkout():
    user = get_current_user()
    data = request.get_json()

    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")

    if not address or not city or not phone:
        return jsonify({"msg": "address, city, phone required"}), 400

    items = Cart.query.filter_by(user_id=user.id).all()

    if not items:
        return jsonify({"msg": "Cart is empty"}), 400

    orders_created = []
    total_amount = 0

    for item in items:
        product = Product.query.get(item.product_id)

        if not product or product.status != "approved":
            continue

        if product.stock < item.quantity:
            return jsonify({"msg": f"{product.name} out of stock"}), 400

        total_price = product.price * item.quantity
        total_amount += total_price

        order = Order(
            user_id=user.id,
            product_id=product.id,
            quantity=item.quantity,
            total_price=total_price,
            status="pending"
        )

        product.stock -= item.quantity

        db.session.add(order)
        db.session.flush()

        delivery = Delivery(
            order_id=order.id,
            address=address,
            city=city,
            phone=phone,
            status="not_assigned"
        )

        db.session.add(delivery)

        orders_created.append(order.id)

    # clear cart
    Cart.query.filter_by(user_id=user.id).delete()

    db.session.commit()

    return jsonify({
        "msg": "Checkout successful",
        "orders": orders_created,
        "total_amount": total_amount
    })