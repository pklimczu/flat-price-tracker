import base64, os.path, pickle, re
from googleapiclient.discovery import build
from offer import Offer


class MailParser:
    """
    Reads emails and parses its content
    """

    def __init__(self):
        self.service = None
        self.offers = []


    def build_service(self):
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

            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as error:
            print(error)


    def parse_all_messages(self):
        """
        Parse all messages from given mailbox
        """
        response = self.service.users().messages().list(userId='me').execute()
        message_ids = []
        if 'messages' in response:
            message_ids.extend(response['messages'])

        self.__parse_messages(message_ids)
        

    def parse_new_messages(self, start_id):
        """
        Parse messages that are newer than the one with provided start_id
        """
        response = self.service.users().history().list(userId='me', startHistoryId=start_id).execute()
        message_ids = []
        if 'history' in response:
            for history_entry in response['history']:
                if 'messagesAdded' in history_entry:
                    message_ids.extend(history_entry['messages'])

        if message_ids:
            self.__parse_messages(message_ids)


    def __parse_messages(self, message_ids):
        """
        Go message_id by message_id, check if 'otodom' and if so - parse single message
        """
        for message_id in message_ids:
            result = self.service.users().messages().get(userId='me', id=message_id['id']).execute()
            if 'otodom' in result['snippet']:
                self.__parse_message(result)


    def __parse_message(self, message):
        """
        Go through each message structure and attempts to parse message
        """
        isParsed = False

        if 'payload' in message:
            if 'parts' in message['payload']:
                for msg_part in message['payload']['parts']:
                    (isParsed, offer) = self.__extract_data(base64.urlsafe_b64decode(msg_part['body']['data']).decode("utf-8"))
                    if isParsed:
                        offer.setHistoryId(message["historyId"])
                        self.offers.append(offer)
                        # offer.show()
                        break
                    else:
                        # TODO add some debug messages
                        print("[ERROR] Message was not parsed")


    def __extract_data(self, data):
        """
        Parses mail content
        """
        is_all_parsed = True
        new_offer = Offer()
        url_pattern = r"https:\/\/www.otodom.pl\/oferta.+.html"
        url_match = re.search(url_pattern, data)
        if url_match:
            new_offer.setUrl(url_match.group())

        region_pattern = r"Warszawa, (.+) -"
        region_match = re.search(region_pattern, data)
        if region_match:
            new_offer.setRegion(region_match.group(1))

        price_pattern = r"\n([\d][\d\s]+) zł"
        price_match = re.search(price_pattern, data)
        if price_match:
            new_offer.setPrice(price_match.group(1))

        info_pattern = r"\n([\d][\s]pok.*)"
        info_match = re.search(info_pattern, data)
        if info_match:
            new_offer.setInfo(info_match.group(1))

        is_all_parsed = url_match and region_match and price_match and info_match
        return (is_all_parsed, new_offer)


if __name__ == "__main__":
    mailParser = MailParser()
    mailParser.build_service()
    # mailParser.parse_all_messages()
    mailParser.parse_new_messages(54831)
