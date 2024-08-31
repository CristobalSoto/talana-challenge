from . import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

class AvailableDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(128), unique=True, nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    availability_hours = db.Column(db.Integer)
    skills = db.relationship('Skill', secondary='employee_skills', backref=db.backref('employees', lazy='dynamic'))
    available_days = db.relationship('AvailableDay', secondary='employee_available_days', backref=db.backref('employees', lazy='dynamic'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    due_date = db.Column(db.Date)
    duration = db.Column(db.Integer)  # Duration in hours
    required_skills = db.relationship('Skill', secondary='task_skills', backref=db.backref('tasks', lazy='dynamic'))
    assigned = db.Column(db.Boolean, default=False)  # Indicates if the task is assigned
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    employee = db.relationship('Employee', backref='tasks', foreign_keys=[assigned_to])

# Junction tables
employee_skills = db.Table('employee_skills',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

employee_available_days = db.Table('employee_available_days',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('available_day_id', db.Integer, db.ForeignKey('available_day.id'), primary_key=True)
)

task_skills = db.Table('task_skills',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)
