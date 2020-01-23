from bs4 import BeautifulSoup
import requests

base_url = 'https://ballotpedia.org'
candidates = '/Democratic_presidential_nomination,_2020'


def get_candidates():
    response = requests.get(f"{base_url}{candidates}")
    soup = BeautifulSoup(response.text, 'html.parser')
    candidates_list = []
    tables = soup.find_all('table', attrs={'align': 'center', 'style': '"margin-top:.2em;'})
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            imgs = row.find_all('img')
            links = row.find_all('a')
            for x in range(0, len(links)):
                candidates_list.append({'name': links[x].text,
                                        'link': f"{base_url}{links[x].attrs['href']}",
                                        'img': imgs[x].attrs['src']})
    return candidates_list
