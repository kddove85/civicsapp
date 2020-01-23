import requests
import os
import utilities


class OpenStates:
    def __init__(self):
        self.senate_members_list = []
        self.senate_democrats = 0
        self.senate_republicans = 0
        self.senate_independents = 0
        self.house_members_list = []
        self.house_democrats = 0
        self.house_republicans = 0
        self.house_independents = 0

    def get_state_members(self, state):
        response_object = {'state': state}
        response = requests.get(f"https://openstates.org/api/v1/legislators?state={state}",
                                headers={'X-API-Key': os.getenv('OPENSTATE_API_KEY')})
        response_dict = response.json()
        for item in response_dict:
            self.add_member(item)
        try:
            response_object['senators'] = sorted(self.senate_members_list, key=lambda i: (int(i['district']), i['last_name']))
        except ValueError:
            response_object['senators'] = sorted(self.senate_members_list, key=lambda i: (i['district'], i['last_name']))

        try:
            response_object['congressmen'] = sorted(self.house_members_list, key=lambda i: (int(i['district']), i['last_name']))
        except ValueError:
            response_object['congressmen'] = sorted(self.house_members_list, key=lambda i: (i['district'], i['last_name']))

        response_object['senate_dems'] = self.senate_democrats
        response_object['senate_reps'] = self.senate_republicans
        response_object['senate_inds'] = self.senate_independents

        response_object['house_dems'] = self.house_democrats
        response_object['house_reps'] = self.house_republicans
        response_object['house_inds'] = self.house_independents

        return response_object

    def add_member(self, item):
        if item['chamber'] == 'upper':
            party = item['party'].split('/')
            if len(party) > 1:
                if party[0] == 'Democratic':
                    item['party'] = 'Democratic'
            if item['party'] == 'Democratic':
                item['color'] = 'bg-info'
                self.senate_democrats += 1
            elif item['party'] == 'Republican':
                item['color'] = 'bg-danger'
                self.senate_republicans += 1
            else:
                item['color'] = 'bg-secondary'
                self.senate_independents += 1
            self.senate_members_list.append({'name': item['full_name'],
                                             'last_name': item['last_name'],
                                             'party': item['party'],
                                             'color': item['color'],
                                             'district': item['district'],
                                             'search_string': utilities.get_search_string(item)
                                             })
        if item['chamber'] == 'lower':
            party = item['party'].split('/')
            if len(party) > 1:
                if party[0] == 'Democratic':
                    item['party'] = 'Democratic'
            if item['party'] == 'Democratic':
                item['color'] = 'bg-info'
                self.house_democrats += 1
            elif item['party'] == 'Republican':
                item['color'] = 'bg-danger'
                self.house_republicans += 1
            else:
                item['color'] = 'bg-secondary'
                self.house_independents += 1
            self.house_members_list.append({'name': item['full_name'],
                                            'last_name': item['last_name'],
                                            'party': item['party'],
                                            'color': item['color'],
                                            'district': item['district'],
                                            'search_string': utilities.get_search_string(item)
                                            })
