import requests

from MatchData import MatchData


class TicketMaster:
    def __init__(self):
        self.match_data = []
        self.init_db()

    def init_db(self):
        api_key = "gqNMqLW7n7OteoTikxPe4sSiLhqKtccP"
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}"

        # Use requests to get json content
        response = requests.get(url)
        data = response.json()
        for event in data["_embedded"]["events"]:
            self.match_data.append(event)

    def get_match_time(self, event):
        return (event['dates']['start']['localDate'] + ":" + event['dates']['start']['localTime'])

    def get_team_info(self, event):
        return event['name']

    def get_price(self, event):
        if 'priceRanges' in event:
            # print(event['priceRanges'])
            return str(event['priceRanges'])

    def match_date(self, query_time):
        ms = []
        for event in self.match_data:

            price = self.get_price(event)
            match_date = self.get_match_time(event)
            team = self.get_team_info(event)
            print(match_date, team, price)

            if match_date >= query_time:
                ms.append(MatchData("TicketMaster", match_date, team, price, query_time, event['url']))

        return ms


if __name__ == '__main__':
    sd = TicketMaster()
    sd.match_date("123")
