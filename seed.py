""" Facilitate a database setup instead of manually 
    typing commands each time we have new data to seed the database """
from datetime import datetime
from random import choice, randint
import model, server, crud
import os


os.system('dropdb petdiscussions')
os.system('createdb petdiscussions')

model.connect_to_db(server.app)
model.db.create_all()



# Create 10 users and store them in a list to create vets and questions;
users_ls = []
admin_ls = []
for n in range(10):
    email = f'user{n}@test.com'  
    password = f'test{n}'
   
    # make user0 an admin
    if n == 0:
        is_vet = False
        is_admin = True
        db_user = crud.create_user(email, password, is_vet, is_admin)
        users_ls.append(db_user)
        admin_ls.append(db_user)
    # make user1 a vet
    elif n == 1:
        is_vet = True
        is_admin = False
        db_user = crud.create_user(email, password, is_vet, is_admin)
        users_ls.append(db_user)
    # all other users are neither vet nor admin 
    else:
        is_vet = False
        is_admin = False   
        db_user = crud.create_user(email, password, is_vet, is_admin)
        users_ls.append(db_user)



#Create vets from the 10 users created and store them in a list to create answers
vets_ls = []
for user in users_ls:
    
    if user.is_vet == True: 
        last_name = choice(['Koning','Smith','Lee','Mendez','Anderson','Huynh'])
        license_type = 'DVM'
        license_number = randint(1000,1999)
        verification_status = choice(['active','expired','retired'])
        is_vet_pending = True
        user = user

        db_vet = crud.create_vet(last_name,license_type,license_number,verification_status,is_vet_pending,user)
        vets_ls.append(db_vet)


# Create 10 questions and 10 according answers 
question_content_ls = ["What do bunnies eat?", 
                    "Can dog eat chocolate?", 
                    "Can bunnies eat fruits?",
                    "Should I bath my bunny?",
                    "How long do cats live?",
                    "Can bunnies be potty trained?",
                    "How often should I bath my dog?",
                    "What does catnip do to cats?",
                    "Can I brush my dog's teeth daily?",
                    "Do all bunnies need bondmate?"]

answer_content_ls = ["Bunnies eat hay, veggies and hay-based pellets",
                    "Chocolate is toxic for dogs",
                    "Bunnies can eat fruits but only in small amount as treats",
                    "Bunnies cannot be bathed",
                    "The average lifespan of an indoor cat is 13 to 17 year",
                    "Bunnies can be potty trained to go in a litterbox",
                    "Depend on different needs but usually once a month is good",
                    "Catnip is not considered harmful and the responses vary from sedation to hyper activity",
                    "Daily brushing is most ideal",
                    "Most of them prefer to be in pairs but some do fine being alone"]


for question,answer in zip(question_content_ls,answer_content_ls):

    # Create 10 questions
    date_created = datetime.now()
    comment_count = 1
    question_body = question
    vote_count = randint(1,10)
    img_url = ''
    user = choice(users_ls)
    db_question = crud.create_question(date_created,comment_count,question_body,vote_count,img_url,user)
    

    # Create 10 according answers
    date_created = datetime.now()
    answer_body = answer
    vet = choice(vets_ls)
    question = db_question 
    db_answer = crud.create_answer(date_created,answer_body,vet,question)
    


