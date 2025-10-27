#!/usr/bin/env python3
"""
Demo script for the Attrition Prediction API
This script demonstrates how to use the API with different employee profiles
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def demo_prediction():
    """Demonstrate the API with different employee profiles"""
    print("=" * 60)
    print("EMPLOYEE ATTRITION PREDICTION API DEMO")
    print("=" * 60)
    
    # Example 1: High-risk employee (young, low salary, overtime, frequent travel)
    high_risk_employee = {
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
    
    # Example 2: Low-risk employee (experienced, high salary, good work-life balance)
    low_risk_employee = {
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
    
    # Example 3: Medium-risk employee (mid-career, moderate conditions)
    medium_risk_employee = {
        "Age": 35,
        "Gender": "Male",
        "MaritalStatus": "Married",
        "Department": "Human Resources",
        "JobRole": "HR Manager",
        "JobLevel": 3,
        "JobSatisfaction": 3,
        "MonthlyIncome": 5000.0,
        "DailyRate": 250.0,
        "HourlyRate": 30.0,
        "MonthlyRate": 5000.0,
        "YearsAtCompany": 5,
        "YearsInCurrentRole": 3,
        "YearsSinceLastPromotion": 2,
        "TotalWorkingYears": 8,
        "YearsWithCurrManager": 2,
        "NumCompaniesWorked": 2,
        "PerformanceRating": 3,
        "PercentSalaryHike": 10.0,
        "TrainingTimesLastYear": 2,
        "OverTime": "No",
        "BusinessTravel": "Travel_Rarely",
        "DistanceFromHome": 15,
        "WorkLifeBalance": 3,
        "EnvironmentSatisfaction": 3,
        "RelationshipSatisfaction": 3,
        "Education": 3,
        "EducationField": "Human Resources",
        "StockOptionLevel": 1
    }
    
    employees = [
        ("High Risk Employee", high_risk_employee),
        ("Low Risk Employee", low_risk_employee),
        ("Medium Risk Employee", medium_risk_employee)
    ]
    
    for name, employee_data in employees:
        print(f"\n{name}:")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=employee_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Prediction: {result['prediction']}")
                print(f"Probability: {result['probability']:.3f}")
                print(f"Confidence: {result['confidence']}")
                
                # Interpretation
                if result['prediction'] == 'Yes':
                    print("WARNING: HIGH ATTRITION RISK - Employee likely to leave")
                else:
                    print("GOOD: LOW ATTRITION RISK - Employee likely to stay")
                    
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error making prediction: {e}")
    
    print("\n" + "=" * 60)
    print("API ENDPOINTS AVAILABLE:")
    print("=" * 60)
    print("• GET  /              - API information")
    print("• GET  /health         - Health check")
    print("• GET  /sample-data    - Sample employee data")
    print("• POST /predict        - Make predictions")
    print("• GET  /docs           - Interactive API documentation")
    print("\nTo view the interactive API documentation, visit:")
    print("http://localhost:8000/docs")

if __name__ == "__main__":
    demo_prediction()
