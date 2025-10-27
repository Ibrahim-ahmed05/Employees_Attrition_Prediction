from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
import os
import numpy as np
from typing import Dict, Any

# -----------------------------
# 1️⃣ Initialize FastAPI app
# -----------------------------
app = FastAPI(title="Attrition Prediction API")

# -----------------------------
# 2️⃣ Enable CORS (optional, for frontend later)
# -----------------------------
origins = [
    "http://localhost:3000",  # React dev server, if used later
    "*",                       # Allow all origins for testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 3️⃣ Define Pydantic models for input and output
# -----------------------------
class EmployeeInput(BaseModel):
    # Basic demographics
    Age: int
    Gender: str
    MaritalStatus: str
    
    # Job information
    Department: str
    JobRole: str
    JobLevel: int
    JobSatisfaction: int
    
    # Compensation
    MonthlyIncome: float
    DailyRate: float
    HourlyRate: float
    MonthlyRate: float
    
    # Work experience
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    TotalWorkingYears: int
    YearsWithCurrManager: int
    NumCompaniesWorked: int
    
    # Performance and training
    PerformanceRating: int
    PercentSalaryHike: float
    TrainingTimesLastYear: int
    
    # Work conditions
    OverTime: str
    BusinessTravel: str
    DistanceFromHome: int
    WorkLifeBalance: int
    EnvironmentSatisfaction: int
    RelationshipSatisfaction: int
    
    # Education
    Education: int
    EducationField: str
    
    # Stock options
    StockOptionLevel: int

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    confidence: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    message: str

# -----------------------------
# 4️⃣ Load saved pipeline with error handling
# -----------------------------
pipeline_path = "xgb_attrition_pipeline.joblib"
pipeline = None

def load_model():
    global pipeline
    try:
        if not os.path.exists(pipeline_path):
            raise FileNotFoundError(f"Pipeline file not found at {pipeline_path}")
        
        pipeline = joblib.load(pipeline_path)
        print("Pipeline loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading pipeline: {str(e)}")
        return False

# Load model on startup
model_loaded = load_model()

# -----------------------------
# 5️⃣ Health check endpoint
# -----------------------------
@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check if the model is loaded and API is healthy"""
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        message="Model loaded successfully" if model_loaded else "Model failed to load"
    )

# -----------------------------
# 6️⃣ Sample data endpoint
# -----------------------------
@app.get("/sample-data")
def get_sample_data():
    """Get sample employee data for testing"""
    sample_data = {
        "high_risk_employee": {
            "Age": 25,
            "Gender": "Male",
            "MaritalStatus": "Single",
            "Department": "Sales",
            "JobRole": "Sales Representative",
            "JobLevel": 1,
            "JobSatisfaction": 2,
            "MonthlyIncome": 2000.0,
            "DailyRate": 100.0,
            "HourlyRate": 12.0,
            "MonthlyRate": 2000.0,
            "YearsAtCompany": 1,
            "YearsInCurrentRole": 1,
            "YearsSinceLastPromotion": 1,
            "TotalWorkingYears": 2,
            "YearsWithCurrManager": 1,
            "NumCompaniesWorked": 1,
            "PerformanceRating": 2,
            "PercentSalaryHike": 5.0,
            "TrainingTimesLastYear": 1,
            "OverTime": "Yes",
            "BusinessTravel": "Travel_Frequently",
            "DistanceFromHome": 20,
            "WorkLifeBalance": 2,
            "EnvironmentSatisfaction": 2,
            "RelationshipSatisfaction": 2,
            "Education": 2,
            "EducationField": "Life Sciences",
            "StockOptionLevel": 0
        },
        "low_risk_employee": {
            "Age": 45,
            "Gender": "Female",
            "MaritalStatus": "Married",
            "Department": "Research & Development",
            "JobRole": "Research Scientist",
            "JobLevel": 4,
            "JobSatisfaction": 4,
            "MonthlyIncome": 8000.0,
            "DailyRate": 400.0,
            "HourlyRate": 50.0,
            "MonthlyRate": 8000.0,
            "YearsAtCompany": 10,
            "YearsInCurrentRole": 5,
            "YearsSinceLastPromotion": 2,
            "TotalWorkingYears": 15,
            "YearsWithCurrManager": 3,
            "NumCompaniesWorked": 2,
            "PerformanceRating": 4,
            "PercentSalaryHike": 15.0,
            "TrainingTimesLastYear": 3,
            "OverTime": "No",
            "BusinessTravel": "Travel_Rarely",
            "DistanceFromHome": 5,
            "WorkLifeBalance": 4,
            "EnvironmentSatisfaction": 4,
            "RelationshipSatisfaction": 4,
            "Education": 4,
            "EducationField": "Life Sciences",
            "StockOptionLevel": 2
        }
    }
    return sample_data

# -----------------------------
# 7️⃣ Prediction endpoint
# -----------------------------
@app.post("/predict", response_model=PredictionResponse)
def predict_attrition(data: EmployeeInput):
    """
    Accepts employee features and returns attrition prediction with probability
    """
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check /health endpoint.")
    
    try:
        # Convert input to DataFrame (pipeline expects 2D input)
        input_df = pd.DataFrame([data.dict()])
        
        # Debug: Print input data
        print(f"Input data shape: {input_df.shape}")
        print(f"Input columns: {list(input_df.columns)}")
        print(f"Sample input: {input_df.iloc[0].to_dict()}")
        
        # Make prediction
        pred = pipeline.predict(input_df)[0]
        print(f"Raw prediction: {pred} (type: {type(pred)})")
        
        # Get prediction probability if available
        try:
            pred_proba = pipeline.predict_proba(input_df)[0]
            print(f"Raw probabilities: {pred_proba}")
            probability = float(pred_proba[1]) if len(pred_proba) > 1 else float(pred_proba[0])
            print(f"Selected probability: {probability}")
        except Exception as proba_error:
            print(f"Error getting probabilities: {proba_error}")
            probability = 0.5  # Default if predict_proba not available
        
        # Convert prediction to Yes/No
        pred_int = int(pred)  # Convert numpy.int64 to Python int
        label = "Yes" if pred_int == 1 else "No"
        print(f"Final label: {label}, probability: {probability}")
        
        # Determine confidence level
        if probability >= 0.8:
            confidence = "High"
        elif probability >= 0.6:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        return PredictionResponse(
            prediction=label,
            probability=float(probability),  # Ensure it's a Python float
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# -----------------------------
# 8️⃣ Test prediction endpoint
# -----------------------------
@app.post("/test-prediction")
def test_prediction():
    """Test the model with sample data to verify it's working"""
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Use the sample data from get_sample_data
        sample_data = {
            "Age": 25,
            "Gender": "Male",
            "MaritalStatus": "Single",
            "Department": "Sales",
            "JobRole": "Sales Representative",
            "JobLevel": 1,
            "JobSatisfaction": 2,
            "MonthlyIncome": 2000.0,
            "DailyRate": 100.0,
            "HourlyRate": 12.0,
            "MonthlyRate": 2000.0,
            "YearsAtCompany": 1,
            "YearsInCurrentRole": 1,
            "YearsSinceLastPromotion": 1,
            "TotalWorkingYears": 2,
            "YearsWithCurrManager": 1,
            "NumCompaniesWorked": 1,
            "PerformanceRating": 2,
            "PercentSalaryHike": 5.0,
            "TrainingTimesLastYear": 1,
            "OverTime": "Yes",
            "BusinessTravel": "Travel_Frequently",
            "DistanceFromHome": 20,
            "WorkLifeBalance": 2,
            "EnvironmentSatisfaction": 2,
            "RelationshipSatisfaction": 2,
            "Education": 2,
            "EducationField": "Life Sciences",
            "StockOptionLevel": 0
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame([sample_data])
        print(f"Test input shape: {input_df.shape}")
        print(f"Test input columns: {list(input_df.columns)}")
        
        # Make prediction
        pred = pipeline.predict(input_df)[0]
        print(f"Test prediction: {pred} (type: {type(pred)})")
        
        # Get probabilities
        pred_proba = pipeline.predict_proba(input_df)[0]
        print(f"Test probabilities: {pred_proba}")
        
        return {
            "test_data": sample_data,
            "prediction": int(pred),  # Convert numpy.int64 to Python int
            "probabilities": pred_proba.tolist(),
            "model_info": {
                "pipeline_type": str(type(pipeline)),
                "has_predict_proba": hasattr(pipeline, 'predict_proba')
            }
        }
        
    except Exception as e:
        return {"error": str(e), "traceback": str(e.__traceback__)}

# -----------------------------
# 9️⃣ Root endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Attrition Prediction API is running!",
        "endpoints": {
            "health": "/health - Check API and model status",
            "sample_data": "/sample-data - Get sample employee data for testing",
            "test_prediction": "/test-prediction - Test model with sample data",
            "predict": "/predict - Make attrition predictions",
            "docs": "/docs - Interactive API documentation"
        },
        "model_loaded": model_loaded
    }
