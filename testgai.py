import os
import google.generativeai as generativeai

generativeai.configure(api_key="AIzaSyDB7MIvqNNHcBlxcB62E4nlOwCvpx6u8LI")
response=generativeai.GenerativeModel('gemini-2.0-flash-exp').generate_content('掰掰')
print(response.text)