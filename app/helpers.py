from datetime import datetime

from flask import flash

from app import db
from app.models import Position, Department, WorkHistory, Employee


def get_all_positions():
    return [(position.id, position.name) for position in Position.query.all()]


def get_all_departments():
    return [(department.id, department.name) for department in Department.query.all()]


def str_to_date(date, format='%d/%m/%Y'):
    try:
        parsed_date = datetime.strptime(date, format).date()
    except ValueError:
        parsed_date = None
    return parsed_date


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s: %s" % (
                getattr(form, field).label.text,
                error
            ))


def update_position(employee, new_position_id, new_department_id, start_date):
    old_position = WorkHistory.query.filter_by(
        employee_id=employee.id,
        position_id=employee.position_id,
        department_id=employee.department_id
    ).first()
    if old_position:
        old_position.end = start_date

    new_position = WorkHistory(
        employee_id=employee.id,
        position_id=new_position_id,
        department_id=new_department_id,
        start=start_date
    )
    db.session.add(new_position)


def update_director(department_id, employee, new_director):
    if new_director:
        director = Employee.query.filter_by(department_id=department_id, is_director=True).first()
        if director:
            director.is_director = False
        employee.is_director = True
    else:
        employee.is_director = False