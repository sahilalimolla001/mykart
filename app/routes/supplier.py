from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import Product, Order
from app.routes.auth import supplier_required, get_current_user

supplier_bp = Blueprint("supplier", __name__)


@supplier_bp.route("/supplier/products", methods=["GET"])
@jwt_required()
def supplier_products():
    if not supplier_required():
        return jsonify({"msg": "Supplier only"}), 403

    user = get_current_user()

    products = Product.query.filter_by(supplier_id=user.id).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "image_url": p.image_url,
            "status": p.status
        }
        for p in products
    ])


@supplier_bp.route("/supplier/orders", methods=["GET"])
@jwt_required()
def supplier_orders():
    if not supplier_required():
        return jsonify({"msg": "Supplier only"}), 403

    user = get_current_user()

    products = Product.query.filter_by(supplier_id=user.id).all()
    product_ids = [p.id for p in products]

    orders = Order.query.filter(Order.product_id.in_(product_ids)).all()

    return jsonify([
        {
            "order_id": o.id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "total_price": o.total_price,
            "status": o.status
        }
        for o in orders
    ])


@supplier_bp.route("/supplier/update-stock/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_stock(product_id):
    if not supplier_required():
        return jsonify({"msg": "Supplier only"}), 403

    user = get_current_user()
    data = request.get_json()

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Product not found"}), 404

    if product.supplier_id != user.id:
        return jsonify({"msg": "You can update only your product"}), 403

    product.stock = data.get("stock", product.stock)
    db.session.commit()

    return jsonify({
        "msg": "Stock updated successfully",
        "stock": product.stock
    })


@supplier_bp.route("/supplier/delete-product/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_supplier_product(product_id):
    if not supplier_required():
        return jsonify({"msg": "Supplier only"}), 403

    user = get_current_user()
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Product not found"}), 404

    if product.supplier_id != user.id:
        return jsonify({"msg": "You can delete only your product"}), 403

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg": "Product deleted successfully"})