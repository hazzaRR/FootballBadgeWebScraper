from bs4 import BeautifulSoup
import requests
import os
import re


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
        teams.append((team_details[0].a['href'].replace("https://en.m.wikipedia.org", ""), team_details[0].text.strip().replace(" AFC", "").replace(" A.F.C.", "").replace(" F.C.", ""), team_details[1].text.strip()))
        
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

    #creates png file named as club name and write image content to it
    with open(f'{filename}.png', 'wb') as handler: 
        handler.write(img_data) 


if __name__ == "__main__":
    CURRENT_PATH = os.getcwd()

    teams = get_all_english_football_teams()

    for team in teams:
        img_url = get_club_badge_src(team[0])
        league_name = re.sub(r'\(\d+\)', '', team[2])
        # path_to_save = os.path.join(CURRENT_PATH, "Badges", league_name.strip())
        path_to_save = os.path.join(CURRENT_PATH, "Badges")

        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        team_name = team[1]
        save_image_from_url(f"{path_to_save}\{team_name}", img_url)

    # img_url = get_club_badge_src("/wiki/Leyton_Orient_F.C.")
    # path_to_save = os.path.join(CURRENT_PATH, "Badges", "EFL League One")
    # save_image_from_url(f"{path_to_save}\Leyton Orient", img_url)


