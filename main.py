from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import mysql.connector
import os
from dotenv import load_dotenv


# Database Configuration
load_dotenv()
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)

# FastAPI App Initialization
app = FastAPI()


# Pydantic Model for Student
class Student(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0, lt=100)
    grade: str = Field(..., min_length=1, max_length=10)


# GET: All Students
@app.get("/students")
def get_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return students


# GET: One Student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# POST: Add New Student
@app.post("/students")
def add_student(student: Student):
    cursor.execute(
        "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
        (student.name, student.age, student.grade)
    )
    db.commit()
    return {"message": "Student added successfully", "id": cursor.lastrowid}


# DELETE: Remove Student by ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Student not found")
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    db.commit()
    return {"message": "Student deleted successfully"}

# PUT
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    cursor.execute("SELECT * FROM students WHERE id= %s", (student_id,))
    if not cursor.fetchone():
        raise HTTPException( status_code=404, detail="Student not found!")
    
    cursor.execute("UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s",
                   (student.name, student.age, student.grade, student_id))
    db.commit()

    return{ "message": "Student updated successfully",
        "student_id": student_id}