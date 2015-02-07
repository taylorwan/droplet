from flask import Flask
import oauth2
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/wowmom')
def wow_mom():
    return 'Wow mom, world!'


if __name__ == '__main__':
    app.run()
