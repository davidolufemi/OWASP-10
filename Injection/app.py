from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize the database (same as before)
def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        password TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user', 'user123')")
    conn.commit()
    conn.close()

# Vulnerable login function (same as before)
def login(username, password):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
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