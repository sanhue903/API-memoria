from app.application import bp as app
from app.extensions import db
from app.models import Application, Chapter, Question, User
from app.schemas import PostAppSchema
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask import jsonify, request

@app.route('/register', methods=['POST'])
@jwt_required(locations=['headers'])
def app_aplication():
    user = db.session.scalar(db.select(User).where(User.id == get_jwt_identity()))
    
    if not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    schema = PostAppSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    app = Application(validated_data['id'], validated_data['name'])
    db.session.add(app)

    for chapter in validated_data['chapters']:
        new_chapter = Chapter(id=chapter['id'], app_id=app.id, number=chapter['number'], name=chapter['name'])
        db.session.add(new_chapter)
        
        for question in chapter['questions']:
            new_question = Question(id=question['id'], chapter_id=new_chapter.id, number=question['number'], text=question['text'])
            db.session.add(new_question)
            
    db.session.commit()
    
    access_token = create_access_token(identity=app.id, expires_delta=False)
    
    response = jsonify({'token': access_token}), 201
    return response

@app.route('/<app_id>', methods=['GET'])
@jwt_required(locations=['headers'])
def get_application(app_id):
    user = db.session.scalar(db.select(User).where(User.id == get_jwt_identity()))
    
    if not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    app = db.session.scalar(db.select(Application).where(Application.id == app_id))
    
    if app is None:
        return jsonify({'message': f'Application with id {app_id} not found'}), 404
    
    #access_token = create_access_token(identity=app.id, expires_delta=False)
    
    #return jsonify({'token': access_token}), 200

    json = {
        'id': app.id,
        'name': app.name,
        'chapter_count': len(app.chapters),
        'chapters': [{
            'id': chapter.id,
            'number': chapter.number,
            'name': chapter.name,
            'question_count': len(chapter.questions),
            'questions': [{
                'id': question.id,
                'number': question.number,
                'text': question.text
            } for question in chapter.questions]
            } for chapter in app.chapters]
    }

    return jsonify(json), 200