import unittest
from datetime import date
from app import db, create_app
from app.models import Employee, Task, Skill, AvailableDay
from app.services import assign_tasks, generate_assignment_report
from base import BaseTestCase

class TestReport(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.app = create_app()
        with self.app.app_context():
            db.create_all()
            # Create skills and days
            self.skill_python = Skill(name="Python")
            self.day_monday = AvailableDay(day="Monday")
            self.day_tuesday = AvailableDay(day="Tuesday")

            db.session.add_all([self.skill_python, self.day_monday, self.day_tuesday])
            db.session.commit()

            # Set up employees and tasks
            employee = Employee(
                name="Alice",
                skills=[self.skill_python],
                availability_hours=8,
                available_days=[self.day_monday, self.day_tuesday]
            )
            db.session.add(employee)

            task = Task(
                title="Develop API",
                due_date=date(2023, 8, 28),  # Monday
                duration=4,
                required_skills=[self.skill_python]
            )
            db.session.add(task)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        super().tearDown()

    def test_generate_assignment_report(self):
        with self.app.app_context():
            assign_tasks(date(2023, 8, 28))  # Assign tasks to employees
            report = generate_assignment_report(date(2023, 8, 28))  # Now request the report
            self.assertEqual(len(report), 1)  # One task should be assigned
            self.assertEqual(report[0]['employee_name'], 'Alice')
            self.assertEqual(report[0]['task_title'], 'Develop API')
