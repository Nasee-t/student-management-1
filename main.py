from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from database import get_cursor
from fastapi.staticfiles import StaticFiles

# FastAPI App Initialization
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Model
class Student(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0, lt=100)
    grade: str = Field(..., min_length=1, max_length=10)

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100) 
    age: Optional[int] = Field(None, gt=0, lt=100)
    grade: Optional[str] = Field(None, min_length=1, max_length=10)

class Course(BaseModel):
    name: str
    code: str
    credits: int

class Enrollment(BaseModel):
    student_id: int
    course_id: int


#STUDENTS-------------------------------------------------------

# GET: All Students
@app.get("/students")
def get_students():
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    db.close()
    return students


# GET: One Student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.close()
    return student


# POST: Add New Student
@app.post("/students")
def add_student(student: Student):
    db, cursor = get_cursor()
    cursor.execute(
        "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
        (student.name, student.age, student.grade)
    )
    db.commit()
    db.close()
    return {"message": "Student added successfully", "id": cursor.lastrowid}


# DELETE: Remove Student by ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Student not found")
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    db.commit()
    db.close()
    return {"message": "Student deleted successfully"}

# PUT
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM students WHERE id= %s", (student_id,))
    if not cursor.fetchone():
        raise HTTPException( status_code=404, detail="Student not found!")
    
    cursor.execute("UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s",
                   (student.name, student.age, student.grade, student_id))
    db.commit()
    db.close()
    return{ "message": "Student updated successfully",
        "student_id": student_id}

#PATCH
@app.patch("/students/{student_id}")
def patch_student( student_id: int, student: StudentUpdate):
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    existing_student = cursor.fetchone()

    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    name= student.name if student.name is not None else existing_student["name"]
    age= student.age if student.age is not None else existing_student["age"]
    grade= student.grade if student.grade is not None else existing_student["grade"]

    cursor.execute("UPDATE students SET name = %s, age = %s, grade = %s WHERE id = %s",
        (name, age, grade, student_id))

    db.commit()
    db.close()
    return {
        "message" : "Student updated successfully (partial)",
        "student_id" : student_id
    }

#COURSES---------------------------------------------------

@app.get("/courses")
def get_courses():
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    db.close()
    return courses


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
    course = cursor.fetchone()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.close()
    return course


@app.post("/courses")
def add_course(course: Course):
    db, cursor = get_cursor()
    cursor.execute(
        "INSERT INTO courses (name, code, credits) VALUES (%s, %s, %s)",
        (course.name, course.code, course.credits)
    )
    db.commit()
    db.close()
    return {"message": "Course added", "id": cursor.lastrowid}


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Course not found")

    cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
    db.commit()
    db.close()
    return {"message": "Course deleted"}

@app.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):
    db, cursor = get_cursor()
    cursor.execute("SELECT id FROM courses WHERE id = %s", (course_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Course not found")

    cursor.execute("UPDATE courses SET name = %s, code = %s, credits = %s WHERE id = %s",
                   (course.name, course.code, course.credits, course_id))
    db.commit()
    db.close()
    return {"message": "Course updated"}


# ENROLL--------------------------------------------

#POST
@app.post("/enroll")
def enroll_student(enrollment: Enrollment):
    db, cursor = get_cursor()
    # Check student exists
    cursor.execute("SELECT id FROM students WHERE id = %s", (enrollment.student_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Student not found")

    # Check course exists
    cursor.execute("SELECT id FROM courses WHERE id = %s", (enrollment.course_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Course not found")

    # Prevent duplicate enrollment
    cursor.execute(
        "SELECT id FROM enrollments WHERE student_id = %s AND course_id = %s",
        (enrollment.student_id, enrollment.course_id)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Student already enrolled")

    # Enroll
    cursor.execute(
        "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
        (enrollment.student_id, enrollment.course_id)
    )
    db.commit()
    db.close()
    return {"message": "Student enrolled successfully"}


#GET - Courses for a student
@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int):
    db, cursor = get_cursor()
    cursor.execute(
        """
        SELECT c.id, c.name, c.code, c.credits
        FROM courses c
        JOIN enrollments e ON c.id = e.course_id
        WHERE e.student_id = %s
        """, (student_id,)
    )
    courses = cursor.fetchall()
    db.close()
    return courses

# GET - Students in a course
@app.get("/courses/{course_id}/students")
def get_course_students(course_id: int):
    db, cursor = get_cursor()
    cursor.execute(
        """
        SELECT s.id, s.name, s.age, s.grade
        FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = %s
        """, (course_id,)
    )
    students = cursor.fetchall()
    db.close()
    return students

# DELETE
@app.delete("/enroll")
def delete_enrollment(enrollment: Enrollment):
    db, cursor = get_cursor()
    cursor.execute( "SELECT id FROM enrollments WHERE student_id = %s AND course_id = %s",
                   (enrollment.student_id, enrollment.course_id))
    
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Enrollment not found")

    cursor.execute( "DELETE FROM enrollments WHERE student_id = %s AND course_id = %s",
                   (enrollment.student_id, enrollment.course_id)
    )
    db.commit()
    db.close()
    return {"message": "Enrollment deleted"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")