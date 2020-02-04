from bs4 import BeautifulSoup
import requests
import states
import datetime
import inflect
import constants


class Opponent:
    def __init__(self, name, party, color, link):
        self.name = name
        self.party = party
        self.color = color
        self.link = link

    def compare(self, other_opponent):
        if self.name == other_opponent.name and self.party == other_opponent.party and self.color == other_opponent.color and self.link == other_opponent.link:
            return True
        return False


def get_senate_opponents(state):
    current_year = str(datetime.datetime.now().year)
    opponents = []
    state_name = states.return_name(state)
    state_name = state_name.replace(' ', '_')
    response = requests.get(
        f"{constants.ballotpedia_url}/United_States_Senate_election_in_{state_name},_{current_year}")
    if response.status_code != 200:
        response = requests.get(
            f"{constants.ballotpedia_url}/United_States_Senate_special_election_in_{state_name},_{current_year}")
    soup = BeautifulSoup(response.text, 'html.parser')
    unordered_lists = soup.find_all('ul')
    for ul in unordered_lists:
        try:
            list_items = ul.find_all('li')
            for li in list_items:
                links = li.find_all('a')
                for link in links:
                    attrs = link.attrs
                    if constants.ballotpedia_url in attrs['href'] and 'Incumbent' not in li.text:
                        party = 'Independent'
                        color = 'bg-default'
                        if 'democrat' in ul.fetchPrevious('span')[0].text.lower():
                            party = 'Democratic'
                            color = 'bg-info'
                        if 'republican' in ul.fetchPrevious('span')[0].text.lower():
                            party = 'Republican'
                            color = 'bg-danger'
                        exists = False
                        new_opponent = Opponent(link.text, party, color, attrs['href'])
                        for opponent in opponents:
                            if new_opponent.compare(opponent):
                                exists = True
                                break
                        if not exists:
                            opponents.append(Opponent(link.text, party, color, attrs['href']))
        except (AttributeError, KeyError):
            continue
    return opponents


def get_congressional_opponents(state, district):
    p = inflect.engine()
    current_year = str(datetime.datetime.now().year)
    opponents = []
    state_name = states.return_name(state)
    if district != 'At-Large':
        district_name = p.ordinal(district)
    else:
        district_name = district
    state_name = state_name.replace(' ', '_')
    url = f"{constants.ballotpedia_url}/{state_name}{constants.apostrophe}s_{district_name}_Congressional_District_election,_{current_year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    unordered_lists = soup.find_all('ul')
    for ul in unordered_lists:
        try:
            list_items = ul.find_all('li')
            for li in list_items:
                links = li.find_all('a')
                for link in links:
                    attrs = link.attrs
                    if constants.ballotpedia_url in attrs['href'] and 'Incumbent' not in li.text:
                        party = 'Independent'
                        color = 'bg-default'
                        if 'democrat' in ul.fetchPrevious('span')[0].text.lower() or '(D)' in li.text:
                            party = 'Democratic'
                            color = 'bg-info'
                        if 'republican' in ul.fetchPrevious('span')[0].text.lower() or '(R)' in li.text:
                            party = 'Republican'
                            color = 'bg-danger'
                        exists = False
                        new_opponent = Opponent(link.text, party, color, attrs['href'])
                        for opponent in opponents:
                            if new_opponent.compare(opponent):
                                exists = True
                                break
                        if not exists:
                            opponents.append(Opponent(link.text, party, color, attrs['href']))
        except (AttributeError, KeyError):
            continue
    return opponents
