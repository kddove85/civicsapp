import requests
import os


def get_senate_members():
    response_object = {}
    democrats = 0
    republicans = 0
    independents = 0
    senate_members_list = []
    response = requests.get('https://api.propublica.org/congress/v1/116/senate/members.json',
                            headers={'X-API-Key': os.getenv('PROPUBLICA_API_KEY')})
    response_dict = response.json()
    for member in response_dict['results'][0]['members']:
        if member['party'].upper() == 'R':
            member['party'] = 'Republican'
            member['color'] = 'bg-danger'
            republicans += 1
        if member['party'].upper() == 'D':
            member['party'] = 'Democrat'
            member['color'] = 'bg-info'
            democrats += 1
        if member['party'].upper() == 'ID':
            member['party'] = 'Independent'
            member['color'] = 'table-secondary'
            independents += 1
        senate_members_list.append({'first_name': member['first_name'],
                                    'last_name': member['last_name'],
                                    'party': member['party'],
                                    'state': member['state'],
                                    'next_election': member['next_election'],
                                    'color': member['color'],
                                    'search_string': get_search_string(member)})
    response_object['senators'] = sorted(senate_members_list, key=lambda i: (i['state'], i['last_name']))
    response_object['dems'] = democrats
    response_object['reps'] = republicans
    response_object['inds'] = independents
    for member in response_object['senators']:
        print(member)
    return response_object


def get_search_string(member):
    search_string_prefix = "https://news.google.com/search?q="
    search_string_suffix = "&hl=en-US&gl=US&ceid=US%3Aen"
    name = f"{member['first_name']} {member['last_name']}"
    name_list = name.split(" ")
    separator = '%20'
    new_name = separator.join(name_list)
    search_string = f"{search_string_prefix}{new_name}{search_string_suffix}"
    return search_string
