import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.env import nc_cal_id
from src.representation import Event

SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_google(ev: Event) -> None:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    service.events().insert(calendarId=nc_cal_id, body=ev.as_google_dict()).execute()


create_google(Event('Meeting', '', datetime.datetime(2023, 2, 27, 13, 37), datetime.datetime(2023, 2, 27, 15, 00), []))
