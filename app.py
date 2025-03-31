# filepath: /c:/Users/lincy/Desktop/mp/app.py
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, send_from_directory,session
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
    from model import Student, Admin, MealPlan, Notice, Room, Attendance,Stu,FeeDetails,Leave

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
@app.route('/student_login', methods=['POST'])
def student_login():
    try:
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Check credentials in Stu table
        stu_query = text("SELECT username FROM stu WHERE username = :username AND password = :password")
        result = db.session.execute(stu_query, {"username": username, "password": password})
        student_auth = result.fetchone()

        if student_auth:
            # If authenticated, get student details from Student table
            student = Student.query.filter_by(email=username).first()
            if student:
                session['student_username'] = username
                session['student_id'] = student.id
                session['student_name'] = student.name
                return redirect(url_for('student_dashboard', student_name=student.name))

        flash('Invalid username or password', 'error')
        return redirect(url_for('home'))

    except Exception as e:
        print(f"Login error: {str(e)}")
        flash('Login failed. Please try again.', 'error')
        return redirect(url_for('home'))
@app.route('/adfee', methods=['GET'])
def adfee():
    try:
        admin_username = request.args.get('admin_username', 'Admin')
        return render_template('adfee.html', admin_username=admin_username)
    except Exception as e:
        flash(f'Error loading Fee Details page: {str(e)}', 'danger')
        return redirect(url_for('dashboard', admin_username=admin_username))

@app.route('/student_dashboard')
def student_dashboard():
    try:
        # Check if the student is logged in
        if 'student_username' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('home'))

        student_username = session['student_username']

        # Fetch the latest notices from the database
        notices = Notice.query.order_by(Notice.date.desc()).limit(5).all()

        # Render the student dashboard with notices
        return render_template('sdash.html', student_name=student_username, notices=notices)

    except Exception as e:
        flash(f'Dashboard error: {str(e)}', 'error')
        return redirect(url_for('home'))
    
@app.route('/dashboard')
def dashboard():
    try:
        admin_username = request.args.get('admin_username', 'Admin')

        # Fetch notices or other data for the dashboard
        notices = Notice.query.order_by(Notice.date.desc()).limit(5).all()

        return render_template('addash.html', admin_username=admin_username, notices=notices)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
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
@app.route('/add_fees', methods=['GET', 'POST'])
def add_fees():
    try:
        admin_username = request.args.get('admin_username', 'Admin')

        if request.method == 'POST':
            # Process the form data
            selected_month = request.form['month']
            selected_year = request.form['year']
            student_ids = request.form.getlist('student_id')
            amounts = request.form.getlist('amount')

            # Add fees for each student
            for student_id, amount in zip(student_ids, amounts):
                # Fetch the student's email from the Student table
                student = Student.query.get(student_id)
                if not student:
                    flash(f"Student with ID {student_id} not found.", "danger")
                    continue

                # Check if the student's email exists in the stu table
                stu_entry = Stu.query.filter_by(username=student.email).first()
                if not stu_entry:
                    flash(f"Email {student.email} not found in the stu table.", "danger")
                    continue

                # Insert fee details into the FeeDetails table
                fee = FeeDetails(
                    student_id=student_id,
                    email=student.email,
                    month=selected_month,
                    year=int(selected_year),
                    amount=int(amount),
                    status='Not Paid'  # Default status
                )
                db.session.add(fee)

            db.session.commit()
            flash('Fees added successfully!', 'success')

            # Redirect to the same page or a confirmation page
            return redirect(url_for('add_fees', admin_username=admin_username))

        # Handle GET request to fetch students based on the selected year
        selected_year = request.args.get('year', '1st Year')
        current_year = datetime.now().year
        students = []

        if 'MCA' in selected_year:
            if selected_year == 'MCA 1st Year':
                students = Student.query.filter(
                    Student.course == 'MCA',
                    current_year - Student.academic_year_start == 0
                ).order_by(Student.name).all()
            elif selected_year == 'MCA 2nd Year':
                students = Student.query.filter(
                    Student.course == 'MCA',
                    current_year - Student.academic_year_start == 1
                ).order_by(Student.name).all()
        else:
            year_map = {
                '1st Year': current_year - 0,
                '2nd Year': current_year - 1,
                '3rd Year': current_year - 2,
                '4th Year': current_year - 3
            }
            join_year = year_map.get(selected_year)
            students = Student.query.filter(
                Student.course != 'MCA',
                Student.academic_year_start == join_year
            ).order_by(Student.name).all()

        return render_template(
            'adminaddfee.html',
            admin_username=admin_username,
            students=students,
            selected_year=selected_year
        )

    except Exception as e:
        flash(f'Error adding fees: {str(e)}', 'danger')
        db.session.rollback()
        return redirect(url_for('dashboard', admin_username=admin_username))

@app.route('/student_fee_details')
def student_fee_details():
    try:
        # Check if the student is logged in
        if 'student_username' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('home'))

        # Render the sfee.html template
        return render_template('sfee.html')

    except Exception as e:
        print(f"Error loading fee details page: {str(e)}")
        flash('Error loading fee details page', 'error')
        return redirect(url_for('student_dashboard'))

@app.route('/sview_fee', methods=['GET', 'POST'])
def sview_fee():
    try:
        if request.method == 'POST':
            # Get form data
            student_email = request.form['studentEmail']
            selected_month = request.form['month']
            selected_year = request.form['year']

            # Query the FeeDetails table for the entered email, month, and year
            fees = FeeDetails.query.join(Student, FeeDetails.student_id == Student.id).filter(
                Student.email == student_email,
                FeeDetails.month == selected_month,
                FeeDetails.year == int(selected_year)
            ).all()

            return render_template('sviewfee.html', fees=fees, student_email=student_email, month=selected_month, year=selected_year)

        # Render the form if it's a GET request
        return render_template('sviewfee.html', fees=None)

    except Exception as e:
        print(f"Error fetching fee details: {str(e)}")
        flash('Error fetching fee details. Please try again.', 'error')
        return redirect(url_for('sfee'))
@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    try:
        # Get form data
        student_email = request.form['studentEmail']
        selected_month = request.form['month']
        selected_year = request.form['year']
        transaction_id = request.form['transactionId']

        # Query the FeeDetails table for the entered email, month, and year
        fee = FeeDetails.query.join(Student, FeeDetails.student_id == Student.id).filter(
            Student.email == student_email,
            FeeDetails.month == selected_month,
            FeeDetails.year == int(selected_year)
        ).first()

        if not fee:
            flash('No fee record found for the provided details.', 'error')
            return redirect(url_for('sfeepayment'))

        # Update the transaction ID and status
        fee.transaction_id = transaction_id
        fee.status = 'Waiting'
        db.session.commit()

        flash('Payment submitted successfully! Status updated to "Waiting".', 'success')
        return redirect(url_for('sfee'))

    except Exception as e:
        print(f"Error submitting payment: {str(e)}")
        flash('Error submitting payment. Please try again.', 'error')
        return redirect(url_for('sfeepayment'))

@app.route('/sfeepayment', methods=['GET'])
def sfeepayment():
    try:
        return render_template('sfeepayment.html')
    except Exception as e:
        print(f"Error loading payment page: {str(e)}")
        flash('Error loading payment page. Please try again.', 'error')
        return redirect(url_for('sfee'))  
    
@app.route('/adview_fee', methods=['GET'])
def adview_fee():
    try:
        admin_username = request.args.get('admin_username', 'Admin')
        return render_template('adviewfee.html', admin_username=admin_username)
    except Exception as e:
        print(f"Error loading fee details page: {str(e)}")
        flash('Error loading fee details page', 'error')
        return redirect(url_for('dashboard', admin_username=admin_username))

@app.route('/get_fee_details', methods=['GET'])
def get_fee_details():
    try:
        student_year = request.args.get('studentYear')
        month = request.args.get('month')
        year = request.args.get('year')
        current_year = datetime.now().year

        # Determine the academic year start based on student year
        if 'MCA' in student_year:
            if student_year == 'MCA 1st Year':
                students = Student.query.filter(
                    Student.course == 'MCA',
                    current_year - Student.academic_year_start == 0
                )
            else:  # MCA 2nd Year
                students = Student.query.filter(
                    Student.course == 'MCA',
                    current_year - Student.academic_year_start == 1
                )
        else:
            year_map = {
                '1st Year': current_year - 0,
                '2nd Year': current_year - 1,
                '3rd Year': current_year - 2,
                '4th Year': current_year - 3
            }
            join_year = year_map.get(student_year)
            students = Student.query.filter(
                Student.course != 'MCA',
                Student.academic_year_start == join_year
            )

        # Join with FeeDetails to get fee information
        fee_details = FeeDetails.query.join(
            Student, FeeDetails.student_id == Student.id
        ).filter(
            FeeDetails.month == month,
            FeeDetails.year == int(year),
            Student.id.in_([s.id for s in students])
        ).all()

        # Format the data for response
        fees_data = [{
            'reg_no': fee.student.registration_number,  # Changed from fee.Student to fee.student
            'student_name': fee.student.name,           # Changed from fee.Student to fee.student
            'transaction_id': fee.transaction_id or 'Not Paid',
            'amount': fee.amount,
            'status': fee.status,
            'fee_id': fee.fee_id
        } for fee in fee_details]

        return jsonify({'success': True, 'fees': fees_data})

    except Exception as e:
        print(f"Error fetching fee details: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})
@app.route('/update_fee_status', methods=['POST'])
def update_fee_status():
    try:
        fee_id = request.json.get('fee_id')
        action = request.json.get('action')

        fee = FeeDetails.query.get(fee_id)
        if not fee:
            return jsonify({'success': False, 'error': 'Fee record not found'})

        if action == 'approve':
            fee.status = 'Approved'
        elif action == 'reject':
            fee.status = 'Rejected'

        db.session.commit()
        return jsonify({'success': True, 'message': f'Payment {action}d successfully'})

    except Exception as e:
        print(f"Error updating fee status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 

@app.route('/stuleaveform')
def stuleaveform():
    try:
        return render_template('stuleaveform.html')
    except Exception as e:
        print(f"Error loading leave form: {str(e)}")
        flash('Error loading leave form', 'error')
        return redirect(url_for('home'))

@app.route('/submit_leave', methods=['POST'])
def submit_leave():
    try:
        # Create new leave request
        new_leave = Leave(
            student_id=request.form['student_id'],  # Add this line
            name=request.form['name'],
            email=request.form['email'],
            class_name=request.form['class'],
            leave_from=datetime.strptime(request.form['from'], '%Y-%m-%d').date(),
            leave_until=datetime.strptime(request.form['to'], '%Y-%m-%d').date(),
            place_of_travel=request.form['place'],
            mode_of_travel=request.form['mode'],
            purpose=request.form['purpose']
        )

        db.session.add(new_leave)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Leave request submitted successfully!'})

    except Exception as e:
        print(f"Error submitting leave request: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin_leave_form', methods=['GET', 'POST'])
def admin_leave_form():
    try:
        admin_username = request.args.get('admin_username', 'Admin')
        selected_date = request.args.get('date')
        
        if selected_date:
            # Convert string date to datetime
            search_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            
            # Query leaves that include the selected date
            leaves = Leave.query.filter(
                Leave.leave_from <= search_date,
                Leave.leave_until >= search_date
            ).all()
        else:
            leaves = []

        return render_template('leaveform.html', 
                            admin_username=admin_username,
                            leaves=leaves,
                            selected_date=selected_date)

    except Exception as e:
        print(f"Error loading leave form: {str(e)}")
        flash('Error loading leave form', 'error')
        return redirect(url_for('dashboard', admin_username=admin_username))
    
if __name__ == "__main__":
    app.run(debug=True)