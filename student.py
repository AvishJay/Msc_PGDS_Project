"""
student.py
Written by : Avishka Jayamanna
Student hierarchy, enrollment, GPA, and SecureStudentRecord.

"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from person import Person
import math


# Grade to points mapping (4.0 scale)
GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D": 1.0, "F": 0.0
}


@dataclass
class Student(Person):
    """
    Generic Student class.
    - course_records: dict semester -> list of tuples (course_code, credits, grade_or_None)
    - current_enrollments: dict course_code -> credits
    """
    student_id: str
    course_records: Dict[str, List[Tuple[str, int, Optional[str]]]] = field(default_factory=dict)
    current_enrollments: Dict[str, int] = field(default_factory=dict)  # course_code -> credits
    max_credits_per_semester: int = 30

    def enroll_course(self, course_code: str, credits: int, semester: str) -> None:
        """
        Enroll in a course for a semester. Adds to current_enrollments and the semester record.
        Validation of limits should be performed by the registration system (department/course),
        but basic per-student validation is here.
        """
        if credits <= 0:
            raise ValueError("Credits must be positive.")
        current_credits = sum(self.current_enrollments.values())
        if current_credits + credits > self.max_credits_per_semester:
            raise ValueError(f"Enrolling would exceed max credits ({self.max_credits_per_semester}).")
        if course_code in self.current_enrollments:
            raise ValueError("Already enrolled in course.")
        # add to current enrollments
        self.current_enrollments[course_code] = credits
        # add to course_records for the semester with grade None (ongoing)
        self.course_records.setdefault(semester, []).append((course_code, credits, None))

    def drop_course(self, course_code: str, semester: str) -> None:
        """
        Drop a currently enrolled course. Remove from current_enrollments and semester record if ungraded.
        If the course already has a grade recorded, dropping is not allowed here (policy decision).
        """
        if course_code not in self.current_enrollments:
            raise ValueError("Not enrolled in the given course.")
        # find and remove from semester record (only if grade is None)
        recs = self.course_records.get(semester, [])
        for idx, (c_code, credits, grade) in enumerate(recs):
            if c_code == course_code:
                if grade is not None:
                    raise ValueError("Cannot drop a course that already has a grade.")
                recs.pop(idx)
                break
        else:
            raise ValueError("Course record not found for semester.")
        # remove from current enrollments
        del self.current_enrollments[course_code]

    def _grade_points(self, grade: Optional[str]) -> Optional[float]:
        if grade is None:
            return None
        return GRADE_POINTS.get(grade.upper())

    def calculate_gpa(self, up_to_semester: Optional[str] = None) -> float:
        """
        Calculate GPA across all semesters or up to a certain semester (lexicographic semester ordering).
        Only include graded courses (grade != None).
        """
        total_points = 0.0
        total_credits = 0
        for sem, recs in self.course_records.items():
            if up_to_semester is not None and sem > up_to_semester:
                continue
            for course_code, credits, grade in recs:
                pts = self._grade_points(grade)
                if pts is None:
                    continue
                total_points += pts * credits
                total_credits += credits
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 3)

    def get_academic_status(self, up_to_semester: Optional[str] = None) -> str:
        """
        Determine academic status based on GPA and recent credits.
        Rules (example policy):
          - Dean's List: GPA >= 3.7 and at least 12 graded credits
          - Probation: GPA < 2.0 and at least 6 graded credits
          - Good Standing: otherwise
        """
        # compute cumulative GPA and graded credits
        total_credits = 0
        total_points = 0.0
        for sem, recs in self.course_records.items():
            if up_to_semester is not None and sem > up_to_semester:
                continue
            for _, credits, grade in recs:
                pts = self._grade_points(grade)
                if pts is None:
                    continue
                total_credits += credits
                total_points += pts * credits

        if total_credits == 0:
            return "Good Standing"  # no graded record yet

        gpa = total_points / total_credits
        if gpa >= 3.7 and total_credits >= 12:
            return "Dean's List"
        if gpa < 2.0 and total_credits >= 6:
            return "Probation"
        return "Good Standing"

    def record_grade(self, course_code: str, semester: str, grade: str) -> None:
        """
        Assign a grade to a semester record for the student.
        """
        recs = self.course_records.get(semester, [])
        for i, (c_code, credits, g) in enumerate(recs):
            if c_code == course_code:
                recs[i] = (c_code, credits, grade)
                # once graded, it's not part of current_enrollments
                self.current_enrollments.pop(course_code, None)
                return
        raise ValueError("Course not found in student's semester records.")

    def get_responsibilities(self) -> str:
        return "Attend classes, submit assignments, follow program requirements."


class UndergraduateStudent(Student):
    def __init__(self, id: Optional[int], full_name: str, email: Optional[str], student_id: str, level: str = "UG"):
        super().__init__(id=id, full_name=full_name, email=email, student_id=student_id)
        self.level = level  # could be 'UG' or year info

    def get_responsibilities(self) -> str:
        base = super().get_responsibilities()
        return f"{base} (Undergraduate responsibilities: complete core modules)."


class GraduateStudent(Student):
    def __init__(self, id: Optional[int], full_name: str, email: Optional[str], student_id: str, research_area: Optional[str] = None):
        super().__init__(id=id, full_name=full_name, email=email, student_id=student_id)
        self.research_area = research_area

    def get_responsibilities(self) -> str:
        base = super().get_responsibilities()
        return f"{base} (Graduate responsibilities: research, thesis)."


class SecureStudentRecord:
    """
    Wrapper class that maintains private attributes and validates writes.
    Demonstrates encapsulation: _gpa must remain 0.0-4.0 and record writes validated.
    """
    def __init__(self, student: Student):
        self._student = student
        self._private_notes = ""  # private field
        # We do NOT cache GPA here — compute when requested

    @property
    def student(self) -> Student:
        return self._student

    @property
    def private_notes(self) -> str:
        return self._private_notes

    @private_notes.setter
    def private_notes(self, note: str):
        if not isinstance(note, str):
            raise TypeError("Notes must be text.")
        if len(note) > 2000:
            raise ValueError("Notes too long.")
        self._private_notes = note

    def set_grade(self, course_code: str, semester: str, grade: str):
        # validate grade
        if grade.upper() not in GRADE_POINTS:
            raise ValueError("Invalid grade string.")
        self._student.record_grade(course_code, semester, grade)

    def get_gpa(self, up_to_semester: Optional[str] = None) -> float:
        gpa = self._student.calculate_gpa(up_to_semester)
        # validate range explicitly
        if gpa < 0.0 or gpa > 4.0 or math.isnan(gpa):
            raise ValueError("Computed GPA out of valid range.")
        return gpa

    def get_academic_status(self, up_to_semester: Optional[str] = None) -> str:
        return self._student.get_academic_status(up_to_semester)
