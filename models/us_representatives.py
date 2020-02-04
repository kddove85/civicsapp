
class USSenator:
    def __init__(self, name, party, state, next_election, opponents_link, news_link):
        self.name = name
        self.party = party
        self.state = state
        self.next_election = next_election
        self.opponents_link = opponents_link
        self.news_link = news_link


class USCongressman:
    def __init__(self, name, party, state, district, next_election, opponents_link, news_link):
        self.name = name
        self.party = party
        self.state = state
        self.district = district
        self.next_election = next_election
        self.opponents_link = opponents_link
        self.news_link = news_link
