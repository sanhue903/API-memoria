from app.extensions import db
from app.student import bp as app
from app.models import Student, Application, User

from app.schemas import StudentSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import jsonify, request

@app.route('',methods=['GET'])
@jwt_required(locations=['headers'])
def get_students_from_app(app_id: str):
    app = db.session.scalar(db.select(Application).where(Application.id == app_id))
    if app is None:
        return jsonify({'message': f'App with id {app_id} not found'}), 404
    
    #cambiar id int por algo más seguro
    user_id = get_jwt_identity()
    
    try:
        user = db.session.scalar(db.select(User).where(User.id == user_id))
    except Exception as e:
        return jsonify({'message': 'invalid type'}), 400

    if user is None:
        return jsonify({'message': 'Unauthorized'}), 403
    
    #pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    
    #filters
    age_equal = request.args.get('age', None, type=int)
    age_low_bound = request.args.get('age[gte]', None, type=int)
    age_high_bound = request.args.get('age[lte]', None, type=int)
    
    query = db.select(Student).where(Student.app_id == app_id)
    
    if age_equal is not None:
        query = query.where(Student.age == age_equal)    
    
    if age_low_bound is not None:
        query = query.where(Student.age >= age_low_bound)
        
    if age_high_bound is not None:
        query = query.where(Student.age <= age_high_bound)
         

    if limit is None:
        students = db.session.scalars(query).all()
    else:
        students = db.paginate(query, page=page, per_page=limit,max_per_page=None, error_out=False).items
    
    schema = StudentSchema(many=True)

    return jsonify({'students': schema.dump(students)}), 200
  
@app.route('',methods=['POST'])    
@jwt_required(locations=['headers'])
def post_student(app_id: str):
    if get_jwt_identity() != app_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    app = db.session.scalar(db.select(Application).where(Application.id == app_id))
    if app is None:
        return jsonify({'message': f'App with id {app_id} not found'}), 404
    
    schema = StudentSchema()

    data = request.get_json()
    data['app_id'] = app_id
    
    try:
        validated_data: Student = schema.load(data)
    except ValidationError as err:
        print(err.messages)
        return jsonify(err.messages), 422
    
    db.session.add(validated_data)
    db. session.commit()

    return jsonify({'student': schema.dump(validated_data)}), 201