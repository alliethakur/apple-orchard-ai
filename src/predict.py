import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import json
import torch.nn as nn
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load disease info from JSON
with open(BASE_DIR / "src" / "diseases.json", "r", encoding="utf-8") as f:
    disease_info = json.load(f)

# Class names must match training order
class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot", 
    "Apple___Cedar_apple_rust",
    "Apple___healthy"
]

# Image transform - same as training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def load_model(model_path):
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 4)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    return model

def predict(image, model):
    # Accept either a path/file-like object or an already-opened PIL Image
    if not isinstance(image, Image.Image):
        image = Image.open(image).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    
    # Get prediction
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

if __name__ == "__main__":
    model = load_model(BASE_DIR / "data" / "apple_disease_model_v2.pth")
    print("Model loaded successfully!")
    print("Predict function ready!")