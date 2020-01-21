from bs4 import BeautifulSoup
import requests

base_url = 'https://www.supremecourt.gov/about/'
biographies = 'biographies.aspx'


def get_justices():
    response = requests.get(f"{base_url}{biographies}")
    soup = BeautifulSoup(response.text, 'html.parser')

    supreme_court_justices = get_justices_info(soup)
    photos = get_photos(soup)
    final_dict = combine(supreme_court_justices, photos)

    return final_dict


def get_justices_info(soup):
    supreme_court_justices = []
    for justice in soup.find_all('strong'):
        justice = justice.text.split(',')
        justice_structure = []
        for item in justice:
            if 'Jr.' not in item:
                justice_structure.append(item)
        if 'Retired' not in justice_structure[0]:
            justice_entry = {'name': justice_structure[0], 'title': justice_structure[1]}
            supreme_court_justices.append(justice_entry)
    return supreme_court_justices


def get_photos(soup):
    photos = []
    for media in soup.find_all('div', class_='media'):
        for kid in media.children:
            try:
                name = kid.attrs['title'].split(',')[0]
                photo = kid.attrs['src']
                if 'Retired' not in name:
                    photos.append({'name': name, 'photo': photo})
            except (AttributeError, KeyError):
                pass
    return photos


def combine(justices, photos):
    for justice in justices:
        for photo in photos:
            if justice['name'] == photo['name']:
                justice['photo'] = f"{base_url}{photo['photo']}"
    return justices
