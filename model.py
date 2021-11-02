"""Models for pet care app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    vet_status = db.Column(db.Boolean, default = False)
    admin_status = db.Column(db.Boolean)

    # vet = a list of Vet objects
    # question = a list of Question objects
    # vote = a list of Vote objects

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"



class Vet(db.Model):
    """A vet."""

    __tablename__ = "vets"

    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id"),
                        primary_key = True)
    last_name = db.Column(db.String)
    license_type = db.Column(db.String)
    license_number = db.Column(db.Integer)
    verification_status = db.Column(db.String)

    user = db.relationship("User", backref = "vet")
    # answer = a list of Answer objects

    def __repr__(self):
        return f"<Vet user_id={self.user_id} last_name={self.last_name}>"



class Question(db.Model):
    """A question submitted by a user."""

    __tablename__ = "questions"
    
    question_id = db.Column(db.Integer,
                            autoincrement = True,
                            primary_key = True)
    date_created = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    comment_count = db.Column(db.Integer)
    question_body = db.Column(db.Text)
    vote_count = db.Column(db.Integer)

    user = db.relationship("User", backref = "question")
    # answer = a list of Answer objects
    # vote = a list of Vote objects

    def __repr__(self):
        return f"<Question question_id={self.question_id} question_body={self.question_body}>"



class Answer(db.Model):
    """An answer made by a veterinarian in response to a question."""

    __tablename__ = "answers"

    answer_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    date_created = db.Column(db.Date)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("vets.user_id"))
    answer_body = db.Column(db.Text)

    vet = db.relationship("Vet", backref = "answer")
    question = db.relationship("Question", backref = "answer")

    def __repr__(self):
        return f"<Answer answer_id={self.answer_id} answer_body={self.answer_body}>"



class Vote(db.Model):
    """A vote given by a user to a question."""

    __tablename__ = "votes"

    vote_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref = "vote")
    question = db.relationship("Question", backref = "vote")

    def __repr__(self):
        return f"<Vote vote_id={self.vote_id} question_id={self.question_id}>"



def connect_to_db(flask_app, db_uri="postgresql:///petdiscussions", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
