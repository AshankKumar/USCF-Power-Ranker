import gspread
from oauth2client.service_account import ServiceAccountCredentials

import urllib.request as urllib2
from bs4 import BeautifulSoup

from Player import Player

def get_credentials():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

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
        if(i.get_rating() == 0):
            i.set_rating("Unrated")

    return sortedPlayers

def main():
    gc = gspread.authorize(get_credentials())

    wks = gc.open("HSN Chess Club POWER RANKINGS 2017-2018").get_worksheet(0)

    list_of_lists = wks.get_all_values()

    list_of_lists.pop(0) #remove row with column names

    players = []

    for row in list_of_lists:
        rate = get_rating(row[1])
        players.append(Player(row[1], row[2], rate))

    sortedPlayers = sort_players(players)

    for i in range(2, len(sortedPlayers)+2): #+2 for the format of the spreadsheet
        num = str (i)
        cells = 'B'+num+":"+'D'+num
        #print(cells)
        cell_list = wks.range(cells)
        j = 1 #player = people.pop()
        player = sortedPlayers.pop(0) #change naming
        for cell in cell_list:
            if(j == 1):
                cell.value = player.get_idNum() #uscf id: people.get_ID()
            if(j == 2):
                cell.value = player.get_name() #name: people.get_name()
            if(j == 3):
                cell.value = player.get_rating() #rating: people.get_rating()
            j += 1
        wks.update_cells(cell_list)
        
    #print('ID, Name, Rating:')
    #for i in sortedPlayers:
        #print(i)

if __name__ == '__main__':
    main()
    
