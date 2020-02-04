from bs4 import BeautifulSoup
import requests
import states
import datetime
import inflect

p = inflect.engine()
current_year = str(datetime.datetime.now().year)
base_url = 'https://ballotpedia.org'
candidates = f'/Democratic_presidential_nomination,_{current_year}'
rcp = f'https://www.realclearpolitics.com/epolls/2020/president/us/{current_year}_democratic_presidential_nomination-6730.html'
apostrophe = '%27'


def get_senate_opponents(state):
    opponents = []
    state_name = states.return_name(state)
    state_name = state_name.replace(' ', '_')
    response = requests.get(f"{base_url}/United_States_Senate_election_in_{state_name},_{current_year}")
    if response.status_code != 200:
        response = requests.get(f"{base_url}/United_States_Senate_special_election_in_{state_name},_{current_year}")
    soup = BeautifulSoup(response.text, 'html.parser')
    unordered_lists = soup.find_all('ul')
    for ul in unordered_lists:
        try:
            list_items = ul.find_all('li')
            for li in list_items:
                links = li.find_all('a')
                for link in links:
                    attrs = link.attrs
                    if base_url in attrs['href'] and '(Incumbent)' not in li.text:
                        party = 'Independent'
                        color = 'bg-default'
                        if 'democrat' in ul.fetchPrevious('span')[0].text.lower():
                            party = 'Democratic'
                            color = 'bg-info'
                        if 'republican' in ul.fetchPrevious('span')[0].text.lower():
                            party = 'Republican'
                            color = 'bg-danger'
                        opponents.append({'name': link.text, 'party': party, 'color': color, 'link': attrs['href']})
        except (AttributeError, KeyError):
            continue
    return opponents


def get_congressional_opponents(state, district):
    opponents = []
    state_name = states.return_name(state)
    if district != 'At-Large':
        district_name = p.ordinal(district)
    else:
        district_name = district
    state_name = state_name.replace(' ', '_')
    url = f"{base_url}/{state_name}{apostrophe}s_{district_name}_Congressional_District_election,_{current_year}"
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
                    if base_url in attrs['href'] and '(Incumbent)' not in li.text:
                        party = 'Independent'
                        color = 'bg-default'
                        if 'democrat' in ul.fetchPrevious('span')[0].text.lower() or '(D)' in li.text:
                            party = 'Democratic'
                            color = 'bg-info'
                        if 'republican' in ul.fetchPrevious('span')[0].text.lower() or '(R)' in li.text:
                            party = 'Republican'
                            color = 'bg-danger'
                        opponents.append({'name': link.text, 'party': party, 'color': color, 'link': attrs['href']})
        except (AttributeError, KeyError):
            continue
    return opponents

