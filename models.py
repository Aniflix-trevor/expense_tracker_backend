from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

naming_convention = {
    "ix": "ix_%(column_0_label)s",  
    "uq": "uq_%(table_name)s_%(column_0_name)s",  
    "ck": "ck_%(table_name)s_%(constraint_name)s",  
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  
    "pk": "pk_%(table_name)s", 
}

# this allows us to define tables and their columns
metadata = MetaData(naming_convention=naming_convention)

# create a db instance
db = SQLAlchemy(metadata=metadata)


class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=True
    )
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())

    # uselist = False -> this indicates a one relationship
    user = db.relationship("User", back_populates="categories", uselist=False)

    # it removes these fields
    serialize_rules = ("-user_id", "-user")


class Entry(db.Model, SerializerMixin):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    # type = db.Column(db.String(10), nullable=False, default="expense")  # "income" or "expense"
    # is_recurring = db.Column(db.Boolean, nullable=False, default=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="set null"),
        nullable=True,
    )

    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, onupdate=datetime.now)
    deleted_at = db.Column(db.TIMESTAMP)

    user = db.relationship("User", back_populates="entries", uselist=False)


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.VARCHAR, nullable=False, unique=True)
    password = db.Column(db.VARCHAR, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=datetime.now())

    # define relationships
    categories = db.relationship("Category", back_populates="user")
    entries = db.relationship("Entry", back_populates="user")

    serialize_rules = ("-password", "-categories", "-entries")
