from flask import Flask, render_template
from google_calendar import authenticate_google_calendar, get_events_by_keyword
import os

app = Flask(__name__)

@app.route('/')
def index():

    service = authenticate_google_calendar()
    
    event_names = get_events_by_keyword(service, 'Cours')
    
    return render_template('index.html', events=event_names)

if __name__ == '__main__':

    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True)