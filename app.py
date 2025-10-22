from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.utils import secure_filename
import os
import random
import string
import requests
import time
from Car import RentalCars, Person

app = Flask(__name__, template_folder='.')
app.secret_key = 'dev-secret-change-me'

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions for profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize car rental system
rental = RentalCars([
    "ORACLE REDBULL RB20",
    "AMG GLS",
    "FERRARI 296 GTB",
    "APX GP",
    "MCLAREN 720S",
    "LAMBORGHINI HURACÁN",
    "BUGATTI CHIRON",
    "ASTON MARTIN VANTAGE",
    "PORSCHE 911",
    "BMW M3",
    "AUDI R8"
])
person = Person()

# Mapping of car names to image files in static/cars/
# Files present: mclaren-720s.svg, ferrari-296-gtb.svg, lamborghini-huracan.svg, bugatti-chiron.svg, apx gp.jpg, image.png
car_images = {
    # Prefer user-provided local images by exact filename
    "ORACLE REDBULL RB20": "ORACLE REDBULL RB20.jpg",
    "AMG GLS": "AMG GLS.jpeg",
    "FERRARI 296 GTB": "FERRARI 296 GTB.jpg",
    "APX GP": "apx gp.jpg",
    "MCLAREN 720S": "MCLAREN 720S.jpeg",
    "LAMBORGHINI HURACÁN": "LAMBORGHINI HURACÁN.jpeg",
    "BUGATTI CHIRON": "BUGATTI CHIRON.jpeg",
    "ASTON MARTIN VANTAGE": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/2019_Aston_Martin_Vantage_V8_Automatic_4.0_Front.jpg/640px-2019_Aston_Martin_Vantage_V8_Automatic_4.0_Front.jpg",
    "PORSCHE 911": "PORSCHE 911.jpeg",
    "BMW M3": "BMW M3.jpeg",
    "AUDI R8": "AUDI R8.jpeg"
    # Unmapped names will fall back to image.png automatically
}

@app.route('/')
def home():
    # Create a new database manager for this request to avoid thread issues
    from db_manager import DatabaseManager
    db_manager = DatabaseManager()
    try:
        # Get available cars from database
        available_cars = [car.name for car in db_manager.get_available_cars()]
        # Get current user if logged in
        user = None
        if 'user_id' in session:
            user = db_manager.get_user_by_id(session['user_id'])
        return render_template('home.html', cars=available_cars, car_images=car_images, user=user)
    finally:
        db_manager.close()

@app.route('/list')
def list_cars():
    # Create a new database manager for this request to avoid thread issues
    from db_manager import DatabaseManager
    db_manager = DatabaseManager()
    try:
        # Get available cars from database
        available_cars = [car.name for car in db_manager.get_available_cars()]
        # Get current user if logged in
        user = None
        if 'user_id' in session:
            user = db_manager.get_user_by_id(session['user_id'])
        return render_template('list.html', cars=available_cars, car_images=car_images, user=user)
    finally:
        db_manager.close()

@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    if request.method == 'POST':
        name = request.form['name']
        car_name = request.form['car']
        
        # Get user ID if user is logged in
        user_id = session.get('user_id') if 'user_id' in session else None
        
        success = rental.borrowCars(name, car_name, user_id)
        if success:
            flash(f"{car_name} borrowed by {name}", 'success')
        else:
            flash(f"{car_name} is not available", 'error')
        return redirect('/track')
    # Create a new database manager for this request to avoid thread issues
    from db_manager import DatabaseManager
    db_manager = DatabaseManager()
    try:
        # Get available cars from database
        available_cars = [car.name for car in db_manager.get_available_cars()]
        # Get current user if logged in
        user = None
        if 'user_id' in session:
            user = db_manager.get_user_by_id(session['user_id'])
        return render_template('borrow.html', cars=available_cars, user=user)
    finally:
        db_manager.close()

@app.route('/return', methods=['GET', 'POST'])
def return_car():
    if request.method == 'POST':
        name = request.form['name']
        car_name = request.form['car']
        success = rental.returnCars(name, car_name)
        if success:
            flash(f"{car_name} returned by {name}", 'info')
        else:
            flash(f"Error returning {car_name}", 'error')
        return redirect('/list')
    
    # Get borrowed cars for the return form
    # If user is logged in, only show their borrowed cars
    user_id = session['user_id'] if 'user_id' in session else None
    borrowed_records = rental.get_borrowed_cars(user_id)
    borrowed_cars = []
    for record in borrowed_records:
        borrower = record.borrower
        car = record.car
        borrowed_cars.append({
            'borrower_name': borrower.name,
            'car_name': car.name
        })
    
    # Get current user if logged in
    user = None
    if 'user_id' in session:
        from db_manager import DatabaseManager
        db_manager = DatabaseManager()
        try:
            user = db_manager.get_user_by_id(session['user_id'])
        finally:
            db_manager.close()
    
    return render_template('return.html', borrowed_cars=borrowed_cars, car_images=car_images, user=user)

@app.route('/track')
def track_cars():
    # Get current user if logged in
    user = None
    user_id = None
    if 'user_id' in session:
        from db_manager import DatabaseManager
        db_manager = DatabaseManager()
        try:
            user = db_manager.get_user_by_id(session['user_id'])
            user_id = session['user_id']  # Use the session ID directly
        finally:
            db_manager.close()
    
    # Get borrowed, returned, and donated cars
    # If user is logged in, only show their data
    borrowed_records = rental.get_borrowed_cars(user_id)
    returned_records = rental.get_returned_cars(user_id)
    donated_records = rental.get_donated_cars()
    
    return render_template('track.html', 
                          borrowed_records=borrowed_records, 
                          returned_records=returned_records, 
                          donated_records=donated_records,
                          car_images=car_images,
                          user=user)

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(f"Login route accessed with method: {request.method}")
    if request.method == 'POST':
        try:
            print("Processing POST request")
            email = request.form['email']
            print(f"Email from form: {email}")
            
            # Find user by email
            from db_manager import DatabaseManager
            db_manager = DatabaseManager()
            try:
                print("Attempting to get user by email")
                user = db_manager.get_user_by_email(email)
                print(f"User lookup result: {user}")
                if user:
                    # Store user ID in session
                    session['user_id'] = user.id
                    print(f"User ID {user.id} stored in session")
                    flash(f"Welcome back, {user.name}!", 'success')
                    return redirect('/')
                else:
                    flash('No account found with that email. Please register.', 'error')
                    return redirect('/register')
            except Exception as e:
                print(f"Database error: {str(e)}")
                flash(f"Error logging in: {str(e)}", 'error')
                return redirect('/login')
            finally:
                db_manager.close()
        except Exception as e:
            # Log the exception for debugging
            print(f"Exception in login POST: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f"Error processing login: {str(e)}", 'error')
            return redirect('/login')
    
    # Get current user if logged in
    user = None
    if 'user_id' in session:
        from db_manager import DatabaseManager
        db_manager = DatabaseManager()
        try:
            user = db_manager.get_user_by_id(session['user_id'])
        finally:
            db_manager.close()
    
    return render_template('login.html', user=user)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect('/')
        
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Check if email already exists
        from db_manager import DatabaseManager
        db_manager = DatabaseManager()
        try:
            existing_user = db_manager.get_user_by_email(email)
            if existing_user:
                flash('Email already registered. Please log in.', 'error')
                return redirect('/login')
            
            # Handle profile image upload
            profile_image_path = None
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file and file.filename and file.filename != '' and allowed_file(file.filename):
                    # Create a secure filename
                    filename = secure_filename(file.filename)
                    # Add user identifier to filename to avoid conflicts
                    name_part, ext = os.path.splitext(filename)
                    unique_filename = f"{name_part}_{int(time.time())}{ext}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(file_path)
                    # Store relative path for web access
                    profile_image_path = f"uploads/{unique_filename}"
            
            # Create new user
            user = db_manager.create_user(name, email, profile_image_path)
            # Store user ID in session
            session['user_id'] = user.id
            flash(f"Welcome {name}! Your account has been created successfully.", 'success')
            return redirect('/')
        except Exception as e:
            flash(f"Error creating account: {str(e)}", 'error')
            return redirect('/register')
        finally:
            db_manager.close()
    
    # Get current user if logged in
    user = None
    if 'user_id' in session:
        from db_manager import DatabaseManager
        db_manager = DatabaseManager()
        try:
            user = db_manager.get_user_by_id(session['user_id'])
        finally:
            db_manager.close()
    
    return render_template('register.html', user=user)

# User profile route
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'error')
        return redirect('/login')
    
    from db_manager import DatabaseManager
    db_manager = DatabaseManager()
    try:
        user = db_manager.get_user_by_id(session['user_id'])
        if not user:
            session.pop('user_id', None)
            flash('User not found. Please log in again.', 'error')
            return redirect('/login')
        
        return render_template('profile.html', user=user)
    finally:
        db_manager.close()

# User logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)