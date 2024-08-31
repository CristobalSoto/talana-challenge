from app import db, create_app
from app.models import Employee, Task, Skill, AvailableDay
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create skills
    skill_python = Skill(name="Python")
    skill_flask = Skill(name="Flask")
    skill_javascript = Skill(name="JavaScript")
    skill_react = Skill(name="React")
    skill_fastapi = Skill(name="FastAPI")

    # Create available days
    day_monday = AvailableDay(day="Monday")
    day_tuesday = AvailableDay(day="Tuesday")
    day_wednesday = AvailableDay(day="Wednesday")
    day_thursday = AvailableDay(day="Thursday")
    day_friday = AvailableDay(day="Friday")

    # Add skills and days to session
    db.session.add_all([skill_python, skill_flask, skill_javascript, skill_react])
    db.session.add_all([day_monday, day_tuesday, day_wednesday, day_thursday, day_friday])
    db.session.commit()

    # Create employees with new relationship structure
    empl1_skills = [skill_python, skill_flask]
    empl1_avlb_days = [day_monday, day_tuesday, day_wednesday]
    employee1 = Employee(name="Alice", availability_hours=8, skills=empl1_skills, available_days=empl1_avlb_days)

    empl2_skills = [skill_javascript, skill_react]
    empl2_avlb_days = [day_wednesday, day_thursday, day_friday]
    employee2 = Employee(name="Bob", availability_hours=8, skills=empl2_skills, available_days=empl2_avlb_days)

    empl3_skills = [skill_fastapi]
    empl3_avlb_days = [day_thursday]
    employee3 = Employee(name="Cris", availability_hours=4, skills=empl3_skills, available_days=empl3_avlb_days)

    db.session.add_all([employee1, employee2, employee3])

    # Create tasks with new relationship structure
    task1 = Task(
        title="Develop API",
        due_date=date(2023, 8, 28),  # Monday
        duration=4,
        required_skills=[skill_python]
    )

    task2 = Task(
        title="Frontend Component",
        due_date=date(2023, 8, 29),  # Tuesday
        duration=3,
        required_skills=[skill_javascript, skill_react]
    )

    db.session.add_all([task1, task2])

    # Commit all the changes
    db.session.commit()

    print("Database seeded successfully!")
