from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Генератор задач
def generate_math_task():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    fruits = ['apple', 'banana', 'orange']
    fruit = random.choice(fruits)
    return {
        'a': a,
        'b': b,
        'fruit': fruit,
        'answer': a + b,
        'question': f"{a} + {b} = ?"
    }

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
                         time_left=round(session['end_time'] - datetime.now().timestamp()))

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = int(request.form['answer'])
    current_task = session['tasks'][session['current_task']]
    
    if user_answer == current_task['answer']:
        session['score'] += 1
    
    session['current_task'] += 1
    
    if session['current_task'] >= len(session['tasks']) or datetime.now().timestamp() > session['end_time']:
        return redirect(url_for('result'))
    
    return redirect(url_for('math3_5'))

@app.route('/result')
def result():
    score = session.get('score', 0)
    session.clear()
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)