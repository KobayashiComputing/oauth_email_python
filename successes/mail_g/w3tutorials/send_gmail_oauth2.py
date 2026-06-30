# This code is a modified version of code provided by Microsoft CoPilot
# in response to searching for "google-api-python-client users().messages().send()"

from __future__ import print_function
import base64
import os.path
import pickle
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_creds():
    sDir = os.path.dirname(os.path.abspath(__file__))
    # Token is cached in a pickle file for reuse  
    token_path = os.path.join(sDir, '../../../env/token.pickle')

    with open(token_path, 'rb') as token:  
        creds = pickle.load(token)  
    # Refresh token if expired  
    if creds.expired and creds.refresh_token:  
        creds.refresh(Request())  
    return creds

def create_message(sender, to, subject, message_text):
    """
    Create a MIMEText email message and encode it for Gmail API.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    """
    Send an email message using the Gmail API.
    """
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent! ID: {sent_message['id']}")
        return sent_message
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def main():
    # get our saved credentials from the secret 'pickle' file
    creds = get_creds()

    try:
        # Build Gmail API service
        service = build('gmail', 'v1', credentials=creds)

        # Create and send the message
        message = create_message(
            sender="me",  # 'me' means the authenticated user
            to="andy@slowlanecafe.com",
            subject="Test Email from Gmail API",
            message_text="Hello! This is a test email sent via Gmail API."
        )
        send_message(service, "me", message)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    main()