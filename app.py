import os

from flask import Flask, jsonify, request

from models import db, Employee
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        employee = Employee(name, email)
        db.session.add(employee)
        db.session.commit()
        return jsonify(employee.serialize())
    elif request.method == 'GET':
        employees = Employee.query.all()
        return jsonify([e.serialize() for e in employees])


@app.route('/employees/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employee(id):
    if request.method == 'PUT':
        name = request.form.get('name')
        email = request.form.get('email')
        employee = Employee.query.get(id)
        employee.name = name
        employee.email = email
        db.session.commit()
        return jsonify(employee.serialize())
    elif request.method == 'DELETE':
        employee = Employee.query.get(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify(employee.serialize())
    elif request.method == 'GET':
        employee = Employee.query.get(id)
        return jsonify(employee.serialize())


if __name__ == '__main__':
    app.run()
