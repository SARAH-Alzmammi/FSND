import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app)
  CORS(app)

  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods','POST, GET, OPTIONS, DELETE, PATCH ')
      return response

  # @TODO:  
  # Create an endpoint to handle GET requests 
  # for all available categories.
    
  @app.route('/categories')
  def categories():
    categories = Category.query.all()
    formatted_categories= [c.format() for c in categories ]
    return jsonify({  
      "success": True,
      "categories":formatted_categories,
      "total_categories":len(formatted_categories) }

 )

  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 
  @app.route('/questions', methods=['GET'])
  def get_questions():
    items_limit = request.args.get('limit', 10, type=int)
    selected_page = request.args.get('page', 1, type=int)
    current_index = selected_page - 1
    questions = Question.query.order_by(Question.id).limit(items_limit).offset(current_index * items_limit).all()
    formatted_questions= [q.format() for q in questions]
    return jsonify({
      "success": True,
      "questions":formatted_questions,
      "total_questions":len(formatted_questions)
      })
        
  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 

  # @TODO: 
  # Create an endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])

  def delete_question(question_id):
    try:
      Question.query.filter_by(id=question_id).delete()
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return jsonify ({
      "success": True,
      "message": f'question with id {question_id} has been deleted successfully'
      })

  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 

  # @TODO: 
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.
  @app.route('/questions', methods=['POST'])
  def create_questions():
    new_q =Question( 
      question = request.args.get('question'),
      answer = request.args.get('answer'),
      category = request.args.get('category'),
      difficulty = request.args.get('question')
) 
    try:
      data =new_q
      db.session.add(data)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

    return jsonify ({
      "success": True,
      "message": f'question with id {question_id} has been created successfully'
      })

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  

  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 
  @app.route('/question/search/<search_term>', methods=['POST'])
  def search_questions(search_term):
   form=request.form
   search_value = form['search_term']
   search = "% %".format(search_value)
   response = Question.query.filter(Question.name.ilike(search).all())
   formatted_questions= [q.format() for q in response]

   return jsonify ({
      "success": True,
      "questions":formatted_questions
      })

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
 
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 

  @app.route('/questions/category/<int:category_id>', methods=['GET'])
  def get_questions_baseOnC(category_id):
    
     data=Question.query.filter(category_id == Question.category).all()
     formatted_questions= [q.format() for q in data]
     return jsonify({
      "success": True,
      "questions":formatted_questions,
      "message": f'question with category : {Question.category} is showing'
      })


  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
 
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 
  
  
  @app.route('/questions/play/<int:category_id>/<int:question_id>', methods=['GET'])
  def get_questions_play(category_id,question_id):
  
     data=Question.query.filter(category_id == Question.category).all()
     
     if question_id != data[question_id]:
      random_q = random.sample(data, 4)
      formatted_questions= [q.format() for q in random_q]
      return jsonify({
        "success": True,
        "questions":formatted_questions
        })
     else:
      return jsonify({
      "success": False,
      })
  

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
 
  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message":"resource not found"
    }),404
  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message":"unprocessable"
    }),422
  
  return app

    