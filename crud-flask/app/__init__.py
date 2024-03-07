from dotenv import load_dotenv
from flask import Flask
from app.controllers.user import user_routes
from app.controllers.product import product_routes
from app.models.user import User
from app.connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager

import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    return session.query(User).get(int(user_id))

app.register_blueprint(user_routes)
app.register_blueprint(product_routes)

@app.route('/')
def my_app():
    return 'Hello World!'

