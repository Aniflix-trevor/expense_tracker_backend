import os
from datetime import timedelta
from flask import Flask
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from config import DevelopmentConfig 

from models import db
from resources.users import SigninResource, LoginResource, UsersResource
from resources.categories import CategoriesResource
from resources.entries import EntriesResource

# load environment variables
load_dotenv()

app = Flask(__name__)

# setup cors
CORS(app, 
    origins=["https://frontendexpensetracker-production.up.railway.app"],
    supports_credentials=True
)

# setup flask-restful
api = Api(app)

# configure our app
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ECHO"] = True
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["BUNDLE_ERRORS"] = True
app.config.from_object(DevelopmentConfig)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

db.init_app(app)


class Index(Resource):
    def get(self):
        return {"message": "Welcome to the notted api"}


api.add_resource(Index, "/")
api.add_resource(SigninResource, "/signin")
api.add_resource(LoginResource, "/login")
api.add_resource(UsersResource, "/users")
api.add_resource(CategoriesResource, "/categories")
api.add_resource(EntriesResource, "/entries")

if __name__ == "__main__":
    app.run(port=5555)
