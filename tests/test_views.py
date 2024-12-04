import pytest
from website import create_app, db
from website.models import User, Glossary, Role
from flask_login import current_user
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,  
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        
        try:
            # Check for existing roles first
            admin_role = Role.query.filter_by(role_name='admin').first()
            editor_role = Role.query.filter_by(role_name='editor').first()
            
            # Create roles if they don't exist
            if not admin_role:
                admin_role = Role(id=1, role_name='admin')
                db.session.add(admin_role)
            
            if not editor_role:
                editor_role = Role(id=2, role_name='editor')
                db.session.add(editor_role)
            
            # Create test users
            admin = User(
                email='admin@test.com',
                username='admin',
                password=generate_password_hash('password123'),
                role_id=admin_role.id
            )
            
            editor = User(
                email='editor@test.com',
                username='editor',
                password=generate_password_hash('password123'),
                role_id=editor_role.id
            )
            
            db.session.add_all([admin, editor])
            
            # Create test glossary entry
            entry = Glossary(
                posted_by=editor.id,
                name='Test Term',
                type='Category',
                description='Test description'
            )
            db.session.add(entry)
            
            db.session.commit()
            
        except IntegrityError as e:
            db.session.rollback()
            pytest.fail(f"Database initialization failed: {str(e)}")
        except Exception as e:
            db.session.rollback()
            pytest.fail(f"Test setup failed: {str(e)}")
        
        yield db
        
        # Cleanup
        db.session.remove()
        db.drop_all()

def test_home_page(client, init_database):
    # Login as editor
    response = client.post('/login', data={
        'email': 'editor@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert b"Sucessfully logged in" in response.data
    
    response = client.get('/home')
    assert response.status_code == 200

def test_glossary_page(client, init_database):
    # Login as editor
    client.post('/login', data={
        'email': 'editor@test.com',
        'password': 'password123'
    })
    response = client.get('/glossary')
    assert response.status_code == 200
    assert b'Test Term' in response.data

def test_post_glossary(client, init_database):
    # Login as editor
    client.post('/login', data={
        'email': 'editor@test.com',
        'password': 'password123'
    })
    response = client.post('/post-glossary', data={
        'name': 'New Term',
        'category': 'New Category',
        'description': 'New description'
    }, follow_redirects=True)
    assert b'Business Term Created Successful' in response.data

def test_edit_term(client, init_database):
    # Login as editor
    client.post('/login', data={
        'email': 'editor@test.com',
        'password': 'password123'
    })
    response = client.get(
        '/glossary/edit-term/1?category=Updated&description=Updated',
        follow_redirects=True
    )
    assert b'Business term updated successfully' in response.data

def test_delete_term_admin(client, init_database):
    # Login as admin
    client.post('/login', data={
        'email': 'admin@test.com',
        'password': 'password123'
    })
    response = client.get('/glossary/delete-entry/1', follow_redirects=True)
    assert b'Entry Deleted Successfully' in response.data

def test_delete_term_unauthorized(client, init_database):
    # Login as editor
    client.post('/login', data={
        'email': 'editor@test.com',
        'password': 'password123'
    })
    response = client.get('/glossary/delete-entry/1', follow_redirects=True)
    assert b'You are not authorized' in response.data

def test_users_page_admin_access(client, init_database):
    # Login as admin
    client.post('/login', data={
        'email': 'admin@test.com',
        'password': 'password123'
    })
    response = client.get('/users')
    assert response.status_code == 200

def test_users_page_editor_access(client, init_database):
    # Login as editor
    client.post('/login', data={
        'email': 'editor@test.com',
        'password': 'password123'
    })
    response = client.get('/users', follow_redirects=True)
    assert b'You are not authorized' in response.data

def test_change_role_admin(client, init_database):
    # Login as admin
    client.post('/login', data={
        'email': 'admin@test.com',
        'password': 'password123'
    })
    response = client.get('/change-role/user_id=2?role=1', follow_redirects=True)
    assert b'User role updated successfully' in response.data

def test_change_role_unauthorized(client, init_database):
    # Login as editor
    client.post('/login', data={
        'email': 'editor@test.com',
        'password': 'password123'
    })
    response = client.get('/change-role/user_id=1?role=2', follow_redirects=True)
    assert b'You are not authorized' in response.data