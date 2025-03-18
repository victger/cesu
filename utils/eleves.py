from models import Eleve

def get_unique_eleves(cours_data):
    # Utilisation de cours.prenom_eleve pour accéder aux attributs
    unique_eleves = list(set(cours.prenom_eleve for cours in cours_data))

    return unique_eleves

def export_eleves_to_db(cours_data):
    unique_eleves = get_unique_eleves(cours_data)

    eleves_list = []

    for eleve_prenom in unique_eleves:
        eleve = Eleve(
            prenom_eleve=eleve_prenom,
            prenom_responsable=None,
            nom_responsable=None,
            civilite=None,
            date_naissance=None,
            ville_naissance=None,
            departement_naissance=None,
            pays_naissance=None,
            numero_securite_sociale=None,
            numero_rue=None,
            lettre_rue=None,
            type_voie=None,
            libelle_voie=None,
            complement_adresse=None,
            lieu_dit=None,
            code_postal=None,
            ville=None,
            telephone=None,
            prix= None
        )
        eleves_list.append(eleve)

    return eleves_list
