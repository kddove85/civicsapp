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


def get_candidates():
    response = requests.get(f"{base_url}{candidates}")
    soup = BeautifulSoup(response.text, 'html.parser')
    candidates_info = get_candidate_info(soup)

    rcp_response = requests.get(rcp)
    rcp_soup = BeautifulSoup(rcp_response.text, 'html.parser')
    candidates_polls = get_poll(rcp_soup)

    return combine(candidates_info, candidates_polls)


def get_candidate_info(soup):
    candidates_list = []
    tables = soup.find_all('table', attrs={'align': 'center', 'style': '"margin-top:.2em;'})
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            imgs = row.find_all('img')
            links = row.find_all('a')
            for x in range(0, len(links)):
                candidates_list.append({'name': links[x].text,
                                        'link': f"{base_url}{links[x].attrs['href']}",
                                        'img': imgs[x].attrs['src']})
    return candidates_list


def get_poll(soup):
    poll_list = []
    tables = soup.find_all('table')
    table = tables[1]
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            divs = cell.find_all('div')
            name = divs[1].text.split(' ')
            poll_list.append({'name': name[0], 'score': divs[0].text})
    return poll_list


def combine(candidates_list, polls):
    for candidate in candidates_list:
        for poll in polls:
            if candidate['name'].split(' ')[-1] == poll['name']:
                candidate['score'] = poll['score']
    candidates_list = sorted(candidates_list, key=lambda i: float(i['score']), reverse=True)
    return candidates_list


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
                    if 'https://ballotpedia.org/' in attrs['href'] and '(Incumbent)' not in li.text:
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
                    if 'https://ballotpedia.org/' in attrs['href'] and '(Incumbent)' not in li.text:
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

