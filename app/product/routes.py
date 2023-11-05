from . import product_blueprint as product
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import Product



@product.post('/new')
@jwt_required()
def create_a_product(): 
    body = request.json

    if body is None: 
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    name = body.get("name")
    if name is None or name == "":
        response = {
            "message": "invalid request"
        }

        return response, 400
    
    description = body.get("description")
    if description is None or description == "":
        response = {
            "message": "invalid request"
        }

        return response, 400
    
    existing_product = Product.query.filter_by(name = name).one_or_none()
    if existing_product is not None: 
        response={
            "message": "that name is already in use"
        }

        return response, 400
    
    product = Product(name = name, description = description, created_by =current_user.id)
    product.create()

    response = {
        "message": "successfully created quiz", 
        "product": product.to_response()
    }

    return response, 201
  

@product.get('/all')
@jwt_required()
def handle_get_all_products(): 
    products = Product.query.all()
    response = {
        "message": "products retrieved", 
        "products": [product.to_response() for product in products]
    }

    return response, 200 

@product.get('/<product_id>')
@jwt_required()
def handle_get_one_quiz(quiz_id):
    quiz = Product.query.filter_by(id=quiz_id).one_or_none()
    if quiz is None: 
        response = {
            "message" : "quiz does not exist"
        }

        return response, 404

    response = {
        "message": "quiz found",
        "quiz" : product.to_response()
    }
    return response , 201

@product.delete('/product/<product_id>')
@jwt_required()
def handle_delete_quiz(quiz_id): 
    product = Product.query.filter_by(id=quiz_id).one_or_none()
    if product is None: 
        response = {
            "message" : "quiz does not exist"
        }

        return response, 404

    if product.created_by != current_user.id: 
        response = {
            "message": "you cant delete someone elses quiz"
        }
        return response, 401
    
    product.delete()

    response = {
        "message": f"quiz {product.id} deleted"
    }

    return response, 200

@product.post("/<quiz_id>/add-question")
@jwt_required
def handle_add_question(product_id): 
    body = request.json
    if body is None:
        response ={
        "message" : "quiz not found"
        }

        return response, 404
    

    product = Product.query.filter_by(id=product_id).one_or_none()
    if product is None: 
        response = {
            "message": "quiz not found"
        }
        return response, 404
    
    if product.created_by != current_user.id: 
        response ={
            "message": "you cant add questions to someone elses quiz"
        
        }
        return response, 401
    
    prompt = body.get("prompt")
    opt_one= body.get("option_one")
    opt_two= body.get("option_two")
    opt_three= body.get("option_three")
    answer = body.get("answer")

    if all([prompt, opt_one, opt_two, opt_three, answer]):
        response = {
            "message": "invalid request"
        }

        return response, 400
    question = Product(prompt = prompt, option_one = opt_one, option_two = opt_two, option_three = opt_three, answer = answer, quiz_id = product.id):
    question.create()

    product.questions.append(question)
    product.update()


    response = {
        "message" : "question added", 
        "quiz" : product.to_response()
    }

    return response , 201

@product.delete('</question/question_id>')
@jwt_required()
def handle_delete_question(question_id): 
    question = Question.query.filter_by(id=question_id).one_or_none()
    if Question is None: 
        response = {
            "message": "question does not exist"
        }

        return response, 404
    if question.quiz.author.id != current_user.id:
        response = {
            "message": "unauthorized"
        }

        return response , 401
    
    quiz_id = question.quiz.id 
    
    updated_questions = [q for q in question.quiz.questions if q.id != question_id]
    question.quiz.questions = updated_questions


    question.delete()

    quiz = Product.query.filter_by(id = quiz_id).first()
    response = {
        "message": "question deleted",
        "quiz": quiz.to_response()
    }
    return response, 200

@product.put('/update/quiz/<quiz_id>')
def handle_update_quiz(product_id): 
    body = request.json

    product = Product.query.filter_by(id = product_id)
    if product is None:
        response = {
        "message" : "not found"
        }
        return response, 404
    
    if product.created_by != current_user.id:
        response = {"message":"no sir/maam"}
        return response, 401

    product.title=body.get('title', product.title)
    product.description = body.get('description', product.description)

    product.update()

    response = {
        "message": "product updated", 
        "product": product.to_response()

    }
    return response , 200
