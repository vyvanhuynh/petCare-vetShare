""" Server for pet care discussion app. """

from random import randint

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from flask_msearch import Search
from model import connect_to_db
import crud, model
from jinja2 import StrictUndefined
from datetime import datetime
import os
import cloudinary.uploader

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dzezncjgc"

app = Flask(__name__)
app.secret_key = "pet"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def create_homepage():
    return render_template('homepage.html')


@app.route('/register')
def show_registration_form():
    return render_template('register.html')


@app.route('/register', methods = ["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    is_vet = False
    is_admin = False
    db_email = crud.get_user_by_email(email)

    # check if the email and password are valid and create a new user if they are
    if db_email:
        flash(f"{email} is already registered. Please try a different email")
    else:
        crud.create_user(email, password, is_vet, is_admin)        
        flash("Your account has been successfully created! You can now log in")        
    return redirect('/')


@app.route('/vet_register')
def show_vet_registration_form():
    return render_template('vet_register.html')


@app.route('/vet_register', methods = ["POST"])
def register_vet():
    email = request.form.get("email")
    password = request.form.get("password")
    db_user = crud.get_user_by_email(email)

    # check if the email and password are valid
    if db_user:
        flash(f"{email} is already registered. Please try a different email")
    else:
        is_vet = True
        is_admin = False

        # create a new user 
        user = crud.create_user(email, password, is_vet, is_admin) 

        last_name = request.form.get("last_name")
        license_type = request.form.get("license_type")
        license_number = request.form.get("license_number")
        is_vet_pending = True
        verification_status = request.form.get("verification_status")
       
        # create a vet from this new user
        crud.create_vet(last_name,license_type,license_number,verification_status,is_vet_pending,user)  

        flash(f"Thank you, {email} is successfully registered! Your vet status is pending. You will be able to answer questions once the admin verify your status!")     
    return redirect('/')


@app.route('/login', methods = ["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    db_login = crud.validate_login(email,password)
    if db_login:
        session['email'] = email
        flash(f"Welcome,{email}!")
        user = crud.get_user_by_email(email)
        if user.is_admin == True:
            return redirect('/admin')
        else: 
            return redirect('/forum')
    else:
        flash("Please try again, we can't verify your email and/or your password")
        return redirect('/')
    

@app.route('/admin')
def admin_activities():
    users = crud.list_all_users()
    vets = crud.list_all_vets_as_users()
    return render_template('admin_page.html', users = users, vets=vets)

@app.route('/admin/<email>')
def show_user_details(email):
    user = crud.get_user_by_email(email)
    vet = crud.get_vet_by_user(user)
    if vet == None:
        return render_template('user_details.html', user = user)
    else:
        return render_template('vet_details.html', user = user, vet = vet)


@app.route('/verifying', methods = ["POST"])
def verify_vet():
    user_id = request.form.get("user_id")
    email = request.form.get("email")
    crud.verify_vet(user_id)
    flash (f"Succesfully verify {email} as a vet!")
    return redirect('/admin')



@app.route("/submit_question", methods=["POST"])
def submit_question():
    """Add a question to the database."""

    # get the image uploaded
    img_url = request.args.get('imgURL')
    print("*" * 20)
    print(img_url)
    print("*" * 20)

    # get the rest of info to create question
    date_created = datetime.now()
    comment_count = 0 # still need to be updating
    question_body = request.form.get("questionBody")
    vote_count = 0
    email = session['email']
    user = crud.get_user_by_email(email)
    crud.create_question(date_created, comment_count, question_body, vote_count, img_url, user)
    return "Your question has been added"


@app.route("/post_image", methods=["POST"])
def submit_image():
    images_file = request.files['images-file']
    result = cloudinary.uploader.upload(images_file, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    img_url = result['secure_url'] 

    return redirect(url_for('submit_question', imgURL=img_url))


@app.route('/show-image')
def show_image():
    img_url = request.args.get('imgURL')
    return render_template('show_img.html', img_src=img_url)


# @app.route("/submit_answer", methods=["POST"])
# def submit_answer():
#     """Add an answer to the database."""
#     # create answer
#     date_created = datetime.now()
#     email = session['email']
#     user = crud.get_user_by_email(email)
#     answer_body = request.form.get("answerBody")
#     vet = crud.get_vet_by_user(user) 
#     question_id = request.form.get("question_id")
#     question = crud.get_question_by_question_id(question_id)
#     if vet == None :
#         flash("Sorry, you are not allowed to answer the question because you're not registered as a vet")
#     elif vet.is_vet_pending == True:
#         flash ("Sorry, your vet status is pending")
#     else:
#         crud.create_answer(date_created, answer_body, vet, question)
#     return "Your answer has been added"




@app.route('/forum', methods = ["GET","POST"])
def submit_answer_vote():
    
    date_created = datetime.now()
    email = session['email']
    user = crud.get_user_by_email(email)
    
    # create answer if user is a vet
    answer_body = request.form.get("new_answer")
    vet = crud.get_vet_by_user(user) 
    question_id = request.form.get("question_id")
    question = crud.get_question_by_question_id(question_id)
    if "new answer" in request.form and answer_body != "":
        if vet == None :
            flash("Sorry, you are not allowed to answer the question because you're not registered as a vet")
        elif vet.is_vet_pending == True:
            flash ("Sorry, your vet status is pending")
        else:
            crud.create_answer(date_created, answer_body, vet, question)
            answer_body = ""
            return redirect('/forum')
    
    # create vote 
    if "new vote" in request.form:
        user_id = user.user_id
        db_vote = crud.get_vote_by_question_id_and_user_id(question_id, user_id)
        if db_vote:
            flash(f"Sorry, you can only vote once per question")
        else:
            crud.create_vote(question_id, user_id, user, question)
            crud.increase_vote(question_id)
            return redirect('/forum')

    
    questions = crud.list_all_questions()
    # search for questions based on keyword 
    if "new search" in request.form:
        keyword = str(request.form.get("key_word"))
        matched_questions = crud.get_questions_by_keyword(keyword)
        return render_template('forum.html', questions=questions, matched_questions=matched_questions)

    # display all questions and answers in db
    return render_template('forum.html', questions=questions, matched_questions=[])
    







@app.route("/map")
def view_vet_map():
    """Show map of vets."""

    return render_template("map.html")


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
