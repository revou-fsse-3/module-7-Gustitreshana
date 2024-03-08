from flask import Blueprint, render_template, request, redirect, jsonify, url_for
from app.models.user import User
from app.connectors.mysql_connector import Session, engine
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, unset_jwt_cookies
import bcrypt
from sqlalchemy.exc import SQLAlchemyError

user_routes = Blueprint('user_routes', __name__)

# Session = sessionmaker(bind=engine)

@user_routes.route('/register', methods=['GET'])
def get_register_form():
    return render_template('users/register.html')

@user_routes.route('/register', methods=['POST'])
def user_register():
    session = None

    try:
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'message': 'Content-Type must be application/json'}), 415

        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'message': 'Incomplete data provided'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)

        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_user)
        session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except SQLAlchemyError as e:
        if session is not None:
            session.rollback()
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500
    
    finally:
        if session is not None:
            session.close()

@user_routes.route('/login', methods=['GET'])
def get_login():
    return render_template('users/login.html')
    
@user_routes.route('/login', methods=['POST'])
def user_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        session = Session()

        user = session.query(User).filter_by(email=email).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'message': 'Invalid password'}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'message': 'Database error'}), 500
    
    finally:
        session.close()
    
@user_routes.route('/logout', methods=['GET'])
@jwt_required()
def user_logout():
    unset_jwt_cookies()
    return jsonify({"message": "Successfully logged out"}), 200
