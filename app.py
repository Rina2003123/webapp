from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

FRUITS = ['apple', 'banana', 'orange', 'grapes', 'watermelon']

def generate_math_task():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    operation = random.choice(['+', '-'])
    fruit = random.choice(FRUITS)

    if operation == '+':
        answer = a + b
    else:
        # Чтобы избежать отрицательных чисел: делаем a >= b
        if a < b:
            a, b = b, a
        answer = a - b

    return {'a': a, 'b': b, 'fruit': fruit, 'operation': operation, 'answer': answer}

def generate_pair_task():
    correct_fruit = random.choice(FRUITS)
    options = random.sample(FRUITS, 3)
    if correct_fruit not in options:
        options[random.randint(0, 2)] = correct_fruit
    random.shuffle(options)

    return {
        'correct_fruit': correct_fruit,
        'options': options
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
    return render_template(
        'math_game.html',
        task=session['tasks'][session['current_task']],
        current_score=session['score'],
        end_time=int(session['end_time'])
    )

@app.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        user_answer = int(request.form['answer'])
        if user_answer == session['tasks'][session['current_task']]['answer']:
            session['score'] += 1
        session['current_task'] += 1
        return {
            'status': 'finished' if session['current_task'] >= 15 else 'next',
            'score': session['score']
        }
    except Exception as e:
        print(f"Error: {e}")
        return {'status': 'error'}, 400

@app.route('/result')
def result():
    score = request.args.get('score', 0)
    return render_template('result.html', score=score)

@app.route('/pair-game')
def pair_game():
    if 'pair_tasks' not in session:
        session['pair_tasks'] = [generate_pair_task() for _ in range(15)]
        session['current_pair_task'] = 0
        session['pair_score'] = 0
        session['pair_end_time'] = (datetime.now() + timedelta(minutes=5)).timestamp()

    task = session['pair_tasks'][session['current_pair_task']]
    return render_template(
        'pair_game.html',
        task=task,
        current_score=session.get('pair_score', 0),
        end_time=int(session['pair_end_time'])
    )

@app.route('/check_pair', methods=['POST'])
def check_pair():
    try:
        selected_fruit = request.form['fruit']
        current_task = session['pair_tasks'][session['current_pair_task']]
        is_correct = selected_fruit == current_task['correct_fruit']

        if is_correct:
            session['pair_score'] += 1

        session['current_pair_task'] += 1

        if (
            session['current_pair_task'] >= len(session['pair_tasks']) or
            datetime.now().timestamp() > session['pair_end_time']
        ):
            return {'status': 'finished', 'score': session['pair_score']}

        return {
            'status': 'next',
            'score': session['pair_score'],
            'is_correct': is_correct
        }
    except Exception as e:
        print(f"Error: {e}")
        return {'status': 'error'}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
