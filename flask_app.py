from flask import Flask, render_template
from flask import jsonify, request
from google_calendar import authenticate_google_calendar, get_events_by_keyword
from utils.cours import export_cours_to_db
from utils.eleves import export_eleves_to_db
from models import db, Cours, Eleve, Emploi
import os

service = authenticate_google_calendar()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():

    get_cours = Cours.query.all()
    
    cours_data = [{
        'prenom_eleve': c.prenom_eleve,
        'date_debut': c.date_debut.isoformat(),
        'date_fin': c.date_fin.isoformat(),
        'duree': c.duree
    } for c in get_cours]

    return render_template('index.html', cours_data=cours_data)

@app.route('/add_cours_bulk', methods=['GET'])
# Pas prore, à modifier
def add_cours_bulk():
    try:
        cours_data_list = export_cours_to_db(get_events_by_keyword(service, 'Cours'))
        eleves_data_list = export_eleves_to_db(cours_data_list)

        db.session.bulk_save_objects(cours_data_list)
        db.session.bulk_save_objects(eleves_data_list)

        db.session.commit()

        return jsonify({'message': 'Cours ajoutés avec succès en bulk !'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['DELETE', 'GET'])
def clear_database():
    try:
        for table in db.metadata.tables.values():
            db.session.execute(table.delete())

        db.session.commit()

        return jsonify({'message': 'La base de données a été nettoyée avec succès !'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/eleves', methods=['GET'])
def get_eleves():
    eleves_data = Eleve.query.all()

    print(eleves_data)
    return render_template('eleves.html', eleves_data=eleves_data)

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True)