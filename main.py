from bs4 import BeautifulSoup
import requests


DATE_FORMAT_STRING = "%d %b %Y"

def get_all_english_football_teams():
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Cache-Control': 'no-cache'
    }
    url = f"https://simple.wikipedia.org/wiki/List_of_English_football_teams"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')


    """
    finds table on wiki page containing all the english league football teams and removes first row which
    contains the headers for the table
    """
    teamTable = soup.find('table', class_="wikitable sortable").tbody.find_all('tr')
    teamTable = teamTable[1:]

    

    for team in teamTable:
        team_details = team.find_all('td')
        print(team_details[0].a['href'])
        print(team_details[0].text)
        print("*************")

    # seasons = match_content.find('ul', class_="linkList").find_all('li')




if __name__ == "__main__":
    get_all_english_football_teams()