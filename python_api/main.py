from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/v1/{url:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def api_proxy(request: Request, url: str):
    base_url = f"https://api.openai.com/v1/{url}"

    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'} 

    if request.method == "GET":
        response = requests.get(base_url, params=request.query_params, headers=headers)
    elif request.method == "POST":
        response = requests.post(base_url, json=await request.json(), headers=headers)
    elif request.method == "PUT":
        response = requests.put(base_url, json=await request.json(), headers=headers)
    elif request.method == "DELETE":
        response = requests.delete(base_url, headers=headers)

    else:
        return JSONResponse(status_code=405, content="Method not supported")

    return Response(content=response.content, status_code=response.status_code,
                    headers=dict(response.headers))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5175)