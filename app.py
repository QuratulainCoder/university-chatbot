from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbott import UniversityChatbot
import os

app = Flask(__name__)
CORS(app)
chatbot = UniversityChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = chatbot.process_message(user_message)
    return jsonify({'response': response})

@app.route('/api/voice', methods=['POST'])
def voice_chat():
    # Handle voice input (you can extend this)
    return jsonify({'response': 'Voice feature in development'})

@app.route('/api/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file'})
    
    pdf_file = request.files['pdf']
    if pdf_file.filename.endswith('.pdf'):
        pdf_path = f"uploads/{pdf_file.filename}"
        pdf_file.save(pdf_path)
        response = chatbot.pdf_processor.load_pdf(pdf_path)
        return jsonify({'response': response})
    
    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, port=5000)
