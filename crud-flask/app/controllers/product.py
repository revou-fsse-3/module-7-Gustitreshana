from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.connectors.mysql_connector import Session
from app.models.product import Product
from flask_login import login_required, current_user
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    response_data = dict()
    current_user = get_jwt_identity()
    
    try:
        session = Session()
        product_query = select(Product)
        
        if request.args.get('query') != None:
            search_query = request.args.get('query')
            product_query = product_query.where(or_(Product.name.like(f'%{search_query}%'), Product.description.like(f'%{search_query}%')))
            
        products = session.execute(product_query)
        products = products.scalars()
        response_data['products'] = products
        response_data['username'] = current_user
        
    except SQLAlchemyError as e:
        response_data['message'] = 'Error getting products: ' + str(e)
        
    finally:
        session.close()
        
    return render_template('products/product_home.html', response_data=response_data)

@product_routes.route('/products/<id>', methods=['GET'])
@jwt_required()
def get_product(id):
    response_data = dict()
    session = Session()
    
    try:
        product = session.query(Product).filter(Product.id == id).first()
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        response_data['product'] = product
        
    except SQLAlchemyError as e:
        response_data['message'] = 'Error getting product: ' + str(e)
        
    finally:
        session.close()
        
    return render_template('products/product_detail.html', response_data=response_data)

@product_routes.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.json
        new_product = Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            created_at=datetime.now()
        )

        with Session() as session:
            session.add(new_product)
            session.commit()

        return jsonify({'message': 'Product created successfully'}), 201
    
    except KeyError as e:
        return jsonify({'message': f'Missing key in JSON data: {str(e)}'}), 400
    
    except SQLAlchemyError as e:
        return jsonify({'message': 'Error creating product: ' + str(e)}), 500


@product_routes.route('/products/<id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    try:
        with Session() as session:
            product = session.query(Product).filter(Product.id == id).first()
            if not product:
                return jsonify({'message': 'Product not found'}), 404
            
            data = request.json
            # Use correct keys to access the data from the request JSON object
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.description = data.get('description', product.description)
            
            session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
    
    except SQLAlchemyError as e:
        return jsonify({'message': 'Error updating product: ' + str(e)}), 500


@product_routes.route('/products/<id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    session = Session()
    session.begin()
    
    try:
        product = session.query(Product).filter(Product.id == id).first()
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        session.delete(product)
        session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'message': 'Error deleting product: ' + str(e)}), 500
    
    finally:
        session.close()
