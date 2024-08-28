from flask import Blueprint, request, jsonify
from . import db
from .services import assign_tasks, generate_assignment_report
from .models import Employee, Task

main = Blueprint('main', __name__)

@main.route('/add_employee', methods=['POST'])
def add_employee():
    employee_data = request.get_json()
    new_employee = Employee(
        name=employee_data['name'],
        skills=employee_data['skills'],
        availability_hours=employee_data['availability_hours'],
        available_days=employee_data['available_days']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added'}), 201

@main.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_list = [{'name': e.name, 'skills': e.skills, 'availability_hours': e.availability_hours, 'available_days': e.available_days} for e in employees]
    return jsonify(employee_list)

@main.route('/add_task', methods=['POST'])
def add_task():
    task_data = request.get_json()
    new_task = Task(
        title=task_data['title'],
        due_date=task_data['due_date'],
        duration=task_data['duration'],
        required_skills=task_data['required_skills']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added'}), 201

@main.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{'title': t.title, 'due_date': t.due_date, 'duration': t.duration, 'required_skills': t.required_skills} for t in tasks]
    return jsonify(task_list)

@main.route('/assign_tasks', methods=['POST'])
def api_assign_tasks():
    assign_tasks()
    return jsonify({'message': 'Tasks assigned successfully'}), 200

@main.route('/report_assignments', methods=['GET'])
def report_assignments():
    date = request.args.get('date')  # Get the date parameter from the request
    return generate_assignment_report(date)