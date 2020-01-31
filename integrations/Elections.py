from bs4 import BeautifulSoup
import datetime
import requests
import states

gp_url = 'http://www.thegreenpapers.com/G20/'
elections_endpoint = 'PollingHours.phtml'


def get_election_info():
    elections_list = []
    response = requests.get(f"{gp_url}{elections_endpoint}")
    soup = BeautifulSoup(response.text, 'html.parser')
    for dd in soup.find_all('table')[0].find_all('dl')[0].find_all('dd'):
        state = dd.fetchPrevious('dt')[0].text
        for child in dd.find_all('i'):
            try:
                text = child.text.replace('.', '')
                text = text.split(' ')
                day = int(text[1])
                month = text[2]
                year = int(text[3])
                election_date = datetime.datetime.strptime(f'{day} {month}, {year}', '%d %B, %Y')
                date_string = election_date.strftime('%Y-%m-%d')
                election_name = ' '.join([str(text[i]) for i in range(4, len(text))])
                election_name = f"{state} {election_name}"
                level_value = states.return_alpha(state)
                if level_value is None:
                    level_value = state
                elections_list.append({'name': election_name, 'date': date_string, 'level': 'STATE',
                                       'level_value': level_value})
            except ValueError:
                continue
    elections_list = sorted(elections_list, key=lambda i: i['date'])
    return elections_list
