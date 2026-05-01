from app import create_app, db
import os
app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:123@localhost:5432/ecommerce_db"
)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()