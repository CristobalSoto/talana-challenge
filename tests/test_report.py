from app import db
from app.models import Employee, Task
from app.services import assign_tasks
from datetime import date
from base import BaseTestCase


class TestReport(BaseTestCase):
    def test_generate_assignment_report(self):
        # Set up employees and tasks as before
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

        assign_tasks("2023-08-28")  # Assign tasks to employees

        # Now request the report
        with self.client:
            response = self.client.get('/report_assignments?date=2023-08-28')
            self.assertEqual(response.status_code, 200)
            report_data = response.json
            self.assertEqual(len(report_data), 1)  # One task should be assigned
            self.assertEqual(report_data[0]['employee_name'], 'Alice')
