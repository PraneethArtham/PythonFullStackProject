# app.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to my Social Media Platform!'

@app.route('/about')
def about():
    return 'About the Social Media Platform'

if __name__ == '__main__':
    app.run(debug=True)
