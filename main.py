from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import os
from datetime import date
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

users_db = {}

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

class Registration(BaseModel):
    Full_Name: str
    Date_of_Birth: date
    Gender: str
    Phone_Number: str
    Email: str
    Address: str
    Highest_Degree: str
    Technical_Skills: str
    Nationality: str
    Department: str
    Date_of_Joining: date
    Expected_Salary: float

@app.post("/registration")
async def registration(
    Full_Name: str = Form(...),
    Date_of_Birth: date = Form(...),
    Gender: str = Form(...),
    Phone_Number: str = Form(...),
    Email: str = Form(...),
    Address: str = Form(...),
    Highest_Degree: str = Form(...),
    Technical_Skills: str = Form(...),
    Nationality: str = Form(...),
    Department: str = Form(...),
    Date_of_Joining: date = Form(...),
    Expected_Salary: float = Form(...),
    file: UploadFile = File(...), 
):
    if Email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users_db[Email] = {
        "Full_Name": Full_Name,
        "Date_of_Birth": Date_of_Birth,
        "Gender": Gender,
        "Phone_Number": Phone_Number,
        "Email": Email,
        "Address": Address,
        "Highest_Degree": Highest_Degree,
        "Technical_Skills": Technical_Skills,
        "Nationality": Nationality,
        "Department": Department,
        "Date_of_Joining": Date_of_Joining,
        "Expected_Salary": Expected_Salary,
    }

    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
        return JSONResponse(
            content={
                "message": "User registered successfully",
                "email": Email,
                "resume": f"Resume uploaded successfully. Saved as {file.filename}",
            },
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading resume: {str(e)}")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0.",port=8000 ,log_level = "debug")

