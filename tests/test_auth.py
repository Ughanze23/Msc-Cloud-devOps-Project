import pytest
from website import create_app, db
from website.models import User, Role
from flask_login import current_user
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
   app = create_app()
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
   app.config['TESTING'] = True
   return app

@pytest.fixture
def client(app):
   return app.test_client()

@pytest.fixture
def runner(app):
   return app.test_cli_runner()

@pytest.fixture
def init_database(app):
   with app.app_context():
       db.create_all()
       # Create role
       role = Role(id=2, role_name='user')
       db.session.add(role)
       db.session.commit()

       # Create user
       user = User(
           email='test@test.com',
           username='testuser', 
           password=generate_password_hash('password123'),
           role_id=2
       )
       db.session.add(user)
       db.session.commit()
       yield db
       db.drop_all()

def test_login_success(client, init_database):
   response = client.post('/login', data={
       'email': 'test@test.com',
       'password': 'password123'
   }, follow_redirects=True)
   assert b"Sucessfully logged in" in response.data

def test_login_wrong_password(client, init_database):
   response = client.post('/login', data={
       'email': 'test@test.com',
       'password': 'wrongpass'
   })
   assert b"Incorrect password" in response.data

def test_signup_success(client, init_database):
   response = client.post('/sign-up', data={
       'email': 'new@test.com',
       'username': 'newuser',
       'password1': 'password123',
       'password2': 'password123'
   }, follow_redirects=True)
   assert b"User created Successfully" in response.data

def test_reset_password_request(client, init_database):
   response = client.post('/reset-password-request', data={
       'email': 'test@test.com'
   }, follow_redirects=True)
   assert response.status_code == 200

def test_reset_password(client, init_database):
   response = client.post('/reset-password/1', data={
       'password1': 'newpassword',
       'password2': 'newpassword'
   }, follow_redirects=True)
   assert b"Password has been reset" in response.data

def test_logout(client, init_database):
   client.post('/login', data={
       'email': 'test@test.com',
       'password': 'password123'
   })
   response = client.get('/log-out', follow_redirects=True)
   assert b"Login" in response.data