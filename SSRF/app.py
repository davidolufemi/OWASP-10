from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Vulnerable endpoint that fetches a URL provided by the user
@app.route('/fetch', methods=['GET', 'POST'])
def fetch_url():
    content = ""
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # Make a request to the user-provided URL (vulnerable to SSRF)
            response = requests.get(url)
            content = response.text
        except Exception as e:
            content = f"Error: {str(e)}"
    return render_template_string('''
        <h1>SSRF Demo</h1>
        <form method="POST">
            URL: <input type="text" name="url" placeholder="Enter URL" required>
            <input type="submit" value="Fetch">
        </form>
        <h2>Response:</h2>
        <pre>{{ content }}</pre>
    ''', content=content)

@app.route('/')
def home():
    return render_template_string('''
        <h1>SSRF Demo</h1>
        <p>Visit <a href="/fetch">/fetch</a> to test SSRF.</p>
    ''')

if __name__ == '__main__':
    app.run(debug=True)