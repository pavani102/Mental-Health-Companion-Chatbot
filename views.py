from django.shortcuts import render
from django.conf import settings
import google.generativeai as genai
import json
import re

# Configure Gemini with your API key
genai.configure(api_key="AIzaSyCjEKiH-Qk62LMN0sm25LnPwRKbPYCV_vY")

# Load Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')


# Helper to extract JSON safely
def extract_json(text):
    try:
        json_str = re.search(r'\{.*\}', text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception as e:
        print("JSON extraction error:", e)
        return None


def detect_emotion_with_gemini(user_input):
    prompt = f"""
You are a mental health support assistant. Your job is to detect the emotion from the user's message 
and provide a short, comforting message.

User input: "{user_input}"

Only reply with valid JSON. Do not add anything else.

Format:
{{
  "emotion": "<emotion>",
  "response": "<supportive message>"
}}
"""

    try:
        response = model.generate_content(prompt)
        print("Gemini raw response:", response.text)  # Debug

        result = extract_json(response.text.strip())
        if result:
            return result.get("emotion"), result.get("response")

    except Exception as e:
        print("Gemini API error:", e)

    return None, None


def home(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        if user_input:
            emotion, response = detect_emotion_with_gemini(user_input)
            if emotion and response:
                return render(request, 'example.html', {
                    'emotion': emotion,
                    'response': response
                })
            else:
                return render(request, 'example.html', {
                    'error': "Sorry, I couldn't understand your emotion. But I'm here for you 💙"
                })

    return render(request, 'example.html')
