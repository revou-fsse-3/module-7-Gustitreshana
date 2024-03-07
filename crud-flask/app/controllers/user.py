from flask import Blueprint, render_template, request, redirect
from app.models.user import User
from app.connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['GET'])
def get_users():
    return render_template('users/register.html')

@user_routes.route('/register', methods=['POST'])
def user_register():
    
    username = request.form['name']
    email = request.form['email']
    password = request.form['password']
    NewUser = User(username=username, email=email)
    NewUser.set_password(password)
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    session.begin()
    
    try:
        session.add(NewUser)
        session.commit()
        return {'message': 'User created successfully'}, 201
    
    except Exception as e:
        session.rollback()
        return {'message': 'Error creating user'}, 500
    
@user_routes.route('/login', methods=['GET'])
def get_login():
    return render_template('users/login.html')

@user_routes.route('/login', methods=['POST'])
def user_login():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    try:
       email = request.form['email']
       password = request.form['password']
       
       print("Email:", email)
       print("Password:", password)
       
       user = session.query(User).filter_by(email=email).first()
       print("User:", user)
       
       if user is None:
           print("User not found")
           return {'message': 'User not found'}, 404
       
       if not user.check_password(password):
           print("Invalid password")
           return {'message': 'Invalid password'}, 401
       
       login_user(user, remember=False)
       print("Login successful")
       return redirect('/products')
   
    except Exception as e:
       print("Error:", e)
       return {'message': 'Error logging in'}, 500
   
@user_routes.route('/logout', methods=['GET'])
def user_logout():
    logout_user()
    return redirect('/login')