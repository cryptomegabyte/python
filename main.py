from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load the text generation model (distilgpt2 for faster demo)
generator = pipeline('text-generation', model='distilgpt2')

class PredictRequest(BaseModel):
    text: str
    max_length: int = 50

@app.get("/")
def read_root():
    return {"message": "Text Prediction API"}

@app.post("/predict")
def predict_text(request: PredictRequest):
    # Generate text continuation
    result = generator(request.text, max_length=request.max_length, num_return_sequences=1)
    return {"prediction": result[0]['generated_text']}