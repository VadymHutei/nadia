from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/galleries/')
def galleries():
    return render_template('galleries.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)