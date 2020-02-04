from bs4 import BeautifulSoup
import os
import datetime
import requests
import states
import constants


class Election:
    def __init__(self, name, date, level, level_value):
        self.name = name
        self.date = date
        self.level = level
        self.level_value = level_value


def get_google_elections():
    elections_list = []
    response = requests.get(constants.google_elections_url,
                            params={'key': os.getenv('GOOGLE_API_KEY')})
    civics_dict = response.json()
    if civics_dict['elections']:
        for election in civics_dict['elections']:
            if election['ocdDivisionId']:
                levels = election['ocdDivisionId'].split('/')
                level = levels[-1].split(':')
                election['level'] = level[0].upper()
                election['level_value'] = level[1].upper()
                new_election = Election(election['name'], election['electionDay'], level[0].upper(), level[1].upper())
                elections_list.append(new_election)
        elections_list = sorted(elections_list, key=lambda i: i.date)
    else:
        elections_list = None
    return elections_list


def get_gp_elections():
    elections_list = []
    response = requests.get(f"{constants.gp_url_g20}{constants.gp_elections_endpoint}")
    soup = BeautifulSoup(response.text, 'html.parser')
    for dd in soup.find_all('table')[0].find_all('dl')[0].find_all('dd'):
        state = dd.fetchPrevious('dt')[0].text
        for child in dd.find_all('i'):
            try:
                text = child.text.replace('.', '')
                text = text.split(' ')
                day = int(text[1])
                month = text[2]
                year = int(text[3])
                election_date = datetime.datetime.strptime(f'{day} {month}, {year}', '%d %B, %Y')
                date_string = election_date.strftime('%Y-%m-%d')
                election_name = ' '.join([str(text[i]) for i in range(4, len(text))])
                election_name = f"{state} {election_name}"
                level_value = states.return_alpha(state)
                if level_value is None:
                    level_value = state
                new_election = Election(election_name, date_string, 'STATE', level_value)
                elections_list.append(new_election)
            except ValueError:
                continue
    elections_list = sorted(elections_list, key=lambda i: i.date)
    return elections_list


def get_elections():
    elections_list = []
    google_elections = get_google_elections()
    gp_elections = get_gp_elections()
    for election in gp_elections:
        elections_list.append(election)
    initial_list = elections_list
    is_election_new = True
    for election in google_elections:
        for initial_election in initial_list:
            if election.date == initial_election.date and election.level_value == initial_election.level_value:
                is_election_new = False
                break
        if is_election_new:
            elections_list.append(election)
        is_election_new = True
    elections_list = sorted(elections_list, key=lambda i: i.date)
    return elections_list
