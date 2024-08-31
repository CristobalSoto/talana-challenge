# tests/test_services.py

import unittest
from datetime import date
from app import db
from app.models import Employee, Task
from app.services import assign_tasks
from base import BaseTestCase

class TestTaskAssignment(BaseTestCase):

    def setUp(self):
        super().setUp()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super().tearDown()

    def test_task_assignment_success(self):
        # This test should pass since Alice is available on Monday
        employee = Employee(
            name="Alice",
            skills=['Python', 'Flask'],
            availability_hours=8,
            available_days=['Monday', 'Tuesday']
        )
        db.session.add(employee)
        
        task = Task(
            title="Develop API",
            due_date=date(2023, 8, 28),  # Monday
            duration=4,
            required_skills=['Python']
        )
        db.session.add(task)
        db.session.commit()

        assign_tasks("2023-08-28")
        db.session.refresh(task)
        self.assertTrue(task.assigned)
        self.assertEqual(task.assigned_to, employee.id)

    def test_task_assignment_failure_due_to_availability(self):
        # This test should fail to assign since Alice is not available on Friday
        employee = Employee(
            name="Alice",
            skills=['Python', 'Flask'],
            availability_hours=8,
            available_days=['Monday', 'Tuesday']
        )
        db.session.add(employee)
        
        task = Task(
            title="Develop API",
            due_date=date(2023, 9, 1),  # Friday
            duration=4,
            required_skills=['Python']
        )
        db.session.add(task)
        db.session.commit()
        assign_tasks("2023-09-01")
        
        db.session.refresh(task)
        self.assertFalse(task.assigned)

    def test_task_assignment_failure_due_to_skills(self):
        # Create an employee without matching skills
        employee = Employee(
            name="Bob",
            skills=['JavaScript'],
            availability_hours=8,
            available_days=['Monday', 'Tuesday']
        )
        db.session.add(employee)
        
        # Create a task that does not match the employee's skills
        task = Task(
            title="Develop API",
            due_date=date(2023, 9, 1),  # Monday
            duration=4,
            required_skills=['Python']
        )
        db.session.add(task)
        db.session.commit()

        assign_tasks("2023-09-01")
        db.session.refresh(task)
        self.assertFalse(task.assigned)
