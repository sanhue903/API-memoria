import pytest
from flask_jwt_extended import create_access_token

test_student = {
    'age': 1,
    'name': 'Test Student'
}

def test_post_student(test_client, mock_application):
    headers = {'Authorization': f'Bearer {mock_application["token"]}'}
    response = test_client.post(f'/apps/{mock_application["app"].id}/students' , headers=headers,json=test_student)
    
    print(response.json)
    assert response.status_code == 201

def test_post_student_not_authentication(test_client, mock_application):
    response = test_client.post(f'/apps/{mock_application["app"].id}/students', json=test_student)
    
    assert response.status_code == 401

def test_post_student_unauthorized(test_client, mock_application, mock_user):
    headers = {'Authorization': f'Bearer {mock_user["token"]}'}
    response = test_client.post(f'/apps/{mock_application["app"].id}/students', headers=headers,json=test_student)
    
    assert response.status_code == 403
    
def test_post_student_invalid_app(test_client, mock_application):
    headers = {'Authorization': f'Bearer {mock_application["token"]}'}
    response = test_client.post(f'/apps/OTHER1/students', headers=headers,json=test_student)
    
    assert response.status_code == 403

def test_post_student_invalid_app(test_client, mock_application):
    app_id = 'OTHER1'
    headers = {'Authorization': f'Bearer {create_access_token(identity=app_id)}'}
    response = test_client.post(f'/apps/{app_id}/students', headers=headers,json=test_student)
    
    assert response.status_code == 404

def test_post_student_invalid_data(test_client, mock_application):
    headers = {'Authorization': f'Bearer {mock_application["token"]}'}
    response = test_client.post(f'/apps/{mock_application["app"].id}/students', headers=headers,json={'age': 'a', 'name': 'Test Student'})
    
    assert response.status_code == 422
    
def test_get_students(test_client, mock_application, mock_user, mock_student):
    headers = {'Authorization': f'Bearer {mock_user["token"]}'}
    response = test_client.get(f'/apps/{mock_application["app"].id}/students', headers=headers)
    
    assert response.status_code == 200
    assert len(response.json['students']) == 2

def test_get_students_not_authentication(test_client, mock_application, mock_user):
    response = test_client.get(f'/apps/{mock_application["app"].id}/students')
    
    assert response.status_code == 401 

def test_get_students_unauthorized(test_client, mock_application):
    headers = {'Authorization': f'Bearer {mock_application["token"]}'}
    response = test_client.get(f'/apps/{mock_application["app"].id}/students', headers=headers)
    
    assert response.status_code == 403

def test_get_students_invalid_app(test_client, mock_application, mock_user):
    headers = {'Authorization': f'Bearer {mock_user["token"]}'}
    response = test_client.get(f'/apps/OTHER1/students', headers=headers)
    
    assert response.status_code == 404
