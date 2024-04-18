from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Replace with your secret key

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harsh",
    database="temple_tours"
)
cursor = db.cursor()

# Create table if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    phone VARCHAR(20) NOT NULL
)
"""
cursor.execute(create_table_query)
db.commit()

@app.route('/')
def home():
    return render_template('BON_VOYAGE.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        phone = request.form['phone']

        # Validate the Date of Birth
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            now = datetime.now()

            # Calculate the date 100 years ago
            min_dob = now - timedelta(days=365*100)
    
            if dob_date > now or dob_date < min_dob:
                error = 'Invalid Date of Birth'
                return render_template('register.html', error=error)

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Capture registration time
            registration_time = datetime.now().time().strftime('%H:%M:%S')

            # Insert user data into the database
            insert_query = "INSERT INTO users (firstName, lastName, email, password, dob, phone) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (firstName, lastName, email, hashed_password, dob, phone))

            db.commit()

            return redirect('/')
        except ValueError:
            error = 'Invalid Date Format'
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Query the database to check if the username and password match
        select_query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(select_query, (email, hashed_password))
        user = cursor.fetchone()

        if user:
            # Store user data in session
            session['user'] = user
            flash('Login successful!', 'success')  # Flash success message
            return redirect('/book_ticket')  # Redirect to booking page upon successful login
        else:
            flash('Invalid email or password. Please try again.', 'error')  # Flash error message
            return redirect('/login')  # Redirect back to login page if login fails
    else:
        return render_template('login.html')

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if 'user' in session:
        if request.method == 'POST':
            # Handle POST request data here if needed
            # return "Booking submitted successfully!"  # Placeholder response for POST request
            return render_template('book_ticket.html')
        else:
            return render_template('book_ticket.html')
    else:
        flash('Please login to access booking page.', 'error')
        return redirect('/login')

@app.route('/golden_temple_details')
def golden_temple_details():
    return render_template('golden_temple_details.html')

@app.route('/tirupati_balaji_temple_details')
def tirupati_balaji_temple_details():
    return render_template('tirupati_balaji_temple_details.html')

@app.route('/meenakshi_temple_details')
def meenakshi_temple_details():
    return render_template('meenakshi_temple_details.html')

@app.route('/varanasi_temples_details')
def varanasi_temples_details():
    return render_template('varanasi_temples_details.html')

@app.route('/contact')
def contact():
    return render_template('contact_floating_bar.html')

@app.route('/konark_sun_temple_details')
def konark_sun_temple_details():
    return render_template('konark_sun_temple_details.html') 

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'tour': request.form['tour'],
        'date': request.form['date'],
        'method': request.form['method'],
        'name': request.form['name'],
        'email': request.form['email'],
        'cardNumber': request.form['cardNumber'],
        'expiryDate': request.form['expiryDate'],
        'cvv': request.form['cvv'],
        'cardType': request.form['cardType'],
        'upiId': request.form['upiId']
    }
    print("Form Data:", data)  # Print form data for debugging
    conn = connect_to_database()
    if conn:
        insert_booking(conn, data)
        conn.close()
        flash('Booking submitted successfully!', 'success')
        return redirect('/')
    else:
        flash('Error connecting to the database.', 'error')
        return redirect('/')

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saksham9100",
            database="temple_tours"
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return None

def insert_booking(conn, data):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO bookings (tour, date, method, name, email, cardNumber, expiryDate, cvv, cardType, upiId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, tuple(data.values()))
        print("Before committing transaction")
        conn.commit()
        print("After committing transaction")
        print("Booking inserted successfully")
    except mysql.connector.Error as e:
        print("Error inserting data:", e)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return redirect('/book_ticket')  # Redirect to booking page if user is logged in
    else:
        return redirect('/login')  # Redirect to login page if user is not logged in

if __name__ == '__main__':
    app.run(debug=True)
