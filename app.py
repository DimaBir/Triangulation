#!flask/bin/python
import json
from flask import Flask, abort, request
from main import calculate_triangulation

app = Flask(__name__)


@app.route('/api/geo-positioning', methods=['POST'])
def triangulate():
    content = request.get_json()

    clusters = calculate_triangulation(reports=content)

    if len(clusters) == 0:
        abort(404)

    return json.dumps(clusters)


if __name__ == '__main__':
    app.run(debug=True)
