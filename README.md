---
title: Apple Orchard AI
emoji: 🍎
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
---

# 🍎 Apple Orchard AI

AI-powered apple leaf disease detection — built from my family's apple orchards in Himachal Pradesh.

**[Live Demo →](https://alliethakur-apple-orchard-ai.hf.space/)**

![Apple Orchard AI Screenshot](assets/screenshot-hero.png)

## What it does

Upload a photo of an apple leaf, and the model identifies the disease (or confirms it's healthy) with a confidence score, plus treatment and prevention guidance drawn from real orchard practices.

**Detects:**
- Apple Scab
- Black Rot
- Cedar Apple Rust
- Healthy

## Why I built this

Growing up around my family's apple orchards, I saw firsthand how much crop loss comes from late disease detection. This project applies computer vision to a problem I actually understand — giving orchard workers a fast, accessible way to flag issues before they spread.

## See it in action

![Diagnosis result example](assets/screenshot-result.png)

## Tech Stack

- **Model:** EfficientNet-B0 (transfer learning) on the PlantVillage dataset
- **Frontend:** Streamlit, custom warm-minimal UI with a rotating fact ticker
- **Deployment:** Docker on Hugging Face Spaces
- **Tracking:** MLflow for experiment tracking across training runs

## Results

- Near-100% validation accuracy across 2 GPU training runs on Kaggle
- Confidence threshold (60%) to flag unclear/ambiguous images instead of guessing

## Setup (local)

```bash
git clone https://github.com/alliethakur/apple-orchard-ai.git
cd apple-orchard-ai
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Project Structure
apple-orchard-ai/
├── Dockerfile              # HF Spaces deployment config
├── app/streamlit_app.py    # Streamlit frontend
├── api/main.py             # FastAPI backend (optional/local use)
├── data/                   # Model weights + test images
├── src/predict.py          # Inference logic
├── src/diseases.json       # Disease metadata (treatment, prevention, season)
├── src/apple_facts.json    # Orchard Digest ticker facts
└── assets/                 # Hero illustration + screenshots

## Roadmap

- [ ] CI/CD via GitHub Actions
- [ ] Model monitoring
- [ ] Mobile-responsive layout polish