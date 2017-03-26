from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError

from app.helpers import get_all_positions, get_all_departments, str_to_date


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class VacancyForm(FlaskForm):
    position_id = SelectField('Position', coerce=int, choices=get_all_positions(), validators=[DataRequired()])
    publishment_date = StringField('Publishment date', description='%d/%m/%y', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, **kwargs):
        super(VacancyForm, self).__init__(**kwargs)
        self.position_id.choices = get_all_positions()

    def validate(self):
        publishment_date = str_to_date(self.publishment_date.data, self.publishment_date.description)
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
    position_id = SelectField('Position', coerce=int, validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField(
        'Phone number',
        validators=[DataRequired(), Regexp('^\+[0-9]{12}$', 0, 'Invalid phone number')]
    )
    birth_date = StringField('Birth date', render_kw={"placeholder": "dd/mm/yy"}, validators=[DataRequired()])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    start_date = StringField('Start date', validators=[DataRequired()])
    director = BooleanField('Director')
    submit = SubmitField('Submit')

    def __init__(self, **kwargs):
        super(EmployeeForm, self).__init__(**kwargs)
        self.position_id.choices = get_all_positions()
        self.department_id.choices = get_all_departments()

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        birth_date = str_to_date(self.birth_date.data)
        if not birth_date:
            self.birth_date.errors.append("Invalid birth date")
            return False
        if birth_date >= datetime.date(datetime.today()):
            self.birth_date.errors.append("A birth date can not be today or later.")
            return False
        self.birth_date.data = birth_date

        start_date = str_to_date(self.start_date.data)
        if not start_date:
            start_date = datetime.date(datetime.today())
        self.start_date.data = start_date
        return True

