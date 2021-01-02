import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Book

class BookShelfTestCase(unittest.TestCase):
    """This class represents the ___ test case"""

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf"
        self.database_path = "postgresql://{}:{}@{}/{}".format('Yousif', 'yousif','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        #dictionary format
        self.new_book = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables if not exist
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_books(self):
        """Test _____________ """
        res = self.client().get('/books') #get is the method name
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)
        self.assertTrue(res_data['books'])
        self.assertTrue(res_data['total_books'])

    def test_update_book_rating(self):
        book_id = 4
        rating = 4
        res = self.client().patch('/books/{}'.format(book_id), json={'rating': rating})   #patch is the method name
        res_data = json.loads(res.data)

        updated_book = Book.query.get(book_id)
        formated_updated_book = updated_book.format()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)
        self.assertEqual(res_data['book_id'], book_id)
        self.assertEqual(formated_updated_book['rating'], rating)

    def test_create_book(self):
        res = self.client().post('/books', json=self.new_book)  #post is the method name
        res_data = json.loads(res.data)
        created_book = Book.query.order_by(Book.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)
        self.assertEqual(res_data['created'], created_book.id)
        self.assertTrue(res_data['books'])
        self.assertTrue(res_data['total_books'])

    def test_404_page_not_found(self):
        res = self.client().get('/books?page=100')  #get is the method name
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data['success'], False)
        self.assertEqual(res_data['message'], 'Not Found')

    def test_405_not_allowed_action(self):
        book_id = 1
        res = self.client().post('/books/{}'.format(book_id), json=self.new_book) #post is the method name
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(res_data['success'], False)
        self.assertEqual(res_data['message'], 'Not Allowed')

    def test_422_unprocessable_action(self):
        book_id = 100000
        res = self.client().delete('/books/{}'.format(book_id)) #delete is the method name
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data['success'], False)
        self.assertEqual(res_data['message'], 'Unprocessable')

    def test_assert_None(self):
        self.assertFalse(None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()