"""
person.py
Written by : Avishka Jayamanna
Base Person classes and Staff placeholder.

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    """
    Base class for all people in the system.
    """
    id: Optional[int]
    full_name: str
    email: Optional[str]

    def get_responsibilities(self) -> str:
        """Generic responsibilities (overridden in subclasses)."""
        return "General Responsibilties for a person."

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.full_name} id={self.id}>"


class Staff(Person):
    """
    Generic Staff member (non-teaching). Could be extended further.
    """
    def __init__(self, id: Optional[int], full_name: str, email: Optional[str], position: str):
        super().__init__(id=id, full_name=full_name, email=email)
        self.position = position

    def get_responsibilities(self) -> str:
        return f"Administrative responsibilities as {self.position}."
