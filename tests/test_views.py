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
            # Create roles
            admin_role = Role(id=1, role_name='admin')
            editor_role = Role(id=2, role_name='editor')
            viewer_role = Role(id=3, role_name='viewer')
            db.session.add_all([admin_role, editor_role, viewer_role])
            
            # Create admin user
            admin = User(
                email='admin@test.com',
                username='admin',
                password=generate_password_hash('password123'),
                role_id=admin_role.id
            )
            
            # Create editor user
            editor = User(
                email='editor@test.com',
                username='editor',
                password=generate_password_hash('password123'),
                role_id=editor_role.id
            )
            
            # Create test user
            test_user = User(
                email='test@test.com',
                username='testuser',
                password=generate_password_hash('password123'),
                role_id=viewer_role.id
            )
            
            db.session.add_all([admin, editor, test_user])
            
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

# Auth Tests
class TestAuth:
    def test_login_success(self, client, init_database):
        response = client.post('/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        assert b"Sucessfully logged in" in response.data

    def test_login_wrong_password(self, client, init_database):
        response = client.post('/login', data={
            'email': 'test@test.com',
            'password': 'wrongpass'
        })
        assert b"Incorrect password" in response.data

    def test_signup_success(self, client, init_database):
        response = client.post('/sign-up', data={
            'email': 'new@test.com',
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123'
        }, follow_redirects=True)
        assert b"User created Successfully" in response.data

    def test_signup_existing_email(self, client, init_database):
        response = client.post('/sign-up', data={
            'email': 'test@test.com',
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        assert b"Email already exists" in response.data

    def test_logout(self, client, init_database):
        client.post('/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        })
        response = client.get('/log-out', follow_redirects=True)
        assert b"Login" in response.data

# Views Tests
class TestViews:
    def test_home_page(self, client, init_database):
        client.post('/login', data={
            'email': 'editor@test.com',
            'password': 'password123'
        })
        response = client.get('/home')
        assert response.status_code == 200

    def test_glossary_page(self, client, init_database):
        client.post('/login', data={
            'email': 'editor@test.com',
            'password': 'password123'
        })
        response = client.get('/glossary')
        assert response.status_code == 200
        assert b'Test Term' in response.data

    def test_post_glossary(self, client, init_database):
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

    def test_edit_term(self, client, init_database):
        client.post('/login', data={
            'email': 'editor@test.com',
            'password': 'password123'
        })
        response = client.get(
            '/glossary/edit-term/1?category=Updated&description=Updated',
            follow_redirects=True
        )
        assert b'Business term updated successfully' in response.data

    def test_delete_term_admin(self, client, init_database):
        client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'password123'
        })
        response = client.get('/glossary/delete-entry/1', follow_redirects=True)
        assert b'Entry Deleted Successfully' in response.data

    def test_delete_term_unauthorized(self, client, init_database):
        client.post('/login', data={
            'email': 'editor@test.com',
            'password': 'password123'
        })
        response = client.get('/glossary/delete-entry/1', follow_redirects=True)
        assert b'You are not authorized' in response.data

    def test_users_page_admin(self, client, init_database):
        client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'password123'
        })
        response = client.get('/users')
        assert response.status_code == 200

    def test_change_role_admin(self, client, init_database):
        client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'password123'
        })
        response = client.get('/change-role/user_id=2?role=1', follow_redirects=True)
        assert b'User role updated successfully' in response.data