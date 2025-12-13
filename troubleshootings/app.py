from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello, Guys! This is Flask App! for crashloop testing by Naveen Kalapala'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=8000)