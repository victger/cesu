import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from models import Cours, db
from sqlalchemy.exc import SQLAlchemyError

# Si vous modifiez ces SCOPES, supprimez le fichier token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():

    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Si aucun token valide n'est disponible, demandez à l'utilisateur de se connecter.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Enregistrez les tokens pour la prochaine exécution
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service= build('calendar', 'v3', credentials=creds)

    return service

def get_all_events(service):
    
    events = []
    page_token = None

    while True:
        events_result = service.events().list(
            calendarId='primary',
            singleEvents=True,
            orderBy='startTime',
            pageToken=page_token
        ).execute()
        events.extend(events_result.get('items', []))
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    return events

def get_events_by_keyword(service, keyword):

    filtered_events = []
    for event in get_all_events(service):
        if keyword in event['summary']:
            filtered_events.append(event)
    return filtered_events

from models import Cours
from sqlalchemy.exc import SQLAlchemyError
import datetime
import pandas as pd

def export_lessons_to_db(events):
    try:
        # Parcourir les événements
        for event in events:
            event_name = event['summary']
            prenom = event_name.split("Cours ")[1].split(" ")[0]  # Extraire le prénom de l'élève
            date_debut_str = event['start'].get('dateTime', event['start'].get('date'))
            date_fin_str = event['end'].get('dateTime', event['end'].get('date'))
            
            # Convertir les chaînes de caractères en objets datetime
            date_debut = datetime.datetime.strptime(date_debut_str, '%Y-%m-%dT%H:%M:%S%z').date()
            date_fin = datetime.datetime.strptime(date_fin_str, '%Y-%m-%dT%H:%M:%S%z').date()
            
            duree = (datetime.datetime.strptime(date_fin_str, '%Y-%m-%dT%H:%M:%S%z') - 
                     datetime.datetime.strptime(date_debut_str, '%Y-%m-%dT%H:%M:%S%z')).total_seconds() / 3600

            # Créer un objet Cours pour chaque événement
            cours = Cours(
                prenom_eleve=prenom,
                date_debut=date_debut,
                date_fin=date_fin,
                duree=duree,
                prix=None  # Tu peux définir une valeur pour le prix si nécessaire
            )
            
            # Ajouter l'événement à la session SQLAlchemy
            db.session.add(cours)

        # Sauvegarder les modifications dans la base de données
        db.session.commit()
        print("Les événements ont été ajoutés avec succès à la base de données.")

    except SQLAlchemyError as e:
        db.session.rollback()  # Annuler les modifications en cas d'erreur
        print(f"Erreur lors de l'ajout des événements à la base de données : {str(e)}")

# def export_lessons_to_csv(events, filename='data.csv'):

#     dataframe = pd.DataFrame(columns=['Prénom', 'Date de début', 'Date de fin', 'Durée'])

#     for event in events:
#         event_name = event['summary']
#         prenom = event_name.split("Cours ")[1].split(" ")[0]
#         date_debut = event['start'].get('dateTime', event['start'].get('date'))
#         date_fin = event['end'].get('dateTime', event['end'].get('date'))
#         duree = datetime.datetime.strptime(date_fin, '%Y-%m-%dT%H:%M:%S%z') - datetime.datetime.strptime(date_debut, '%Y-%m-%dT%H:%M:%S%z')
#         duree = duree.total_seconds() / 3600

#         new_row = pd.DataFrame([{
#             'Prénom': prenom,
#             'Date de début': date_debut,
#             'Date de fin': date_fin,
#             'Durée': duree,
#         }])

#         dataframe = pd.concat([dataframe, new_row], ignore_index=True)

#     dataframe.to_csv(filename, index=False)