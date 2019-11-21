import requests
import os
import json


def get_reps_by_zip(zip_code):
    reps_dict = {}
    reps_list = []
    response = requests.get('https://www.googleapis.com/civicinfo/v2/representatives',
                            params={'address': zip_code,
                                    'key': os.getenv('GOOGLE_API_KEY')})

    civics_dict = response.json()
    for office in civics_dict['offices']:
        for item in office['officialIndices']:
            reps_list.append(f"{office['name']}, {civics_dict['officials'][item]['name']}")
    return reps_list
