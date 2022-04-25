from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/tsp', methods=["POST"])
def do_tsp():
    input_json = request.get_json(force=True)
    idList = map(lambda x: x['id'], input_json)
    print(idList)
    return jsonify(list(idList))


if __name__ == '__main__':
    app.run()
