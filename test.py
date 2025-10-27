from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI + Supabase (Employees) connected 🚀"}


@app.post("/add_employee")
def add_employee(
    name: str,
    age: int,
    gender: str,
    department: str,
    job_role: str,
    years_at_company: int,
    monthly_income: float,
    overtime: bool,
    job_satisfaction: int,
    perfomance_rating: int,
    attrition_pred: str,
    prediction_prob: float
):
    """
    Add a new employee record to Supabase 'employees' table.
    """
    try:
        data = {
            "name": name,
            "age": age,
            "gender": gender,
            "department": department,
            "job_role": job_role,
            "years_at_company": years_at_company,
            "monthly_income": monthly_income,
            "overtime": overtime,
            "job_satisfaction": job_satisfaction,
            "perfomance_rating": perfomance_rating,
            "attrition_pred": attrition_pred,
            "prediction_prob": prediction_prob
        }

        response = supabase.table("employees").insert(data).execute()
        return {"success": True, "data": response.data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/employees")
def get_employees():
    """
    Fetch all employee records from Supabase 'employees' table.
    """
    try:
        response = supabase.table("employees").select("*").execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
