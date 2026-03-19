import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "..", ".config")
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")

for folder in [CONFIG_DIR, MODELS_DIR, STATIC_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

sys.path.append(CONFIG_DIR)

def bootstrap():
    if not os.listdir(CONFIG_DIR):
        subprocess.check_call([
            sys.executable, "-m", "pip", 
            "install", 
            "--target", CONFIG_DIR, 
            "fastapi", "uvicorn", "llama-cpp-python", "pydantic"
        ])

bootstrap()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llama_cpp import Llama
import uvicorn

app = FastAPI()

model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith(".gguf")]
if model_files:
    model_path = os.path.join(MODELS_DIR, model_files[0])
    llm = Llama(model_path=model_path, n_ctx=2048)
else:
    llm = None

class ChatRequest(BaseModel):
    prompt: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not llm:
        return {"error": "No .gguf model found in models directory"}
    
    output = llm(
        f"User: {request.prompt}\nAI:", 
        max_tokens=128, 
        stop=["User:", "\n"]
    )
    return {"answer": output["choices"][0]["text"]}

@app.get("/api/status")
async def status():
    return {
        "status": "online",
        "model_loaded": llm is not None,
        "config_path": CONFIG_DIR
    }

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
