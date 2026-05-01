from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from sqlalchemy.engine import URL
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password="sahil@123",   # अपना postgres password
            host="localhost",
            port=5432,
            database="ecommerce_db"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False





    db.init_app(app)
    JWTManager(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.product import product_bp
    app.register_blueprint(product_bp)

    from app.routes.order import order_bp
    app.register_blueprint(order_bp)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.supplier import supplier_bp
    app.register_blueprint(supplier_bp)

    from app.routes.cart import cart_bp
    app.register_blueprint(cart_bp)




    return app

