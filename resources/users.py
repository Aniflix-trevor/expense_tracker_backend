# resources/users.py
from flask_restful import Resource
from flask import request
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

class SigninResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')

        if not email or not password or not full_name:
            return {"error": "Missing required fields"}, 400

        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 400

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, full_name=full_name, password=hashed)

        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id)
        return {"token": token, "message": "User created successfully"}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return {"error": "Invalid credentials"}, 401

        token = create_access_token(identity=user.id)
        return {"token": token}
    
class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        result = [
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
            for user in users
        ]
        return result, 200

