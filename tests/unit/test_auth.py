import pytest

template_test_user = {
        'email': 'test@test.cl',
        'password': 'testtest',
        'confirm_password': 'testtest'
    }

def test_sign_up(test_client):
    response = test_client.post('/auth/signup', json=template_test_user)

    assert response.status_code == 201

def test_sign_up_missing_field(test_client):
    test_user = template_test_user.copy()
    test_user.pop('confirm_password')
    
    response = test_client.post('/auth/signup', json=test_user)
    
    assert response.status_code == 422

def test_email_already_exist(test_client, mock_user):
    test_user = template_test_user.copy()
    test_user['email'] = mock_user['user'].email
    
    response = test_client.post('/auth/signup', json=test_user)
    
    assert response.status_code == 409
    
def test_error_confirm_password_dont_match(test_client):
    test_user = template_test_user.copy()
    test_user['confirm_password'] = 'testtest2'
    
    response = test_client.post('/auth/signup', json=test_user)
    
    assert response.status_code == 400

def test_login(test_client, mock_user):
    response = test_client.post('/auth/login', json={
        'email': mock_user['user'].email,
        'password': 'testtest'
    })

    assert response.status_code == 201
    
def test_login_missing_field(test_client):
    test_user = template_test_user.copy()
    test_user.pop('confirm_password')
    test_user.pop('password')
    
    response = test_client.post('/auth/login', json=test_user)
    
    assert response.status_code == 422
    
def test_login_wrong_password(test_client, mock_user):
    response = test_client.post('/auth/login', json={
        'email': mock_user['user'].email,
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    
def test_login_user_not_found(test_client):
    test_user = template_test_user.copy()
    test_user.pop('confirm_password')
    
    response = test_client.post('/auth/login', json=test_user)
    
    assert response.status_code == 404
    
