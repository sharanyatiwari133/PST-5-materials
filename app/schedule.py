import json
import datetime
import csv
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.finance_log = []
        self.attendance_log = []
        self.next_lesson_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # TODO: Load students, teachers, and courses as before.
                for student in data["students"]:
                    student_object = StudentUser(student["id"], student["name"])
                    student_object.enrolled_course_ids = student["enrolled_course_ids"]
                    self.students.append(student_object)

                for teacher in data["teachers"]:
                    teacher_object = TeacherUser(teacher["id"], teacher["name"], teacher["speciality"])
                    self.teachers.append(teacher_object)

                for course in data["courses"]:
                    course_object = Course(
                        course["id"],
                        course["name"],
                        course["instrument"],
                        course["teacher_id"]
                    ) 
                    course_object.enrolled_student_ids = course["enrolled_student_ids"] 
                    course_object.lessons = course["lessons"]  
                    self.courses.append(course_object)

                
                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
                self.attendance_log = data.get("attendance", [])
                self.finance_log = data.get("finance_log", [])
                self.next_lesson_id = data.get("next_lesson_id", 1)
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],

            # TODO: Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            "finance_log": self.finance_log,
            "next_lesson_id": self.next_lesson_id
            # ... (next_id counters) ...
        }

        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
             json.dump(data_to_save, f, indent=4)

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
    
        if not student or not course:
           print("Error: Check-in failed. Invalid Student or Course ID.")
           return False
        
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
    
        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print("Success: Student {student.name} checked into {course.name}.")
        return True
 
    def find_student_by_id(self, student_id):
            for student in self.students:
                if student.id == student_id:
                   return student
            return None

    def find_course_by_id(self, course_id):
            for course in self.courses:
                if course.id == course_id:
                   return course
            return None

    def create_course(self, name, instrument, teacher_id):
        course_id = len(self.courses) + 1

        new_course = Course(course_id, name, instrument, teacher_id)

        self.courses.append(new_course)
        self._save_data()

        return new_course
    
    def register_new_student(self, name, instrument):
        """Registers a new student."""
        student_id = len(self.students) + 1
        new_student = StudentUser(student_id, name)
        self.students.append(new_student)

        for course in self.courses:
            if course.instrument == instrument:
               course.enrolled_student_ids.append(student_id)
               new_student.enrolled_course_ids.append(course.id)
               self._save_data()
               return new_student
        return None

    
    def record_payment(self, student_id, amount, method):
        payment_record = {
            "student_id": student_id,
            "amount": amount,
            "method": method,
            "timestamp": datetime.datetime.now().isoformat()
        }

        self.finance_log.append(payment_record)
        self._save_data()

        print(f"Payment of {amount} recorded for student ID {student_id}.")

    def get_payment_history(self, student_id):
        return [
            payment for payment in self.finance_log
            if payment["student_id"] == student_id
        ]

    def export_report(self, kind, out_path):
        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]

        elif kind == "attendance":
            data_to_export = self.attendance_log
            headers = ["student_id", "course_id", "timestamp"]

        else:
            print("Error: Unknown report type.")
            return

        with open(out_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_to_export)

        print(f"{kind.capitalize()} report exported to {out_path}.")