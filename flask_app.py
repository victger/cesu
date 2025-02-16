from flask import Flask, render_template
from flask import jsonify, request
from google_calendar import authenticate_google_calendar, get_events_by_keyword
from models import db, Student
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Base de données dans le dossier 'instance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():

    service = authenticate_google_calendar()
    event_names = get_events_by_keyword(service, 'Cours')
    
    return render_template('index.html', events=event_names)

@app.route('/students', methods=['GET'])
def get_students():

    students = Student.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'email': s.email, 'phone': s.phone, 'address': s.address} for s in students])

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    student = Student(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({'id': student.id, 'message': 'Élève ajouté avec succès !'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.phone = data.get('phone', student.phone)
    student.address = data.get('address', student.address)
    db.session.commit()
    return jsonify({'message': 'Élève modifié avec succès !'})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Élève supprimé avec succès !'})

if __name__ == '__main__':

    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True)