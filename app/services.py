from .models import Employee, Task
from . import db  # Import the db object here
from datetime import datetime
from flask import jsonify
from sqlalchemy.orm import joinedload

def assign_tasks(date):
    tasks = Task.query.filter_by(assigned=False, due_date=date).all()
    employees = Employee.query.all()

    employee_skills = get_employees_skills(employees)

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
                if is_employee_available(employee, task):
                    assign_task_to_employee(task, employee)
                    break

    db.session.commit()

def is_employee_available(employee, task):
    task_day = task.due_date.strftime("%A")
    is_available = task_day in employee.available_days and employee.availability_hours >= task.duration
    return is_available

def get_employees_skills(employees):
    employee_skills = {}
    for employee in employees:
        for skill in employee.skills:
            if skill in employee_skills:
                employee_skills[skill].append(employee)
            else:
                employee_skills[skill] = [employee]

    return employee_skills

def assign_task_to_employee(task, employee):
    employee.availability_hours -= task.duration
    task.assigned = True
    task.assigned_to = employee.id

def generate_assignment_report(date):
    tasks = Task.query.options(joinedload(Task.employee)).filter_by(due_date=date).all()

    report = []
    for task in tasks:
        report.append({
            'task_title': task.title,
            'employee_name': task.employee.name if task.employee else None,
            'task_duration': task.duration,
            'employee_hours_remaining': task.employee.availability_hours if task.employee else None,
            'skills_required': task.required_skills,
            'employee_skills': task.employee.skills if task.employee else None
        })

    return jsonify(report)


