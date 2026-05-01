from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, Product, Order
from app.routes.auth import admin_required

admin_bp = Blueprint("admin", __name__)

allowed_status = ["pending","confirmed","shipped","out_for_delivery","delivered","cancelled"]


@admin_bp.route("/admin/users", methods=["GET"])
@jwt_required()
def get_users():
    if not admin_required():
        return jsonify({"msg": "Admin only"}), 403

    users = User.query.all()

    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "role": u.role
        }
        for u in users
    ])


@admin_bp.route("/admin/products", methods=["GET"])
@jwt_required()
def get_all_products():
    if not admin_required():
        return jsonify({"msg": "Admin only"}), 403

    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "image_url": p.image_url,
            "supplier_id": p.supplier_id,
            "status": p.status
        }
        for p in products
    ])


@admin_bp.route("/admin/approve-product/<int:product_id>", methods=["PUT"])
@jwt_required()
def approve_product(product_id):
    if not admin_required():
        return jsonify({"msg": "Admin only"}), 403

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Product not found"}), 404

    product.status = "approved"
    db.session.commit()

    return jsonify({"msg": "Product approved successfully"})


@admin_bp.route("/admin/reject-product/<int:product_id>", methods=["PUT"])
@jwt_required()
def reject_product(product_id):
    if not admin_required():
        return jsonify({"msg": "Admin only"}), 403

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Product not found"}), 404

    product.status = "rejected"
    db.session.commit()

    return jsonify({"msg": "Product rejected successfully"})


@admin_bp.route("/admin/orders", methods=["GET"])
@jwt_required()
def get_all_orders():
    if not admin_required():
        return jsonify({"msg": "Admin only"}), 403

    orders = Order.query.all()

    return jsonify([
        {
            "id": o.id,
            "user_id": o.user_id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "total_price": o.total_price,
            "status": o.status
        }
        for o in orders
    ])


@admin_bp.route("/admin/update-order-status/<int:order_id>", methods=["PUT"])
@jwt_required()
def update_order_status(order_id):
    if not admin_required():
        return jsonify({"msg": "Admin only"}), 403

    data = request.get_json()
    status = data.get("status")

    allowed_status = ["pending", "confirmed", "shipped", "delivered", "cancelled"]

    if status not in allowed_status:
        return jsonify({"msg": "Invalid status"}), 400

    order = Order.query.get(order_id)

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    order.status = status
    db.session.commit()

    return jsonify({
        "msg": "Order status updated successfully",
        "status": status
    })