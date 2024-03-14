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


    teams = []
    

    for team in teamTable:
        team_details = team.find_all('td')
        # print(team_details[0].a['href'])
        # print(team_details[0].text.strip().strip())
        # print(team_details[1].text.strip())

        teams.append((team_details[0].a['href'], team_details[0].text.strip().replace(" F.C.", ""), team_details[1].text.strip()))
        # print("*************")

    # seasons = match_content.find('ul', class_="linkList").find_all('li')
        
    return teams


def get_club_badge_src(link):

    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Cache-Control': 'no-cache'
    }
    url = f"https://en.wikipedia.org{link}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    statsTable = soup.find('table', class_="infobox vcard").tbody.find_all("tr")

    badge_image_url = statsTable[0].img['src']

    return badge_image_url


def save_image_from_url(filename, img_url):

    # get the image from the url
    img_data = requests.get(f"https:{img_url}").content 

    with open(f'{filename}.png', 'wb') as handler: 
        handler.write(img_data) 


if __name__ == "__main__":
    teams = get_all_english_football_teams()
    img_url = get_club_badge_src("Derby County", "/wiki/Derby_County_F.C.")
    save_image_from_url("Derby County", img_url)
