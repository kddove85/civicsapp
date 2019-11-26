import requests
import os
import json


def get_reps_by_zip(zip_code):
    response_dict = {'zip_code': zip_code}
    democrats = 0
    republicans = 0
    reps_list = []
    response = requests.get('https://www.googleapis.com/civicinfo/v2/representatives',
                            params={'address': zip_code,
                                    'key': os.getenv('GOOGLE_API_KEY')})

    civics_dict = response.json()
    for office in civics_dict['offices']:
        for item in office['officialIndices']:
            rep_dict = {'title': office['name'],
                        'name': civics_dict['officials'][item]['name']}
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

            reps_list.append(rep_dict)
    response_dict['reps'] = reps_list
    response_dict['dem_count'] = democrats
    response_dict['rep_count'] = republicans
    return response_dict
