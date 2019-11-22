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
                rep_dict['party'] = civics_dict['officials'][item]['party']
                if 'democrat' in rep_dict['party'].lower():
                    democrats += 1
                if 'republican' in rep_dict['party'].lower():
                    republicans += 1
            except KeyError:
                rep_dict['party'] = 'None'
            # reps_list.append(f"{office['name']}, {civics_dict['officials'][item]['name']}")
            reps_list.append(rep_dict)
    response_dict['reps'] = reps_list
    response_dict['dem_count'] = democrats
    response_dict['rep_count'] = republicans
    return response_dict
