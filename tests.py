from unittest import TestCase

from app import app, db
from models import User, Post, DEFAULT_IMG_URL

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)


    def test_display_user_listing(self):
        with self.client as c:
            resp = c.get('/', follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<!-- Display Users -->', html)


    def test_create_new_user(self):
        with self.client as c:
            resp = c.post('/users/new', follow_redirects = True,
                data =
                {'first_name': 'test_test',
                'last_name': 'test_test',
                'image_url': DEFAULT_IMG_URL})

            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_test', html)


    def test_update_user_profile(self):
        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/edit", follow_redirects = True,
                data =
                {'first_name': 'new_test_name',
                'last_name': 'new_test_name',
                'image_url': DEFAULT_IMG_URL})

            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new_test_name', html)
            # can check if old name isnt there assertNotIn
# Different assert checks?!?!?!

    def test_delete_user(self):
        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/delete", follow_redirects = True)

            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("was successfully deleted.", html)

    # test removing image and see if default image loads




class PostViewTestCase(TestCase):
    """Test posts for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete() # we delete posts first to have a clean slate and prevent referential errors
        User.query.delete()

        self.client = app.test_client()



        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        first_test_post = Post(title="test_title1", content="test_content", user_id = test_user.id)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)

        second_test_post = Post(title="test_title2", content="test_content", user_id = second_user.id)


        db.session.add_all([test_user, second_user])
        db.session.add_all([first_test_post, second_test_post])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = first_test_post.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_display_post_form(self):
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/posts/new', follow_redirects = True)
            html = resp.get_data(as_text = True)

            breakpoint()

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<!-- Create a new post -->', html)

    def test_handle_add_form(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/posts/new', follow_redirects = True,
                data={"title":"test_title", "content":"test_content"})
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_title', html)

    def test_delete_post(self):
        with self.client as c:
            resp = c.post(f'/posts/{self.post_id}/delete', follow_redirects = True)

            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('test_title1', html)


