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

def get_user_by_user_id(user_id):
    return User.query.filter(User.user_id == user_id).first()

def validate_login(email, password):
    return User.query.filter(User.email == email, User.password == password).first()


def create_vet(last_name,license_type,license_number,verification_status,is_vet_pending,user):
    """Create and return a new vet"""

    vet = Vet(last_name=last_name,
            license_type=license_type,
            license_number=license_number,
            verification_status=verification_status,
            is_vet_pending=is_vet_pending,
            user=user)

    db.session.add(vet)
    db.session.commit()

    return vet


def verify_vet(user_id):
    """Verify vet/Update vet_pending status to False"""
    vet_verified = Vet.query.filter_by(user_id=user_id).first()
    vet_verified.is_vet_pending = False
    user_vet_verified = User.query.filter_by(user_id=user_id).first()
    user_vet_verified.is_vet = True
    db.session.commit()


def list_all_vets():
    return Vet.query.all()

def list_all_vets_as_users():
    return User.query.filter(User.is_vet == True).all()

def get_vet_by_user(user):
    return Vet.query.filter(Vet.user == user).first()

def create_question(date_created, comment_count, question_body, vote_count, img_url, user):
    """Create and return a new question"""

    question = Question(date_created=date_created, 
                    comment_count=comment_count,
                    question_body=question_body,
                    vote_count=vote_count,
                    img_url=img_url,
                    user=user)

    db.session.add(question)
    db.session.commit()

    return question

def list_all_questions():
    return Question.query.all()

def get_question_by_question_id(question_id):
    return Question.query.filter(Question.question_id == question_id).first()

def get_question_by_question_body(question_body):
    return Question.query.filter(Question.question_body == question_body).first()

def get_questions_by_keyword(keyword):
    return Question.query.filter(Question.question_body.like("%"+keyword+"%")).all()

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

def create_vote(question_id, user_id, user, question):
    """Create and return a vote"""

    vote = Vote(question_id=question_id,
                user_id=user_id,
                user=user,
                question=question)
        
    db.session.add(vote)
    db.session.commit()

    return vote

def get_vote_by_question_id_and_user_id(question_id, user_id):
    return Vote.query.filter(Vote.question_id == question_id, Vote.user_id == user_id).first()

def increase_vote(question_id):
    question = Question.query.filter(Question.question_id == question_id).first()
    question.vote_count += 1
    
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)