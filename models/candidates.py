from bs4 import BeautifulSoup
import requests
import datetime
import constants


class Candidate:
    def __init__(self, photo_url, name, poll_score, bio_link):
        self.photo_url = photo_url
        self.name = name
        self.poll_score = poll_score
        self.bio_link = bio_link


def get_candidates():
    current_year = str(datetime.datetime.now().year)
    response = requests.get(f"{constants.ballotpedia_url}{constants.candidates}{current_year}")
    soup = BeautifulSoup(response.text, 'html.parser')
    candidates_info = get_candidate_info(soup)

    rcp_response = requests.get(f"{constants.rcp_url}{current_year}{constants.poll_endpoint}")
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
                                        'link': f"{constants.ballotpedia_url}{links[x].attrs['href']}",
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
    final_candidates_list = []
    for candidate in candidates_list:
        for poll in polls:
            if candidate['name'].split(' ')[-1] == poll['name']:
                final_candidates_list.append(
                    Candidate(candidate['img'], candidate['name'], poll['score'], candidate['link']))
    final_candidates_list = sorted(final_candidates_list, key=lambda i: float(i.poll_score), reverse=True)
    return final_candidates_list
