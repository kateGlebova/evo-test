from datetime import datetime

from flask import flash

from app.models import Position, Department


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
