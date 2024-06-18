import pytest
from app import create_app
from config import TestingConfig

from app.extensions import db
from app.models import User, Application, Chapter, Question, Student, Score
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='function') 
def test_client():
    flask_app = create_app(TestingConfig)
    
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
            db.session.close_all()
            db.drop_all()

@pytest.fixture(scope='function')
def mock_user(test_client):
    test_user = User('test@test.cl', 'testtest')
    db.session.add(test_user)
    db.session.commit()
    
    yield {'user': test_user, 
           'token':create_access_token(identity=test_user.id)
        }
    
@pytest.fixture(scope='function')
def mock_application(test_client):
    test_app = Application(id='TESAPP', name='Test Application')
    db.session.add(test_app)
    
    db.session.commit()
   
    yield {'app': test_app,
           'token':create_access_token(identity=test_app.id)
        } 
    
@pytest.fixture(scope='function')
def mock_app_content(test_client, mock_application):
    chapter1 = Chapter(id='TESCH1', app_id=mock_application['app'].id, number=1, name='Test Chapter 1')
    db.session.add(chapter1)
    
    chapter2 = Chapter(id='TESCH2', app_id=mock_application['app'].id, number=2, name='Test Chapter 2')
    db.session.add(chapter2)
    
    question1_1 = Question(id='TESQ11', chapter_id=chapter1.id, number=1, text='Test Question 1.1')
    db.session.add(question1_1)
    
    question1_2 = Question(id='TESQ12', chapter_id=chapter1.id, number=2, text='Test Question 1.2')
    db.session.add(question1_2)
    
    question2_1 = Question(id='TESQ21', chapter_id=chapter2.id, number=1, text='Test Question 2.1')
    db.session.add(question2_1) 
   
    db.session.commit() 
    yield mock_application
    
@pytest.fixture(scope='function')
def mock_student(test_client, mock_application):
    test_student1 = Student(app_id=mock_application['app'].id, name='Test Student', age=5)
    db.session.add(test_student1)
    db.session.commit()
    
    test_student2 = Student(app_id=mock_application['app'].id, name='Test Student 2', age=7)
    db.session.add(test_student2)
    db.session.commit()
    
    yield [test_student1, test_student2]
    
@pytest.fixture(scope='function')
def mock_scores(test_client, mock_app_content, mock_student):
    chapter1 = mock_app_content['app'].chapters[0]
    
    question1_1 = chapter1.questions[0]
    question1_2 = chapter1.questions[1]
    
    chapter2 = mock_app_content['app'].chapters[1]
    question2_1 = chapter2.questions[0]     
    
    # First student
    score1 = Score(student_id=mock_student[0].id, question_id=question1_1.id, answer='wrong', seconds=10.0, is_correct=False, session=1)
    db.session.add(score1)
    
    score2 = Score(student_id=mock_student[0].id, question_id=question1_1.id, answer='correct', seconds=3.7, is_correct=True, attempt=2, session=2)
    db.session.add(score2)
    
    score3 = Score(student_id=mock_student[0].id, question_id=question1_2.id, answer='correct', seconds=5.8, is_correct=True, session=2)
    db.session.add(score3)
    
    score4 = Score(student_id=mock_student[0].id, question_id=question2_1.id, answer='correct', seconds=2.8, is_correct=True, session=2)
    db.session.add(score4)
    
    # Second student
    score5 = Score(student_id=mock_student[1].id, question_id=question1_1.id, answer='correct', seconds=6.8, is_correct=True, session=1)
    db.session.add(score5)
    
    score6 = Score(student_id=mock_student[1].id, question_id=question1_2.id, answer='wrong', seconds=4.8, is_correct=False, session=1)
    db.session.add(score6)
    
    score7 = Score(student_id=mock_student[1].id, question_id=question1_2.id, answer='correct', seconds=2.8, is_correct=True, attempt=2, session=1)
    db.session.add(score7)
    
    score8 = Score(student_id=mock_student[1].id, question_id=question2_1.id, answer='wrong', seconds=4.8, is_correct=False, session=1)
    db.session.add(score8)
    
    score9 = Score(student_id=mock_student[1].id, question_id=question2_1.id, answer='wrong', seconds=1.8, is_correct=False, attempt=2, session=1)
    db.session.add(score9)
    
    score10 = Score(student_id=mock_student[1].id, question_id=question2_1.id, answer='correct', seconds=2.3, is_correct=True, attempt=3, session=1)
    db.session.add(score10)
    
    db.session.commit()
    
    yield mock_app_content, [score1, score2, score3, score4, score5, score6, score7, score8, score9, score10]