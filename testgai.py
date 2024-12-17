import os
import google.generativeai as generativeai

generativeai.configure(api_key="AIzaSyAFWUnppV2fjKko5uqTVOVMbZRknBbSpwA")
response = generativeai.GenerativeModel('gemini-2.0-flash-exp').generate_content('你好?')
print(response.text)