

import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

class TaskHandler:
    def __init__(self):
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build('calendar', 'v3', credentials=creds)

    def handle_task(self, intent, entities):
        if intent == 'schedule':
            return self.schedule_task(entities.get('task'), entities.get('date'), entities.get('time'))
        elif intent == 'reminder':
            return self.set_reminder(entities.get('reminder'), entities.get('date'), entities.get('time'))
        elif intent == 'information':
            return self.retrieve_information(entities.get('query'))

    def schedule_task(self, task, date, time):
        try:
            # Parse date and time
            start_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            end_time = start_time + timedelta(hours=1)  # Assume 1-hour duration

            event = {
                'summary': task,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Your_Timezone',  # e.g., 'America/New_York'
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Your_Timezone',  # e.g., 'America/New_York'
                },
            }

            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return f"Task '{task}' scheduled for {date} at {time}"
        except Exception as e:
            return f"An error occurred while scheduling the task: {str(e)}"

    def set_reminder(self, reminder, date, time):
        try:
            # Parse date and time
            reminder_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

            event = {
                'summary': f"Reminder: {reminder}",
                'start': {
                    'dateTime': reminder_time.isoformat(),
                    'timeZone': 'Your_Timezone',  # e.g., 'America/New_York'
                },
                'end': {
                    'dateTime': (reminder_time + timedelta(minutes=15)).isoformat(),
                    'timeZone': 'Your_Timezone',  # e.g., 'America/New_York'
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return f"Reminder set: '{reminder}' for {date} at {time}"
        except Exception as e:
            return f"An error occurred while setting the reminder: {str(e)}"

    def retrieve_information(self, query):
        try:
            # Get the upcoming 10 events
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                       maxResults=10, singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                return 'No upcoming events found.'
            
            event_list = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                event_list.append(f"{start}: {event['summary']}")
            
            return "Upcoming events:\n" + "\n".join(event_list)
        except Exception as e:
            return f"An error occurred while retrieving information: {str(e)}"