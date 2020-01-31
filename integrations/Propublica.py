import requests
import os
import utilities
import datetime


class Propublica:
    def __init__(self):
        self.senate_members_list = []
        self.senate_democrats = 0
        self.senate_republicans = 0
        self.senate_independents = 0
        self.house_members_list = []
        self.house_democrats = 0
        self.house_republicans = 0
        self.house_independents = 0
        self.current_year = str(datetime.datetime.now().year)

    def get_us_members(self):
        response_object = {}
        senate_response = requests.get(
            f"https://api.propublica.org/congress/v1/{os.getenv('CONGRESS')}/senate/members.json",
            headers={'X-API-Key': os.getenv('PROPUBLICA_API_KEY')}).json()
        house_response = requests.get(
            f"https://api.propublica.org/congress/v1/{os.getenv('CONGRESS')}/house/members.json",
            headers={'X-API-Key': os.getenv('PROPUBLICA_API_KEY')}).json()

        for item in senate_response['results'][0]['members']:
            if item['in_office']:
                self.add_member('upper', item)
        for item in house_response['results'][0]['members']:
            if item['in_office']:
                self.add_member('lower', item)

        try:
            response_object['senators'] = sorted(self.senate_members_list, key=lambda i: (i['state'], i['last_name']))
        except ValueError:
            response_object['senators'] = sorted(self.senate_members_list,
                                                 key=lambda i: (int(i['state']), i['last_name']))

        try:
            response_object['congressmen'] = sorted(self.house_members_list,
                                                    key=lambda i: (i['state'], int(i['district']), i['last_name']))
        except ValueError:
            response_object['congressmen'] = sorted(self.house_members_list,
                                                    key=lambda i: (i['state'], i['district'], i['last_name']))

        for congressman in response_object['congressmen']:
            if congressman['district'] == 0:
                congressman['district'] = 'At-Large'

        response_object['senate_dems'] = self.senate_democrats
        response_object['senate_reps'] = self.senate_republicans
        response_object['senate_inds'] = self.senate_independents

        response_object['house_dems'] = self.house_democrats
        response_object['house_reps'] = self.house_republicans
        response_object['house_inds'] = self.house_independents

        response_object['current_year'] = self.current_year

        return response_object

    def add_member(self, chamber, item):
        item['full_name'] = f"{item['first_name']} {item['last_name']}"
        if chamber == 'upper':
            if item['party'].upper() == 'D':
                item['party'] = 'Democrat'
                item['color'] = 'bg-info'
                self.senate_democrats += 1
            if item['party'].upper() == 'R':
                item['party'] = 'Republican'
                item['color'] = 'bg-danger'
                self.senate_republicans += 1
            if item['party'].upper() == 'ID':
                item['party'] = 'Independent'
                item['color'] = 'bg-secondary'
                self.senate_independents += 1
            self.senate_members_list.append({'name': item['full_name'],
                                             'last_name': item['last_name'],
                                             'party': item['party'],
                                             'color': item['color'],
                                             'state': item['state'],
                                             'next_election': item['next_election'],
                                             'search_string': utilities.get_search_string(item)
                                             })
        if chamber == 'lower':
            if item['district'].lower() == 'at-large':
                item['district'] = 0
            if item['party'].upper() == 'D':
                item['party'] = 'Democrat'
                item['color'] = 'bg-info'
                self.house_democrats += 1
            if item['party'].upper() == 'R':
                item['party'] = 'Republican'
                item['color'] = 'bg-danger'
                self.house_republicans += 1
            if item['party'].upper() == 'I':
                item['party'] = 'Independent'
                item['color'] = 'bg-secondary'
                self.house_independents += 1
            self.house_members_list.append({'name': item['full_name'],
                                            'last_name': item['last_name'],
                                            'party': item['party'],
                                            'color': item['color'],
                                            'state': item['state'],
                                            'district': item['district'],
                                            'next_election': item['next_election'],
                                            'search_string': utilities.get_search_string(item)
                                            })
