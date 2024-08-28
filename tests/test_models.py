from base import BaseTestCase
from app.models import Employee, Task
from datetime import date
from app import db  # Make sure to import db directly

class TestModels(BaseTestCase):
    
    def test_employee_creation(self):
        """ Test adding a new employee """
        employee = Employee(name="John Doe", skills=['Python', 'Flask'], availability_hours=8, available_days=['Monday', 'Wednesday'])
        db.session.add(employee)  # Use db directly
        db.session.commit()
        self.assertEqual(Employee.query.count(), 1)

    def test_task_creation(self):
        """ Test adding a new task """
        due_date = date(2023, 9, 1)  # Create a date object
        task = Task(title="API Development", due_date=due_date, duration=5, required_skills=['Python'])
        db.session.add(task)
        db.session.commit()
        self.assertEqual(Task.query.count(), 1)


