from flask import Blueprint, render_template, request, jsonify
from app.connectors.mysql_connector import Session
from app.models.product import Product
from flask_login import login_required, current_user
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products', methods=['GET'])
@login_required
def get_products():
    response_data = dict()
    session = Session()
    
    try:
        product_query = select(Product)
        
        if request.args.get('query') != None:
            search_query = request.args.get('query')
            product_query = product_query.where(or_(Product.name.like(f'%{search_query}%'), Product.description.like(f'%{search_query}%')))
            
        products = session.execute(product_query)
        products = products.scalars()
        response_data['products'] = products
        response_data['username'] = current_user.username
        
    except SQLAlchemyError as e:
        response_data['message'] = 'Error getting products: ' + str(e)
        
    return render_template('products/product_home.html', response_data=response_data)

@product_routes.route('/products/<id>', methods=['GET'])
@login_required
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
        
    return render_template('products/product_detail.html', response_data=response_data)

@product_routes.route('/products', methods=['POST'])
@login_required
def create_product():
    session = Session()
    session.begin()
    
    try:
        new_product = Product(
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description']
        )
        
        session.add(new_product)
        session.commit()
        return jsonify({'message': 'Product created successfully'}), 201
    
    except (KeyError, SQLAlchemyError) as e:
        session.rollback()
        return jsonify({'message': 'Error creating product: ' + str(e)}), 500

@product_routes.route('/products/<id>', methods=['PUT'])
@login_required
def update_product(id):
    session = Session()
    session.begin()
    
    try:
        product = session.query(Product).filter(Product.id == id).first()
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        product.name = request.form['productName']
        product.price = request.form['productPrice']
        product.description = request.form['productDescription']
        
        session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200
    
    except (KeyError, SQLAlchemyError) as e:
        session.rollback()
        return jsonify({'message': 'Error updating product: ' + str(e)}), 500

@product_routes.route('/products/<id>', methods=['DELETE'])
@login_required
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
