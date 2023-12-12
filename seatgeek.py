import requests

from MatchData import MatchData

api_url = 'https://api.seatgeek.com/2/events'

api_key = 'Mzg4MjkzNTh8MTcwMjE5NDA3NC40MjcyNDI4'
client_secret = '8c02b66209e32a2376f47467bdaf6f8c9cc00dc5368f67f8076a2829cf6fd768'

params = {
    'client_id': api_key,
    'client_secret': client_secret,
    'datetime_utc.gte': '2022-04-01',
}


class SeatGeek:
    def __init__(self):
        pass

    def match_date(self, query_date):
        api_url = 'https://api.seatgeek.com/events'
        params = {
            'client_id': api_key,
            'client_secret': client_secret,
            # 'performers.slug': 'nba',
            'datetime_utc.gte': query_date,
        }

        response = requests.get(api_url, params=params)
        print(response.text)
        ms = []

        if response.status_code == 200:
            data = response.json()
            data = data['events']
            for d in data:
                ms.append(MatchData("SeatGeek", d['datetime_utc'], d['type'], d['stats']['average_price'], query_date, d['url']))
        return ms


if __name__ == '__main__':
    seatGeek = SeatGeek()
    seatGeek.match_date("2023-12-10")
