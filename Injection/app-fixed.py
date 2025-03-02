from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        password TEXT)''')
    # Insert sample data if it doesn't already exist
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user', 'user123')")
    conn.commit()
    conn.close()

# Secure login function using parameterized queries
def login(username, password):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # Use parameterized queries to prevent SQL injection
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login(username, password)
        if user:
            message = f"Login successful! Welcome, {user[1]}."
        else:
            message = "Login failed. Invalid credentials."
    return render_template('index.html', message=message)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)