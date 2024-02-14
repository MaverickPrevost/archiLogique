from flask import jsonify , abort , make_response , request, url_for
from .app import app
from .models import tasks
from models import db
from models import Questionnaire, Question, Answer
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task',task_id = task['id'],_external = True)
        else:
            new_task[field] = task[field]
    return new_task
@app.route('/tasks', methods = ['GET'])
def get_tasks():
    return jsonify(tasks =[ make_public_task(t) for t in tasks])

@app.route('/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({"task": make_public_task(task[0])})

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    
    if len(task) == 0:
        abort(404)
    
    if not request.json:
        abort(400)
    
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    
    if 'description' in request.json and not isinstance(request.json['description'], str):
        abort(400)
    
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)
    
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    
    return jsonify({'task': make_public_task(task[0])})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    
    tasks.remove(task[0])
    
    return jsonify({'result': True})

@app.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    questionnaires = Questionnaire.query.all()
    return jsonify([q.to_json() for q in questionnaires])

@app.route('/questionnaires', methods=['POST'])
def create_questionnaire():
    data = request.get_json()
    title = data.get('title')
    if title:
        questionnaire = Questionnaire(title=title)
        db.session.add(questionnaire)
        db.session.commit()
        return jsonify({'message': 'Questionnaire created successfully'}), 201
    else:
        return jsonify({'error': 'Title is required'}), 400

@app.route('/questionnaires/<int:questionnaire_id>', methods=['PUT'])
def update_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
    data = request.get_json()
    title = data.get('title')
    if title:
        questionnaire.title = title
        db.session.commit()
        return jsonify({'message': 'Questionnaire updated successfully'})
    else:
        return jsonify({'error': 'Title is required'}), 400

@app.route('/questionnaires/<int:questionnaire_id>', methods=['DELETE'])
def delete_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({'message': 'Questionnaire deleted successfully'})

@app.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    content = data.get('content')
    question_type = data.get('question_type')
    questionnaire_id = data.get('questionnaire_id')
    if content and question_type and questionnaire_id:
        question = Question(content=content, question_type=question_type, questionnaire_id=questionnaire_id)
        db.session.add(question)
        db.session.commit()
        return jsonify({'message': 'Question created successfully'}), 201
    else:
        return jsonify({'error': 'Content, question type, and questionnaire ID are required'}), 400

@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    content = data.get('content')
    question_type = data.get('question_type')
    if content and question_type:
        question.content = content
        question.question_type = question_type
        db.session.commit()
        return jsonify({'message': 'Question updated successfully'})
    else:
        return jsonify({'error': 'Content and question type are required'}), 400

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted successfully'})

@app.route('/answers', methods=['POST'])
def create_answer():
    data = request.get_json()
    content = data.get('content')
    question_id = data.get('question_id')
    if content and question_id:
        answer = Answer(content=content, question_id=question_id)
        db.session.add(answer)
        db.session.commit()
        return jsonify({'message': 'Answer created successfully'}), 201
    else:
        return jsonify({'error': 'Content and question ID are required'}), 400

@app.route('/answers/<int:answer_id>', methods=['PUT'])
def update_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    data = request.get_json()
    content = data.get('content')
    if content:
        answer.content = content
        db.session.commit()
        return jsonify({'message': 'Answer updated successfully'})
    else:
        return jsonify({'error': 'Content is required'}), 400

@app.route('/answers/<int:answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    db.session.delete(answer)
    db.session.commit()
    return jsonify({'message': 'Answer deleted successfully'})