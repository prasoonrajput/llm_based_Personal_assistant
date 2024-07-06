import autogen
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_AI_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-pro')

class GeminiLLM(autogen.ConversableAgent):
    def __init__(self, name):
        super().__init__(name)

    def generate_reply(self, messages, sender):
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        response = gemini_model.generate_content(prompt)
        return response.text

assistant = GeminiLLM("assistant")

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "coding"},
)

def generate_autogen_response(user_input):
    user_proxy.initiate_chat(
        assistant,
        message=user_input
    )
    return assistant.last_message()["content"]