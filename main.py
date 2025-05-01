from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    use_auth_token=True
).to("cpu")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_image(data: PromptRequest):
    prompt = data.prompt
    image = pipe(prompt).images[0]
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{uuid.uuid4()}.png"
    image.save(filename)
    return {"image_url": f"http://localhost:8000/{filename}"}
