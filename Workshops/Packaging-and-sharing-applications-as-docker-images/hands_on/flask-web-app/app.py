# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Welcome to the Docker Workshop. I am Flask!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)