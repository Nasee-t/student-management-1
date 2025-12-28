from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
    name: str
    age: int
    grade: str


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
