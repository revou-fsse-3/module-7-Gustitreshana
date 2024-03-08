from dotenv import load_dotenv
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.user import user_routes
from app.controllers.product import product_routes

load_dotenv()

app = Flask(__name__)

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
jwt = JWTManager(app)

# Register the blueprints
app.register_blueprint(user_routes)
app.register_blueprint(product_routes)

@app.route('/')
def my_app():
    return 'Hello World!'
