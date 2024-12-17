import os
import google.generativeai as generativeai
import dotenv

dotenv.load_dotenv

api_key = os.getenv("gemini_api_key")
generativeai.configure(api_key=api_key)
response = generativeai.GenerativeModel("gemini-2.0-flash-exp").generate_content("你所得到的資訊最新的是什麼時候的?")
print(response.text)