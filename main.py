from flask import Flask, render_template, request, redirect, url_for, make_response, session
import random, copy, string
from quizutils import load_questions
app = Flask(__name__)
app.secret_key = "meinhertzinflammen"

questions = dict() # {"hello":[["hEllo","hellO"],["hellO"]]}

def get_learned():
    learned = list(filter(lambda x:session['streak'][x]>=4,list(questions.keys())))
    almost = list(reversed(sorted(map(lambda x:(session['streak'][x],x),filter(lambda x:session['streak'][x]<4,list(questions.keys()))))))
    return learned, len(learned)/len(questions), almost

@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect(url_for('make_session'))
    #return render_template('index.html')

@app.route("/quiz", methods = ["GET", "POST"])
def quiz():
    cur = session['cur']
    return render_template("quiz.html",q=cur,a=questions[cur][0],lw=get_learned())

@app.route("/view_answer", methods = ["GET", "POST"])
def view_answer():
    cur = session['cur']
    return render_template("quizanswer.html",question=cur,answers=questions[cur][0],correct=questions[cur][1],answered=session['answer'],lw=get_learned())

@app.route("/next_question", methods = ["GET", "POST"])
def next_question():
    session['cur'] = get_word()
    return redirect(url_for('quiz'))

def get_word():
    w = random.choice(list(questions.keys()))
    while session['streak'][w] >= 4:
        w = random.choice(list(questions.keys()))
    return w

@app.route('/make_session', methods = ["GET", "POST"])
def make_session():
    #user = request.form['nm']
    user = "default"
    session['username'] = user
    session['streak'] = {w:0 for w in list(questions.keys())}
    session['cur'] = get_word()
    session['answer'] = ''
    session['correct'] = 0

    return redirect(url_for('quiz'))


@app.route("/submit", methods = ["GET", "POST"])
def submit_answer():
    answered = request.form["answer"]
    session['answer'] = answered
    if answered in questions[session['cur']][1]:
        temp = session['streak']
        temp[session['cur']] += 1
        session['streak'] = temp
    return redirect(url_for('view_answer'))

@app.route("/results", methods = ["GET", "POST"])
def get_results():
    q = list(zip(map(lambda x: questions[x], session['questions'][:len(session['answer'])]),session['answers']))
    print(q)
    return render_template("results.html",q = q, lw=get_learned())
if __name__ == "__main__":
    print("bibib")
    questions = load_questions()
    app.run(host="0.0.0.0", port=5000, debug=True)