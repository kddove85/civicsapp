import requests
import os
import constants


class Representative:
    def __init__(self, title, photo_url, name, party, color, phones, news_link, site_links, social_medias, address,
                 emails):
        self.title = title
        self.photo_url = photo_url
        self.name = name
        self.party = party
        self.color = color
        self.phones = phones
        self.news_link = news_link
        self.site_links = site_links
        self.social_medias = social_medias
        self.address = address
        self.emails = emails

    def __str__(self):
        return f"{self.title}: {self.name}"


def get_reps_by_address(address):
    response_dict = {'address': address}
    democrats = 0
    republicans = 0
    reps_list = []
    response = requests.get(constants.google_representatives_url,
                            params={'address': address,
                                    'key': os.getenv('GOOGLE_API_KEY')})

    civics_dict = response.json()
    for office in civics_dict['offices']:
        for item in office['officialIndices']:
            title = office['name']
            name = civics_dict['officials'][item]['name']
            try:
                if 'democrat' in civics_dict['officials'][item]['party'].lower():
                    democrats += 1
                    party = 'Democratic Party'
                    color = 'bg-info'
                if 'republican' in civics_dict['officials'][item]['party'].lower():
                    republicans += 1
                    party = 'Republican Party'
                    color = 'bg-danger'
            except KeyError:
                party = 'None'
                color = 'bg-default'

            try:
                photo = civics_dict['officials'][item]['photoUrl']
            except KeyError:
                photo = constants.default_photo

            phones_list = []
            try:
                for phone in civics_dict['officials'][item]['phones']:
                    phones_list.append(phone)
            except KeyError:
                continue

            urls_list = []
            try:
                for url in civics_dict['officials'][item]['urls']:
                    urls_list.append(url)
            except KeyError:
                urls_list.append('No Links Found')

            channels = {}
            try:
                for channel in civics_dict['officials'][item]['channels']:
                    channels[channel['type']] = channel['id']
            except KeyError:
                print('No Channels Found')

            address_list = []
            try:
                for address in civics_dict['officials'][item]['address']:
                    address_list.append(address)
            except KeyError:
                print('No Address Found')

            emails_list = []
            try:
                for email in civics_dict['officials'][item]['emails']:
                    emails_list.append(email)
            except KeyError:
                print('No Email Found')

            name_list = name.split(" ")
            separator = '%20'
            new_name = separator.join(name_list)
            search_string = f"{constants.search_string_prefix}{new_name}{constants.search_string_suffix}"
            reps_list.append(
                Representative(title, photo, name, party, color, phones_list, search_string, urls_list, channels,
                               address_list, emails_list))

    response_dict['reps'] = reps_list
    response_dict['dem_count'] = democrats
    response_dict['rep_count'] = republicans

    return response_dict
