from flask import Flask, request, jsonify
from flask_cors import CORS
from services.nlu_service import extract_intent_and_entities
from services.gemini_service import generate_gemini_response
from services.autogen_service import generate_autogen_response
from models.task_handler import TaskHandler
from utils.evaluator import Evaluator

app = Flask(__name__)
CORS(app)

task_handler = TaskHandler()
evaluator = Evaluator()

@app.route('/assistant', methods=['POST'])
def assistant():
    user_input = request.json['input']
    intent, entities = extract_intent_and_entities(user_input)
    
    if intent in ['schedule', 'reminder', 'information']:
        response = task_handler.handle_task(intent, entities)
    else:
        gemini_response = generate_gemini_response(user_input)
        autogen_response = generate_autogen_response(user_input)
        response = f"Gemini: {gemini_response}\nAutogen: {autogen_response}"
    
    evaluator.evaluate(user_input, response, "Expected output")  # You'd need to define expected outputs
    
    return jsonify({'response': response})

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(evaluator.get_metrics())

if __name__ == '__main__':
    app.run(port=5000,debug=True)