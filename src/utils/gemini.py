from dotenv import load_dotenv
from os import getenv
from PIL import Image
import google.generativeai as genai

load_dotenv()

gemini_api = getenv('GEMINI_API')
genai.configure(api_key=gemini_api)

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def gemini_response(img: Image, text:str):
    print('Prompting model ...')
    model = genai.GenerativeModel('gemini-pro-vision')
    reponse = model.generate_content(
        [text,img],
        safety_settings=safety_settings
    )
    return reponse.text
