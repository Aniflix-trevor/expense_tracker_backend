from app import app, db
from models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    # Replace these values with your desired user info
    full_name = "Test User"
    email = "test@example.com"
    password = "password123"

    # full_name = "Jeff Bezos"
    # email = "jeff@bezos.com"
    # password = "password123"

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create the user
    user = User(full_name=full_name, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    print(f"User {email} added!")