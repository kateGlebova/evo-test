from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError

from app.helpers import get_all_positions, get_all_departments, parse_datepicker_date, parse_date


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class VacancyForm(FlaskForm):
    position = SelectField('Position', coerce=int, choices=get_all_positions(), validators=[DataRequired()])
    publishment_date = StringField('Publishment date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate(self):
        publishment_date = parse_datepicker_date(self.publishment_date.data)
        if not publishment_date:
            publishment_date = datetime.date(datetime.today())
        self.publishment_date.data = publishment_date
        return True


class PositionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    position = SelectField('Position', coerce=int, choices=get_all_positions(), validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone number', validators=[DataRequired(), Regexp('\+[0-9]{12}')])
    birth_date = StringField('Birth date', render_kw={"placeholder": "dd/mm/yy"}, validators=[DataRequired()])
    department = SelectField('Department', coerce=int, choices=get_all_departments(), validators=[DataRequired()])
    start_date = StringField('Start date', validators=[DataRequired()])
    director = BooleanField('Director')
    submit = SubmitField('Submit')

    def validate(self):
        birth_date = parse_date(self.birth_date.data, '%d/%m/%Y')
        if not birth_date:
            raise ValidationError("Invalid birth date")
        if birth_date >= datetime.date(datetime.today()):
            raise ValidationError("A birth date can not be today or later.")
        self.birth_date.data = birth_date

        start_date = parse_datepicker_date(self.start_date.data)
        if not start_date:
            start_date = datetime.date(datetime.today())
        self.start_date.data = start_date
        return True

