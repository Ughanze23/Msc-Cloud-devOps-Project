import pytest
from website import create_app, db
from website.models import User, Glossary, Role
from flask_login import current_user

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
def init_database(app):
   with app.app_context():
       db.create_all()
       
       # Create roles
       admin_role = Role(role_name='admin')
       user_role = Role(role_name='user')
       db.session.add_all([admin_role, user_role])
       
       # Create test users
       admin = User(email='admin@test.com', username='admin', password='password123', role=admin_role)
       user = User(email='user@test.com', username='user', password='password123', role=user_role)
       db.session.add_all([admin, user])
       
       # Create test glossary entry
       entry = Glossary(posted_by=user.id, name='Test Term', type='Category', description='Test description')
       db.session.add(entry)
       
       db.session.commit()
       yield db
       db.drop_all()

def test_home_page(client, init_database):
   client.post('/login', data={'email': 'user@test.com', 'password': 'password123'})
   response = client.get('/home')
   assert response.status_code == 200

def test_glossary_page(client, init_database):
   client.post('/login', data={'email': 'user@test.com', 'password': 'password123'})
   response = client.get('/glossary')
   assert response.status_code == 200
   assert b'Test Term' in response.data

def test_post_glossary(client, init_database):
   client.post('/login', data={'email': 'user@test.com', 'password': 'password123'})
   response = client.post('/post-glossary', data={
       'name': 'New Term',
       'category': 'New Category',
       'description': 'New description'
   }, follow_redirects=True)
   assert b'Business Term Created Successful' in response.data

def test_edit_term(client, init_database):
   client.post('/login', data={'email': 'user@test.com', 'password': 'password123'})
   response = client.get('/glossary/edit-term/1?category=Updated&description=Updated', follow_redirects=True)
   assert b'Business term updated successfully' in response.data

def test_delete_term_admin(client, init_database):
   client.post('/login', data={'email': 'admin@test.com', 'password': 'password123'})
   response = client.get('/glossary/delete-entry/1', follow_redirects=True)
   assert b'Entry Deleted Successfully' in response.data

def test_delete_term_unauthorized(client, init_database):
   client.post('/login', data={'email': 'user@test.com', 'password': 'password123'})
   response = client.get('/glossary/delete-entry/1', follow_redirects=True)
   assert b'You are not authorized' in response.data

def test_users_page(client, init_database):
   client.post('/login', data={'email': 'admin@test.com', 'password': 'password123'})
   response = client.get('/users')
   assert response.status_code == 200

def test_change_role_admin(client, init_database):
   client.post('/login', data={'email': 'admin@test.com', 'password': 'password123'})
   response = client.get('/change-role/user_id=2?role=1', follow_redirects=True)
   assert b'User role updated successfully' in response.data