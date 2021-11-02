import os, json
from datetime import date
from random import choice, randint
import model, server

model.connect_to_db(server.app)
model.db.create_all()

# Load question data from JSON file
with open('data/questions.json') as f:
    movie_data = json.loads(f.read())