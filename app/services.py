from .models import Employee, Task
from . import db  # Import the db object here
from datetime import datetime
from flask import jsonify

def assign_tasks():
    tasks = Task.query.filter_by(assigned=False).all()
    employees = Employee.query.all()

    for task in tasks:
        suitable_employees = []

        for employee in employees:
            if employee_is_suitable(employee, task):
                suitable_employees.append(employee)

        if suitable_employees:
            assign_task_to_employee(task, suitable_employees[0])

    db.session.commit()

def employee_is_suitable(employee, task):
    # Check if the employee has the required skills and is available
    has_skills = all(skill in employee.skills for skill in task.required_skills)
    is_available = task.due_date.strftime("%A") in employee.available_days and employee.availability_hours >= task.duration
    return has_skills and is_available

def assign_task_to_employee(task, employee):
    employee.availability_hours -= task.duration
    task.assigned = True
    task.assigned_to = employee.id

def generate_assignment_report(date):
    tasks = Task.query.filter_by(due_date=date).all()  # Get all tasks due on the given date
    report = []

    for task in tasks:
        employee = Employee.query.get(task.assigned_to)
        report.append({
            'task_title': task.title,
            'employee_name': employee.name if employee else None,
            'task_duration': task.duration,
            'employee_hours_remaining': employee.availability_hours if employee else None,
            'skills_required': task.required_skills,
            'employee_skills': employee.skills if employee else None
        })

    return jsonify(report)


