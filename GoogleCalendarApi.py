from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# https://developers.google.com/calendar/overview

class GoogleCalendar:
    def __init__(self):
        # https://developers.google.com/calendar/auth
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']

        self.creds = None
        self.calendarId = None
        self.service = None

    def set_calendarid(self, calendarId):
        # https://docs.simplecalendar.io/find-google-calendar-id/
        self.calendarId = calendarId

    def _have_calendarid(self):
        return self.calendarId is not None

    def login(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)
        print("login success")

    def events_list(self):
        if self._have_calendarid:
            return self.service.events().list(calendarId=self.calendarId).execute().get('items', [])
        else:
            print("pls use .set_calendarid() setting Calendar ID")

    def delete(self, eventId):
        self.service.events().delete(calendarId=self.calendarId, eventId=eventId).execute()
        print(f"delete {eventId} event")

    def delete_all(self):
        events_data = self.events_list()
        for i in events_data:
            self.service.events().delete(calendarId=self.calendarId, eventId=i["id"]).execute()
        print(f"delete all events")

    def insert(self, event):
        if self._have_calendarid:
            self.service.events().insert(calendarId=self.calendarId, body=event).execute()
        else:
            print("pls use .set_calendarid() setting Calendar ID")

    def calendar_list(self):
        calendar_list_data = self.service.calendarList().list().execute()
        return calendar_list_data.get("items", [])

    def i_want_try_some_thing(self):
        return self.service
