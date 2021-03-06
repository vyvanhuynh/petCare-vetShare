""" Models for pet care app. """

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    is_vet = db.Column(db.Boolean, default = False)
    is_admin = db.Column(db.Boolean, default = False)

    # vet = a list of Vet objects
    # questions = a list of Question objects
    # votes = a list of Vote objects

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"



class Vet(db.Model):
    """A user who is also a vet."""

    __tablename__ = "vets"

    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id"),
                        primary_key = True)
    last_name = db.Column(db.String)
    license_type = db.Column(db.String)
    license_number = db.Column(db.Integer)
    verification_status = db.Column(db.String)
    is_vet_pending = db.Column(db.Boolean, default = True)

    user = db.relationship("User", backref = "vet", uselist = False)
    # answers = a list of Answer objects

    # @hybrid_property
    # def verification(self):
    #     return User.is_vet
    
    # @verification.setter
    # def verification(self,value):
    #     if value and not self.verification:
    #         User.is_vet = False
    #     if not value and self.verification:
    #         User.is_vet = True


    def __repr__(self):
        return f"<Vet user_id={self.user_id} last_name={self.last_name}>"



class Question(db.Model):
    """A question submitted by a user."""

    __tablename__ = "questions"
    
    question_id = db.Column(db.Integer,
                            autoincrement = True,
                            primary_key = True)
    date_created = db.Column(db.DateTime) #format date
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    comment_count = db.Column(db.Integer)
    question_body = db.Column(db.Text)
    vote_count = db.Column(db.Integer)
    img_url = db.Column(db.Text, default = '')

    user = db.relationship("User", backref = "questions")
    # answers = a list of Answer objects
    # votes = a list of Vote objects

    def __repr__(self):
        return f"<Question question_id={self.question_id} question_body={self.question_body}>"



class Answer(db.Model):
    """An answer made by a veterinarian in response to a question."""
    
    __tablename__ = "answers"

    answer_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    date_created = db.Column(db.DateTime)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("vets.user_id"))
    answer_body = db.Column(db.Text)

    vet = db.relationship("Vet", backref = "answers")
    question = db.relationship("Question", backref = "answers")

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

    user = db.relationship("User", backref = "votes")
    question = db.relationship("Question", backref = "votes")

    def __repr__(self):
        return f"<Vote vote_id={self.vote_id} question_id={self.question_id} user_id={self.user_id}>"


def example_data():
    """Create some sample datas."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Vet.query.delete()
    Question.query.delete()
    Answer.query.delete()
    Vote.query.delete()

    # Add sample users, vets, questions, answers and votes 
    testvetu = User(email="u1@test.com", 
            password="testu1", 
            is_vet=True, 
            is_admin=False)
            
    testadu = User(email="u2@test.com", 
            password="testu2", 
            is_vet=False, 
            is_admin=True)

    testvet = Vet(last_name="last_name",
            license_type="license_type",
            license_number=1234,
            verification_status=True,
            is_vet_pending=False,
            user=testvetu)

    testques = Question(date_created=datetime.now(), 
                    comment_count=2,
                    question_body="question_body",
                    vote_count=3,
                    img_url="",
                    user=testadu)
    
    testans = Answer(date_created=datetime.now(),
                answer_body="answer_body",
                vet=testvet,
                question=testques)

    testvot = Vote(question_id=1,
                user_id=1,
                user=testadu,
                question=testques)

    db.session.add_all([testvetu, testadu, testvet, testques, testans, testvot])
    db.session.commit()


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
