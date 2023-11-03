

from flask import request
from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import logging

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

logging.basicConfig(filename='404_errors.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
@limiter.limit("1 per second")
def check():
    url = request.form['url']
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"Success: URL {url} is live.")
            return f"Success: {url} is live."
        else:
            logging.error(f"Error {response.status_code}: URL {url} returned an error.")
            return f"Error {response.status_code}: {url} returned an error."
    except requests.RequestException as e:
        logging.error(f"Error: {url} | {e}")
        return f"Error: {url} | {e}"

if __name__ == '__main__':
    app.run(debug=True)
