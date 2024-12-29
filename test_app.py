# test_app.py
from unittest import TestCase

from app import app
from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly_db'
app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():        
    db.drop_all()        
    db.create_all()

class UserRoutesTestCase(TestCase):
    """Tests for user routes."""

    def setUp(self):
        """Add Sample User"""
        with app.app_context():
            User.query.delete()
            Post.query.delete()
            # Add a sample user for tests
            user = User(first_name="Test", 
                        last_name="User", 
                        image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
            
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        """Clean up any transactions after each test."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        """Test GET /users route."""

        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user(self):
        """Test GET /users/[user-id] route."""

        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_add_user(self):
        """Test POST /users/new route."""
        with app.test_client() as client:
            data = {
            "first_name": "New",
            "last_name": "User",
            "image_url": "https://example.com/new.jpg"
            }

            resp = client.post('/users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New User', html)

    def test_edit_user(self):
        """Test POST /users/[user-id]/edit route."""
        with app.test_client() as client:
            data = {
                "first_name": "Updated",
                "last_name": "User",
                "image_url": "https://example.com/updated.jpg"
            }

            resp = client.post(f'/users/{self.user_id}/edit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Updated User', html)

    def test_delete_user(self):
        """Test POST /users/[user-id]/delete route."""
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test User', html)

class PostRoutesTestCase(TestCase):
    """Tests for post routes"""
    
    def setUp(self):
        """Add sample post."""
        with app.app_context():
            Post.query.delete()
            User.query.delete()

        # Add a sample user
            user = User(first_name="Test", 
                        last_name="User", 
                        image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
            
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id


        # Add a sample post
            post = Post(title="Sample Post", content="Sample content", user_id= user.id)
            db.session.add(post)
            db.session.commit()
            self.post_id = post.id

    def tearDown(self):
        """Clean up any transactions after each test."""
        with app.app_context():
            db.session.rollback()

    def test_show_new_post_form(self):
        """Test GET /users/[user-id]/posts/new route."""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post', html)

    def test_create_post(self):
        """Test POST /users/[user-id]/posts/new route."""
        with app.test_client() as client:
            data = {
                "title": "New Post",
                "content": "New post content"
            }
            resp = client.post(f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Post', html)

    def test_show_post(self):
        """Test GET /posts/[post-id] route."""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sample Post', html)
            self.assertIn('Sample content', html)

    def test_edit_post(self):
        """Test POST /posts/[post-id]/edit route."""
        with app.test_client() as client:
            data = {
                "title": "Updated Post",
                "content": "Updated content"
            }
            resp = client.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Updated Post', html)

    def test_delete_post(self):
        """Test POST /posts/[post-id]/delete route."""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Sample Post', html)


if __name__ == "__main__":
    TestCase.main()
