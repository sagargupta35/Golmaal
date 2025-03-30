from flask import Flask, request, jsonify
from sagar.my_object.object import Environment
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_evaluator.evaluator import eval, is_error
from waitress import serve
from flask_cors import CORS
import requests
import threading
import time

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def welcome():
    return "Om Sai Ram"

@app.route('/evaluate', methods=['POST'])
def receive_data():
    data = request.get_json()
    code = data.get("code", None)  
    if not code or not len(code):
        return jsonify({'Error': "Code cannot be empty"})
    env = Environment(print_statements=[])
    l = new_lexer(code)
    p = Parser(l)
    program = p.parse_program()

    if len(p.errors):
        return jsonify({'Error':p.errors})
    
    try:
        evaluated = eval(program, env)
        if is_error(evaluated):
            return jsonify({'Error': evaluated.message, 'Output': env.print_statements})
        return jsonify({
            'Output': env.print_statements
        })
    except Exception as e:
        return jsonify({'Cannot evaluated code (probably an internal error)': e})

@app.route("/ping", methods=["GET"])
def ping():
    print("Someone pinged")
    return {"message": "pong"}, 200


NODE_API_URL = "https://golmaal-x4f5.onrender.com/api/ping"

def ping_node():
    while True:
        try:
            requests.get(NODE_API_URL)
            print("Pinged Node.js API")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)  # 5 minutes

threading.Thread(target=ping_node, daemon=True).start()

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)