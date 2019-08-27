#!flask/bin/python
import json
from flask import Flask, jsonify, abort, request
from main import calculate_triangulation

app = Flask(__name__)

# Global dictionary as JSON
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/api/geo-positioning', methods=['POST'])
def triangulate():
    content = request.get_json()

    clusters = calculate_triangulation(reports=content, use_new=True)
    if clusters is None:
        return json.dumps('EMPTY')
    if len(clusters) == 0:
        abort(404)

    return json.dumps(clusters)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    clusters = calculate_triangulation()

    # task = [task for task in tasks if task['id'] == task_id]
    if len(clusters) == 0:
        abort(404)

    return json.dumps(clusters)


if __name__ == '__main__':
    app.run(debug=True)