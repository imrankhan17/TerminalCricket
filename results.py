import sys
import requests
from BeautifulSoup import BeautifulSoup
import pandas as pd
import numpy as np
import re

url = "http://www.espncricinfo.com/ci/engine/match/index/live.html"
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)

def innings_parser(x, inning=1):
    if '&amp;' in x:
        return re.split(r'(^[^\d]+)', x)[2].split(' &amp; ')[inning-1]
    elif inning > 1:
        return np.nan
    else:
        return re.split(r'(^[^\d]+)', x)[2]
    
def get_format(x):
    if 'unofficial' not in x:
        if 'Test' in x:
            return 'Test'
        elif 'ODI' in x:
            return 'ODI'
        elif 'T20I' in x:
            return 'T20I'
        else:
            return 'other'
    else:
        return 'other'

details = {
'match_details': [],
'match_link': [],
'match_status': [],
'team1': [],
'team2': []
}

for i in soup.findAll('span', attrs={'class': 'match-no'}):
    details['match_details'].append(i.text)
    details['match_link'].append(i.a['href'])

for i in soup.findAll('div', attrs={'class': 'match-status'}):
    details['match_status'].append(i.text)

for i in soup.findAll('div', attrs={'class': 'innings-info-1'}):
    details['team1'].append(i.text)
    
for i in soup.findAll('div', attrs={'class': 'innings-info-2'}):
    details['team2'].append(i.text)
    
df = pd.DataFrame(details)
df['batting_first_team'] = df.team1.apply(lambda x: re.split(r'(^[^\d]+)', x)[1])
df['batting_second_team'] = df.team2.apply(lambda x: re.split(r'(^[^\d]+)', x)[1])
df['innings1_score'] = df.team1.apply(innings_parser, args=(1,))
df['innings2_score'] = df.team2.apply(innings_parser, args=(1,))
df['innings3_score'] = df.team1.apply(innings_parser, args=(2,))
df['innings4_score'] = df.team2.apply(innings_parser, args=(2,))
df['match_status'] = df.match_status.apply(lambda x: x.replace('&nbsp;', ' '))
df['match_format'] = df.match_details.apply(get_format)
df['match_format'] = pd.Categorical(df['match_format'], ["Test", "ODI", "T20I", 'other'])
df = df.sort_values('match_format').reset_index(drop=True)

if len(sys.argv) == 1:
    for i in df[df.match_format.isin(['Test', 'ODI', 'T20I'])].itertuples():
        print i.match_format
        print '{} v {} - {}'.format(i.batting_first_team, i.batting_second_team, i.match_details)
        print '{}'.format(i.match_status)
        print ''

for f in ['Test', 'ODI', 'T20I', 'other']:
    if f in sys.argv:
        for i in df[df.match_format == f].itertuples():
            if f != 'other':
                print i.match_format
            print '{} v {} - {}'.format(i.batting_first_team, i.batting_second_team, i.match_details)
            print '{}'.format(i.match_status)
            print ''
