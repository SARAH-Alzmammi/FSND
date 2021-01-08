import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "testing"
        self.database_path =  "postgres://postgres:password@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.searchTerm = 'Taj'
        self.new_q ={
            "question" : "test Question",
            "answer":"test answer",
            "category": "test Art ",
            "difficulty": "very hard"

}


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)




    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],1)
 
    def test_delete_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        question =  Question.query.filter(Question.id ==1).one_or_none()
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],1)

  
    def test_create_questions(self):
        res = self.client().get('/questions',json = self.new_q)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],1)
        
        
    def test_search_question(self):
        res = self.client().get(f'/questions/search/{self.searchTerm}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

  
    def test_get_questions_baseOnC(self):
        res = self.client().get('/questions/category/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_get_questions_play(self):
        res = self.client().get('/questions/play/2/3')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)


     
        
    def test_404(self):
        
        res = self.client().get('/questions/oiu')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        
    # def test_422(self):
        # I did not know how to raise this kind of error so I comment it out
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code,422)
    #     self.assertEqual(data['message'],'unprocessable')


        
       


        
       



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()