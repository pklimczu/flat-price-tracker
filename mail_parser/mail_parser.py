import base64, os.path, pickle
from googleapiclient.discovery import build

class MailParser:

    def __init__(self):
        self.service = None

    @classmethod
    def build_service(cls):
        """
        Build GMail service
        """
        try:
            creds = None
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            else:
                raise Exception("Credentials not found")

            cls.service = build('gmail', 'v1', credentials=creds)
        except Exception as error:
            print(error)

    @classmethod
    def get_all_urls(cls):
        """
        Get all URLs from given mailbox
        """
        response = cls.service.users().messages().list(userId='me').execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        for message in messages:
            result = cls.service.users().messages().get(userId='me', id=message['id']).execute()
            if 'otodom' in result['snippet']:
                cls.__parse_message(result)
        

    @classmethod
    def get_new_urls(cls, start_id):
        """
        Get URLs since given start_id
        """
        result = (cls.service.users().history().list(userId='me', startHistoryId=start_id).execute())
        return result

    @classmethod
    def __parse_message(cls, message):
        isParsed = False

        if 'payload' in message:
            if 'parts' in message['payload']:
                for msg_part in message['payload']['parts']:
                    print(base64.urlsafe_b64decode(msg_part['body']['data']))
                isParsed = True

        if not isParsed:
            # TODO add some debug messages
            print("[ERROR] Message was not parsed")


if __name__ == "__main__":
    mailParser = MailParser()
    mailParser.build_service()
    print(mailParser.get_all_urls())
