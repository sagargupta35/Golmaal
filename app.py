from flask import Flask, request, jsonify
from sagar.my_object.object import Environment
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_evaluator.evaluator import eval, is_error
from waitress import serve


app = Flask(__name__)

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
        return jsonify({'Parse Error':p.errors})
    
    try:
        evaluated = eval(program, env)
        if is_error(evaluated):
            return jsonify({'Error': evaluated.message})
        return jsonify({
            'Output': '\n'.join(env.print_statements)
        })
    except Exception as e:
        return jsonify({'Cannot evaluated code:': e})


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)