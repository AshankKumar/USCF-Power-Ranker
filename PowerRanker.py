from __future__ import print_function
import httplib2
import os

import urllib.request as urllib2
from bs4 import BeautifulSoup

from Player import Player

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_rating(idNum):
    uscf = "http://www.uschess.org/msa/thin.php?"

    page = urllib2.urlopen(uscf+idNum)

    soup = BeautifulSoup(page, 'html.parser')

    values = []

    for input in soup.findAll('input'):
        if input.has_attr('value'):
            values.append(input['value'])

    rating = str (values[5])

    if "*" in rating:
        rating = rating[0 : rating.index("*")]
        return int (rating)
    elif "/" in rating:
        rating = rating[0 : rating.index("/")]
        return int (rating)
    else:
        return 0 #return zero for players who are unrated for easy sorting

    
def sort_players(people):
    sortedPlayers = sorted(people, key = lambda people: people.rating, reverse = True)

    #change all ratings at zero back to unrated
    for i in people:
        if(i.get_rating() == "0"):
            i.set_rating("Unrated")

    return sortedPlayers

def main():

    players = []
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1Dz1PjHX8mZjbX7DsePL54-BEWStnCJwn1iSrllmXIKs'
    rangeName = 'Sheet1!A2:C'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            rate = get_rating(row[1])
            players.append(Player(row[2], rate))
            #print('%s, %s' % (row[2], rate)) 

    sortedPlayers = sort_players(players)

    print('Name, Rating:')
    for i in sortedPlayers:
        print(i)

    #write to google sheet

if __name__ == '__main__':
    main()
