from flask import Flask, render_template
from flask import jsonify, request
from google_calendar import authenticate_google_calendar, get_events_by_keyword
from models import db, Cours, Eleve, Emploi
import os

app = Flask(__name__)

# Configurer la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Base de données SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Page d'accueil
@app.route('/')
def index():
    service = authenticate_google_calendar()
    event_names = get_events_by_keyword(service, 'Cours')
    return render_template('index.html', events=event_names)

# Routes pour les cours (Cours)
@app.route('/cours', methods=['GET'])
def get_cours():
    cours = Cours.query.all()
    return jsonify([{
        'id': c.id,
        'prenom_eleve': c.prenom_eleve,
        'date_debut': c.date_debut.isoformat(),
        'date_fin': c.date_fin.isoformat(),
        'duree': c.duree,
        'prix': c.prix
    } for c in cours])

@app.route('/cours', methods=['POST'])
def add_cours():
    data = request.json
    cours = Cours(
        prenom_eleve=data['prenom_eleve'],
        date_debut=data['date_debut'],
        date_fin=data['date_fin'],
        duree=data['duree'],
        prix=data.get('prix')
    )
    db.session.add(cours)
    db.session.commit()
    return jsonify({'id': cours.id, 'message': 'Cours ajouté avec succès !'}), 201

# Routes pour les élèves (Eleve)
@app.route('/eleves', methods=['GET'])
def get_eleves():
    eleves = Eleve.query.all()
    return jsonify([{
        'id': e.id,
        'prenom_eleve': e.prenom_eleve,
        'prenom_responsable': e.prenom_responsable,
        'nom_responsable': e.nom_responsable,
        'civilite': e.civilite,
        'date_naissance': e.date_naissance.isoformat(),
        'ville_naissance': e.ville_naissance,
        'departement_naissance': e.departement_naissance,
        'pays_naissance': e.pays_naissance,
        'numero_securite_sociale': e.numero_securite_sociale,
        'numero_rue': e.numero_rue,
        'lettre_rue': e.lettre_rue,
        'type_voie': e.type_voie,
        'libelle_voie': e.libelle_voie,
        'complement_adresse': e.complement_adresse,
        'lieu_dit': e.lieu_dit,
        'code_postal': e.code_postal,
        'ville': e.ville,
        'telephone': e.telephone
    } for e in eleves])

@app.route('/eleves', methods=['POST'])
def add_eleve():
    data = request.json
    eleve = Eleve(
        prenom_eleve=data['prenom_eleve'],
        prenom_responsable=data['prenom_responsable'],
        nom_responsable=data['nom_responsable'],
        civilite=data['civilite'],
        date_naissance=data['date_naissance'],
        ville_naissance=data['ville_naissance'],
        departement_naissance=data['departement_naissance'],
        pays_naissance=data['pays_naissance'],
        numero_securite_sociale=data['numero_securite_sociale'],
        numero_rue=data.get('numero_rue'),
        lettre_rue=data.get('lettre_rue'),
        type_voie=data.get('type_voie'),
        libelle_voie=data.get('libelle_voie'),
        complement_adresse=data.get('complement_adresse'),
        lieu_dit=data.get('lieu_dit'),
        code_postal=data['code_postal'],
        ville=data['ville'],
        telephone=data['telephone']
    )
    db.session.add(eleve)
    db.session.commit()
    return jsonify({'id': eleve.id, 'message': 'Élève ajouté avec succès !'}), 201

# Routes pour l'emploi (Emploi)
@app.route('/emploi', methods=['GET'])
def get_emplois():
    emplois = Emploi.query.all()
    return jsonify([{
        'id': e.id,
        'prenom_eleve': e.prenom_eleve,
        'activite': e.activite,
        'conges_payes': e.conges_payes
    } for e in emplois])

@app.route('/emploi', methods=['POST'])
def add_emploi():
    data = request.json
    emploi = Emploi(
        prenom_eleve=data['prenom_eleve'],
        activite=data['activite'],
        conges_payes=data['conges_payes']
    )
    db.session.add(emploi)
    db.session.commit()
    return jsonify({'id': emploi.id, 'message': 'Emploi ajouté avec succès !'}), 201

@app.route('/clear', methods=['DELETE', 'GET'])
def clear_database():
    try:
        # Supprimer toutes les données dans les tables
        for table in db.metadata.tables.values():
            db.session.execute(table.delete())

        # Commiter les changements
        db.session.commit()

        return jsonify({'message': 'La base de données a été nettoyée avec succès !'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True)