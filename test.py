
import unittest
from app import app
from models import User, Feedback, db

class BaseTestCase(unittest.TestCase):
    """A base test case"""

    def setUp(self):
        db.create_all()
        db.session.add(User(username="jman1276", password="jman1276", email="jman1276@gmail.com", first_name="joe", last_name="schmoe"))
        db.session.add(Feedback(title="fb 1", content="why didn't you spell out feedback", username="jman1276"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class FlaskTestCase(BaseTestCase):
    def test_index(self):
        with app.test_client() as client:
            res = client.get('/', content_type="html/text")
            self.assertEqual(res.status_code, 200)

    def test_index_redirect(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "/register")
            self.assertIn('<h1 class="display-1">Sign Up</h1>', html)

    def test_login_form(self):
        with app.test_client() as client:
            res = client.get("/login")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-1">Login</h1>', html)

    def test_login_form_post(self):
        with app.test_client() as client:
            d = {"username": "jman1276", "password": "jman1276"}
            resp = client.post("/login", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)  # Corrected status_code
            self.assertIn('Welcome Back, jman1276!', html)

    def test_registration_form(self):
        with app.test_client() as client:
            res = client.get("/register")  # Corrected "/registration" to "/register"
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<input name="username"', html)

    def test_registration_form_post(self):
        with app.test_client() as client:
            d = {"username": "jgirl1276", "password": "jgirl1276", "email": "jgirl1276@gmail.com", "first_name": "jane", "last_name": "schmoe"}
            resp = client.post("/register", data=d, follow_redirects=True)  # Corrected "/login" to "/register"
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)  # Corrected status_code
            self.assertIn('Welcome! Successfully Created Your Account!', html)

if __name__ == '__main__':
    unittest.main()
