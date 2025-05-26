from flask import Flask, render_template, request, jsonify
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Initialize Vertex AI
vertexai.init(project=os.getenv("GCP_PROJECT"), 
              location=os.getenv("GCP_REGION"))
model = GenerativeModel("MODEL_NAME")
chat = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    try:
        # Get text input from frontend
        data = request.get_json()
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({"error": "No text input provided"}), 400

        # Get Gemini response
        response = chat.send_message(user_input)
        model_reply = response.text
        app.logger.debug(f"Gemini replied: {model_reply}")

        return jsonify({
            "user_input": user_input,
            "response": model_reply
        })

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)