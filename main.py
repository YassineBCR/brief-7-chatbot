import sys
sys.path.append("../../")
import json
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Set the API key and the headers
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzNmYWJhNGUtZDE1NS00N2M4LThjNzUtMGMyNDU5Mjk1ZmQwIiwidHlwZSI6ImFwaV90b2tlbiJ9.xgPtY8eTTtMfNUi-9MKE2cB8PDehR-B2kczHpfPxCs0"}
provider = "meta"
url = "https://api.edenai.run/v2/text/chat"

# Scraping all the text of my website and remove the leading and trailing whitespaces with strip()
response = requests.get("http://localhost:8001")
soup = BeautifulSoup(response.content, "html.parser")
site_content = soup.get_text().strip()

app = FastAPI()

# Allow CORS
origins = ["http://localhost", "http://localhost:8001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict this to specific HTTP methods if needed
    allow_headers=["*"],  # You can restrict this to specific headers if needed
)

@app.get("/test/{prompt}")
async def read_item(prompt):
    return {"It works"}


@app.post("/{prompt}")
async def bot_request(prompt):
    site_content = soup.get_text().strip()

    payload = {
        "providers": provider,
        "text": "",
        "chatbot_global_action": f"en francais , agir en tans que Yassine le proriétaire du site dont voici le contenue: {site_content}",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": ""
    }

    payload['text'] = prompt

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)[provider]

    payload['previous_history'].append(result['message'][0])
    payload['previous_history'].append(result['message'][1])

    return result['generated_text']

uvicorn.run(app)