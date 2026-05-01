from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # user / admin / supplier
    role = db.Column(db.String(20), default="user")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))

    supplier_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    # pending / approved / rejected
    status = db.Column(db.String(30), default="pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float, default=0)

    # pending / confirmed / shipped / delivered / cancelled
    status = db.Column(db.String(30), default="pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)

    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    # not_assigned / assigned / out_for_delivery / delivered
    status = db.Column(db.String(50), default="not_assigned")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    quantity = db.Column(db.Integer, default=1)