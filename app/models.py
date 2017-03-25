from app import db


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    vacancies = db.relationship('Vacancy', backref='department')
    employees = db.relationship('Employee', backref='department')

class Position(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    vacancies = db.relationship('Vacancy', backref='position')
    employees = db.relationship('Employee', backref='position')


class Vacancy(db.Model):
    __tablename__ = 'vacancies'

    id = db.Column(db.Integer, primary_key=True)
    publishment_date = db.Column(db.Date, nullable=False)
    closing_date = db.Column(db.Date)
    is_open = db.Column(db.Boolean, nullable=False, default=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    employee = db.relationship('Employee', uselist=False, back_populates='vacancy')


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    is_director = db.Column(db.Boolean, default=False)
    is_fired = db.Column(db.Boolean, default=False)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    vacancy = db.relationship('Vacancy', back_populates='employee')
