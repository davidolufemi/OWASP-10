from flask import Flask, request, render_template_string
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# List of allowed domains
ALLOWED_DOMAINS = ['example.com', 'trusted-site.com']

def is_url_allowed(url):
    """Check if the URL is allowed."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain in ALLOWED_DOMAINS

@app.route('/fetch', methods=['GET', 'POST'])
def fetch_url():
    content = ""
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            content = "Error: URL is required."
        elif not is_url_allowed(url):
            content = "Error: URL not allowed."
        else:
            try:
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