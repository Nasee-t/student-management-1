CREATE DATABASE student_db;
USE student_db;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    grade VARCHAR(10) NOT NULL
);

-- Optional sample data
INSERT INTO students (name, age, grade) VALUES
('Alice Johnson', 15, '10th'),
('Bob Smith', 16, '11th');

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    credits INT NOT NULL
);

-- Sample data
INSERT INTO courses (name, code, credits) VALUES
('Mathematics', 'MATH101', 4),
('Physics', 'PHY101', 3),
('Computer Science', 'CS101', 5),
('English', 'ENG101', 2);

SELECT * FROM courses;

CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL
);

ALTER TABLE enrollments
ADD CONSTRAINT fk_student
FOREIGN KEY (student_id)
REFERENCES students(id)
ON DELETE CASCADE;

ALTER TABLE enrollments
ADD CONSTRAINT fk_course
FOREIGN KEY (course_id)
REFERENCES courses(id)
ON DELETE CASCADE;
