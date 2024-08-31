from datetime import datetime
from flask import Blueprint, abort, request, jsonify
from . import db
from .services import assign_tasks, generate_assignment_report
from .models import AvailableDay, Employee, Skill, Task
from sqlalchemy.orm import joinedload

main = Blueprint('main', __name__)

@main.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        employee_data = request.get_json()
        # Fetch or create the skills and available days from the database
        skill_objects = [Skill.query.filter_by(name=skill).first() or Skill(name=skill) for skill in employee_data['skills']]
        day_objects = [AvailableDay.query.filter_by(day=day).first() or AvailableDay(day=day) for day in employee_data['available_days']]

        new_employee = Employee(
            name=employee_data['name'],
            skills=skill_objects,  # Attach the Skill objects
            availability_hours=employee_data['availability_hours'],
            available_days=day_objects  # Attach the AvailableDay objects
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({'message': 'Employee added'}), 201
    except KeyError as e:
        # Handle missing data fields
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        # General error handling
        abort(500, description=str(e))
@main.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_list = [
        {
            'name': e.name,
          'skills': [skill.name for skill in e.skills],
          'availability_hours': e.availability_hours,
          'available_days': [avl_day.day for avl_day in e.available_days],
        } for e in employees]
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
    tasks = Task.query.options(joinedload(Task.employee)).all()
    task_list = [
        {
            'title': t.title,
            'due_date': t.due_date,
            'duration': t.duration,
            'assigned': t.assigned,
            'assigned_to': t.employee.name if t.employee else "Unassigned",
            'required_skills': [skill.name for skill in t.required_skills]
        } for t in tasks
    ]
    return jsonify(task_list)

@main.route('/assign_tasks', methods=['POST'])
def api_assign_tasks():
    data = request.get_json()
    date_str = data['date']
    try:
        task_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError as error:
        return jsonify({"error": "Invalid date format, please use YYYY-MM-DD"}), 400
    assign_tasks(task_date)
    return jsonify({'message': 'Tasks assigned successfully'}), 200

@main.route('/report_assignments', methods=['GET'])
def report_assignments():
    date = request.args.get('date')  # Get the date parameter from the request
    return generate_assignment_report(date)