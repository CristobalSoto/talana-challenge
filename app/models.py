from . import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    skills = db.Column(db.PickleType)  # Storing list of skills
    availability_hours = db.Column(db.Integer)
    available_days = db.Column(db.PickleType)  # Consider normalizing this as well if practical

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    due_date = db.Column(db.Date)
    duration = db.Column(db.Integer)  # Duration in hours
    required_skills = db.Column(db.PickleType)  # Storing list of required skills
    assigned = db.Column(db.Boolean, default=False)  # Indicates if the task is assigned
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)  # Foreign key to Employee
    employee = db.relationship('Employee', backref='tasks', foreign_keys=[assigned_to])
