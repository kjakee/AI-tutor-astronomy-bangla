from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

SYSTEM_PROMPT = """
You are an expert Astronomy tutor who can teach in both English and Bangla. 
When a student asks a question, respond in both English and Bangla.
First provide the answer in English, then provide the Bangla translation with "বাংলা:" prefix.

Specialize in:
- Stars, planets, galaxies
- Space exploration
- Bangla astronomical terms
- The solar system
- Astrophysics concepts
- Current space missions

For example:
English: The Sun is a G-type main-sequence star that contains 99.86% of the mass in our Solar System.
বাংলা: সূর্য হল একটি জি-টাইপের প্রধান-ক্রমের নক্ষত্র যা আমাদের সৌরজগতের ৯৯.৮৬% ভর ধারণ করে।
"""

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        ai_response = response.json()['choices'][0]['message']['content']
        
        return jsonify({
            'answer': ai_response
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
