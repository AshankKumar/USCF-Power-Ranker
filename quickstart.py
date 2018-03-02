from __future__ import print_function
import httplib2
import os

import urllib.request as urllib2
from bs4 import BeautifulSoup

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

    uscf = "http://www.uschess.org/msa/MbrDtlMain.php?"

    page = urllib2.urlopen(uscf+idNum)

    soup = BeautifulSoup(page, 'html.parser')

    bTags = []

    for i in soup.findAll("b"):
        bTags.append(i.text)


    rating = str (bTags[2]) #change method
    rating = rating.strip()
    rating = rating.rstrip() #maybe not necesarry

    if "\n" not in rating:
        return rating
    else:
        rating = rating[0:rating.index("\n")]
        return rating
    

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
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
        print('Name, Rating:')
        for row in values:
            rate = get_rating(row[1])
            print('%s, %s' % (row[2], rate)) 

    #print(names)
    #print(ratings)      
    #make list of all the uscf ids
    #go to http://www.uschess.org/msa/MbrDtlMain.php?[USCF_ID]
    #get rating
    #store in list as a player object
    #sort list
    #write to google sheet

if __name__ == '__main__':
    main()
