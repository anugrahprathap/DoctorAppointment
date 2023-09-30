from fastapi import FastAPI, HTTPException
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

origins = [
    "*",  # For local development
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development, replace with your production origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


from pydantic import BaseModel
from typing import List
X = 20
class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    availability: List[str]  # List of available weekdays (e.g., ["Monday", "Wednesday"])

class Appointment(BaseModel):
    doctor_id: int
    date: str  # Date of the appointment (e.g., "2023-10-10")
    patient_name: str


doctors_db = [
    Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", availability=["Monday", "Wednesday"]),
    Doctor(id=2, name="Dr. Johnson", specialization="Dermatologist", availability=["Tuesday", "Thursday"]),
    Doctor(id=3, name="Dr. Brown", specialization="Pediatrician", availability=["Monday", "Wednesday", "Friday"]),
    Doctor(id=4, name="Dr. Davis", specialization="Orthopedic Surgeon", availability=["Tuesday", "Thursday"]),
    Doctor(id=5, name="Dr. Wilson", specialization="Gynecologist", availability=["Monday", "Wednesday"]),
    Doctor(id=6, name="Dr. Lee", specialization="Neurologist", availability=["Tuesday", "Thursday"]),
    Doctor(id=7, name="Dr. Evans", specialization="Psychiatrist", availability=["Sunday"]),
    Doctor(id=8, name="Dr. Allen", specialization="Ophthalmologist", availability=["Tuesday", "Thursday"]),
]


appointments_db = []



@app.get("/", response_model=List[Doctor])
async def get_doctors():
    return doctors_db

@app.get("/doctor/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: int):
    doctor = next((d for d in doctors_db if d.id == doctor_id), None)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@app.post("/book-appointment")
async def book_appointment(appointment: Appointment):
    # Check if the date is valid
    if not is_valid_date(appointment.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Please use 'YYYY-MM-DD'.")

    # Check if the doctor exists
    doctor = next((d for d in doctors_db if d.id == appointment.doctor_id), None)
    if doctor is None:
        return {"message": "Doctor not found"}

    # Check if the doctor is available on the requested date
    date_obj = datetime.strptime(appointment.date, '%Y-%m-%d')
    # Get the day of the week as an integer (0 = Monday, 6 = Sunday)
    
    day_of_week = date_obj.weekday()
    
    # Convert the integer to the day name
    day_name = date_obj.strftime('%A')
    

    if day_name not in doctor.availability:
        return {"message": f"Doctor is not available on {appointment.date}"}

    # Check if the doctor has available slots for appointments (X number of patients)
    appointments_count = sum(1 for a in appointments_db if a.doctor_id == appointment.doctor_id and a.date == appointment.date)
    if appointments_count >= X:  # X is the maximum number of patients per day
        return {'message': f"Doctor has no available slots on {appointment.date}"}

    # Check if the appointment slot is already taken
    if any(a.doctor_id == appointment.doctor_id and a.date == appointment.date for a in appointments_db):
        return {'message': f"Appointment slot for {appointment.date} with this doctor is already taken"}

    # Add the appointment to the appointments_db
    appointments_db.append(appointment)
    
    return {
        "message": "Appointment booked successfully",
        
    }

