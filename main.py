from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Load Stable Diffusion model on GPU with float16
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# Optional: reduce memory usage if needed
pipe.enable_attention_slicing()

# Request schema
class PromptRequest(BaseModel):
    prompt: str

# POST endpoint
@app.post("/generate")
async def generate_image(data: PromptRequest):
    prompt = data.prompt
    os.makedirs("outputs", exist_ok=True)

    # Generate image with faster config
    image = pipe(
        prompt,
        num_inference_steps=25,   # Speed-quality trade-off
        guidance_scale=7.5        # Creativity control
    ).images[0]

    filename = f"outputs/{uuid.uuid4()}.png"
    image.save(filename)

    return {"image_url": f"http://localhost:8000/outputs/{os.path.basename(filename)}"}
