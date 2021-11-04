""" Server for pet care discussion app. """

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

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
        user = crud.create_user(email, password, is_vet, is_admin)        
        flash("Your account has been successfully created! You can now log in")        
    return redirect('/')


@app.route('/vets')
def show_vet_registration_form():
    return render_template('vet_verify.html')


@app.route('/vets', methods = ["POST"])
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
        verification_status = request.form.get("verification_status")
       
        # create a vet from this new user
        vet = crud.create_vet(last_name,license_type,license_number,verification_status,user)       
    return redirect('/')


@app.route('/login', methods = ["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    db_login = crud.validate_login(email,password)
    if db_login:
        session['email'] = email
        flash(f"Welcome,{email}!")
    else:
        flash("Please try again, we can't verify your email and/or your password")
    return redirect('/')



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
