import datetime
from models import Cours

def export_cours_to_db(events):
    cours_list = []

    for event in events:
        event_name = event['summary']
        prenom = event_name.split("Cours ")[1].split(" ")[0]
        date_debut_str = event['start'].get('dateTime', event['start'].get('date'))
        date_fin_str = event['end'].get('dateTime', event['end'].get('date'))

        date_debut = datetime.datetime.strptime(date_debut_str, '%Y-%m-%dT%H:%M:%S%z').date()
        date_fin = datetime.datetime.strptime(date_fin_str, '%Y-%m-%dT%H:%M:%S%z').date()

        duree = (datetime.datetime.strptime(date_fin_str, '%Y-%m-%dT%H:%M:%S%z') - 
                 datetime.datetime.strptime(date_debut_str, '%Y-%m-%dT%H:%M:%S%z')).total_seconds() / 3600

        cours = Cours(
                prenom_eleve=prenom,
                date_debut=date_debut,
                date_fin=date_fin,
                duree=duree
        )
        cours_list.append(cours)

    return cours_list