from flask import Flask 
from .models import db , User
from config import Config
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate 
from .product import product_blueprint
from .auth import auth_blueprint
app = Flask(__name__)


app.config.from_object(Config)




db.init_app(app)



 
migrate = Migrate(app,db)


jwt= JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity =jwt_data["sub"]
    return User.query.filter_by(id= identity).one_or_none()



app.register_blueprint(auth_blueprint)
app.register_blueprint(product_blueprint)
from . import models, routes
