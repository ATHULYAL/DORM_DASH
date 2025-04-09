# filepath: /c:/Users/lincy/Desktop/mp/model.py
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ✅ This is the correct primary key
    name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
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
    student_id = db.Column(db.Integer, nullable=False)  # Add this line
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    leave_from = db.Column(db.Date, nullable=False)
    leave_until = db.Column(db.Date, nullable=False)
    place_of_travel = db.Column(db.String(255), nullable=False)
    mode_of_travel = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Leave {self.name} from {self.leave_from} to {self.leave_until}>'
class Stu(db.Model):
    __tablename__ = 'stu'
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(20), nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class FeeDetails(db.Model):
    __tablename__ = 'fees'
    fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    email = db.Column(db.String(100), db.ForeignKey('stu.username'), nullable=False)
    month = db.Column(db.String(20), nullable=False)  # Store the month as a string
    year = db.Column(db.Integer, nullable=False)  # Store the year as an integer
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Not Paid')
    transaction_id = db.Column(db.String(100), nullable=True) 
    
    student = db.relationship('Student', backref='fee_details')

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feedback = db.Column(db.Text, nullable=False)
    room_no = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default="pending", nullable=False)# Removed ForeignKey constraint




    