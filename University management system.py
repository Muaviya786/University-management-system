import datetime
from typing import List, Dict, Optional


class Student:
    def __init__(self, student_id: str, name: str, address: str):
        self.student_id = student_id
        self.name = name
        self.address = address
        self.courses: List[Course] = []
        self.grades: Dict[str, float] = {}
        self.attendance: Dict[str, Dict[datetime.date, bool]] = {}
        self.gpa: float = 0.0

    def update_details(self, name: Optional[str] = None, address: Optional[str] = None):
        if name:
            self.name = name
        if address:
            self.address = address

    def enroll_course(self, course: 'Course'):
        if course not in self.courses:
            self.courses.append(course)
            self.attendance[course.course_id] = {}

    def record_grade(self, course: 'Course', grade: float):
        self.grades[course.course_id] = grade
        self._update_gpa()

    def mark_attendance(self, course: 'Course', date: datetime.date, present: bool):
        if course.course_id not in self.attendance:
            self.attendance[course.course_id] = {}
        if date in self.attendance[course.course_id]:
            print(f"Warning: Overwriting existing attendance record for {date}")
        self.attendance[course.course_id][date] = present

    def _update_gpa(self):
        total_points = sum(grade * course.credits for course, grade in self.grades.items())
        total_credits = sum(course.credits for course in self.courses)
        self.gpa = total_points / total_credits if total_credits > 0 else 0.0

    def get_attendance_percentage(self, course: 'Course') -> float:
        course_attendance = self.attendance.get(course.course_id, {})
        total_days = len(course_attendance)
        days_present = sum(1 for present in course_attendance.values() if present)
        return (days_present / total_days * 100) if total_days > 0 else 0.0


class Faculty:
    def __init__(self, faculty_id: str, name: str):
        self.faculty_id = faculty_id
        self.name = name
        self.courses_assigned: List[Course] = []
        self.availability: Dict[str, List[str]] = {day: [] for day in
                                                   ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
        self.performance_rating: float = 0.0
        self.student_feedback: List[str] = []

    def assign_course(self, course: 'Course'):
        if course not in self.courses_assigned:
            self.courses_assigned.append(course)

    def set_availability(self, day: str, times: List[str]):
        if day in self.availability:
            self.availability[day] = times

    def add_student_feedback(self, feedback: str):
        self.student_feedback.append(feedback)

    def update_performance_rating(self, rating: float):
        self.performance_rating = rating


class Course:
    def __init__(self, course_id: str, name: str, credits: int, schedule: Dict[str, str],
                 prerequisites: Optional[List[str]] = None):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.schedule = schedule
        self.prerequisites = prerequisites or []
        self.students: List[Student] = []
        self.faculty: Optional[Faculty] = None

    def assign_faculty(self, faculty: Faculty):
        self.faculty = faculty

    def enroll_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)

    def remove_student(self, student: Student):
        if student in self.students:
            self.students.remove(student)

    def modify_schedule(self, new_schedule: Dict[str, str]):
        self.schedule = new_schedule

    def notify_students(self, message: str):
        for student in self.students:
            print(f"Notification to {student.name}: {message}")


class UniversitySystem:
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        self.faculty: Dict[str, Faculty] = {}
        self.tuition_fees: Dict[str, float] = {}
        self.scholarships: Dict[str, float] = {}

    def add_student(self, student_id: str, name: str, address: str):
        if student_id not in self.students:
            new_student = Student(student_id, name, address)
            self.students[student_id] = new_student
            print(f"Student {name} added.")
        else:
            print(f"Student with ID {student_id} already exists.")

    def update_student(self, student_id: str, name: Optional[str] = None, address: Optional[str] = None):
        if student_id in self.students:
            student = self.students[student_id]
            student.update_details(name, address)
            print(f"Student {student_id} details updated.")
        else:
            print(f"Student {student_id} not found.")

    def search_student(self, student_id: str) -> Optional[Student]:
        student = self.students.get(student_id)
        if student:
            print(f"Student ID: {student.student_id}, Name: {student.name}, Address: {student.address}")
            return student
        else:
            print("Student not found.")
            return None

    def add_course(self, course_id: str, name: str, credits: int, schedule: Dict[str, str],
                   prerequisites: Optional[List[str]] = None):
        if course_id not in self.courses:
            new_course = Course(course_id, name, credits, schedule, prerequisites)
            self.courses[course_id] = new_course
            print(f"Course {name} added.")
        else:
            print(f"Course with ID {course_id} already exists.")

    def assign_faculty(self, course_id: str, faculty_id: str):
        if course_id in self.courses and faculty_id in self.faculty:
            faculty = self.faculty[faculty_id]
            course = self.courses[course_id]
            course.assign_faculty(faculty)
            faculty.assign_course(course)
            print(f"Faculty {faculty.name} assigned to course {course.name}.")
        else:
            print("Course or Faculty not found.")

    def enroll_student_in_course(self, student_id: str, course_id: str):
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]

            # Check prerequisites
            if all(prereq in [c.course_id for c in student.courses] for prereq in course.prerequisites):
                course.enroll_student(student)
                student.enroll_course(course)
                print(f"Student {student.name} enrolled in course {course.name}.")
            else:
                print(f"Student {student.name} does not meet prerequisites for course {course.name}.")
        else:
            print("Student or Course not found.")

    def remove_student_from_course(self, student_id: str, course_id: str):
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]
            course.remove_student(student)
            student.courses = [c for c in student.courses if c.course_id != course_id]
            print(f"Student {student.name} removed from course {course.name}.")
        else:
            print("Student or Course not found.")

    def record_student_grade(self, student_id: str, course_id: str, grade: float):
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]
            student.record_grade(course, grade)
            print(f"Grade {grade} recorded for {student.name} in {course.name}.")
        else:
            print("Student or Course not found.")

    def add_faculty(self, faculty_id: str, name: str):
        if faculty_id not in self.faculty:
            new_faculty = Faculty(faculty_id, name)
            self.faculty[faculty_id] = new_faculty
            print(f"Faculty {name} added.")
        else:
            print(f"Faculty with ID {faculty_id} already exists.")

    def modify_course(self, course_id: str, name: Optional[str] = None, credits: Optional[int] = None,
                      schedule: Optional[Dict[str, str]] = None):
        if course_id in self.courses:
            course = self.courses[course_id]
            if name:
                course.name = name
            if credits is not None:
                course.credits = credits
            if schedule:
                course.modify_schedule(schedule)
            print(f"Course {course_id} modified.")
        else:
            print("Course not found.")

    def generate_report(self):
        print("\nUniversity Report:")
        print(f"Total Students: {len(self.students)}")
        print(f"Total Courses: {len(self.courses)}")
        print(f"Total Faculty: {len(self.faculty)}")
        for course_id, course in self.courses.items():
            print(f"\nCourse: {course.name}")
            print(f"Faculty: {course.faculty.name if course.faculty else 'Not assigned'}")
            print(f"Enrolled Students: {len(course.students)}")
            for student in course.students:
                grade = student.grades.get(course_id, "Not graded")
                attendance = student.get_attendance_percentage(course)
                print(f" - {student.name}, Grade: {grade}, Attendance: {attendance:.2f}%")

    def update_tuition_fees(self, course_id: str, new_fee: float):
        if course_id in self.courses:
            self.tuition_fees[course_id] = new_fee
            print(f"Tuition fees for course {course_id} updated to: {new_fee}")
        else:
            print("Course not found.")

    def update_scholarship(self, student_id: str, amount: float):
        if student_id in self.students:
            self.scholarships[student_id] = amount
            print(f"Scholarship of {amount} allocated to {self.students[student_id].name}.")
        else:
            print("Student not found.")

    def generate_class_schedule(self):
        schedule = {day: {} for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
        for course in self.courses.values():
            for day, time in course.schedule.items():
                if time in schedule[day]:
                    print(f"Scheduling conflict: {course.name} on {day} at {time}")
                else:
                    schedule[day][time] = course.name
        return schedule

    def update_class_schedule(self, course_id: str, new_schedule: Dict[str, str]):
        if course_id in self.courses:
            course = self.courses[course_id]
            old_schedule = course.schedule
            course.modify_schedule(new_schedule)

            # Check for conflicts
            for day, time in new_schedule.items():
                for other_course in self.courses.values():
                    if other_course != course and other_course.schedule.get(day) == time:
                        print(f"Scheduling conflict: {course.name} and {other_course.name} on {day} at {time}")
                        course.modify_schedule(old_schedule)
                        return

            print(f"Schedule updated for course {course.name}")
            course.notify_students(f"Schedule for {course.name} has been updated.")
        else:
            print("Course not found.")

    def calculate_retention_rate(self) -> float:
        # Simplified retention rate calculation
        total_students = len(self.students)
        active_students = sum(1 for student in self.students.values() if student.courses)
        return (active_students / total_students) * 100 if total_students > 0 else 0

    def calculate_graduation_rate(self) -> float:
        # Simplified graduation rate calculation
        total_students = len(self.students)
        graduated_students = sum(1 for student in self.students.values() if
                                 student.gpa >= 2.0)  # Assuming 2.0 GPA is required for graduation
        return (graduated_students / total_students) * 100 if total_students > 0 else 0

    def generate_performance_report(self):
        report = "Academic Performance Report\n"
        report += "===========================\n"
        for student in self.students.values():
            report += f"Student: {student.name} (ID: {student.student_id})\n"
            report += f"GPA: {student.gpa:.2f}\n"
            for course in student.courses:
                grade = student.grades.get(course.course_id, "Not graded")
                attendance = student.get_attendance_percentage(course)
                report += f"  Course: {course.name}, Grade: {grade}, Attendance: {attendance:.2f}%\n"
            report += "\n"
        return report

    def display_menu(self):
        while True:
            print("\n--- University Management System ---")
            print("1. Student Management")
            print("2. Course Management")
            print("3. Faculty Management")
            print("4. Class Timetable and Scheduling")
            print("5. Examination and Grading System")
            print("6. Administration and Reporting")
            print("7. Exit")

            choice = input("Select an option (1-7): ")

            if choice == '1':
                self.student_management_menu()
            elif choice == '2':
                self.course_management_menu()
            elif choice == '3':
                self.faculty_management_menu()
            elif choice == '4':
                self.schedule_management_menu()
            elif choice == '5':
                self.examination_management_menu()
            elif choice == '6':
                self.administration_management_menu()
            elif choice == '7':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def student_management_menu(self):
        while True:
            print("\n--- Student Management ---")
            print("1. Add New Student")
            print("2. Update Student Information")
            print("3. View Student Profile")
            print("4. Track Attendance")
            print("5. View Academic Performance")
            print("6. Back to Main Menu")

            choice = input("Select an option (1-6): ")

            if choice == '1':
                student_id = input("Enter student ID: ")
                name = input("Enter student name: ")
                address = input("Enter student address: ")
                self.add_student(student_id, name, address)
            elif choice == '2':
                student_id = input("Enter student ID to update: ")
                name = input("Enter new name (leave blank if no change): ")
                address = input("Enter new address (leave blank if no change): ")
                self.update_student(student_id, name=name or None, address=address or None)
            elif choice == '3':
                student_id = input("Enter student ID to view: ")
                student = self.search_student(student_id)
                if student:
                    print(f"Enrolled Courses: {', '.join(course.name for course in student.courses)}")
                    print(f"GPA: {student.gpa:.2f}")
            elif choice == '4':
                student_id = input("Enter student ID to track attendance: ")
                course_id = input("Enter course ID: ")
                date_str = input("Enter date (YYYY-MM-DD): ")
                present = input("Is the student present? (yes/no): ").lower() == 'yes'
                if student_id in self.students and course_id in self.courses:
                    student = self.students[student_id]
                    course = self.courses[course_id]
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    student.mark_attendance(course, date, present)
                    print(f"Attendance marked for {student_id} in course {course_id} on {date_str}.")
                else:
                    print("Student or Course not found.")
            elif choice == '5':
                student_id = input("Enter student ID to view academic performance: ")
                if student_id in self.students:
                    student = self.students[student_id]
                    print(f"Academic Performance for {student.name}:")
                    print(f"GPA: {student.gpa:.2f}")
                    for course in student.courses:
                        grade = student.grades.get(course.course_id, "Not graded")
                        attendance = student.get_attendance_percentage(course)
                        print(f"Course: {course.name}, Grade: {grade}, Attendance: {attendance:.2f}%")
                else:
                    print("Student not found.")
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def course_management_menu(self):
        while True:
            print("\n--- Course Management ---")
            print("1. Add New Course")
            print("2. Modify Course")
            print("3. Assign Faculty to Course")
            print("4. Enroll Student in Course")
            print("5. Remove Student from Course")
            print("6. View Course Details")
            print("7. Back to Main Menu")

            choice = input("Select an option (1-7): ")

            if choice == '1':
                course_id = input("Enter course ID: ")
                name = input("Enter course name: ")
                credits = int(input("Enter course credits: "))
                schedule = {}
                while True:
                    day = input("Enter day (or 'done' to finish): ")
                    if day.lower() == 'done':
                        break
                    time = input(f"Enter time for {day}: ")
                    schedule[day] = time
                prerequisites = input("Enter prerequisite course IDs (comma-separated, or leave blank): ").split(
                    ',')
                prerequisites = [p.strip() for p in prerequisites if p.strip()]
                self.add_course(course_id, name, credits, schedule, prerequisites)
            elif choice == '2':
                course_id = input("Enter course ID to modify: ")
                name = input("Enter new course name (leave blank if no change): ")
                credits = input("Enter new course credits (leave blank if no change): ")
                schedule = {}
                while True:
                    day = input("Enter day to update schedule (or 'done' to finish): ")
                    if day.lower() == 'done':
                        break
                    time = input(f"Enter new time for {day}: ")
                    schedule[day] = time
                self.modify_course(course_id, name=name or None, credits=int(credits) if credits else None,
                                   schedule=schedule or None)
            elif choice == '3':
                course_id = input("Enter course ID: ")
                faculty_id = input("Enter faculty ID: ")
                self.assign_faculty(course_id, faculty_id)
            elif choice == '4':
                student_id = input("Enter student ID: ")
                course_id = input("Enter course ID: ")
                self.enroll_student_in_course(student_id, course_id)
            elif choice == '5':
                student_id = input("Enter student ID: ")
                course_id = input("Enter course ID: ")
                self.remove_student_from_course(student_id, course_id)
            elif choice == '6':
                course_id = input("Enter course ID to view details: ")
                if course_id in self.courses:
                    course = self.courses[course_id]
                    print(f"Course: {course.name} (ID: {course.course_id})")
                    print(f"Credits: {course.credits}")
                    print(f"Schedule: {course.schedule}")
                    print(f"Prerequisites: {', '.join(course.prerequisites)}")
                    print(f"Enrolled Students: {len(course.students)}")
                    print(f"Faculty: {course.faculty.name if course.faculty else 'Not assigned'}")
                else:
                    print("Course not found.")
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def faculty_management_menu(self):
        while True:
            print("\n--- Faculty Management ---")
            print("1. Add New Faculty")
            print("2. Update Faculty Records")
            print("3. View Assigned Courses")
            print("4. Set Faculty Availability")
            print("5. Record Faculty Performance")
            print("6. Back to Main Menu")

            choice = input("Select an option (1-6): ")

            if choice == '1':
                faculty_id = input("Enter faculty ID: ")
                name = input("Enter faculty name: ")
                self.add_faculty(faculty_id, name)
            elif choice == '2':
                faculty_id = input("Enter faculty ID to update: ")
                name = input("Enter new name (leave blank if no change): ")
                if faculty_id in self.faculty:
                    faculty = self.faculty[faculty_id]
                    if name:
                        faculty.name = name
                    print(f"Faculty {faculty_id} updated.")
                else:
                    print("Faculty not found.")
            elif choice == '3':
                faculty_id = input("Enter faculty ID to view courses: ")
                if faculty_id in self.faculty:
                    faculty = self.faculty[faculty_id]
                    print(f"Courses assigned to {faculty.name}:")
                    for course in faculty.courses_assigned:
                        print(f"- {course.name} (ID: {course.course_id})")
                else:
                    print("Faculty not found.")
            elif choice == '4':
                faculty_id = input("Enter faculty ID to set availability: ")
                if faculty_id in self.faculty:
                    faculty = self.faculty[faculty_id]
                    day = input("Enter day to set availability: ")
                    times = input("Enter available times (comma-separated): ").split(',')
                    faculty.set_availability(day, [t.strip() for t in times])
                    print(f"Availability set for {faculty.name} on {day}.")
                else:
                    print("Faculty not found.")
            elif choice == '5':
                faculty_id = input("Enter faculty ID to record performance: ")
                if faculty_id in self.faculty:
                    faculty = self.faculty[faculty_id]
                    rating = float(input("Enter performance rating (0-5): "))
                    feedback = input("Enter student feedback: ")
                    faculty.update_performance_rating(rating)
                    faculty.add_student_feedback(feedback)
                    print(f"Performance recorded for {faculty.name}.")
                else:
                    print("Faculty not found.")
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def schedule_management_menu(self):
        while True:
            print("\n--- Class Timetable and Scheduling ---")
            print("1. Generate Class Schedule")
            print("2. Update Class Schedule")
            print("3. View Class Schedule")
            print("4. Back to Main Menu")

            choice = input("Select an option (1-4): ")

            if choice == '1':
                schedule = self.generate_class_schedule()
                print("\nGenerated Class Schedule:")
                for day, times in schedule.items():
                    print(f"{day}:")
                    for time, course in times.items():
                        print(f"  {time}: {course}")
            elif choice == '2':
                course_id = input("Enter course ID to update schedule: ")
                new_schedule = {}
                while True:
                    day = input("Enter day (or 'done' to finish): ")
                    if day.lower() == 'done':
                        break
                    time = input(f"Enter time for {day}: ")
                    new_schedule[day] = time
                self.update_class_schedule(course_id, new_schedule)
            elif choice == '3':
                print("\nCurrent Class Schedule:")
                for course in self.courses.values():
                    print(f"{course.name} (ID: {course.course_id}):")
                    for day, time in course.schedule.items():
                        print(f"  {day}: {time}")
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def examination_management_menu(self):
        while True:
            print("\n--- Examination and Grading System ---")
            print("1. Record Exam Results")
            print("2. Calculate GPA")
            print("3. Generate Academic Performance Report")
            print("4. Back to Main Menu")

            choice = input("Select an option (1-4): ")

            if choice == '1':
                student_id = input("Enter student ID: ")
                course_id = input("Enter course ID: ")
                grade = float(input("Enter exam grade: "))
                self.record_student_grade(student_id, course_id, grade)
            elif choice == '2':
                student_id = input("Enter student ID to calculate GPA: ")
                if student_id in self.students:
                    student = self.students[student_id]
                    print(f"GPA for {student.name}: {student.gpa:.2f}")
                else:
                    print("Student not found.")
            elif choice == '3':
                report = self.generate_performance_report()
                print(report)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def administration_management_menu(self):
        while True:
            print("\n--- Administration and Reporting ---")
            print("1. Generate Enrollment Report")
            print("2. Update Tuition Fees")
            print("3. Update Scholarship")
            print("4. Calculate Retention Rate")
            print("5. Calculate Graduation Rate")
            print("6. Back to Main Menu")

            choice = input("Select an option (1-6): ")

            if choice == '1':
                self.generate_report()
            elif choice == '2':
                course_id = input("Enter course ID to update tuition fee: ")
                new_fee = float(input("Enter new tuition fee: "))
                self.update_tuition_fees(course_id, new_fee)
            elif choice == '3':
                student_id = input("Enter student ID for scholarship update: ")
                amount = float(input("Enter scholarship amount: "))
                self.update_scholarship(student_id, amount)
            elif choice == '4':
                retention_rate = self.calculate_retention_rate()
                print(f"Current retention rate: {retention_rate:.2f}%")
            elif choice == '5':
                graduation_rate = self.calculate_graduation_rate()
                print(f"Current graduation rate: {graduation_rate:.2f}%")
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")


university_system = UniversitySystem()
university_system.display_menu()