from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Order, Product, Delivery
from app.routes.auth import get_current_user

order_bp = Blueprint("order", __name__)

@order_bp.route("/cancel-order/<int:order_id>", methods=["PUT"])
@jwt_required()
def cancel_order(order_id):
    user = get_current_user()

    order = Order.query.get(order_id)

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    if order.user_id != user.id:
        return jsonify({"msg": "You can cancel only your order"}), 403

    if order.status in ["shipped", "delivered"]:
        return jsonify({"msg": "Shipped or delivered order cannot be cancelled"}), 400

    if order.status == "cancelled":
        return jsonify({"msg": "Order already cancelled"}), 400

    product = Product.query.get(order.product_id)
    if product:
        product.stock += order.quantity

    order.status = "cancelled"
    db.session.commit()

    return jsonify({"msg": "Order cancelled successfully"})


@order_bp.route("/create-order", methods=["POST"])
@jwt_required()
def create_order():
    user = get_current_user()
    data = request.get_json()

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")

    if not product_id or not address or not city or not phone:
        return jsonify({"msg": "product_id, address, city, phone required"}), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Product not found"}), 404

    if product.status != "approved":
        return jsonify({"msg": "Product not approved"}), 400

    if product.stock < quantity:
        return jsonify({"msg": "Out of stock"}), 400

    total_price = product.price * quantity

    order = Order(
        user_id=user.id,
        product_id=product.id,
        quantity=quantity,
        total_price=total_price,
        status="pending"
    )

    product.stock -= quantity

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
    db.session.commit()

    return jsonify({
        "msg": "Order created successfully",
        "order_id": order.id,
        "total_price": total_price,
        "delivery_status": delivery.status
    }), 201


@order_bp.route("/my-orders", methods=["GET"])
@jwt_required()
def my_orders():
    user = get_current_user()

    orders = Order.query.filter_by(user_id=user.id).all()

    return jsonify([
        {
            "id": o.id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "total_price": o.total_price,
            "status": o.status
        }
        for o in orders
    ])