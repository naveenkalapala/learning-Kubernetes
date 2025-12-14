from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello, Guys! This is Flask App! for Crashloop/LivenessProbe testing by Naveen Kalapala'

@app.route('/health')
def health():
    return 'Im Healthy! Don`t Worry!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)