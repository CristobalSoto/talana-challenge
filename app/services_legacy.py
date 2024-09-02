from .models import Employee, Task
from . import db  # Import the db object here
from datetime import datetime
from flask import jsonify

"""
Historic changes of assign task
"""

class AssignTaskV3:

    def __init__(self):
        print("Initializing the assign task version 3")

    def assign_tasks(self, date):
        tasks = Task.query.filter_by(assigned=False, due_date=date).all()
        employees = Employee.query.all()

        employee_skills = self.get_employees_skills(employees)

        for task in tasks:
            if task.required_skills[0] in employee_skills:
                common_employees = set(employee_skills[task.required_skills[0]])
            else:
                break
            for skill in task.required_skills[1:]:
                common_employees.intersection_update(employee_skills[skill])

            suitable_employees_skills = list(common_employees)
            if suitable_employees_skills:
                for employee in suitable_employees_skills:
                    if self.is_employee_available(employee, task):
                        self.assign_task_to_employee(task, employee)
                        break

        db.session.commit()

    def is_employee_available(self, employee, task):
        task_day = task.due_date.strftime("%A")
        is_available = task_day in employee.available_days and employee.availability_hours >= task.duration
        return is_available

    def get_employees_skills(self, employees):
        employee_skills = {}
        for employee in employees:
            for skill in employee.skills:
                if skill in employee_skills:
                    employee_skills[skill].append(employee)
                else:
                    employee_skills[skill] = [employee]

        return employee_skills

    def assign_task_to_employee(self, task, employee):
        employee.availability_hours -= task.duration
        task.assigned = True
        task.assigned_to = employee.id


class AssignTaskV2:

    def __init__(self):
        print("Initializing the assign task version 2")
    
    def assign_tasks(self):
        tasks = Task.query.filter_by(assigned=False).all()
        employees = Employee.query.all()

        for task in tasks:
            suitable_employees = []

            for employee in employees:
                if self.employee_is_suitable(employee, task):
                    suitable_employees.append(employee)

            if suitable_employees:
                self.assign_task_to_employee(task, suitable_employees[0])

        db.session.commit()

    def employee_is_suitable(self, employee, task):
        # Check if the employee has the required skills and is available
        has_skills = all(skill in employee.skills for skill in task.required_skills)
        is_available = task.due_date.strftime("%A") in employee.available_days and employee.availability_hours >= task.duration
        return has_skills and is_available

    def assign_task_to_employee(self, task, employee):
        employee.availability_hours -= task.duration
        task.assigned = True
        task.assigned_to = employee.id