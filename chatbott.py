from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)

class SimpleChatbot:
    def __init__(self):
        # Roman Urdu to English mapping
        self.urdu_mapping = {
            'salam': 'hello', 'assalamualaikum': 'hello', 'hello': 'hello',
            'programs kya hain': 'what programs', 'courses koun se hain': 'what courses',
            'bs ke bare mein': 'about bs', 'ms ki information': 'ms information',
            'admission kaise lein': 'how to get admission', 'apply karna hai': 'want to apply',
            'merit list kab aayegi': 'when merit list', 'last date kya hai': 'what is last date',
            'result kab aayega': 'when result', 'khuda hafiz': 'goodbye'
        }
        
        self.responses = {
            "program": "🎓 We offer: BS Computer Science, BS Software Engineering, BS IT, MS Computer Science, MS Data Science, MPhil Computer Science",
            "admission": "📝 Admission Process:\n1. Fill online form\n2. Upload documents\n3. Pay fee\n4. Entry test\n5. Check merit list",
            "merit": "🏆 Merit lists announced on university website 2 weeks after entry test",
            "deadline": "⏰ Deadlines:\n• BS: August 30\n• MS: July 30\n• MPhil: September 1",
            "result": "📊 Results uploaded to student portal within 1 week of test",
            "schedule": "📅 Class schedules available on student portal",
            "greeting": "Hello! 👋 I'm your admission assistant. How can I help you today?",
            "default": "🤔 I can help with: Programs, Admission, Deadlines, Merit, Results, Schedules"
        }
    
    def process_roman_urdu(self, text):
        """Convert Roman Urdu to English"""
        text_lower = text.lower()
        for urdu, english in self.urdu_mapping.items():
            if urdu in text_lower:
                return english
        return text_lower
    
    def get_intent(self, text):
        """Simple rule-based intent classification"""
        text = text.lower()
        
        if any(word in text for word in ['hello', 'hi', 'salam', 'hey']):
            return "greeting"
        elif any(word in text for word in ['program', 'course', 'degree', 'bs', 'ms', 'mphil']):
            return "program"
        elif any(word in text for word in ['admission', 'apply', 'procedure', 'process']):
            return "admission"
        elif any(word in text for word in ['merit', 'list', 'selection']):
            return "merit"
        elif any(word in text for word in ['deadline', 'date', 'last date']):
            return "deadline"
        elif any(word in text for word in ['result', 'test', 'exam']):
            return "result"
        elif any(word in text for word in ['schedule', 'timetable', 'class time']):
            return "schedule"
        else:
            return "default"
    
    def get_response(self, message):
        """Get chatbot response"""
        # Convert Roman Urdu to English
        english_text = self.process_roman_urdu(message)
        
        # Detect intent
        intent = self.get_intent(english_text)
        
        # Get response
        return self.responses.get(intent, self.responses["default"])

# Initialize chatbot
chatbot = SimpleChatbot()

@app.route('/')
def home():
    return "Chatbot API is running!"

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        response = chatbot.get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

@app.route('/api/upload_pdf', methods=['POST'])
def upload_pdf():
    return jsonify({'response': '📄 PDF upload feature available in premium version'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)