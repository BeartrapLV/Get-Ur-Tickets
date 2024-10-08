import csv
import json
import datetime
import urllib.request
from encryption_functions import get_key, decrypt_file

KEY_FILE = 'key.encrypted'
CONSTANTS_FILE = 'constants.env'
TICKET_API_KEY, FLIGHT_API_KEY = decrypt_file(CONSTANTS_FILE,
                                              get_key(KEY_FILE))


def get_flight_info(origin: str, destination: str, start_date: str,
                    end_date: str):
    """
    :param origin: 3-letter origin airport code
    :param destination: 3-letter destination airport code
    :param start_date: Date of outbound flight (%mm-%dd-%YYYY)
    :param end_date: Date of inbound flight (%mm-%dd-%YYYY)
    :return: SerpAPI response in JSON format
    """
    with urllib.request.urlopen(
            'https://serpapi.com/search.json?engine=google_flights&output=' +
            'json&departure_id=' + origin + '&arrival_id=' + destination +
            '&outbound_date=' + start_date + '&return_date=' + end_date +
            '&api_key=' + FLIGHT_API_KEY) as url:
        flights = json.load(url)

    return flights


def get_total_price_from_file(origin: str = 'LAS') -> list:
    """
    :param origin: 3-letter origin airport code
    :return: A sorted list of all the total prices (flight + ticket)
    """
    test_file = 'formula-1.txt'
    result = []

    with open(test_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['Price'] = float(row['Price'])

            if row['Airport'] != origin:
                date = datetime.datetime.strptime(row['Date'],
                                                  "%m-%d-%Y")
                start_date = str(date +
                                 datetime.timedelta(days=-1)).split(' ')[0]
                end_date = str(date + datetime.timedelta(days=1)).split(' ')[0]

                flights = get_flight_info(origin, row['Airport'], start_date,
                                          end_date)
                result.append((row['Price'] +
                               flights['price_insights']['lowest_price'],
                               row['Name']))
            else:
                result.append((row['Price'], row['Name']))

    result.sort()
    return result


def get_total_price_from_api(origin: str = 'LAS',
                             keyword: str = 'formula-1') -> list:
    """
    :param origin: 3-letter origin airport code
    :param keyword: Keyword to pass as
    :return: A sorted list of all the total prices (flight + ticket)
    """
    airports = {('Miami Gardens', 'Florida'): 'MIA',
                ('Montreal', 'Quebec'): 'YUL',
                ('Las Vegas', 'Nevada'): 'LAS',
                ('Austin', 'Texas'): 'AUS',
                ('México', 'Ciudad de México'): 'MEX',
                ('Albert Park', 'Victoria'): 'MEL'
                }

    result = []

    with urllib.request.urlopen('https://app.ticketmaster.com/discovery/v2/' +
                                'events.json?apikey=' + TICKET_API_KEY +
                                '&keyword=' + keyword) as url:
        data = json.load(url)

    for event in data['_embedded']['events']:
        if 'url' in event and 'priceRanges' in event:
            name = event['name']
            url = event['url']
            ticket_price = float(event['priceRanges'][0]['min'])

            location = event['_embedded']['venues'][0]

            city = location['city']['name']
            state = location['state']['name']

            venue = (city, state)

            if airports[venue] == origin:
                result.append((ticket_price, name, venue, url))
            else:
                date = event['dates']['start']['localDate']
                date = datetime.datetime.strptime(date, "%Y-%m-%d")

                start_date = str(date +
                                 datetime.timedelta(days=-1)).split(' ')[0]
                end_date = str(date + datetime.timedelta(days=1)).split(' ')[0]

                flights = get_flight_info(origin, airports[venue], start_date,
                                          end_date)

                result.append((ticket_price +
                               flights['price_insights']['lowest_price'], name,
                               venue, url, start_date, end_date))

    result.sort()
    return result


if __name__ == "__main__":
    print(get_total_price_from_api())
