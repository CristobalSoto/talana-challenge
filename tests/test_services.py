import unittest
from datetime import date
from app import db, create_app
from app.models import Employee, Task, Skill, AvailableDay
from app.services import assign_tasks
from base import BaseTestCase

class TestTaskAssignment(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.app = create_app()
        with self.app.app_context():
            db.create_all()
            # Create or find existing skills
            self.skill_python = Skill.query.filter_by(name="Python").first() or Skill(name="Python")
            self.skill_flask = Skill.query.filter_by(name="Flask").first() or Skill(name="Flask")
            self.skill_javascript = Skill.query.filter_by(name="JavaScript").first() or Skill(name="JavaScript")
            self.day_monday = AvailableDay.query.filter_by(day="Monday").first() or AvailableDay(day="Monday")
            self.day_tuesday = AvailableDay.query.filter_by(day="Tuesday").first() or AvailableDay(day="Tuesday")
            self.day_friday = AvailableDay.query.filter_by(day="Friday").first() or AvailableDay(day="Friday")
            db.session.add_all([self.skill_python, self.skill_flask, self.skill_javascript, self.day_monday, self.day_tuesday, self.day_friday])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        super().tearDown()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        super().tearDown()

    def test_task_assignment_success(self):
        # This test should pass since Alice is available on Monday
        with self.app.app_context():
            employee = Employee(
                name="Alice",
                skills=[self.skill_python, self.skill_flask],
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

            assign_tasks(date(2023, 8, 28))
            db.session.refresh(task)
            self.assertTrue(task.assigned)
            self.assertEqual(task.assigned_to, employee.id)

    def test_task_assignment_failure_due_to_availability(self):
        # This test should fail to assign since Alice is not available on Friday
        with self.app.app_context():
            employee = Employee(
                name="Alice",
                skills=[self.skill_python, self.skill_flask],
                availability_hours=8,
                available_days=[self.day_monday, self.day_tuesday]
            )
            db.session.add(employee)
            
            task = Task(
                title="Develop API",
                due_date=date(2023, 9, 1),  # Friday
                duration=4,
                required_skills=[self.skill_python]
            )
            db.session.add(task)
            db.session.commit()
            assign_tasks(date(2023, 9, 1))
            
            db.session.refresh(task)
            self.assertFalse(task.assigned)

    def test_task_assignment_failure_due_to_skills(self):
        # Create an employee without matching skills
        with self.app.app_context():
            employee = Employee(
                name="Bob",
                skills=[self.skill_javascript],
                availability_hours=8,
                available_days=[self.day_monday, self.day_tuesday]
            )
            db.session.add(employee)
            
            # Create a task that does not match the employee's skills
            task = Task(
                title="Develop API",
                due_date=date(2023, 9, 1),  # Monday
                duration=4,
                required_skills=[self.skill_python]
            )
            db.session.add(task)
            db.session.commit()

            assign_tasks(date(2023, 9, 1))
            db.session.refresh(task)
            self.assertFalse(task.assigned)
