# filepath: /c:/Users/lincy/Desktop/mp/app.py
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, send_from_directory
from sqlalchemy import text
from db import db

# Add MealPlan to the imports from model
  # Added MealPlan here

# Add these configurations after creating Flask app
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourusername:yourpassword@localhost/hostel_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)
@app.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
# Import models after db initialization
with app.app_context():
    from model import Student, Admin, MealPlan, Notice, Room, Attendance,StudentCredentials

@app.route('/')
def home():
    return render_template('loginpage.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Strip whitespace from inputs
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # First check admin table using SQL query
        admin_query = text("SELECT username FROM admin WHERE username = :username AND password = :password")
        result = db.session.execute(admin_query, {"username": username, "password": password})
        admin = result.fetchone()

        if admin:
            # Admin login successful
            return redirect(url_for('dashboard', admin_username=username))

        # If not admin, check student table using SQL query with debug logging
        student_query = text("""
            SELECT name 
            FROM student 
            WHERE TRIM(email) = :email 
            AND TRIM(phone) = :phone
        """)
        result = db.session.execute(student_query, {"email": username, "phone": password})
        student = result.fetchone()

        if student:
            # Student login successful
            return redirect(url_for('student_dashboard', student_name=student.name))

        # For debugging: Print attempted credentials
        print(f"Login attempt - Email: '{username}', Phone: '{password}'")
        
        # If neither admin nor student
        flash('Invalid username/email or password/phone', 'error')
        return redirect(url_for('home'))

    except Exception as e:
        print(f"Login error details: {str(e)}")  # Debug logging
        flash(f'Login error: {str(e)}', 'error')
        return redirect(url_for('home'))
@app.route('/dashboard')
def dashboard():
    try:
        admin_username = request.args.get('admin_username')
        if not admin_username:
            return redirect(url_for('home'))
            
        # Get the most recent notices from the database
        notices = Notice.query.order_by(Notice.date.desc()).limit(5).all()
        
        return render_template('addash.html', 
                             admin_username=admin_username,
                             notices=notices)
                             
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('home'))
@app.route('/student_dashboard')
def student_dashboard():
    try:
        student_name = request.args.get('student_name')
        latest_meal_plan = MealPlan.query.order_by(MealPlan.meal_date.desc()).first()
        
        # Debug print
        if latest_meal_plan:
            print(f"Meal plan found:")
            print(f"- File path: {latest_meal_plan.file_path}")
            print(f"- Full path: {os.path.join(app.static_folder, latest_meal_plan.file_path)}")
            print(f"- File exists: {os.path.exists(os.path.join(app.static_folder, latest_meal_plan.file_path))}")
        
        return render_template('sdash.html',
                             student_name=student_name,
                             meal_plan=latest_meal_plan)
                             
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return redirect(url_for('home'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    admin_username = request.args.get('admin_username')
    if request.method == 'POST':
        full_name = request.form['full_name']
        registration_number = request.form['registration_number']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        academic_year_start = request.form['academic_year_start']
        academic_year_end = request.form['academic_year_end']
        room_number = request.form['room_number']
        guardian_name = request.form['guardian_name']
        guardian_phone = request.form['guardian_phone']


        new_student = Student(
            name=full_name,
            registration_number=registration_number,
            address=address,
            email=email,
            phone=phone,
            course=course,
            academic_year_start=academic_year_start,
            academic_year_end=academic_year_end,
            room_number=room_number,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone
        )


        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Student registered successfully!', 'success')
            return redirect(url_for('register', admin_username=admin_username))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('register', admin_username=admin_username))
    return render_template('register.html', admin_username=admin_username)

@app.route('/student_details')
def student_details():
    try:
        admin_username = request.args.get('admin_username')
        students = Student.query.order_by(Student.name).all()
        return render_template('sdetails.html', 
                             admin_username=admin_username,
                             students=students)
    except Exception as e:
        flash(f'Error loading student details: {str(e)}', 'error')
        return redirect(url_for('dashboard', admin_username=admin_username))

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    try:
        admin_username = request.args.get('admin_username')
        student = Student.query.get_or_404(student_id)
        
        if request.method == 'POST':
            student.name = request.form['full_name']
            student.registration_number = request.form['registration_number']
            student.address = request.form['address']
            student.email = request.form['email']
            student.phone = request.form['phone']
            student.course = request.form['course']
            student.academic_year_start = request.form['academic_year_start']
            student.academic_year_end = request.form['academic_year_end']
            student.room_number = request.form['room_number']
            student.guardian_name = request.form['guardian_name']
            student.guardian_phone = request.form['guardian_phone']
            
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('student_details', admin_username=admin_username))
            
        return render_template('edit_student.html', 
                             student=student,
                             admin_username=admin_username)
                             
    except Exception as e:
        flash(f'Error updating student: {str(e)}', 'error')
        return redirect(url_for('student_details', admin_username=admin_username))

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        admin_username = request.args.get('admin_username')
        student = Student.query.get_or_404(student_id)

        # Delete the student record
        db.session.delete(student)
        db.session.commit()

        flash('Student deleted successfully!', 'success')
        return redirect(url_for('student_details', admin_username=admin_username))
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
        return redirect(url_for('student_details', admin_username=admin_username))

@app.route('/test_db')
def test_db():
    try:
        # Perform a simple query
        students = Student.query.all()
        return f"Connected to the database! Found {len(students)} students."
    except Exception as e:
        return f"Failed to connect to the database. Error: {str(e)}"

# Add after imports
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(request.referrer)

    file = request.files['file']
    upload_date = datetime.now().date()

    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Save file with date in filename
        file_extension = filename.rsplit('.', 1)[1].lower()
        new_filename = f"upload_{upload_date}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)
    
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    flash('Invalid file type', 'danger')
    return redirect(request.referrer)
@app.route('/upload', methods=['GET'])
def upload():
    admin_username = request.args.get('admin_username', 'Admin')
    return render_template('mealplan.html', admin_username=admin_username)


@app.route('/mealplan')
def mealplan():
    admin_username = request.args.get('admin_username', 'Admin')
    return render_template('mealplan.html', admin_username=admin_username)

@app.route('/upload_meal_plan', methods=['POST'])
def upload_meal_plan():
    if 'file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(request.referrer)
    
    file = request.files['file']
    meal_date = request.form['date']
    
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.referrer)
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            new_filename = f"meal_plan_{meal_date}_{filename}"
            # Store relative path in database
            relative_path = os.path.join('uploads', new_filename)
            # Use absolute path for saving file
            absolute_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            
            # Save the file
            file.save(absolute_path)
            
            # Convert meal_date string to date object
            meal_date_obj = datetime.strptime(meal_date, '%Y-%m-%d').date()
            
            # Create or update meal plan record
            meal_plan = MealPlan.query.filter_by(meal_date=meal_date_obj).first()
            if meal_plan:
                meal_plan.file_path = relative_path
            else:
                meal_plan = MealPlan(
                    meal_date=meal_date_obj,
                    file_path=relative_path
                )
                db.session.add(meal_plan)
                
            db.session.commit()
            flash('Meal plan uploaded successfully!', 'success')
            return redirect(url_for('mealplan'))
            
        except Exception as e:
            flash(f'Error saving meal plan: {str(e)}', 'danger')
            db.session.rollback()
            return redirect(request.referrer)
    
    flash('Invalid file type', 'danger')
    return redirect(request.referrer)

@app.route('/notice')
def notice():
    admin_username = request.args.get('admin_username', 'Admin')
    notices = Notice.query.order_by(Notice.date.desc()).all()
    return render_template('notice.html', admin_username=admin_username, notices=notices)

@app.route('/add_notice', methods=['POST'])
def add_notice():
    try:
        title = request.form['title']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        admin_username = request.args.get('admin_username')
        
        notice = Notice(
            title=title,
            description=description,
            date=date
                    )
        
        db.session.add(notice)
        db.session.commit()
        flash('Notice added successfully!', 'success')
        
    except Exception as e:
        flash(f'Error adding notice: {str(e)}', 'danger')
        db.session.rollback()
        
    return redirect(url_for('notice'))
@app.route('/delete_notice', methods=['POST'])
def delete_notice():
    try:
        title = request.form['remove-title']
        admin_username = request.args.get('admin_username')
        notice = Notice.query.filter_by(title=title).first()
        
        if notice:
            db.session.delete(notice)
            db.session.commit()
            flash('Notice deleted successfully!', 'success')
        else:
            flash('Notice not found!', 'danger')
            
    except Exception as e:
        flash(f'Error deleting notice: {str(e)}', 'danger')
        db.session.rollback()
        
    return redirect(url_for('notice'))
@app.route('/rooms')
def rooms():
    admin_username = request.args.get('admin_username', 'Admin')
    rooms = Room.query.order_by(Room.room_no).all()
    return render_template('adroom.html', admin_username=admin_username, rooms=rooms)

@app.route('/add_room', methods=['POST'])
def add_room():
    try:
        room_no = int(request.form.get('room_no', 0))
        capacity = int(request.form.get('capacity', 0))
        strength = int(request.form.get('strength', 0))
        
        if room_no <= 0 or capacity <= 0:
            flash('Invalid room number or capacity', 'danger')
            return redirect(url_for('rooms', admin_username=request.args.get('admin_username')))
        
        # Calculate status based on capacity and strength
        if strength == 0:
            status = "Vacant"
        elif strength == capacity:
            status = "Occupied"
        else:
            vacancies = capacity - strength
            status = f"{vacancies} Vacancy"

        # Check if room already exists
        room = Room.query.filter_by(room_no=room_no).first()
        if room:
            # Update existing room
            room.capacity = capacity
            room.strength = strength
            room.status = status
        else:
            # Create new room
            room = Room(
                room_no=room_no,
                capacity=capacity,
                strength=strength,
                status=status
            )
            db.session.add(room)

        db.session.commit()
        flash('Room details saved successfully!', 'success')
        
    except ValueError as e:
        flash('Please enter valid numbers for room details', 'danger')
        db.session.rollback()
    except Exception as e:
        flash(f'Error saving room details: {str(e)}', 'danger')
        db.session.rollback()
        
    return redirect(url_for('rooms', admin_username=request.args.get('admin_username')))
@app.route('/logout')
def logout():
    return redirect(url_for('home'))  # 'home' route renders loginpage.html
@app.route('/attendance')
def attendance():
    try:
        admin_username = request.args.get('admin_username', 'Admin')
        selected_year = request.args.get('year', '1st Year')
        current_year = datetime.now().year
        
        if 'MCA' in selected_year:
            if selected_year == 'MCA 1st Year':
                students = Student.query.filter(
                    Student.course == 'MCA',
                    current_year - Student.academic_year_start == 0
                ).order_by(Student.name).all()
            else:
                students = Student.query.filter(
                    Student.course == 'MCA',
                    current_year - Student.academic_year_start == 1
                ).order_by(Student.name).all()
        else:
            year_map = {
                '1st Year': 2024,  # Students who joined in 2024
                '2nd Year': 2023,  # Students who joined in 2023
                '3rd Year': 2022,  # Students who joined in 2022
                '4th Year': 2021   # Students who joined in 2021
            }
            join_year = year_map.get(selected_year)
            
            # Filter students based on exact joining year
            students = Student.query.filter(
                Student.course != 'MCA',
                Student.academic_year_start == join_year
            ).order_by(Student.name).all()

        return render_template(
            'adattendence.html',
            admin_username=admin_username,
            students=students,
            selected_year=selected_year
        )

    except Exception as e:
        flash(f'Error loading attendance page: {str(e)}', 'danger')
        return redirect(url_for('dashboard', admin_username=admin_username))
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    try:
        student_id = request.form.get('student_id')
        status = request.form.get('status')
        date_str = request.form.get('date')
        
        if not all([student_id, status, date_str]):
            return jsonify({
                'success': False, 
                'message': 'Missing required fields'
            })

        # Convert student_id to integer
        student_id = int(student_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            })
        
        # Check if attendance already exists
        attendance = Attendance.query.filter_by(
            student_id=student_id,
            attendance_date=date
        ).first()

        if attendance:
            attendance.status = status
        else:
            attendance = Attendance(
                student_id=student_id,
                attendance_date=date,
                status=status
            )
            db.session.add(attendance)

        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Attendance marked successfully'
        })

    except Exception as e:
        print(f"Error marking attendance: {str(e)}")  # For debugging
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': str(e)
        })


    except Exception as e:
        flash(f'Error loading student details: {str(e)}', 'error')
        return redirect(url_for('dashboard', admin_username=admin_username))


if __name__ == "__main__":
    app.run(debug=True)
