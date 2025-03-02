from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Sample data for users (in a real-world app, this would come from a database)
users = {
    1: {'username': 'admin', 'role': 'admin', 'name': 'Admin User'},
    2: {'username': 'john', 'role': 'user', 'name': 'John Doe'},
    3: {'username': 'jane', 'role': 'user', 'name': 'Jane Smith'}
}

# Dummy login function to set session (for simplicity)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In a real app, you would hash passwords.
        
        # Just for demonstration, hardcoding login
        for user_id, user in users.items():
            if user['username'] == username and password == 'password':  # simple password check
                session['user_id'] = user_id
                return redirect(url_for('profile', user_id=user_id))
        return 'Invalid credentials', 403
    return render_template('login.html')

# View for user profile with proper access control
@app.route('/profile/<int:user_id>')
def profile(user_id):
    # Get the logged-in user ID from the session
    logged_in_user_id = session.get('user_id')

    if not logged_in_user_id:
        return 'Unauthorized', 401  # User is not logged in

    # Check if the logged-in user is trying to access their own profile or if the user is an admin
    if logged_in_user_id != user_id and users[logged_in_user_id]['role'] != 'admin':
        return 'Access Denied', 403  # Only the user or admin can access this profile
    
    user = users[user_id]
    return f'Profile of {user["name"]} (Username: {user["username"]})'

if __name__ == '__main__':
    app.run(debug=True)
