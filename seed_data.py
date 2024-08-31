from app import db, create_app
from app.models import Employee, Task
from datetime import date

app = create_app()

with app.app_context():
    # Drop and recreate all tables (optional, depending on whether you want to start fresh)
    db.drop_all()
    db.create_all()

    # Create some employees
    employee1 = Employee(
        name="Alice",
        skills=['Python', 'Flask'],
        availability_hours=8,
        available_days=['Monday', 'Tuesday', 'Wednesday']
    )

    employee2 = Employee(
        name="Bob",
        skills=['JavaScript', 'React'],
        availability_hours=8,
        available_days=['Wednesday', 'Thursday', 'Friday']
    )

    db.session.add_all([employee1, employee2])

    # Create some tasks
    task1 = Task(
        title="Develop API",
        due_date=date(2023, 8, 28),  # Monday
        duration=4,
        required_skills=['Python']
    )

    task2 = Task(
        title="Frontend Component",
        due_date=date(2023, 8, 29),  # Tuesday
        duration=3,
        required_skills=['JavaScript', 'React']
    )

    db.session.add_all([task1, task2])

    # Commit all the changes
    db.session.commit()

    print("Database seeded successfully!")