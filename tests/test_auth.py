import pytest
from website import create_app, db
from website.models import User, Role
from flask_login import current_user
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False 
    })
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
        
        try:
            # Check for existing roles first
            editor_role = Role.query.filter_by(role_name='editor').first()
            admin_role = Role.query.filter_by(role_name='admin').first()
            
            # Create roles only if they don't exist
            if not editor_role:
                editor_role = Role(id=2, role_name='editor')
                db.session.add(editor_role)
            
            if not admin_role:
                admin_role = Role(id=1, role_name='admin')
                db.session.add(admin_role)
            
            # Create test user with editor role
            test_user = User(
                email='test@test.com',
                username='testuser',
                password=generate_password_hash('password123'),
                role_id=editor_role.id
            )
            db.session.add(test_user)
            
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

def test_signup_existing_email(client, init_database):
    """Test that signing up with an existing email fails"""
    response = client.post('/sign-up', data={
        'email': 'test@test.com',  # Using existing email
        'username': 'newuser',
        'password1': 'password123',
        'password2': 'password123'
    })
    assert b"Email already exists" in response.data

def test_signup_password_mismatch(client, init_database):
    """Test that signing up with mismatched passwords fails"""
    response = client.post('/sign-up', data={
        'email': 'new@test.com',
        'username': 'newuser',
        'password1': 'password123',
        'password2': 'password456'
    })
    assert b"Passwords don't match" in response.data

def test_reset_password_request(client, init_database):
    response = client.post('/reset-password-request', data={
        'email': 'test@test.com'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_reset_password(client, init_database):
    # log in to create a valid session
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    response = client.post('/reset-password/1', data={
        'password1': 'newpassword',
        'password2': 'newpassword'
    }, follow_redirects=True)
    assert b"Password has been reset" in response.data

def test_logout(client, init_database):
    # Login first
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    # Then test logout
    response = client.get('/log-out', follow_redirects=True)
    assert b"Login" in response.data
    
def test_access_protected_page_without_login(client, init_database):
    """Test that accessing protected pages without login redirects to login page"""
    response = client.get('/home', follow_redirects=True)
    assert b"Login" in response.data



