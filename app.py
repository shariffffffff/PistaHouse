from flask import Flask,render_template,request
app=Flask(__name__)
import sqlite3

# Function to connect to the SQLite database
def connect_db():
    conn=sqlite3.connect('database.db')
    return conn

# Route for the login page
@app.route('/',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()
        
        # Query the database to check if the username and password match
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        print(user)
        conn.close()

        if user:
            # Successful login
            return render_template('home.html')
        else:
            # Failed login
            return 'Invalid username or password'
    else:
        return render_template('login.html')

# Route for successful login
@app.route('/success')
def success():
    return 'Login successful!'
   



# Function to connect to the SQLite database

# Route for the register page
@app.route('/create')
def create():
    return render_template('create.html')

# Route to handle register form submission
@app.route('/create', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if the username already exists in the database
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        # Username already exists
        conn.close()
        return 'Username already exists!'
    else:
        # Insert new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username , password ))
        conn.commit()
        conn.close()
        return render_template('login.html')
# Route for successful registration
@app.route('/regsuccess')
def regsuccess():
    return 'Registration successful!'  

@app.route('/home')
def home():
    return render_template('home.html') 

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/item')
def item():
    return render_template('item.html')

@app.route('/selecteditems')
def selecteditems():
    return render_template('selecteditems.html')

@app.route('/tick')
def tick():
    return render_template('tick.html')

def create_table():
    conn=connect_db()
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS users(username TEXT,password varchar (20))")
    conn.commit()
    conn.close()

if __name__=='__main__':
    create_table()
    app.run(debug=True)