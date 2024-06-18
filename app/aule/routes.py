from app.aule import bp as app
from app.extensions import db
from app.models import Aule, Application
from app.schemas import AuleSchema
from flask_jwt_extended import jwt_required

from flask import request, jsonify, current_app

#TODO modificar todas las funciones

@jwt_required(locations=['cookies'])
@app.route('', methods=['GET'])
def get_aules(mobile_app_id):
    db.get_or_404(Application, mobile_app_id, description=f'MobileApp with id {mobile_app_id} not found')
    
    aules = db.session.scalars(db.select(Aule).where(Aule.mobile_app_id == mobile_app_id)).all()
    
    schema = AuleSchema(many=True)
    return jsonify({'aules': schema.dump(aules)}), 200
    
@jwt_required(locations=['cookies'])
@app.route('', methods=['POST'])
def post_aule(mobile_app_id):
    data = request.get_json()
    schema = AuleSchema()
    
    aule = schema.load(data)
    aule.mobile_app_id = mobile_app_id
    db.session.add(aule)
    db.session.commit()
    
    return schema.jsonify({'message': 'Aule created'}), 201

@app.route('/<aule_code>', methods=['GET'])
def get_aule(mobile_app_id, aule_code):
    aule_code = aule_code.upper()
    db.get_or_404(Application, mobile_app_id, description=f'MobileApp with id {mobile_app_id} not found')
    
    schema = AuleSchema()
    aule = db.session.scalar(db.select(Aule).where(Aule.code == aule_code))
    if aule is None:
        return jsonify({'message': f'Aule with code {aule_code} not found'}), 404
    
    
    return schema.jsonify({'aule': schema.dump(aule)}), 200
    
@jwt_required(locations=['cookies'])
@app.route('/<aule_id>', methods=['PUT'])       
def open_aule(mobile_app_id,aule_id):
    db.get_or_404(Application, mobile_app_id, description=f'MobileApp with id {mobile_app_id} not found')
    
    aule = db.get_or_404(Aule, aule_id, description=f'Aule with id {aule_id} not found')
    aule.generate_temporal_code()
    db.session.commit()
    
    aule.schedule_reset_code(current_app)
    
    return jsonify({'code': aule.code}), 201