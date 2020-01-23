from bs4 import BeautifulSoup
import requests

base_url = 'https://www.supremecourt.gov/about/'
biographies = 'biographies.aspx'

gp_url = 'https://www.thegreenpapers.com/Hx/'
justices_endpoint = 'SupremeCourt.html'


def get_justices():
    response = requests.get(f"{base_url}{biographies}")
    gp_response = requests.get(f"{gp_url}{justices_endpoint}")
    soup = BeautifulSoup(response.text, 'html.parser')
    gp_soup = BeautifulSoup(gp_response.text, 'html.parser')

    supreme_court_justices = get_justices_info(soup)
    appointees = get_appointed_by(gp_soup)
    photos = get_photos(soup)

    final_dict = combine(supreme_court_justices, photos, appointees)

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


def get_appointed_by(soup):
    appointments = []
    tables = soup.find_all('table')
    table = tables[1]
    rows = table.find_all('tr')

    count = 0
    for row in rows:
        if count > 0:
            entry = row.text.split('\r')
            appointments.append({'name': entry[0].strip(), 'appointee': entry[2].strip()})
        count += 1
    return appointments


def combine(justices, photos, appointees):
    for justice in justices:
        for photo in photos:
            if justice['name'] == photo['name']:
                justice['photo'] = f"{base_url}{photo['photo']}"
        for appointee in appointees:
            if name_check(justice['name'], appointee['name']):
                justice['appointee'] = appointee['appointee']
                break
    return justices


def remove_middle_initial(name):
    name_list = name.split(' ')
    if len(name_list) == 3:
        name = f"{name_list[0]} {name_list[2]}"
    return name


def remove_junior(name):
    name_list = name.split(',')
    if len(name_list) == 2:
        name = name_list[0]
    return name


def name_check(name1, name2):
    if name1 == name2:
        return True
    if remove_middle_initial(name1) == remove_middle_initial(name2):
        return True
    if remove_junior(name1) == remove_junior(name2):
        return True
    return False
