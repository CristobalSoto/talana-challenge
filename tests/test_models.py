from base import BaseTestCase
from app.models import Employee, Task, Skill, AvailableDay
from datetime import date
from app import db  # Make sure to import db directly

class TestModels(BaseTestCase):
    
    def setUp(self):
        super().setUp()
        db.create_all()
        self.skill_python = Skill(name="Python")
        self.skill_flask = Skill(name="Flask")
        self.day_monday = AvailableDay(day="Monday")
        self.day_wednesday = AvailableDay(day="Wednesday")
        db.session.add_all([self.skill_python, self.skill_flask, self.day_monday, self.day_wednesday])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super().tearDown()

    def test_employee_creation(self):
        """ Test adding a new employee """
        employee = Employee(
            name="John Doe",
            skills=[self.skill_python, self.skill_flask],
            availability_hours=8,
            available_days=[self.day_monday, self.day_wednesday]
        )
        db.session.add(employee)  # Use db directly
        db.session.commit()
        self.assertEqual(Employee.query.count(), 1)

    def test_task_creation(self):
        """ Test adding a new task """
        due_date = date(2023, 9, 1)  # Create a date object
        task = Task(
            title="API Development",
            due_date=due_date,
            duration=5,
            required_skills=[self.skill_python]
        )
        db.session.add(task)
        db.session.commit()
        self.assertEqual(Task.query.count(), 1)
