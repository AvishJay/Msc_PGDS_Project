"""
faculty.py
Faculty hierarchy: Faculty -> Professor, Lecturer, TA (Teaching Assistant)
Includes calculate_workload override to demonstrate polymorphism.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from person import Person


@dataclass
class Faculty(Person):
    """
    Generic faculty class.
    - courses_assigned: list of course codes
    """
    staff_id: str
    department: Optional[str] = None
    courses_assigned: List[str] = field(default_factory=list)

    def assign_course(self, course_code: str):
        if course_code not in self.courses_assigned:
            self.courses_assigned.append(course_code)

    def calculate_workload(self) -> float:
        """
        Base workload metric: number of credits/responsibilities.
        Overridden in sub-classes for role-specific rules.
        """
        return float(len(self.courses_assigned))

    def get_responsibilities(self) -> str:
        return "Teaching, preparing materials, student consultation."


class Professor(Faculty):
    def __init__(self, id: Optional[int], full_name: str, email: Optional[str], staff_id: str, department: Optional[str] = None):
        super().__init__(id=id, full_name=full_name, email=email, staff_id=staff_id, department=department)

    def calculate_workload(self) -> float:
        # Professors may have additional research load (example multiplier)
        base = super().calculate_workload()
        research_load = 1.5  # abstracted research time factor
        return base + research_load

    def get_responsibilities(self) -> str:
        return "Lead research, supervise students, teach advanced courses."


class Lecturer(Faculty):
    def __init__(self, id: Optional[int], full_name: str, email: Optional[str], staff_id: str, department: Optional[str] = None):
        super().__init__(id=id, full_name=full_name, email=email, staff_id=staff_id, department=department)

    def calculate_workload(self) -> float:
        # Lecturers focus on teaching; maybe more teaching hours per course
        base = super().calculate_workload()
        return base * 1.2

    def get_responsibilities(self) -> str:
        return "Deliver lectures, mark assignments, hold office hours."


class TA(Faculty):
    def __init__(self, id: Optional[int], full_name: str, email: Optional[str], staff_id: str, department: Optional[str] = None, supervising_professor: Optional[str] = None):
        super().__init__(id=id, full_name=full_name, email=email, staff_id=staff_id, department=department)
        self.supervising_professor = supervising_professor

    def calculate_workload(self) -> float:
        # TAs typically have lighter workload
        base = super().calculate_workload()
        return max(0.5, base * 0.5)

    def get_responsibilities(self) -> str:
        return "Assist teaching, run labs, grade under supervision."
