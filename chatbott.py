from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import os

app = Flask(__name__)
CORS(app)

class UniversityChatbot:
    def __init__(self):
        # Load all data from single JSON file
        self.data = self.load_data('../data/roman_urdu_mapping.json')
        print("🤖 Chatbot initialized with single JSON data file")

    def load_data(self, file_path):
        """Load JSON data from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}

    def convert_roman_urdu_to_english(self, text):
        """Convert Roman Urdu phrases to English"""
        text_lower = text.lower()
        
        # Check all Roman Urdu mappings
        roman_urdu_data = self.data.get('roman_urdu_mapping', {})
        for category, phrases in roman_urdu_data.items():
            for urdu_phrase, english_phrase in phrases.items():
                if urdu_phrase in text_lower:
                    return english_phrase
        
        # Special handling for common patterns
        if any(word in text_lower for word in ['kon', 'koun', 'konsa', 'kaun']):
            if any(word in text_lower for word in ['program', 'course']):
                return "which programs do you offer"
        
        if 'kwa rha' in text_lower or 'chala rha' in text_lower:
            return "offering programs"
        
        return text_lower

    def detect_intent(self, text):
        """Detect user intent"""
        english_text = self.convert_roman_urdu_to_english(text)
        
        print(f"🔍 Debug: '{text}' → '{english_text}'")
        
        if any(word in english_text for word in ['hello', 'hi', 'hey', 'salam']):
            return "greeting"
        elif any(word in english_text for word in ['program', 'course', 'degree', 'bs', 'ms', 'mphil', 'offer']):
            return "programs"
        elif any(word in english_text for word in ['admission', 'apply', 'procedure', 'process']):
            return "admission"
        elif any(word in english_text for word in ['merit', 'list', 'selection']):
            return "merit"
        elif any(word in english_text for word in ['deadline', 'date', 'last date']):
            return "deadline"
        elif any(word in english_text for word in ['result', 'test', 'exam']):
            return "result"
        elif any(word in english_text for word in ['schedule', 'time', 'timetable']):
            return "schedule"
        elif any(word in english_text for word in ['contact', 'email', 'phone']):
            return "contact"
        else:
            return "default"

    def get_response(self, message):
        """Get chatbot response"""
        try:
            intent = self.detect_intent(message)
            responses = self.data.get('chatbot_responses', {})
            
            if intent == "programs":
                programs_data = self.data.get('programs', {})
                response = "🎓 **Programs Offered:**\n\n"
                
                for program_type, program_list in programs_data.items():
                    if program_list:
                        response += f"**{program_type.upper().replace('_', ' ')}:**\n"
                        for program in program_list:
                            response += f"• {program}\n"
                        response += "\n"
                
                response += "Which program are you interested in?"
                
            elif intent == "admission":
                admission_data = self.data.get('admission_data', {})
                procedure = admission_data.get('procedure', [])
                response = "📝 **Admission Process:**\n\n"
                
                for i, step in enumerate(procedure, 1):
                    response += f"{i}. {step}\n"
                    
            elif intent == "merit":
                merit_dates = self.data.get('admission_data', {}).get('merit_dates', {})
                response = f"🏆 Merit lists are announced on:\n"
                response += f"• BS: {merit_dates.get('bs_merit_date', 'TBA')}\n"
                response += f"• MS: {merit_dates.get('ms_merit_date', 'TBA')}\n"
                response += f"• MPhil: {merit_dates.get('mphil_merit_date', 'TBA')}\n"
                response += "Check university website → Admissions → Merit List"
                
            elif intent == "deadline":
                deadlines = self.data.get('admission_data', {}).get('deadlines', {})
                response = "⏰ **Application Deadlines:**\n\n"
                for program, date in deadlines.items():
                    response += f"• {program}: {date}\n"
                    
            else:
                response = responses.get(intent, responses.get('default_response', 'I can help you with university admission information.'))
            
            # Add language detection note
            if any(word in message.lower() for word in ['kon', 'kya', 'kab', 'kaise', 'salam', 'kwa']):
                response += "\n\n💡 *Roman Urdu input detected*"
                
            return response
            
        except Exception as e:
            print(f"Error: {e}")
            return "I apologize for the error. Please try rephrasing your question."

# Initialize chatbot
chatbot = UniversityChatbot()

@app.route('/')
def home():
    return jsonify({
        "message": "University Admission Chatbot API",
        "status": "running",
        "data_source": "Single JSON file"
    })

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        
        if not user_message:
            return jsonify({'response': 'Please provide a message'})
        
        response = chatbot.get_response(user_message)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'response': 'Sorry, I encountered an error. Please try again.'})

if __name__ == '__main__':
    print("🚀 Starting University Admission Chatbot...")
    print("📍 Server: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
