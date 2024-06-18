from app.extensions import db
from app.score import bp as app
from app.models import Student, Score, Application, Chapter, Question, User
from app.schemas import PostScoreSchema, GetScoreSchema, ScoreSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Any

from flask import jsonify, request

def parse_json1(scores, app, chapter, question) -> Any:
    results = []
    for chapter_it in app.chapters if len(chapter) == 0 else chapter:
        chapter_data = {
                'chapter': chapter_it.id,
                'questions': []
            }
        
        for question_it in chapter_it.questions if len(question) == 0 else question:
            question_data = {
                'question': question_it.id,
                'scores': []
            }
            
            for score in scores[:]:
                if score.question_id == question_it.id:
                    question_data['scores'].append(score)
                    scores.remove(score)
                            
            chapter_data['questions'].append(question_data)
        
        results.append(chapter_data)
        
    return {'results': results}

def parse_json2(scores, app, chapter, question) -> Any:
    results = []
    for chapter_it in app.chapters if len(chapter) == 0 else chapter:     
        for question_it in chapter_it.questions if len(question) == 0 else question:    
            for score in scores[:]:
                score_data = {
                    'student_id': score.student_id,
                    'chapter_id': chapter_it.id,
                    'question_id': question_it.id,
                    'answer': score.answer,
                    'is_correct': score.is_correct,
                    'seconds': score.seconds,
                    'session': score.session,
                    'attempt': score.attempt,
                    'date': score.date
                }
                if score.question_id == question_it.id:
                    results.append(score_data)
                    scores.remove(score)
                            
        
    return {'scores': results}

@app.route('/<student_id>/scores', methods=['GET'])
@jwt_required(locations=['headers'])
def get_scores_from_student(app_id: str, student_id: int):
    user_id = get_jwt_identity()    

    try:
        user = db.session.scalar(db.select(User).where(User.id == user_id))
    except Exception as e:
        return jsonify({'message': 'invalid type'}), 400
    
    if user is None:
        return jsonify({'message': 'Unauthorized'}), 403
    app = db.session.scalar(db.select(Application).where(Application.id == app_id))
    
    if app is None:
        return jsonify({'message': f'App with id {app_id} not found'}), 404
    
    student = db.session.scalar(db.select(Student).where(Student.id == student_id))
    if student is None:
        return jsonify({'message': f'Student with id {student_id} not found'}), 404
    
    #pagination
    page = request.args.get('page', 1, type=int) 
    limit = request.args.get('limit', None, type=int) 
    
    #filters
    attempt_equal = request.args.get('attempt', None, type=int)
    attempt_low_bound = request.args.get('attempt[gte]', None, type=int)
    attempt_high_bound = request.args.get('attempt[lte]', None, type=int)

    session_equal = request.args.get('session', None, type=int)
    session_low_bound = request.args.get('session[gte]', None, type=int)
    session_high_bound = request.args.get('session[lte]', None, type=int)

    age_equal = request.args.get('age', None, type=int)
    age_low_bound = request.args.get('age[gte]', None, type=int)
    age_high_bound = request.args.get('age[lte]', None, type=int)    
    
    question_id = request.args.get('question', None, type=str)
    chapter_id = request.args.get('chapter', None, type=str)


    query = db.select(Score).where(Score.student_id == student_id)
    #attempt filters
    if attempt_equal is not None:
        query = query.where(Score.attempt == attempt_equal)
        
    if attempt_low_bound is not None:
        query = query.where(Score.attempt >= attempt_low_bound)
    
    if attempt_high_bound is not None:
        query = query.where(Score.attempt <= attempt_high_bound)
    
    #session filters
    if session_equal is not None:
        query = query.where(Score.session == session_equal)
        
    if session_low_bound is not None:
        query = query.where(Score.session >= session_low_bound)
        
    if session_high_bound is not None:
        query = query.where(Score.session <= session_high_bound)
    
    #age filters
    if [age_equal, age_low_bound, age_high_bound].count(None) != 3:
        query = query.join(Student)
    
    if age_equal is not None:
        query = query.where(Student.age == age_equal)
        
    if age_low_bound is not None:
        query = query.where(Student.age >= age_low_bound)
    
    if age_high_bound is not None:
        query = query.where(Student.age <= age_high_bound)
    
        
    #chapter and question filters
    if chapter_id is None and question_id is not None:
        return jsonify({'message': 'You must provide a chapter id to filter by question'}), 400
    
    chapter_filter = []
    question_filter = []
    if chapter_id is not None:
        if chapter_id.isdecimal():
            query = query.join(Score.question).join(Question.chapter).where(Chapter.number == chapter_id)

            chapter = db.session.scalar(db.select(Chapter).where(Chapter.number == chapter_id))
            if chapter is None:
                return jsonify({'message': f'Chapter with id {chapter_id} not found'}), 404
             
            chapter_filter.append(chapter)

        else:
            query = query.join(Score.question).where(Question.chapter_id == chapter_id)
            
            chapter = db.session.scalar(db.select(Chapter).where(Chapter.id == chapter_id))
            if chapter is None:
                return jsonify({'message': f'Chapter with id {chapter_id} not found'}), 404
            
            chapter_filter.append(chapter)
                 
    if question_id is not None:
        if question_id.isdecimal():
            query = query.where(Question.number == question_id)

            question = db.session.scalar(db.select(Question).where(Question.number == question_id).where(Question.chapter_id == chapter.id))
            if question is None:
                return jsonify({'message': f'Question with id {question_id} not found'}), 404
            
            question_filter.append(question)
            
        else:
            query = query.where(Score.question_id == question_id)
            
            question = db.session.scalar(db.select(Question).where(Question.id == question_id).where(Question.chapter_id == chapter.id))
            if question is None:
                return jsonify({'message': f'Question with id {question_id} not found'}), 404
            
            question_filter.append(question)
    
    if limit is None:
        scores = db.session.scalars(query).all()
    else:
        scores = db.paginate(query, page=page, per_page=limit, max_per_page=None, error_out=False).items
    
    json = parse_json2(scores, app, chapter_filter, question_filter)

    return jsonify(json), 200

@app.route('/scores', methods=['GET'])
@jwt_required(locations=['headers'])
def get_scores_from_students(app_id: str):
    user_id = get_jwt_identity()    
    user = db.session.scalar(db.select(User).where(User.id == user_id))
    if user is None:
        return jsonify({'message': 'Unauthorized'}), 403
    
    app = db.session.scalar(db.select(Application).where(Application.id == app_id))
    if app is None:
        return jsonify({'message': f'App with id {app_id} not found'}), 404
    
    #pagination
    page = request.args.get('page', 1, type=int) 
    limit = request.args.get('limit', None, type=int) 
    
    #filters
    attempt_equal = request.args.get('attempt', None, type=int)
    attempt_low_bound = request.args.get('attempt[gte]', None, type=int)
    attempt_high_bound = request.args.get('attempt[lte]', None, type=int)

    session_equal = request.args.get('session', None, type=int)
    session_low_bound = request.args.get('session[gte]', None, type=int)
    session_high_bound = request.args.get('session[lte]', None, type=int)

    age_equal = request.args.get('age', None, type=int)
    age_low_bound = request.args.get('age[gte]', None, type=int)
    age_high_bound = request.args.get('age[lte]', None, type=int)    
    
    question_id = request.args.get('question', None, type=str)
    chapter_id = request.args.get('chapter', None, type=str)


    query = db.select(Score)
    #attempt filters
    if attempt_equal is not None:
        query = query.where(Score.attempt == attempt_equal)
        
    if attempt_low_bound is not None:
        query = query.where(Score.attempt >= attempt_low_bound)
    
    if attempt_high_bound is not None:
        query = query.where(Score.attempt <= attempt_high_bound)
    
    #session filters
    if session_equal is not None:
        query = query.where(Score.session == session_equal)
        
    if session_low_bound is not None:
        query = query.where(Score.session >= session_low_bound)
        
    if session_high_bound is not None:
        query = query.where(Score.session <= session_high_bound)
    
    #age filters
    if [age_equal, age_low_bound, age_high_bound].count(None) != 3:
        query = query.join(Student)
    
    if age_equal is not None:
        query = query.where(Student.age == age_equal)
        
    if age_low_bound is not None:
        query = query.where(Student.age >= age_low_bound)
    
    if age_high_bound is not None:
        query = query.where(Student.age <= age_high_bound)
    
        
    #chapter and question filters
    if chapter_id is None and question_id is not None:
        return jsonify({'message': 'You must provide a chapter id to filter by question'}), 400
    
    chapter_filter = []
    question_filter = []
    if chapter_id is not None:
        if chapter_id.isdecimal():
            query = query.join(Score.question).join(Question.chapter).where(Chapter.number == chapter_id)

            chapter = db.session.scalar(db.select(Chapter).where(Chapter.number == chapter_id))
            if chapter is None:
                return jsonify({'message': f'Chapter with id {chapter_id} not found'}), 404
             
            chapter_filter.append(chapter)

        else:
            query = query.join(Score.question).where(Question.chapter_id == chapter_id)
            
            chapter = db.session.scalar(db.select(Chapter).where(Chapter.id == chapter_id))
            if chapter is None:
                return jsonify({'message': f'Chapter with id {chapter_id} not found'}), 404
            
            chapter_filter.append(chapter)
                 
    if question_id is not None:
        if question_id.isdecimal():
            query = query.where(Question.number == question_id)

            question = db.session.scalar(db.select(Question).where(Question.number == question_id).where(Question.chapter_id == chapter.id))
            if question is None:
                return jsonify({'message': f'Question with id {question_id} not found'}), 404
            
            question_filter.append(question)
            
        else:
            query = query.where(Score.question_id == question_id)
            
            question = db.session.scalar(db.select(Question).where(Question.id == question_id).where(Question.chapter_id == chapter.id))
            if question is None:
                return jsonify({'message': f'Question with id {question_id} not found'}), 404
            
            question_filter.append(question)
    
    if limit is None:
        scores = db.session.scalars(query).all()
    else:
        scores = db.paginate(query, page=page, per_page=limit, max_per_page=None, error_out=False).items
    
    json = parse_json2(scores, app, chapter_filter, question_filter)

    return jsonify(json), 200
    
    ###
    data = parse_json1(scores, app,chapter_filter, question_filter)
    
    #schema = GetScoreSchema()
    #try:
    #    validated_data = schema.dump(data)
    #except ValidationError as err:
    #    return jsonify(err.messages), 422
    
    
    #return jsonify(validated_data), 200
    
    

@app.route('/<student_id>/scores', methods=['POST'])
@jwt_required(locations=['headers'])
def post_student_scores(app_id, student_id):
    app = db.session.scalar(db.select(Application).where(Application.id == app_id))

    if app is None:
        return jsonify({'message': f'App with id {app_id} not found'}), 404
    
    if get_jwt_identity() != app_id:
        return jsonify({'message': 'Unauthorized'}), 403

    json_data = request.get_json()    
    
    schema = PostScoreSchema()

    try:
        validated_data = schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    
    student = db.session.scalar(db.select(Student).where(Student.id == student_id))
    if student is None:
        return jsonify({'message': f'Student with id {student_id} not found'}), 404
     
    if validated_data['chapter']['id'] not in [chapter.id for chapter in app.chapters]: 
        return jsonify({'message': f'Chapter with id {validated_data["chapter"]["id"]} not found'}), 404 
    
    student.session += 1
    chapter = db.session.scalar(db.select(Chapter).where(Chapter.id == validated_data['chapter']['id']))
    
    for score in validated_data['chapter']['scores']:
        if score['question_id'] not in [question.id for question in chapter.questions]:
            return jsonify({'message': f'Question with id  not found in chapter {chapter.id}'}), 404
        
        last_attempt = db.session.scalar(db.select(Score).where(Score.student_id == student_id).order_by(Score.attempt.desc()).limit(1))

        new_score = Score(student.id, score['question_id'], answer=score['answer'], seconds=score['seconds'], is_correct=score['is_correct'],
                          attempt=last_attempt.attempt + 1 if last_attempt is not None else 1, session=student.session)
        db.session.add(new_score)
    
    db.session.commit()

    return jsonify({'message': 'scores added correcly'}), 201