from flask import Flask, render_template, request, jsonify
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Hardcoded configuration
PROJECT_ID = "eight-brothers"  # REPLACE WITH YOUR ACTUAL PROJECT ID
REGION = "us-central1"          # Must be a supported Vertex AI region
MODEL_NAME = "gemini-2.5-flash-preview-05-20" # Current recommended model

def initialize_vertex_ai():
    try:
        vertexai.init(
            project=PROJECT_ID,
            location=REGION
        )
        return GenerativeModel(MODEL_NAME).start_chat(history=[])
    except Exception as e:
        logging.error("Vertex AI initialization failed: %s", e)
        raise

try:
    chat = initialize_vertex_ai()
    logging.info("Vertex AI initialized successfully with model: %s", MODEL_NAME)
except Exception as e:
    logging.error("Service initialization failed: %s", e)
    chat = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    if not chat:
        return jsonify({"error": "Vertex AI service unavailable"}), 503
        
    try:
        data = request.get_json()
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({"error": "No text input provided"}), 400

        response = chat.send_message(user_input)
        return jsonify({
            "user_input": user_input,
            "response": response.text
        })

    except Exception as e:
        logging.error("Error processing request: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
