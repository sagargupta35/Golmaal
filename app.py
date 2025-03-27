from flask import Flask, request, jsonify
from sagar.my_object.object import Environment

app = Flask(__name__)

@app.route("/", methods=['GET'])
def welcome():
    return "Om Sai Ram"

@app.route('/evaluate', methods=['POST'])
def receive_data():
    data = request.json  # Get JSON data from request
    code = data.get('message', None)
    if not code:
        return jsonify({'Error': "Code bhej chodu"})
    env = Environment()
    return jsonify({"message": "Data received successfully!", "data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Allow external access