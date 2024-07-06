import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_AI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def generate_gemini_response(user_input):
    prompt = f"""
    You are a personal assistant. Understand the user's request and respond appropriately.
    User request: {user_input}
    Assistant: Let me help you with that. 
    """
    
    response = model.generate_content(prompt)
    return response.text