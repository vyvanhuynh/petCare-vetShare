""" Server for pet care discussion app. """

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def create_homepage():
    return render_template('homepage.html')

@app.route('/register')
def show_registration_form():
    return render_template('register.html')





    # email = request.form.get("email")
    # password = request.form.get("password")
    # vet_status = request.form.get("vet status")
    # admin_status = request.form.get("admin status")
    # db_email = crud.get_user_by_email(email)
    # if db_email:
    #     flash(f"{email} is already registered. Please try a different email")
    # else:
    #     user = crud.create_user(email, password, vet_status, admin_status)         
    #     flash("Your account has been successfully created and you can now log in")
    # return redirect('/')








if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
