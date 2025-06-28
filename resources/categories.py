from flask_restful import Resource
from models import Category, db
from flask import request
from datetime import datetime

class CategoriesResource(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        query = Category.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        categories = query.all()
        result = []
        for category in categories:
            result.append({
                "id": category.id,
                "name": category.name,
                "user_id": category.user_id,
                "created_at": category.created_at.isoformat() if category.created_at else None,
            })
        return result, 200

    def post(self):
        data = request.get_json()
        name = data.get("name")
        user_id = data.get("user_id")

        if not name:
            return {"error": "Missing required field: name"}, 400

        category = Category(
            name=name,
            user_id=user_id,
            created_at=datetime.now()
        )
        db.session.add(category)
        db.session.commit()
        return {
            "id": category.id,
            "name": category.name,
            "user_id": category.user_id,
            "created_at": category.created_at.isoformat() if category.created_at else None,
        }, 201