import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')  # Use env var in production!
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///expense_tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = 86400  # 24 hours in seconds (if you want to use later)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-very-secret-key')  # Add this line

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False