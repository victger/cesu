from flask_sqlalchemy import SQLAlchemy

# Initialisation de SQLAlchemy
db = SQLAlchemy()

class Cours(db.Model):
    """Modèle pour représenter un cours."""
    id = db.Column(db.Integer, primary_key=True)
    prenom_eleve = db.Column(db.String(100), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    duree = db.Column(db.Float, nullable=False)
    prix = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Cours {self.prenom_eleve} - {self.date_debut}>"

class Eleve(db.Model):
    """Modèle pour représenter un élève."""
    id = db.Column(db.Integer, primary_key=True)
    prenom_eleve = db.Column(db.String(100), nullable=False)
    prenom_responsable = db.Column(db.String(100), nullable=False)
    nom_responsable = db.Column(db.String(100), nullable=False)
    civilite = db.Column(db.String(10), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    ville_naissance = db.Column(db.String(100), nullable=False)
    departement_naissance = db.Column(db.String(100), nullable=False)
    pays_naissance = db.Column(db.String(100), nullable=False)
    numero_securite_sociale = db.Column(db.String(15), nullable=False)
    numero_rue = db.Column(db.String(10), nullable=False)
    lettre_rue = db.Column(db.String(1), nullable=True) # Champ facultatif sur CESU
    type_voie = db.Column(db.String(50), nullable=False)
    libelle_voie = db.Column(db.String(200), nullable=True) # Champ facultatif sur CESU
    complement_adresse = db.Column(db.String(200), nullable=True) # Champ facultatif sur CESU
    lieu_dit = db.Column(db.String(200), nullable=True) # Champ facultatif sur CESU
    code_postal = db.Column(db.String(10), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Eleve {self.prenom_eleve} - {self.nom_responsable}>"

class Emploi(db.Model):
    """Modèle pour représenter l'emploi de l'élève."""
    id = db.Column(db.Integer, primary_key=True)
    prenom_eleve = db.Column(db.String(100), nullable=False)
    activite = db.Column(db.String(100), nullable=False)
    conges_payes = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Emploi {self.prenom_eleve} - {self.activite}>"