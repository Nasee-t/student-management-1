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