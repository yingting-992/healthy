import os
from dotenv import load_dotenv
import google.generativeai as generativeai

load_dotenv()

generativeai.configure(api_key=os.getenv('api_key'))
response=generativeai.GenerativeModel('gemini-2.0-flash-exp').generate_content('掰掰')
print(response.text)