from flask import Flask, render_template, request, redirect, url_for, make_response, session
import random, copy, string
from quizutils import load_questions
app = Flask(__name__)
app.secret_key = "meinhertzinflammen"

questions = dict() # {"hello":[["hEllo","hellO"],["hellO"]]}

@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect(url_for('make_session'))
    #return render_template('index.html')

@app.route("/quiz", methods = ["GET", "POST"])
def quiz():
    cur = session['questions'][session['cur']]
    return render_template("quiz.html",q=cur,a=questions[cur][0])

@app.route("/view_answer", methods = ["GET", "POST"])
def view_answer():
    cur = session['questions'][session['cur']]
    print(session['answers'][session['cur']])
    return render_template("quizanswer.html",question=cur,answers=questions[cur][0],correct=questions[cur][1],answered=session['answers'][session['cur']])

@app.route("/next_question", methods = ["GET", "POST"])
def next_question():
    session['cur'] += 1
    if session['cur']  == len(session['questions']):
        return redirect(url_for('get_results'))
    return redirect(url_for('quiz'))

@app.route('/make_session', methods = ["GET", "POST"])
def make_session():
    #user = request.form['nm']
    n_questions = len(questions)
    user = "default"
    session['username'] = user
    session['questions'] = random.sample(list(questions.keys()),n_questions)
    session['cur'] = 0
    session['answers'] = []
    session['correct'] = 0

    return redirect(url_for('quiz'))


@app.route("/submit", methods = ["GET", "POST"])
def submit_answer():
    answered = request.form["answer"]
    temp = session['answers']
    temp.append(answered)
    session['answers'] = temp
    if answered in questions[session['questions'][session['cur']]][1]:
        session['correct'] += 1
    return redirect(url_for('view_answer'))

@app.route("/results", methods = ["GET", "POST"])
def get_results():
    q = list(zip(map(lambda x: questions[x], session['questions'][:len(session['answers'])]),session['answers']))
    print(q)
    return render_template("results.html",q = q)
if __name__ == "__main__":
    print("bibib")
    questions = load_questions()
    app.run(host="0.0.0.0", port=5000, debug=True)