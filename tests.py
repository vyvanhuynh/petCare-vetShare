"""Tests for crud.py"""
import unittest
from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data, User
from flask import session
import crud
import os



class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""
        os.system('createdb testdb')
        
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'pet'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)

    def test_login(self):
        """Test login page for users that are not admin."""

        result = self.client.post("/login",
                                  data={"email": "u1@test.com", "password": "testu1"},
                                  follow_redirects=True)
        self.assertIn(b"Ask A Question", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()



if __name__ == "__main__":
    # If called like a script, run our tests
     unittest.main()

