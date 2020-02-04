import requests
import os
import utilities
import datetime
import constants


class USRep:
    def __init__(self, name, last_name, party, color, state, next_election, news_link, district=None):
        self.name = name
        self.last_name = last_name
        self.party = party
        self.color = color
        self.state = state
        self.next_election = next_election
        self.district = district
        self.news_link = news_link


def get_us_members():
    info_dictionary = {'senate_members_list': [],
                       'senate_democrats': 0,
                       'senate_republicans': 0,
                       'senate_independents': 0,
                       'house_members_list': [],
                       'house_democrats': 0,
                       'house_republicans': 0,
                       'house_independents': 0}

    response_object = {}
    senate_response = requests.get(
        f"{constants.propublica_url}{os.getenv('CONGRESS')}{constants.senate_endpoint}",
        headers={'X-API-Key': os.getenv('PROPUBLICA_API_KEY')}).json()
    house_response = requests.get(
        f"{constants.propublica_url}{os.getenv('CONGRESS')}{constants.house_endpoint}",
        headers={'X-API-Key': os.getenv('PROPUBLICA_API_KEY')}).json()

    for item in senate_response['results'][0]['members']:
        if item['in_office']:
            info_dictionary = add_member('upper', item, info_dictionary)
    for item in house_response['results'][0]['members']:
        if item['in_office']:
            info_dictionary = add_member('lower', item, info_dictionary)

    response_object['senators'] = sorted(info_dictionary['senate_members_list'],
                                         key=lambda i: (i.state, i.last_name))
    response_object['congressmen'] = sorted(info_dictionary['house_members_list'],
                                            key=lambda i: (i.state, int(i.district), i.last_name))

    for congressman in response_object['congressmen']:
        if congressman.district == 0:
            congressman.district = 'At-Large'

    response_object['senate_dems'] = info_dictionary['senate_democrats']
    response_object['senate_reps'] = info_dictionary['senate_republicans']
    response_object['senate_inds'] = info_dictionary['senate_independents']

    response_object['house_dems'] = info_dictionary['house_democrats']
    response_object['house_reps'] = info_dictionary['house_republicans']
    response_object['house_inds'] = info_dictionary['house_independents']

    response_object['current_year'] = str(datetime.datetime.now().year)

    return response_object


def add_member(chamber, item, info_dictionary):
    item['full_name'] = f"{item['first_name']} {item['last_name']}"
    if chamber == 'upper':
        if item['party'].upper() == 'D':
            item['party'] = 'Democrat'
            item['color'] = 'bg-info'
            info_dictionary['senate_democrats'] += 1
        if item['party'].upper() == 'R':
            item['party'] = 'Republican'
            item['color'] = 'bg-danger'
            info_dictionary['senate_republicans'] += 1
        if item['party'].upper() == 'ID':
            item['party'] = 'Independent'
            item['color'] = 'bg-secondary'
            info_dictionary['senate_independents'] += 1
        info_dictionary['senate_members_list'].append(
            USRep(item['full_name'], item['last_name'], item['party'], item['color'], item['state'],
                  item['next_election'], utilities.get_search_string(item)))

    if chamber == 'lower':
        if item['district'].lower() == 'at-large':
            item['district'] = 0
        if item['party'].upper() == 'D':
            item['party'] = 'Democrat'
            item['color'] = 'bg-info'
            info_dictionary['house_democrats'] += 1
        if item['party'].upper() == 'R':
            item['party'] = 'Republican'
            item['color'] = 'bg-danger'
            info_dictionary['house_republicans'] += 1
        if item['party'].upper() == 'I':
            item['party'] = 'Independent'
            item['color'] = 'bg-secondary'
            info_dictionary['house_independents'] += 1
        info_dictionary['house_members_list'].append(
            USRep(item['full_name'], item['last_name'], item['party'], item['color'], item['state'],
                  item['next_election'], utilities.get_search_string(item), district=item['district']))

    return info_dictionary
