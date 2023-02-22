from flask import Flask, jsonify

from models import db, Employee

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([e.serialize() for e in employees])


@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return jsonify(employee.serialize())


if __name__ == '__main__':
    app.run()
