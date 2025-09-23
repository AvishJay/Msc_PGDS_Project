"""
department.py
Course and Department classes, registration and prerequisite handling.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


class RegistrationError(Exception):
    """Raised when a registration operation fails due to business rules."""
    pass


@dataclass
class Course:
    """
    Course model:
    - course_code: unique identifier (string)
    - name: display name
    - credits: integer
    - capacity: maximum enrolled students
    - prerequisites: set of course_codes that must be completed (graded) before enrollment
    """
    course_code: str
    name: str
    credits: int
    capacity: int = 50
    prerequisites: Set[str] = field(default_factory=set)
    assigned_faculty: Optional[str] = None  # staff_id of professor/lecturer
    enrolled_students: Set[str] = field(default_factory=set)  # student_id set

    def is_full(self) -> bool:
        return len(self.enrolled_students) >= self.capacity

    def add_student(self, student_id: str):
        if self.is_full():
            raise RegistrationError(f"Course {self.course_code} is full.")
        self.enrolled_students.add(student_id)

    def remove_student(self, student_id: str):
        self.enrolled_students.discard(student_id)

    def has_prerequisites_met(self, completed_courses: Set[str]) -> bool:
        return self.prerequisites.issubset(completed_courses)


@dataclass
class Department:
    """
    Department holds lists of courses and faculty.
    The registration logic lives here to encapsulate department rules.
    """
    name: str
    courses: Dict[str, Course] = field(default_factory=dict)     # course_code -> Course
    faculty_members: Dict[str, str] = field(default_factory=dict)  # staff_id -> name
    students_by_id: Dict[str, str] = field(default_factory=dict)  # student_id -> name

    def add_course(self, course: Course):
        if course.course_code in self.courses:
            raise ValueError("Course already exists in department.")
        self.courses[course.course_code] = course

    def assign_faculty(self, course_code: str, staff_id: str):
        course = self.courses.get(course_code)
        if course is None:
            raise ValueError("Course not found.")
        course.assigned_faculty = staff_id
        # optionally add to faculty_members if not present (placeholder)

    def register_student(self, student_id: str, student_name: str):
        self.students_by_id[student_id] = student_name

    def enroll(self, student_id: str, course_code: str, completed_courses: Optional[Set[str]] = None):
        """
        Enroll a student into a course if:
         - Course exists
         - Not full
         - Prerequisites satisfied (based on completed_courses set)
        """
        course = self.courses.get(course_code)
        if course is None:
            raise RegistrationError("Course not offered by this department.")
        if student_id in course.enrolled_students:
            raise RegistrationError("Student already enrolled in course.")
        if course.is_full():
            raise RegistrationError("Course capacity reached.")
        if not course.has_prerequisites_met(completed_courses or set()):
            raise RegistrationError("Prerequisites not satisfied.")
        course.add_student(student_id)

    def drop(self, student_id: str, course_code: str):
        course = self.courses.get(course_code)
        if course is None:
            raise RegistrationError("Course not offered by this department.")
        course.remove_student(student_id)

    def list_course_summary(self) -> List[Dict]:
        summary = []
        for c in self.courses.values():
            summary.append({
                "course_code": c.course_code,
                "name": c.name,
                "credits": c.credits,
                "capacity": c.capacity,
                "enrolled": len(c.enrolled_students),
                "prereqs": list(c.prerequisites)
            })
        return summary
