""" Functions used for CRUD """

from model import db, User, Vet, Question, Answer, Vote, connect_to_db 


def create_user(email, password, is_vet, is_admin):
    """Create and return a new user"""

    user = User(email=email, 
            password=password, 
            is_vet=is_vet, 
            is_admin=is_admin)

    db.session.add(user)
    db.session.commit()

    return user

def list_all_users():
    return User.query.all()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def validate_login(email, password):
    return User.query.filter(User.email == email, User.password == password).first()


def create_vet(last_name,license_type,license_number,verification_status,user):
    """Create and return a new vet"""

    vet = Vet(last_name=last_name,
            license_type=license_type,
            license_number=license_number,
            verification_status=verification_status,
            user=user)

    db.session.add(vet)
    db.session.commit()

    return vet

def list_all_vets():
    return Vet.query.all()


def create_question(date_created, comment_count, question_body, vote_count,user):
    """Create and return a new question"""

    question = Question(date_created=date_created, 
                    comment_count=comment_count,
                    question_body=question_body,
                    vote_count=vote_count,
                    user=user)

    db.session.add(question)
    db.session.commit()

    return question

def list_all_questions():
    return Question.query.all()


def create_answer(date_created, answer_body, vet, question):
    """Create and return a new answer to a question"""

    answer = Answer(date_created=date_created,
                answer_body=answer_body,
                vet=vet,
                question=question)
    
    db.session.add(answer)
    db.session.commit()

    return answer

def list_all_answers():
    return Answer.query.all()

def get_answer_by_question_id(question_id):
    return Answer.query.filter(Answer.question_id == question_id).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)