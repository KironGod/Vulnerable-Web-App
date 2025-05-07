from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key'  # Replace with a secure key for production
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to get a database connection
def get_db_connection():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'vulnerable.db')  # Dynamic path for the database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname'].strip()
        password = request.form['pwd'].strip()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # Insecure: Directly concatenating user input into the SQL query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        # safe query : cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            # Store user information in session
            session['username'] = user['username']
            session['ssn'] = user['ssn']
            session['credit_card_number'] = user['credit_card_number']
            session['hobbies'] = user['hobbies']
            return redirect(url_for('welcome'))
        else:
            return "Login failed. Incorrect username or password."
    return render_template('Login page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname'].strip()
        password = request.form['pwd'].strip()
        ssn = request.form.get('ssn', '').strip() or None
        credit_card_number = request.form.get('credit_card_number', '').strip() or None
        hobbies = request.form.get('hobbies', '').strip() or None
        
        # Validate input
        if not username or not password:
            return "Username and password are required."
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return "Username already exists. Please choose a different one."
        
        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO users (username, password, ssn, credit_card_number, hobbies) VALUES (?, ?, ?, ?, ?)", 
            (username, password, ssn, credit_card_number, hobbies)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    username = session.get('username')
    ssn = session.get('ssn', 'N/A')
    credit_card_number = session.get('credit_card_number', 'N/A')
    hobbies = session.get('hobbies', 'N/A')
    if username:
        return render_template('welcome.html', username=username, ssn=ssn, credit_card_number=credit_card_number, hobbies=hobbies)
    return redirect(url_for('index'))

@app.route('/delete_comments', methods=['POST'])
def delete_comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments")  # Deletes all comments
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('blog'))

@app.route('/blog', methods=['GET'])
def blog():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, comment FROM comments")
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('blog.html', comments=comments,images=images)


@app.route('/add_picture', methods=['POST'])
def add_picture():
    if request.form.get('file_name'):
        file_path = request.form['file_name']
        process_image(file_path)
        return redirect(url_for('blog'))
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            process_image(file_path)
            return redirect(url_for('blog'))
    else:
        return 'No file part'

# Here we directly use the file path, introducing a vulnerability
def process_image(file_path):
    try:
        # For demonstration, if the input includes a command separator, we'll use it directly
        if ';' in file_path:
            commands = file_path.split(';')
            for command in commands:
                command = command.strip()
                if command:
                    print(f"Executing command: {command}")  # Debugging statement
                    os.system(command)
        else:
            command = f"convert {file_path} output.png"
            print(f"Executing command: {command}")  # Debugging statement
            os.system(command)
    except Exception as e:
        print(f"Error executing command: {e}")


@app.route('/add_comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (comment) VALUES (?)", (comment,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('blog'))

# Initialize the comments table
def init_comments_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Initialize the database
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    init_comments_table()
    app.run(host='0.0.0.0',port=5000,debug=True)
