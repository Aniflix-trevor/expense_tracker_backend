from flask_restful import Resource
from models import Entry, db
from flask import request
from datetime import datetime

class EntriesResource(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        query = Entry.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        entries = query.all()
        result = []
        for entry in entries:
            result.append({
                "id": entry.id,
                "note": entry.note,
                "amount": float(entry.amount),
                "type": entry.type,
                "is_recurring": entry.is_recurring,
                "user_id": entry.user_id,
                "category_id": entry.category_id,
                "created_at": entry.created_at.isoformat() if entry.created_at else None,
                "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
                "deleted_at": entry.deleted_at.isoformat() if entry.deleted_at else None,
            })
        return result, 200

    def post(self):
        data = request.get_json()
        note = data.get("note")
        amount = data.get("amount")
        type_ = data.get("type", "expense")
        is_recurring = data.get("is_recurring", False)
        user_id = data.get("user_id")
        category_id = data.get("category_id")

        if not note or amount is None or not user_id:
            return {"error": "Missing required fields"}, 400

        entry = Entry(
            note=note,
            amount=amount,
            type=type_,
            is_recurring=is_recurring,
            user_id=user_id,
            category_id=category_id,
            created_at=datetime.now()
        )
        db.session.add(entry)
        db.session.commit()
        return {
            "id": entry.id,
            "note": entry.note,
            "amount": float(entry.amount),
            "type": entry.type,
            "is_recurring": entry.is_recurring,
            "user_id": entry.user_id,
            "category_id": entry.category_id,
            "created_at": entry.created_at.isoformat() if entry.created_at else None,
            "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
            "deleted_at": entry.deleted_at.isoformat() if entry.deleted_at else None,
        }, 201