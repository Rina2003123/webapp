from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/age3-5')
def age3_5():
    return render_template('age3_5.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)