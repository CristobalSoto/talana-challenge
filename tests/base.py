import unittest
from flask_testing import TestCase
from app import create_app, db
from app.config import TestingConfig

class BaseTestCase(TestCase):
    def create_app(self):
        # Pass in the testing configuration
        return create_app(TestingConfig)

    def setUp(self):
        db.create_all()  # Create schema before each test

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Destroy schema after each test
