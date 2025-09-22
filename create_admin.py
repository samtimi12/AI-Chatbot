from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin(username, email, password):
    app = create_app()  # ✅ create the app instance
    with app.app_context():
        db.create_all()
        # Check if email already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"User with email '{email}' already exists.")
            return

        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    create_admin(username, email, password)
