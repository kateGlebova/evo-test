from datetime import datetime

from app.models import Position, Department


def get_all_positions():
    return [(position.id, position.name) for position in Position.query.all()]


def get_all_departments():
    return [(department.id, department.name) for department in Department.query.all()]


def parse_date(date, format):
    try:
        parsed_date = datetime.strptime(date, format).date()
    except ValueError:
        parsed_date = None
    return parsed_date


def parse_datepicker_date(date):
    return parse_date(date, '%m/%d/%Y')
