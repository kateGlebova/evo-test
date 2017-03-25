from datetime import datetime
from flask import redirect, render_template, url_for
from flask import request

from app import app, db
from app.forms import DepartmentForm, VacancyForm, PositionForm, EmployeeForm
from app.models import Department, Vacancy, Position, Employee


@app.route('/', methods=['GET', 'POST'])
def departments():
    departments = Department.query.all()
    form = DepartmentForm()

    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)
        db.session.add(department)
        db.session.commit()
        return redirect(url_for('departments'))

    return render_template('departments.html', departments=departments, form=form)


@app.route('/<department_id>', methods=['GET', 'POST'])
def department(department_id):
    department = Department.query.filter_by(id=department_id).first()
    if department:
        vacancy_form = VacancyForm()
        department_form = DepartmentForm(obj=department)

        if department_form.validate_on_submit():
            department_form.populate_obj(department)
            db.session.commit()
            return redirect(url_for('department', department_id=department.id))

        vacancies = Vacancy.query.filter_by(department_id=department_id, is_open=True).all()
        employees = Employee.query.filter_by(department_id=department_id, is_fired=False).all()
        return render_template(
            'department.html',
            department=Department.query.filter_by(id=department_id).first(),
            vacancy_form=vacancy_form,
            department_form=department_form,
            vacancies=vacancies,
            employees=employees
        )


@app.route('/<department_id>/vacancies', methods=['POST'])
def vacancies(department_id):
    department = Department.query.filter_by(id=department_id).first()
    if department:
        form = VacancyForm(request.form)

        if form.validate_on_submit():
            vacancy = Vacancy(
                position_id=form.position.data,
                department_id=department_id,
                publishment_date=form.publishment_date.data
            )
            db.session.add(vacancy)
            db.session.commit()
        return redirect(url_for('department', department_id=department_id))
    return redirect(url_for('departments'))


@app.route('/<department_id>/vacancies/<vacancy_id>', methods=['GET', 'POST'])
def vacancy(department_id, vacancy_id):
    vacancy = Vacancy.query.filter_by(id=vacancy_id, department_id=department_id).first()
    if vacancy:
        vacancy_form = VacancyForm(obj=vacancy)
        employee_form = EmployeeForm(department=department_id, position=vacancy.position_id)

        if vacancy_form.validate_on_submit():
            vacancy_form.populate_obj(vacancy)
            db.session.commit()
            return redirect(url_for('vacancy', department_id=department_id, vacancy_id=vacancy_id))

        return render_template(
            'vacancy.html',
            vacancy=vacancy,
            vacancy_form=vacancy_form,
            employee_form=employee_form
        )
    return redirect(url_for('department', department_id=department_id))


@app.route('/<department_id>/vacancies/<vacancy_id>/employees', methods=['POST'])
def employees(department_id, vacancy_id):
    vacancy = Vacancy.query.filter_by(id=vacancy_id).first()
    if vacancy:
        form = EmployeeForm(request.form)

        if form.validate_on_submit():
            employee = Employee(
                name=form.name.data,
                surname=form.surname.data,
                position_id=form.position.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                birth_date=form.birth_date.data,
                department_id=form.department.data,
                vacancy_id=vacancy_id
            )
            if form.director.data:
                director = Employee.query.filter_by(department_id=department_id, is_director=True)
                director.is_director = False
                employee.is_director = True
            db.session.add(employee)

            vacancy.is_open = False
            vacancy.closing_date = form.start_date.data

            db.session.commit()
        return redirect(url_for('vacancy', department_id=department_id, vacancy_id=vacancy_id))
    return redirect(url_for('department', department_id=department_id))


@app.route('/positions', methods=['GET', 'POST'])
def positions():
    positions = Position.query.all()
    form = PositionForm()

    if form.validate_on_submit():
        position = Position(name=form.name.data, description=form.description.data)
        db.session.add(position)
        db.session.commit()
        return redirect(url_for('positions'))

    return render_template('positions.html', form=form, positions=positions)


@app.route('/positions/<position_id>', methods=['GET', 'POST'])
def position(position_id):
    position = Position.query.filter_by(id=position_id).first()
    if position:
        form = PositionForm(obj=position)

        if form.validate_on_submit():
            form.populate_obj(position)
            db.session.commit()
            return redirect('position', position_id=position.id)

        return render_template('position.html', position=position, form=form)
