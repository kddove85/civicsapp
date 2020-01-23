from bs4 import BeautifulSoup
import requests

base_url = 'https://ballotpedia.org'
candidates = '/Democratic_presidential_nomination,_2020'

rcp = 'https://www.realclearpolitics.com/epolls/2020/president/us/2020_democratic_presidential_nomination-6730.html'


def get_candidates():
    response = requests.get(f"{base_url}{candidates}")
    soup = BeautifulSoup(response.text, 'html.parser')
    candidates_info = get_candidate_info(soup)

    rcp_response = requests.get(rcp)
    rcp_soup = BeautifulSoup(rcp_response.text, 'html.parser')
    candidates_polls = get_poll(rcp_soup)

    return combine(candidates_info, candidates_polls)


def get_candidate_info(soup):
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


def get_poll(soup):
    poll_list = []
    tables = soup.find_all('table')
    table = tables[1]
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            divs = cell.find_all('div')
            name = divs[1].text.split(' ')
            poll_list.append({'name': name[0], 'score': divs[0].text})
    return poll_list


def combine(candidates_list, polls):
    for candidate in candidates_list:
        for poll in polls:
            if candidate['name'].split(' ')[-1] == poll['name']:
                candidate['score'] = poll['score']
    candidates_list = sorted(candidates_list, key=lambda i: float(i['score']), reverse=True)
    return candidates_list
