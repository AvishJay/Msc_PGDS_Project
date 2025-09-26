=====================================================
 University Management System (Q1 – Programming for DS)
=====================================================

1. Overview
-----------
This project is an object-oriented University Management System developed in Python.
It extends a simple school management system to support:

- Multiple departments
- Students, faculty, and staff roles
- Course registration with prerequisites and capacity checks
- GPA calculation and academic standing
- Encapsulation and data validation
- Polymorphism via role-based responsibilities

The project demonstrates best practices in OOP and covers inheritance, encapsulation, 
polymorphism, and course/department management.

-----------------------------------------------------

2. Project Structure
--------------------
main.py          - Entry point (demo scenario)
person.py        - Base class Person + Staff hierarchy
student.py       - Student hierarchy (UG/PG) + GPA and academic status
faculty.py       - Faculty hierarchy (Professor, Lecturer, TA)
department.py    - Department and Course management

-----------------------------------------------------

3. How to Run
-------------
Step 1: Clone the repository
    git clone <your_repo_url>
    cd university-management-system

Step 2: (Optional) Create and activate a virtual environment
    python -m venv venv
    venv\Scripts\activate      (Windows)
    source venv/bin/activate   (Linux/Mac)
    pip install -r requirements.txt

Step 3: Run the system
    python main.py

-----------------------------------------------------

4. Demo Scenario
----------------
The demo includes:
- Creating departments and courses
- Registering students and faculty
- Enrolling students (with prerequisite and capacity checks)
- Assigning grades and calculating GPA
- Displaying academic status
- Demonstrating polymorphism with responsibilities and workloads

-----------------------------------------------------

5. Features Demonstrated
------------------------
- Inheritance: Person → Student/Faculty/Staff
- Student subclasses: UndergraduateStudent, GraduateStudent
- Faculty subclasses: Professor, Lecturer, TeachingAssistant
- Encapsulation: SecureStudentRecord with validation
- Polymorphism: Responsibilities and workloads by role
- Course Management: Enrollment, drops, prerequisites, capacity
- GPA & Status: Tracks performance across semesters

-----------------------------------------------------

6. Notes
--------
- Current version uses in-memory objects (no database).
- Can be extended with persistence (SQLite/CSV).
- All code follows Python best practices with modular design.

-----------------------------------------------------

7. Author
---------
Developed as project of Programming for Data Science (MSc Data Science – Coventry University).