from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.env import nc_cal_id
from src.representation import Event

SCOPES = ['https://www.googleapis.com/auth/calendar']


def delete_event_nc(event: Event):
    event.raw.delete()


def delete_event_go(event: Event):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    service.events().delete(calendarId=nc_cal_id, eventId=event.raw['id']).execute()
