""" facilitate a database setup instead of manually 
    typing commands each time we have new data to seed the database """
from datetime import date
from random import choice, randint
import model, server

model.connect_to_db(server.app)
model.db.create_all()

questions_in_db = []
for question in questions_in_db:
    date_created = question[date_created]