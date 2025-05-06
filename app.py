from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

def generate_math_task():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    operation = random.choice(['+', '-'])
    fruits = ['apple', 'banana', 'orange']
    fruit = random.choice(fruits)
    
    if operation == '+':
        answer = a + b
    else:
        # Чтобы избежать отрицательных чисел: делаем a >= b
        if a < b:
            a, b = b, a
        answer = a - b
    
    return {'a': a, 'b': b, 'fruit': fruit, 'operation': operation, 'answer': answer}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/age3-5')
def age3_5():
    return render_template('age3_5.html')

@app.route('/math3-5')
def math3_5():
    if 'tasks' not in session:
        session['tasks'] = [generate_math_task() for _ in range(15)]
        session['current_task'] = 0
        session['score'] = 0
        session['end_time'] = (datetime.now() + timedelta(minutes=5)).timestamp()
    return render_template('math_game.html',
                         task=session['tasks'][session['current_task']],
                         current_score=session['score'],
                         end_time=int(session['end_time']))

@app.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        user_answer = int(request.form['answer'])
        if user_answer == session['tasks'][session['current_task']]['answer']:
            session['score'] += 1
        session['current_task'] += 1
        return {'status': 'finished' if session['current_task'] >= 15 else 'next', 'score': session['score']}
    except:
        return {'status': 'error'}, 400

@app.route('/result')
def result():
    score = request.args.get('score', 0)
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)