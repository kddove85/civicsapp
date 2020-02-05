from bs4 import BeautifulSoup
import requests
import os
import datetime
import states
import utilities
import constants


class StateRep:
    def __init__(self, name, last_name, party, color, district, news_link):
        self.name = name
        self.last_name = last_name
        self.party = party
        self.color = color
        self.district = district
        self.news_link = news_link


def get_state_members(state):
    info_dictionary = {'senate_members_list': [],
                       'senate_democrats': 0,
                       'senate_republicans': 0,
                       'senate_independents': 0,
                       'senate_next_election': None,
                       'house_members_list': [],
                       'house_democrats': 0,
                       'house_republicans': 0,
                       'house_independents': 0,
                       'house_next_election': None}

    response = requests.get(f"{constants.ballotpedia_url}/{states.return_name(state.upper())}{constants.state_senate}")
    soup = BeautifulSoup(response.text, 'html.parser')
    infobox = soup.findAll('table', {"class": 'infobox'})[0]
    date = infobox.findAll('a')[-1].text
    date_parts = date.split(',')
    info_dictionary['senate_next_election'] = date_parts[1].strip()

    response = requests.get(f"{constants.ballotpedia_url}/{states.return_name(state.upper())}{constants.state_house}")
    soup = BeautifulSoup(response.text, 'html.parser')
    infobox = soup.findAll('table', {"class": 'infobox'})[0]
    date = infobox.findAll('a')[-1].text
    date_parts = date.split(',')
    info_dictionary['house_next_election'] = date_parts[1].strip()

    response_object = {'state': state}
    response = requests.get(f"{constants.open_states_url}{state}",
                            headers={'X-API-Key': os.getenv('OPENSTATE_API_KEY')})
    response_dict = response.json()
    for item in response_dict:
        info_dictionary = add_member(item, info_dictionary)
    try:
        response_object['senators'] = sorted(info_dictionary['senate_members_list'],
                                             key=lambda i: (int(i.district), i.last_name))
    except ValueError:
        response_object['senators'] = sorted(info_dictionary['senate_members_list'],
                                             key=lambda i: (i.district, i.last_name))

    try:
        response_object['congressmen'] = sorted(info_dictionary['house_members_list'],
                                                key=lambda i: (int(i.district), i.last_name))
    except ValueError:
        print('house value error')
        response_object['congressmen'] = sorted(info_dictionary['house_members_list'],
                                                key=lambda i: (i.district, i.last_name))

    response_object['senate_dems'] = info_dictionary['senate_democrats']
    response_object['senate_reps'] = info_dictionary['senate_republicans']
    response_object['senate_inds'] = info_dictionary['senate_independents']

    response_object['house_dems'] = info_dictionary['house_democrats']
    response_object['house_reps'] = info_dictionary['house_republicans']
    response_object['house_inds'] = info_dictionary['house_independents']

    response_object['senate_next_election'] = info_dictionary['senate_next_election']
    response_object['house_next_election'] = info_dictionary['house_next_election']

    response_object['current_year'] = str(datetime.datetime.now().year)

    return response_object


def add_member(item, info_dictionary):
    if item['chamber'] == 'upper':
        party = item['party'].split('/')
        if len(party) > 1:
            if party[0] == 'Democratic':
                item['party'] = 'Democratic'
        if item['party'] == 'Democratic':
            item['color'] = 'bg-info'
            info_dictionary['senate_democrats'] += 1
        elif item['party'] == 'Republican':
            item['color'] = 'bg-danger'
            info_dictionary['senate_republicans'] += 1
        else:
            item['color'] = 'bg-secondary'
            info_dictionary['senate_independents'] += 1

        info_dictionary['senate_members_list'].append(
            StateRep(item['full_name'], item['last_name'], item['party'], item['color'], item['district'],
                     utilities.get_search_string(item)))

    if item['chamber'] == 'lower':
        party = item['party'].split('/')
        if len(party) > 1:
            if party[0] == 'Democratic':
                item['party'] = 'Democratic'
        if item['party'] == 'Democratic':
            item['color'] = 'bg-info'
            info_dictionary['house_democrats'] += 1
        elif item['party'] == 'Republican':
            item['color'] = 'bg-danger'
            info_dictionary['house_republicans'] += 1
        else:
            item['color'] = 'bg-secondary'
            info_dictionary['house_independents'] += 1

        info_dictionary['house_members_list'].append(
            StateRep(item['full_name'], item['last_name'], item['party'], item['color'], item['district'],
                     utilities.get_search_string(item)))

    return info_dictionary
