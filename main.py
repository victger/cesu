import datetime
import pandas as pd
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Si vous modifiez ces SCOPES, supprimez le fichier token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Récupère tous les événements du calendrier Google et met à jour ceux contenant 'Cours maths XXX'."""
    creds = None
    # Le fichier token.json stocke les tokens d'accès et de rafraîchissement de l'utilisateur, et est
    # créé automatiquement lorsque le flux d'autorisation est complété pour la première fois.
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

    service = build('calendar', 'v3', credentials=creds)

    # Récupérer tous les événements du calendrier
    print('Récupération de tous les événements du calendrier...')
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

    if not events:
        print('Aucun événement trouvé.')
    else:
        print(f"Nombre total d'événements récupérés : {len(events)}")
        for event in events:
            summary = event.get('summary', '')
            if "Cours maths" in summary:
                # Modifier le titre de l'événement
                new_summary = summary.replace("Cours maths", "Cours")
                event['summary'] = new_summary

                # Mettre à jour l'événement dans Google Calendar
                updated_event = service.events().update(
                    calendarId='primary',
                    eventId=event['id'],
                    body=event
                ).execute()

                print(f"Événement mis à jour : {updated_event['summary']} (ID: {updated_event['id']})")

if __name__ == '__main__':
    main()