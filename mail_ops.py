import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser


class GmailOps():
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
        self.creds = None
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(self.creds.to_json())
    
    def build_service_obj(self):
        try:
            self.service = build("gmail", "v1", credentials=self.creds)
        except HttpError as error:
            print(f"An error occurred: {error}")
        # return self.service
   
    def get_header_value(self, email):
        headers = email.get('payload', {}).get('headers', [])
        op_header = dict()
        
        for header in headers:
            if header['name'] in ('From','Subject','Date'):
                op_header[header['name']] = header['value']
                
        return op_header
    
    def get_message_body(self, email):
        parts = email.get('payload', {}).get('parts', [])
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part.get('body', {}).get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode()
        return ''
    
    def get_messages(self):
        date_format = "%a, %d %b %Y %H:%M:%S"
        
        folder = 'INBOX'
        results = self.service.users().messages().list(maxResults=10, userId='me' , labelIds=[folder] ).execute()
        messages = results.get('messages', [])
        email_list = []
        
        for message in messages:
            
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            
            header_value = self.get_header_value(msg)
            
            date_string = header_value.get('Date')
            
            datetime_obj = parser.parse(date_string)
            email_data = {
                'message_id': msg['id'],
                'from_email': header_value.get('From'),
                'subject': header_value.get('Subject'),
                'message': self.get_message_body(msg),
                'received_date': datetime_obj.strftime("%Y-%m-%d %H:%M:%S"),
                'is_read': int('UNREAD' not in msg['labelIds']),
                'is_processed': 0,
                'folder':folder
            }

            email_list.append(email_data)
        
        return email_list
    
    def mark_as_read(self, user_id, msg_id):
        try:
            message = self.service.users().messages().modify(
                userId=user_id,
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            print(f"Message ID {msg_id} marked as read.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return message
    
    def mark_as_unread(self, user_id, msg_id):
        try:
            message = self.service.users().messages().modify(
                userId=user_id,
                id=msg_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
            print(f"Message ID {msg_id} marked as read.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return message

    def move_email_to_folder(self, user_id, msg_id, label_name):
        try:
            label_id = self.find_label_id(user_id, label_name)
            if label_id:
                message = self.service.users().messages().modify(
                    userId=user_id,
                    id=msg_id,
                    body={'addLabelIds': [label_id]}
                ).execute()
                print(f"Message ID {msg_id} marked as read and moved to '{label_name}' folder.")
            else:
                print(f"Label '{label_name}' not found.")
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def find_label_id(self, user_id, label_name):
        try:
            results = self.service.users().labels().list(userId=user_id).execute()
            labels = results.get('labels', [])

            for label in labels:
                if label['name'] == label_name:
                    return label['id']
            return None
        except Exception as e:
            print(f"An error occurred while fetching labels: {e}")
            return None

class FileManager():
    def __init__(self, file_name):
        self.file_name = file_name

    def load_file(self):
        try:
            with open(self.file_name) as fp:
                try:
                    rules = json.load(fp)
                except Exception as e:
                    print('issue parsing data')
                    rules = None
        except FileNotFoundError as fnf:
            print('Unable to locate the rules file', fnf)
        except Exception as e:
            print('Error', e)

        return rules
