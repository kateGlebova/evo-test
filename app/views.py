from flask import redirect, render_template, url_for, abort, request

from app import app, db
from app.forms import DepartmentForm, VacancyForm, PositionForm, EmployeeForm
from app.helpers import flash_errors, update_position, update_director
from app.models import Department, Vacancy, Position, Employee, WorkHistory


@app.route('/', methods=['GET', 'POST'])
def departments():
    departments = Department.query.all()
    form = DepartmentForm()

    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)
        db.session.add(department)
        db.session.commit()
        return redirect(url_for('departments'))

    flash_errors(form)
    return render_template('departments.html', departments=departments, form=form)


@app.route('/<department_id>/', methods=['GET', 'POST'])
def department(department_id):
    department = Department.query.filter_by(id=department_id).first()
    if not department:
        abort(404)
    vacancy_form = VacancyForm()
    department_form = DepartmentForm(obj=department)

    if department_form.validate_on_submit():
        department_form.populate_obj(department)
        db.session.commit()
        return redirect(url_for('department', department_id=department.id))

    vacancies = Vacancy.query.filter_by(department_id=department_id, is_open=True).all()
    employees = Employee.query.filter_by(department_id=department_id, is_fired=False).all()
    flash_errors(department_form)
    return render_template(
        'department.html',
        department=Department.query.filter_by(id=department_id).first(),
        vacancy_form=vacancy_form,
        department_form=department_form,
        vacancies=vacancies,
        employees=employees
    )


@app.route('/<department_id>/vacancies/', methods=['POST'])
def vacancies(department_id):
    department = Department.query.filter_by(id=department_id).first()
    if not department:
        abort(404)
    form = VacancyForm(obj=request.form)

    if form.validate_on_submit():
        vacancy = Vacancy(
            position_id=form.position_id.data,
            department_id=department_id,
            publishment_date=form.publishment_date.data
        )
        db.session.add(vacancy)
        db.session.commit()

    flash_errors(form)
    return redirect(url_for('department', department_id=department_id))


@app.route('/<department_id>/vacancies/<vacancy_id>/', methods=['GET', 'POST'])
def vacancy(department_id, vacancy_id):
    vacancy = Vacancy.query.filter_by(id=vacancy_id, department_id=department_id).first()
    if not vacancy:
        abort(404)

    vacancy_form = VacancyForm(obj=vacancy)
    employee_form = EmployeeForm(department_id=department_id, position_id=vacancy.position_id)

    if vacancy_form.validate_on_submit():
        vacancy_form.populate_obj(vacancy)
        db.session.commit()
        return redirect(url_for('vacancy', department_id=department_id, vacancy_id=vacancy_id))

    flash_errors(vacancy_form)
    return render_template(
        'vacancy.html',
        vacancy=vacancy,
        vacancy_form=vacancy_form,
        employee_form=employee_form
    )


@app.route('/<department_id>/vacancies/<vacancy_id>/employees/', methods=['POST'])
def employees(department_id, vacancy_id):
    vacancy = Vacancy.query.filter_by(id=vacancy_id).first()
    if not vacancy:
        abort(404)
    form = EmployeeForm(obj=request.form)

    if form.validate_on_submit():
        employee = Employee(
            name=form.name.data,
            surname=form.surname.data,
            position_id=form.position_id.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            birth_date=form.birth_date.data,
            department_id=form.department_id.data,
            vacancy=vacancy
        )

        if form.director.data:
            update_director(department_id, employee, True)
        db.session.add(employee)

        vacancy.is_open = False
        vacancy.employee = employee
        vacancy.closing_date = form.start_date.data

        db.session.commit()

        update_position(employee, form.position_id.data, form.department_id.data, form.start_date.data)
        db.session.commit()

    flash_errors(form)
    return redirect(url_for('department', department_id=department_id))


@app.route('/<department_id>/employees/<employee_id>/', methods=['GET', 'POST'])
def employee(department_id, employee_id):
    employee = Employee.query.filter_by(id=employee_id, department_id=department_id).first()
    if not employee:
        abort(404)



    employee_form = EmployeeForm(obj=employee, start_date=employee.vacancy.closing_date)

    if employee_form.validate_on_submit():
        if employee.position_id != employee_form.position_id.data or employee.department_id != employee_form.department_id.data:
            update_position(
                employee,
                employee_form.position_id.data,
                employee_form.department_id.data,
                employee_form.start_date.data
            )

        if employee.is_director != employee_form.director.data:
            update_director(department_id, employee, employee_form.director.data)

        employee_form.populate_obj(employee)
        db.session.commit()
        return redirect(url_for('employee', department_id=employee.department_id, employee_id=employee.id))

    flash_errors(employee_form)
    return render_template('employee.html', employee=employee, employee_form=employee_form)


@app.route('/<department_id>/employees/<employee_id>/fire/')
def fire(department_id, employee_id):
    employee = Employee.query.filter_by(id=employee_id, department_id=department_id).first()
    if not employee:
        abort(404)

    employee.is_fired = True
    db.session.commit()
    return redirect(url_for('department', department_id=department_id))


@app.route('/positions/', methods=['GET', 'POST'])
def positions():
    positions = Position.query.all()
    form = PositionForm()

    if form.validate_on_submit():
        position = Position(name=form.name.data, description=form.description.data)
        db.session.add(position)
        db.session.commit()
        return redirect(url_for('positions'))

    flash_errors(form)
    return render_template('positions.html', form=form, positions=positions)


@app.route('/positions/<position_id>/', methods=['GET', 'POST'])
def position(position_id):
    position = Position.query.filter_by(id=position_id).first()
    if not position:
        abort(404)
    form = PositionForm(obj=position)

    if form.validate_on_submit():
        form.populate_obj(position)
        db.session.commit()
        return redirect(url_for('position', position_id=position.id))

    flash_errors(form)
    return render_template('position.html', position=position, form=form)
