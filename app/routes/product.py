from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Product
from app.routes.auth import get_current_user

product_bp = Blueprint("product", __name__)





@product_bp.route("/add-product", methods=["POST"])
@jwt_required()
def add_product():
    user = get_current_user()

    if not user or user.role not in ["admin", "supplier"]:
        return jsonify({"msg": "Admin or Supplier only"}), 403

    data = request.get_json()

    product = Product(
        name=data.get("name"),
        description=data.get("description"),
        price=data.get("price"),
        stock=data.get("stock", 0),
        image_url=data.get("image_url"),
        supplier_id=user.id,
        status="approved" if user.role == "admin" else "pending"
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "msg": "Product added successfully",
        "product_id": product.id,
        "status": product.status
    }), 201

@product_bp.route("/products", methods=["GET"])
def get_products():
    search = request.args.get("search", "")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    sort = request.args.get("sort")

    query = Product.query.filter_by(status="approved")

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if min_price:
        query = query.filter(Product.price >= float(min_price))

    if max_price:
        query = query.filter(Product.price <= float(max_price))

    if sort == "low":
        query = query.order_by(Product.price.asc())
    elif sort == "high":
        query = query.order_by(Product.price.desc())

    products = query.all()

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