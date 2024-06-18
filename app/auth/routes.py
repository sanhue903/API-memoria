from app.auth import bp as app
from app.extensions import db
from app.models import User
from app.schemas import LoginSchema, SignUpSchema
from marshmallow import ValidationError
from datetime import timedelta
from flask_jwt_extended import create_access_token, set_access_cookies

from flask import jsonify, request

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = LoginSchema()
    
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    user = db.session.scalar(db.select(User).where(User.email == validated_data['email']))
    if user is None:
        return jsonify({'message': 'User not found'}), 404
   
    if not user.check_password(validated_data['password']):
        return jsonify({'message': 'Wrong password'}), 401
    
    access_token = create_access_token(identity=user.id,expires_delta=timedelta(days=365))
    
    response = jsonify({'token': access_token}), 201
    
    return response 
    

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    schema = SignUpSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    if db.session.scalar(db.select(User).where(User.email == validated_data['email'])) is not None:
        return jsonify({'message': 'this email adress has already been registered'}), 409
    
    
    if validated_data['password'] != validated_data['confirm_password']:
        return jsonify({'message': 'Passwords do not match'}), 400
    
    validated_data.pop('confirm_password')
    
    user = create_user(validated_data) 
    create_admin(user)
    
    return jsonify({'message': f'User {user.email} created'}), 201


def create_user(data):
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    
    return new_user

def create_admin(user):
    if db.session.scalar(db.select(User).where(User.is_admin == True)) is not None:
        return 
    
    user.is_admin = True
    db.session.commit()