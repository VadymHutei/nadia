from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/gallery/')
def gallery():
    return 'gallery'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)