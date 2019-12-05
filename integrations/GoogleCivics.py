import requests
import os
import json


def get_reps_by_address(address):
    response_dict = {'address': address}
    democrats = 0
    republicans = 0
    reps_list = []
    response = requests.get('https://www.googleapis.com/civicinfo/v2/representatives',
                            params={'address': address,
                                    'key': os.getenv('GOOGLE_API_KEY')})

    civics_dict = response.json()
    for office in civics_dict['offices']:
        for item in office['officialIndices']:
            rep_dict = {'title': office['name'],
                        'name': civics_dict['officials'][item]['name']}
                        # 'division': get_division(civics_dict['divisions'].values(), item)}
            try:
                if 'democrat' in civics_dict['officials'][item]['party'].lower():
                    democrats += 1
                    rep_dict['party'] = 'Democratic Party'
                    rep_dict['color'] = 'bg-info'
                if 'republican' in civics_dict['officials'][item]['party'].lower():
                    republicans += 1
                    rep_dict['party'] = 'Republican Party'
                    rep_dict['color'] = 'bg-danger'
            except KeyError:
                rep_dict['party'] = 'None'
                rep_dict['color'] = 'bg-default'

            try:
                rep_dict['photo'] = civics_dict['officials'][item]['photoUrl']
            except KeyError:
                rep_dict['photo'] = 'https://www.freeiconspng.com/uploads/no-image-icon-11.PNG'

            phones_list = []
            try:
                for phone in civics_dict['officials'][item]['phones']:
                    phones_list.append(phone)
            except KeyError:
                # rep_dict['phones'] = 'No Phone Numbers Available'
                continue
            rep_dict['phones'] = phones_list

            urls_list = []
            try:
                for url in civics_dict['officials'][item]['urls']:
                    urls_list.append(url)
            except KeyError:
                urls_list.append('No Links Found')
            rep_dict['urls'] = urls_list

            channels = {}
            try:
                for channel in civics_dict['officials'][item]['channels']:
                    channels[channel['type']] = channel['id']
            except KeyError:
                print('No Channels Found')
            rep_dict['channels'] = channels

            address_list = []
            try:
                for address in civics_dict['officials'][item]['address']:
                    address_list.append(address)
            except KeyError:
                print('No Address Found')
            rep_dict['address_list'] = address_list

            emails_list = []
            try:
                for email in civics_dict['officials'][item]['emails']:
                    emails_list.append(email)
            except KeyError:
                print('No Email Found')
            rep_dict['emails_list'] = emails_list

            search_string_prefix = "https://news.google.com/search?q="
            search_string_suffix = "&hl=en-US&gl=US&ceid=US%3Aen"
            name = rep_dict['name']
            name_list = name.split(" ")
            separator = '%20'
            new_name = separator.join(name_list)
            search_string = f"{search_string_prefix}{new_name}{search_string_suffix}"
            rep_dict['search_string'] = search_string

            reps_list.append(rep_dict)
    for rep in reps_list:
        print(rep)
    response_dict['reps'] = reps_list
    response_dict['dem_count'] = democrats
    response_dict['rep_count'] = republicans
    return response_dict


def get_division(divisions, item):
    for division in divisions:
        try:
            if item in division['officeIndices']:
                return division['name']
        except KeyError:
            continue


def get_elections():
    elections_list = []
    response = requests.get('https://www.googleapis.com/civicinfo/v2/elections',
                            params={'key': os.getenv('GOOGLE_API_KEY')})
    civics_dict = response.json()
    if civics_dict['elections']:
        for election in civics_dict['elections']:
            if election['ocdDivisionId']:
                levels = election['ocdDivisionId'].split('/')
                level = levels[-1].split(':')
                election['level'] = level[0].upper()
                election['level_value'] = level[1].upper()
                elections_list.append(election)
    else:
        elections_list = None
    return elections_list
