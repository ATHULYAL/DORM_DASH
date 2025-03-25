# filepath: /c:/Users/lincy/Desktop/mp/model.py
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    academic_year_start = db.Column(db.Integer, nullable=False)
    academic_year_end = db.Column(db.Integer, nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    guardian_name = db.Column(db.String(100), nullable=False)
    guardian_phone = db.Column(db.String(20), nullable=False)

class Admin(db.Model):
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
class MealPlan(db.Model):
    meal_date = db.Column(db.Date, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())
class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
class Room(db.Model):
    __tablename__ = 'room_details'
    room_no = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=True)
    strength = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    
class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Present', 'Absent'), nullable=False)

class Leave(db.Model):
    __tablename__ = 'leaveform'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    leave_from = db.Column(db.Date, nullable=False)
    leave_until = db.Column(db.Date, nullable=False)
    place_of_travel = db.Column(db.String(255), nullable=False)
    mode_of_travel = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

class StudentCredentials(db.Model):
    __tablename__ = 'slog'
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False, unique=True)
    student = db.relationship('Student', backref=db.backref('credentials', uselist=False))

    def __init__(self, username, password, student_id):
        self.username = username
        self.password = password
        self.student_id = student_id
class FeeDetails(db.Model):
    __tablename__ = 'fee_details'
    fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Paid', 'Pending', 'Overdue'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __init__(self, student_id, amount, due_date, status):
        self.student_id = student_id
        self.amount = amount
        self.due_date = due_date
        self.status = status