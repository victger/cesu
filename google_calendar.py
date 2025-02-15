import datetime
import pandas as pd
import os.path
import unicodedata
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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

def export_lessons_to_csv(events, filename='data.csv'):

    dataframe = pd.DataFrame(columns=['Student', 'Start', 'End', 'Duration'])

    for event in events:
        event_name = event['summary']
        student = event_name.split("Cours ")[1].split(" ")[0]
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))
        duration = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z') - datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
        duration = duration.total_seconds() / 3600

        new_row = pd.DataFrame([{
            'Student': student,
            'Start': start_time,
            'End': end_time,
            'Duration': duration,
        }])

        dataframe = pd.concat([dataframe, new_row], ignore_index=True)

    dataframe.to_csv(filename, index=False)