from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from flask import render_template
from flask import Blueprint, request, jsonify, render_template



auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    if role not in ["user", "admin", "supplier"]:
        return jsonify({"msg": "Invalid role"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(
        username=username,
        password=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        return jsonify({"msg": "Wrong password"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "msg": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role
    })


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def admin_required():
    user = get_current_user()
    return user and user.role == "admin"


def supplier_required():
    user = get_current_user()
    return user and user.role == "supplier"

@auth_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@auth_bp.route("/")
def home_page():
    return render_template("index.html")

@auth_bp.route("/page/products")
def products_page():
    return render_template("products.html")

@auth_bp.route("/page/cart")
def cart_page():
    return render_template("cart.html")

@auth_bp.route("/page/checkout")
def checkout_page():
    return render_template("checkout.html")

@auth_bp.route("/page/payment")
def payment_page():
    return render_template("payment.html")

@auth_bp.route("/page/login")
def login_page():
    return render_template("login.html")

@auth_bp.route("/page/admin")
def admin_page():
    return render_template("admin.html")

@auth_bp.route("/page/supplier")
def supplier_page():
    return render_template("supplier.html")

@auth_bp.route("/page/orders")
def orders_page():
    return render_template("orders.html")

@auth_bp.route("/page/admin-orders")
def admin_orders_page():
    return render_template("admin_orders.html")

@auth_bp.route("/page/product/<int:product_id>")
def product_details_page(product_id):
    return render_template("product_details.html")