import logging
from sqlalchemy.exc import SQLAlchemyError
from .models import db, Employee, Task
from sqlalchemy.orm import joinedload
from datetime import datetime

# Setting up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def assign_tasks(assignment_date):
    # Convert string date to datetime.date object if needed
    if isinstance(assignment_date, str):
        assignment_date = datetime.strptime(assignment_date, "%Y-%m-%d").date()

    try:
        tasks = Task.query.options(joinedload(Task.required_skills), joinedload(Task.employee)).filter_by(assigned=False, due_date=assignment_date).all()
        employees = Employee.query.options(joinedload(Employee.skills), joinedload(Employee.available_days)).all()

        for task in tasks:
            suitable_employees = find_suitable_employees(task, employees)
            if suitable_employees:
                assign_task_to_employee(task, suitable_employees[0])

        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error assigning tasks: {e}")
        raise

    db.session.commit()

def find_suitable_employees(task, employees):
    suitable_employees = []
    for employee in employees:
        if all(skill in employee.skills for skill in task.required_skills) and is_employee_available(employee, task):
            suitable_employees.append(employee)
    return suitable_employees

def assign_task_to_employee(task, employee):
    employee.availability_hours -= task.duration
    task.assigned = True
    task.assigned_to = employee.id

def is_employee_available(employee, task):
    return task.due_date.strftime("%A") in [day.day for day in employee.available_days] and employee.availability_hours >= task.duration

def generate_assignment_report(report_date):
    # Convert string date to datetime.date object if needed
    if isinstance(report_date, str):
        report_date = datetime.strptime(report_date, "%Y-%m-%d").date()

    try:
        tasks = Task.query.options(joinedload(Task.employee)).filter_by(due_date=report_date).all()
        report = []
        for task in tasks:
            report.append({
                'task_title': task.title,
                'employee_name': task.employee.name if task.employee else None,
                'task_duration': task.duration,
                'employee_hours_remaining': task.employee.availability_hours if task.employee else None,
                'skills_required': [skill.name for skill in task.required_skills],
                'employee_skills': [skill.name for skill in task.employee.skills] if task.employee else None
            })
        return report
    except SQLAlchemyError as e:
        logger.error(f"Error generating report: {e}")
        raise