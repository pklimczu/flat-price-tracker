"""Get a list of Messages from the user's mailbox.
"""

from __future__ import print_function
from apiclient import errors
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email

# https://developers.google.com/gmail/api/v1/reference/users/messages/get?
 

def main():

    creds = None

    print(os.getcwd())

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me').execute()
    print(len(results))

    # for result in results['messages']:
    result = results['messages'][0]
    message_id = result['id']
    message = service.users().messages().get(userId='me', id=message_id).execute()
    chunk = message['payload']['parts'][0]['body']['data']
    chunk = chunk.replace("-", "+") + "====="

    decoded = base64.urlsafe_b64decode(chunk.encode('ASCII'))
    print(email.message_from_bytes(decoded))


if __name__ == '__main__':
    main()
