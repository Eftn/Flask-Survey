from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES = "responses" 

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def first_page():
    """start survey"""
    return render_template("start.html", survey=survey)

@app.route("/click", methods=["POST"])
def start():
    """First lets clear the responses from previous session"""
    #This will clear out previous responses from different
    # users, if you didn't use this, it would keep adding
    #on data to the same list.

    session[RESPONSES] = []
    return redirect("/questions/0")

@app.route ("/answer", methods=["POST"])
def handle_question():
    """Save the user's response and redirect to the next page"""
    #request.form is a dictionary on the request
    #that keeps track of the input name answer
    
    choice = request.form["answer"]
    
    # grabs the list of the responses from the session
    responses = session[RESPONSES]

    #appends the choice that the user gave from the form
    responses.append(choice)

    # reset the list on session to the new value of responses
    #this is a list with the new choice added on
    session[RESPONSES] = responses
    
    raise(responses)
   # if length of responses is two send them to the questions/2
    return redirect(f"/questions/{len(responses)}")

    

@app.route("/questions/<int:q>")
def show_question(q):
    
    responses = session.get(RESPONSES)
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != q):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {q}.")
        return redirect(f"/questions/{len(responses)}")
# this is what is adding the questions to different pages
    question = survey.questions[q]
    return render_template("question.html", question_num =q, question=question)

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")