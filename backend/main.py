import json
import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/generatePost/")
async def generatePost(request: Request):
    data = await request.json()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="Missing GROQ_API_KEY")

    prompt = f"""
    You are a professional LinkedIn content writer.

    Role: {data.get('role', '')}
    Tone: {data.get('tone', '')}
    Purpose: {data.get('purpose', '')}
    Key Highlights: {data.get('highlights', '')}
    Insights/Learnings: {data.get('insights', '')}
    Gratitude: {data.get('gratitude', '')}
    Tags: {data.get('tags', '')}
    Resources: {data.get('resources', '')}
    Reflection: {data.get('reflection', '')}
    Call to Action: {data.get('cta', '')}
    Hashtags: {data.get('hashtags', '')}
    Extras: {data.get('extras', '')}
    """

    payload = json.dumps({
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.3
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post(url, headers=headers, data=payload, timeout=30)

    try:
        groq_response = response.json()
        print("Groq Response:", groq_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if "choices" not in groq_response:
        return {"post": "⚠️ Unable to generate post. Please try again."}

    generated_post = groq_response['choices'][0]['message']['content']

    return {"post": generated_post.strip()}