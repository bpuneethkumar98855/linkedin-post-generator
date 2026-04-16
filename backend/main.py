import json
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Enable CORS for all origins (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq API endpoint
url = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/generatePost/")
async def generatePost(request: Request):
    data = await request.json()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not set. Add it to backend/.env before starting the server.",
        )

    # Build smart prompt
    prompt = f"""
    You are a professional LinkedIn content writer. Your task is to write an authentic, engaging, and well-structured LinkedIn post using the details below.

    Dont end with like this sentences(Let me know if you need any adjustments!) please end with the hastags and also dont mention what i didnt give you. you have to mention in the post only whatever the user entered in input those things only you have to mention in the output or post and also dont start with Here's a compelling likedin post that grabs attention like that just start with professional lines. dont mention(As a professional LinkedIn content writer, I've crafted a post that meets your requirements. Here's the output:) like this sentences and i gave a role as input you are not including them 
    Use the following inputs to generate the post:

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
    # Prepare request to Groq
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

    # Send request to Groq API
    response = requests.post(url, headers=headers, data=payload)

    try:
        groq_response = response.json()
        print("Groq Response:", groq_response)  # For debugging
    except Exception as e:
        return {"error": f"Failed to parse JSON: {str(e)}"}

    # Handle missing 'choices'
    if "choices" not in groq_response:
        return {"error": f"Groq API Error: {groq_response}"}

    # Extract generated content
    generated_post = groq_response['choices'][0]['message']['content']
    return {"post": generated_post}

