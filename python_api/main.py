from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import openai
import os
import uvicorn
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/v1/chat/completions")
# async def call_remote_api(data: dict):
#     response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers={'Authorization': 'Bearer '+ os.getenv("OPENAI_API_KEY")})
#     if data['stream'] == True:
#       return concatenate_response(response.text)
#     to_return = json.loads(response.text)
#     return to_return
       

@app.post("/v1/chat/completions")
async def call_remote_api(data: dict):
    if data['stream'] == True:
      response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers={'Authorization': 'Bearer '+ os.getenv("OPENAI_API_KEY")}, stream=True)
      return handle_response(response)
    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers={'Authorization': 'Bearer '+ os.getenv("OPENAI_API_KEY")})
    to_return = json.loads(response.text)
    return to_return

@app.get('/v1/models')
async def list_models():
    response = openai.Model.list()
    return response

def handle_response(r):
    buffer = ""
    for chunk in r.iter_content(chunk_size=1):
        if chunk.endswith(b'\n'):
            data_json = json.loads(buffer)
            if 'data' in data_json:
                data_content = data_json['data']
                if 'choices' in data_content:
                    content = data_content['choices'][0]['delta'].get('content', '')
                    print(f"Received: {content}")
                    if '[DONE]' in content:
                        break
                elif 'error' in data_content:
                    msg = data_content['error'].get('message', '')
                    print(f"Error: {msg}")
                    break
            buffer = ""
        else:
            buffer += chunk.decode()

def concatenate_response(response_text):
  try:
    # Split the response text into separate lines
    response_lines = response_text.split("\n")

    # Initialize an empty string to store the full content
    full_content = ""

    for line in response_lines:
        # Only process line if it starts with 'data:'
        if line.startswith('data:'):
            if line.startswith("data: [DONE]"):
               return full_content
            # Load the JSON object from the line
            data = json.loads(line[5:])

            if line.startswith('error:'):
               return data['error']['message']
            
            # Extract the content string from the JSON object and append it to the full content string
            full_content += data['choices'][0]['delta'].get('content','')

    
    return full_content
  except Exception as e:
     print(e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5175)