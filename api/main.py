from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import json
import torch.nn as nn
import io
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Apple Orchard AI", version="1.0")

# CORS - allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load disease info
with open(BASE_DIR / "src" / "diseases.json", "r", encoding="utf-8") as f:
    disease_info = json.load(f)

# Class names
class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy"
]

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Load model once at startup
def load_model():
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 4)
    model.load_state_dict(torch.load(BASE_DIR / "data" / "apple_disease_model_v2.pth",
                                      map_location="cpu"))
    model.eval()
    return model

model = load_model()

@app.get("/")
def home():
    return {"message": "Apple Orchard AI is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Transform and predict
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)
        confidence, predicted = probs.max(1)
    
    disease = class_names[predicted.item()]
    confidence = confidence.item() * 100
    info = disease_info[disease]
    
    return {
        "disease": disease,
        "local_name": info["local_name"],
        "confidence": f"{confidence:.2f}%",
        "description": info["description"],
        "treatment": info["treatment"],
        "prevention": info["prevention"],
        "season": info["season"]
    }