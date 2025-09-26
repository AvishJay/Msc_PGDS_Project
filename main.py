"""
main.py
Use for: seeding data, demonstrating enrollment, GPA, encapsulation, polymorphism.
Click Run in VS Code to execute the demo scenario automatically.
"""

from student import UndergraduateStudent, GraduateStudent, SecureStudentRecord
from faculty import Professor, Lecturer, TA
from department import Department, Course, RegistrationError


def seed_demo():
    # Create department and courses
    cs = Department(name="Computer Science")
    cs.add_course(Course(course_code="CS101", name="Intro to Programming", credits=3, capacity=3))
    cs.add_course(Course(course_code="CS201", name="Data Visualization", credits=4, capacity=2, prerequisites={"CS101"}))
    cs.add_course(Course(course_code="CS301", name="Machine Learning", credits=4, capacity=2, prerequisites={"CS201"}))

    # Create students
    s1 = UndergraduateStudent(id=1, full_name="Avishka Jayamanna", email="avishkaj@nibm.com", student_id="MSU001")
    s2 = UndergraduateStudent(id=2, full_name="Nawanjana Pathirage", email="nawanjanp@nibm.com", student_id="MSU002")
    s3 = GraduateStudent(id=3, full_name="Janith Perera", email="janithp@nibm.com", student_id="MSG001", research_area="ML")

    # Register students in department
    for s in (s1, s2, s3):
        cs.register_student(s.student_id, s.full_name)

    # Faculty
    prof = Professor(id=10, full_name="Dr. Kumara Perera", email="kumarap@nibm.com", staff_id="P1001", department="Computer Science")
    lec = Lecturer(id=11, full_name="Mr. Janith Silva", email="janiths@nibm.com", staff_id="P1002", department="Computer Science")
    ta = TA(id=12, full_name="Sarah Silva", email="sarahs@nibm.com", staff_id="P1003", department="Computer Science", supervising_professor=prof.staff_id) 

    # Assign faculty to courses
    cs.assign_faculty("CS101", prof.staff_id)
    cs.assign_faculty("CS201", lec.staff_id)

    return cs, [s1, s2, s3], [prof, lec, ta]


def demo_registration_and_gpa():
    cs, students, faculty = seed_demo()
    s1, s2, s3 = students

    # Enrollment attempts with prerequisite checking
    print("=== Registration attempts ===")
    try:
        cs.enroll(s1.student_id, "CS201", completed_courses=set())  # should fail (missing CS101)
    except RegistrationError as e:
        print("Expected fail (prereq):", e)

    # Enroll in CS101 first
    cs.enroll(s1.student_id, "CS101", completed_courses=set())
    cs.enroll(s2.student_id, "CS101", completed_courses=set())
    cs.enroll(s3.student_id, "CS101", completed_courses=set())

    # Simulate grading for CS101
    s1.course_records.setdefault("2025S1", []).append(("CS101", 3, "A"))
    s2.course_records.setdefault("2025S1", []).append(("CS101", 3, "B+"))

    # Now enroll into CS201 using completed_courses set
    cs.enroll(s1.student_id, "CS201", completed_courses={"CS101"})
    cs.enroll(s2.student_id, "CS201", completed_courses={"CS101"})
    # third student should fail because capacity 2
    try:
        cs.enroll(s3.student_id, "CS201", completed_courses={"CS101"})
    except RegistrationError as e:
        print("Expected fail (capacity):", e)

    # Show course summaries
    print("\nCourse summary:")
    for s in cs.list_course_summary():
        print(s)

    # Demonstrate student GPA & statuses via SecureStudentRecord
    secure_s1 = SecureStudentRecord(s1)
    secure_s2 = SecureStudentRecord(s2)

    # Pre-add CS201 for the new semester before setting grade
    s1.course_records.setdefault("2025S2", []).append(("CS201", 4, None))
    s2.course_records.setdefault("2025S2", []).append(("CS201", 4, None))

    # Now assign grades safely
    secure_s1.set_grade("CS201", "2025S2", "A-")
    secure_s2.set_grade("CS201", "2025S2", "B")

    print("\nGPAs and statuses:")
    print(f"{s1.full_name} GPA: {secure_s1.get_gpa()} Status: {secure_s1.get_academic_status()}")
    print(f"{s2.full_name} GPA: {secure_s2.get_gpa()} Status: {secure_s2.get_academic_status()}")

    # Demonstrate polymorphism: call get_responsibilities on mixed list
    print("\n=== Polymorphism demo: responsibilities ===")
    people = [s1, s3] + faculty
    for p in people:
        workload = getattr(p, 'calculate_workload', lambda: 'N/A')()
        print(f"{p.full_name} ({p.__class__.__name__}): {p.get_responsibilities()} workload_metric={workload}")

    # Show faculty workload calculations
    print("\nFaculty workloads:")
    for f in faculty:
        f.assign_course("CS101")
        f.assign_course("CS201")
        print(f"{f.full_name} ({f.__class__.__name__}) workload -> {f.calculate_workload()}")

    # Demonstrate SecureStudentRecord input validation
    print("\nSecure record validation test:")
    try:
        secure_s1.private_notes = "Good progress."
        secure_s1.private_notes = 123  # should raise
    except Exception as exc:
        print("Caught expected type error for private_notes:", type(exc).__name__, exc)

    # Demonstrate dropping: drop s2 from CS201
    cs.drop(s2.student_id, "CS201")
    print("\nAfter drop, CS201 enrolled:", list(cs.courses["CS201"].enrolled_students))

    print("\nDemo finished.")


if __name__ == "__main__":
    print("Running demo scenario...\n")
    demo_registration_and_gpa()
