from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from transformers import pipeline
from typing import Optional

app = FastAPI(title="Text Prediction API", description="ML-powered text prediction service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Preact dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception for ML errors
class PredictionError(Exception):
    def __init__(self, message: str):
        self.message = message

# Exception handler
@app.exception_handler(PredictionError)
async def prediction_error_handler(request: Request, exc: PredictionError):
    return {"error": "Prediction failed", "detail": exc.message, "status_code": 500}

# Load the text generation model (distilgpt2 for faster demo)
generator = pipeline('text-generation', model='distilgpt2')

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="Input text to continue")
    max_length: int = Field(50, ge=10, le=200, description="Maximum length of generated text")

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()

class PredictResponse(BaseModel):
    prediction: str
    input_length: int
    generated_length: int

@app.get("/")
def read_root():
    return {"message": "Text Prediction API", "version": "1.0"}

@app.post("/predict", response_model=PredictResponse)
def predict_text(request: PredictRequest):
    try:
        # Generate text continuation
        result = generator(request.text, max_length=request.max_length, num_return_sequences=1)
        prediction = result[0]['generated_text']
        
        # Calculate lengths
        input_length = len(request.text)
        generated_length = len(prediction) - input_length
        
        return PredictResponse(
            prediction=prediction,
            input_length=input_length,
            generated_length=generated_length
        )
    except Exception as e:
        raise PredictionError(f"Model prediction failed: {str(e)}")