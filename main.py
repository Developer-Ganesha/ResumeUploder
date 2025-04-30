from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os ,urllib 
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from pathlib import Path
username = "postgres"
password = 'RGS@123'
encoded_password = urllib.parse.quote_plus(password)
DB_URL = f"postgresql://{username}:{encoded_password}@localhost:5432/resume_db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
# ✅ Define User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    highest_degree = Column(String, nullable=False)
    technical_skills = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    department = Column(String, nullable=False)
    date_of_joining = Column(String, nullable=False)
    expected_salary = Column(Float, nullable=False)
    resume_filename= Column(String, nullable=False)
# ✅ Ensure database tables are created when the app starts

Base.metadata.create_all(bind=engine)
# ✅ Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# ✅ Improved registration endpoint
@app.post("/registration")
async def registration(
    full_name: str = Form(...),
    date_of_birth: str = Form(...), 
    gender: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    highest_degree: str = Form(...),
    technical_skills: str = Form(...),
    nationality: str = Form(...),
    department: str = Form(...),
    date_of_joining: str = Form(...), 
    expected_salary: float = Form(...),
    resume_filename: UploadFile = File(...), db: Session = Depends(get_db)):
    # ✅ Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        full_name=full_name,
        date_of_birth=date_of_birth,
        gender=gender,
        phone_number=phone_number,
        email=email,
        address=address,
        highest_degree=highest_degree,
        technical_skills=technical_skills,
        nationality=nationality,
        department=department,
        date_of_joining=date_of_joining,
        expected_salary=expected_salary,
        resume_filename = resume_filename.filename )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
        content={"message": "User registered successfully","email": email,"user_id":User.id})
############ GET PROFILE #############    

@app.post("/profile")
async def get_profile(email:str= Form(...) , db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {
            "status ":"0" ,"message":"User not found" ,"results":{}}
    user_data = {
        "user_id":User.id,
        "full_name": user.full_name,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "phone_number": user.phone_number,
        "email": user.email,
        "address": user.address,
        "highest_degree": user.highest_degree,
        "technical_skills": user.technical_skills,
        "nationality": user.nationality,
        "department": user.department,
        "date_of_joining": user.date_of_joining,
        "expected_salary": user.expected_salary,
        " resume_filename": user. resume_filename}    
    return{"status":"1","message":"Profile fetch successfully","results":user_data}
###    UPDATE PROFILE ###
@app.post("/update_profile")
async def update_profile(
    id : int , 
    full_name: str = Form(...),
    date_of_birth: str = Form(...),
    gender: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    highest_degree: str = Form(...),
    technical_skills: str = Form(...),
    nationality: str = Form(...),
    department: str = Form(...),
    date_of_joining: str = Form(...),
    expected_salary: float = Form(...),
    resume_filename: UploadFile = File(...),
    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"status": "0", "message": "User not found", "result": {}}
    # Update user fields directly
    user.id = id
    user.full_name = full_name
    user.date_of_birth = date_of_birth
    user.gender = gender
    user.phone_number = phone_number
    user.address = address
    user.highest_degree = highest_degree
    user.technical_skills = technical_skills
    user.nationality = nationality
    user.department = department
    user.date_of_joining = date_of_joining
    user.expected_salary = expected_salary
    user. resume_filename =  resume_filename

    db.commit()
    return {
        "status": "1",
        "message": "Profile updated successfully",
        "user_id":User.id,
        "user_name": user.full_name }
@app.delete("/Delete")
def delete_user(id:int = Form(...),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id ==id).first()
    if not user:
        return{"status":"user not found"}
    db.delete(get_db)
    db.commit()
    return{"message":"user data deleted successfully"}
           
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
