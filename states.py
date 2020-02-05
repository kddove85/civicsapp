states = [
    {"name": "Alabama", "alpha": "AL"},
    {"name": "Alaska", "alpha": "AK"},
    {"name": "Arizona", "alpha": "AZ"},
    {"name": "Arkansas", "alpha": "AR"},
    {"name": "California", "alpha": "CA"},
    {"name": "Colorado", "alpha": "CO"},
    {"name": "Connecticut", "alpha": "CT"},
    {"name": "Delaware", "alpha": "DE"},
    {"name": "Florida", "alpha": "FL"},
    {"name": "Georgia", "alpha": "GA"},
    {"name": "Hawaii", "alpha": "HI"},
    {"name": "Idaho", "alpha": "ID"},
    {"name": "Illinois", "alpha": "IL"},
    {"name": "Indiana", "alpha": "IN"},
    {"name": "Iowa", "alpha": "IA"},
    {"name": "Kansas", "alpha": "KS"},
    {"name": "Kentucky", "alpha": "KY"},
    {"name": "Louisiana", "alpha": "LA"},
    {"name": "Maine", "alpha": "ME"},
    {"name": "Maryland", "alpha": "MD"},
    {"name": "Massachusetts", "alpha": "MA"},
    {"name": "Michigan", "alpha": "MI"},
    {"name": "Minnesota", "alpha": "MN"},
    {"name": "Mississippi", "alpha": "MS"},
    {"name": "Missouri", "alpha": "MO"},
    {"name": "Montana", "alpha": "MT"},
    {"name": "Nebraska", "alpha": "NE"},
    {"name": "Nevada", "alpha": "NV"},
    {"name": "New Hampshire", "alpha": "NH"},
    {"name": "New Jersey", "alpha": "NJ"},
    {"name": "New Mexico", "alpha": "NM"},
    {"name": "New York", "alpha": "NY"},
    {"name": "North Carolina", "alpha": "NC"},
    {"name": "North Dakota", "alpha": "ND"},
    {"name": "Ohio", "alpha": "OH"},
    {"name": "Oklahoma", "alpha": "OK"},
    {"name": "Oregon", "alpha": "OR"},
    {"name": "Pennsylvania", "alpha": "PA"},
    {"name": "Rhode Island", "alpha": "RI"},
    {"name": "South Carolina", "alpha": "SC"},
    {"name": "South Dakota", "alpha": "SD"},
    {"name": "Tennessee", "alpha": "TN"},
    {"name": "Texas", "alpha": "TX"},
    {"name": "Utah", "alpha": "UT"},
    {"name": "Vermont", "alpha": "VT"},
    {"name": "Virginia", "alpha": "VA"},
    {"name": "Washington", "alpha": "WA"},
    {"name": "West Virginia", "alpha": "WV"},
    {"name": "Wisconsin", "alpha": "WI"},
    {"name": "Wyoming", "alpha": "WY"},
    {"name": "American Samoa", "alpha": "AS"},
    {"name": "District of Columbia", "alpha": "DC"},
    {"name": "Guam", "alpha": "GU"},
    {"name": "Virgin Islands", "alpha": "VI"},
]


def get_states():
    choices = [(s['alpha'], s['name']) for s in states]
    choices.remove(('AS', 'American Samoa'))
    choices.remove(('GU', 'Guam'))
    choices.remove(('VI', 'Virgin Islands'))
    choices.remove(('DC', 'District of Columbia'))
    return choices


def return_name(alpha):
    for state in states:
        if state['alpha'] == alpha:
            return state['name']


def return_alpha(name):
    for state in states:
        if state['name'] == name:
            return state['alpha']
