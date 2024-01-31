from flask import jsonify , abort , make_response , request, url_for
from .app import app
from .models import tasks
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