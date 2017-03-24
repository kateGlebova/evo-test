from flask import redirect, render_template, url_for

from app import app, db
from app.forms import DepartmentForm
from app.models import Department


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

@app.route('/<department_id>', methods=['GET', 'POST', 'PUT'])
def department(department_id):
    return render_template('department.html')


