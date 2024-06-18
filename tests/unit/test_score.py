import pytest
from app.extensions import db
from app.models import Score

score = {
  "answer": "Test Answer",
  "seconds": 10.0,
  "is_correct": True,
  "question_id": None 
}

def make_headers(token):
  return {'Authorization': f'Bearer {token}'}

def make_json(chapter_id, scores):
  new_request = {
    "chapter": {
      "id": None,
      "scores": []
    }
  }
  new_request['chapter']['id'] = chapter_id
    
  for score in scores:
    new_request['chapter']['scores'].append(score) 
    
  return new_request
    
def test_post_scores(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
    
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
    
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id

  test_score2_1 = score.copy()
  test_score2_1['question_id'] = chapter.questions[1].id
    
  scores = [test_score1_1, test_score1_2, test_score2_1]
    
  request = make_json(chapter.id, scores)
    
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=request)
    
  assert response.status_code == 201

def test_attempt_count(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
  
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
  
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id  
  
  test_score2_1 = score.copy()
  test_score2_1['question_id'] = chapter.questions[1].id
  
  scores_json = [test_score1_1, test_score1_2, test_score2_1]
  
  request = make_json(chapter.id, scores_json) 
  
  scores = db.session.scalars(db.select(Score).where(Score.question_id == chapter.questions[0].id)).all()
  assert len(scores) == 0
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=request)
  assert response.status_code == 201

  print(response.get_json())

  scores = db.session.scalars(db.select(Score).where(Score.question_id == chapter.questions[0].id)).all()

  assert len(scores) == 2
  assert scores[0].attempt == 1
  assert scores[1].attempt == 2

def test_session_count(test_client, mock_app_content, mock_student):
  headers = make_headers(mock_app_content['token'])
  
  chapter = mock_app_content['app'].chapters[0]
  
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
  
  request = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=make_json(chapter.id, [test_score1_1]))
  
  assert request.status_code == 201
  
  assert mock_student[0].session == 1
  
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id
  
  request = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=make_json(chapter.id, [test_score1_2]))
  
  assert request.status_code == 201
  assert mock_student[0].session == 2
  
  

def test_post_scores_wrong_app(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
    
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
    
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id

  test_score2_1 = score.copy()
  test_score2_1['question_id'] = chapter.questions[1].id
    
  scores = [test_score1_1, test_score1_2, test_score2_1]
    
  request = make_json(chapter.id, scores)
    
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/WRONAP/students/{mock_student[0].id}/scores', headers=headers, json=request)
    
  assert response.status_code == 404

def test_post_scores_no_authentication(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
    
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
    
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id

  test_score2_1 = score.copy()
  test_score2_1['question_id'] = chapter.questions[1].id
    
  scores = [test_score1_1, test_score1_2, test_score2_1]
    
  request = make_json(chapter.id, scores)
    
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', json=request)
    
  assert response.status_code == 401
  
def test_post_scores_no_authorized(test_client, mock_app_content, mock_student, mock_user):
  chapter = mock_app_content['app'].chapters[0]
    
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
    
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id

  test_score2_1 = score.copy()
  test_score2_1['question_id'] = chapter.questions[1].id
    
  scores = [test_score1_1, test_score1_2, test_score2_1]
    
  request = make_json(chapter.id, scores)
    
  headers = {'Authorization': f'Bearer {mock_user["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=request)
    
  assert response.status_code == 403

def test_post_scores_wrong_student(test_client, mock_app_content):
  chapter = mock_app_content['app'].chapters[0]
  
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
  
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id  
  
  test_score2_1 = score.copy()
  test_score2_1['question_id'] = chapter.questions[1].id
  
  scores = [test_score1_1, test_score1_2, test_score2_1]
  
  request = make_json(chapter.id, scores)
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/99/scores', headers=headers, json=request)
  
  assert response.status_code == 404
  
def test_post_scores_wrong_chapter(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
  
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
  
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id  
  
  test_score2_1 = score.copy()
  test_score2_1['question_id'] = chapter.questions[1].id
  
  scores = [test_score1_1, test_score1_2, test_score2_1]
  
  request = make_json('WRONCH', scores)
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=request)
  
  assert response.status_code == 404
  
def test_post_scores_wrong_question(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
  
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['is_correct'] = False
  
  test_score1_2 = score.copy()
  test_score1_2['question_id'] = chapter.questions[0].id  
  
  test_score2_1 = score.copy()
  test_score2_1['question_id'] = 'WRONQU'
  
  scores = [test_score1_1, test_score1_2, test_score2_1]
  
  request = make_json(chapter.id, scores)
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=request)
  
  assert response.status_code == 404
  
def test_post_scores_missing_data(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
  
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1.pop('answer')
  

  scores = [test_score1_1]
  
  request = make_json(chapter.id, scores)
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=request)
  
  assert response.status_code == 422

def test_post_scores_invalid_data(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
  
  test_score1_1 = score.copy()
  test_score1_1['question_id'] = chapter.questions[0].id
  test_score1_1['seconds'] = 'a'
  
  scores = [test_score1_1]
  
  request = make_json(chapter.id, scores)
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores', headers=headers, json=request)
  
  assert response.status_code == 422
  
def test_get_scores(test_client, mock_user, mock_scores):
  headers = {'Authorization': f'Bearer {mock_user["token"]}'}
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
      
      
  print(json)
      
  assert total_scores == len(mock_scores[1])

def test_get_scores_wrong_app(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user["token"])
  
  response = test_client.get(f'/apps/WROGAP/students/scores', headers=headers)

  assert response.status_code == 404

def test_get_scores_no_authentication(test_client, mock_scores):
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores')

  assert response.status_code == 401

def test_get_scores_no_authorized(test_client, mock_user, mock_application, mock_scores):
  headers = make_headers(mock_scores[0]['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores', headers=headers)

  assert response.status_code == 403
  
def test_chapter_filter(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?chapter=TESCH1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.question.chapter_id == 'TESCH1']
  
  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])

  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?chapter=1', headers=headers)
      
  assert total_scores == len(scores)

def test_wrong_chapter_filter(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?chapter=WRONG', headers=headers)
  
  assert response.status_code == 404
  
def test_question_filter(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?chapter=TESCH1&question=TESQ11', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.question_id == 'TESQ11']
  
  assert len(json['results'][0]['questions'][0]['scores']) == len(scores)
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?chapter=TESCH1&question=1', headers=headers)

  assert len(json['results'][0]['questions'][0]['scores']) == len(scores)

def test_equal_attempt_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?attempt=1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.attempt == 1]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)
  
def test_low_bound_attempt_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?attempt[gte]=1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.attempt >= 1]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)

def test_high_bound_attempt_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?attempt[lte]=1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.attempt <= 1]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)
  
def test_low_and_high_bound_attempt_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?attempt[gte]=1&attempt[lte]=2', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.attempt >= 1 and score.attempt <= 2]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)

def test_inversed_low_and_high_bound_attempt_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?attempt[gte]=2&attempt[lte]=1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == 0

def test_equal_session_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?session=2', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.session == 2]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)

def test_low_bound_session_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?session[gte]=2', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.session >= 2]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)

def test_high_bound_session_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?session[lte]=1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.session <= 1]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)
  
def test_low_and_high_bound_session_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?session[gte]=1&session[lte]=2', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.session >= 1 and score.session <= 2]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)

def test_inversed_low_and_high_bound_session_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?session[gte]=2&session[lte]=1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == 0
  
def test_equal_age_filters(test_client, mock_user, mock_student, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?age={mock_student[0].age}', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.student.age == mock_student[0].age]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)
  
def test_low_bound_age_filters(test_client, mock_user, mock_student, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?age[gte]={mock_student[1].age}', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.student.age >= mock_student[1].age]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)
  
def test_high_bound_age_filters(test_client, mock_user, mock_student, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?age[lte]={mock_student[0].age}', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.student.age <= mock_student[0].age]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)
  
def test_low_and_high_bound_age_filters(test_client, mock_user, mock_student, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?age[gte]={mock_student[0].age}&age[lte]={mock_student[1].age}', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  scores =[score for score in mock_scores[1] if score.student.age >= mock_student[0].age and score.student.age <= mock_student[1].age]

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == len(scores)

def test_inversed_low_and_high_bound_age_filters(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores?age[gte]=2&age[lte]=1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()

  total_scores = 0
  for chapter in json['results']:
    for question in chapter['questions']:
      total_scores += len(question['scores'])
  
  assert total_scores == 0