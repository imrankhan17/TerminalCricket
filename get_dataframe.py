#!/usr/bin/env python

'''Script to create full dataframe of match details.'''

import requests
import pandas as pd
import numpy as np

r = requests.get('http://fcast.us-east-1.espncdn.com/FastcastService/pubsub/profiles/12000/topic/event-topevents-espncricinfo-gb-en/message/1006375/checkpoint').json()

tours = pd.DataFrame(r['sports'][0]['leagues'])[['abbreviation', 'isTournament', 'name']]
tours.columns = ['abbreviation', 'isTournament', 'tour_name']

matches = pd.DataFrame()
for match in r['sports'][0]['leagues']:
    matches = matches.append(pd.DataFrame(match['events']) \
    [['date', 'description', 'endDate', 'eventType', 'name', 'shortName', 'title']]).reset_index(drop=True)

matches2 = pd.DataFrame()
for match in r['sports'][0]['leagues']:
    matches2 = matches2.append(pd.DataFrame(match['events'][0]['fullStatus']).loc[['description']] \
                               [['dayNumber', 'period', 'summary', 'type']]).reset_index(drop=True)

home_teams = []; away_teams = []
is_home_national = []; is_away_national = []
batting_first_team = []; winners = []
innings1 = []; innings2 = []
link = []; ground = []

for match in r['sports'][0]['leagues']:
    home_teams.append(match['events'][0]['competitors'][0]['displayName'])
    away_teams.append(match['events'][0]['competitors'][1]['displayName'])   
    link.append(match['events'][0]['link'])
    ground.append(match['events'][0]['location'])
    
    if match['events'][0]['competitors'][0]['isNational']:
        is_home_national.append(1)
    else:
        is_home_national.append(0)
        
    if match['events'][0]['competitors'][1]['isNational']:
        is_away_national.append(1)
    else:
        is_away_national.append(0)
    
    if match['events'][0]['competitors'][0]['winner']:
        winners.append(match['events'][0]['competitors'][0]['displayName'])
    elif match['events'][0]['competitors'][1]['winner']:
        winners.append(match['events'][0]['competitors'][1]['displayName'])
    else:
        winners.append(np.nan)
    
    if match['events'][0]['competitors'][0]['order'] == 1:
        batting_first_team.append(match['events'][0]['competitors'][0]['displayName'])
    else:
        batting_first_team.append(match['events'][0]['competitors'][1]['displayName'])
        
    if match['events'][0]['competitors'][0]['order'] == 1:
        innings1.append(match['events'][0]['competitors'][0]['score'])
        innings2.append(match['events'][0]['competitors'][1]['score'])
    else:
        innings1.append(match['events'][0]['competitors'][1]['score'])
        innings2.append(match['events'][0]['competitors'][0]['score'])

teams = pd.DataFrame(zip(home_teams, away_teams, is_home_national, is_away_national,
                         batting_first_team, winners, innings1, innings2, ground, link), 
                     columns = ['home_team', 'away_team', 'is_home_national', 'is_away_national',
                                'batting_first_team', 'winner', 'innings1', 'innings2', 'ground', 'scorecard_link'])

df = matches2.join(matches).join(tours).join(teams)
df.columns = ['current_day', 'current_innings', 'match_summary', 'is_finished', 'full_date', 'description', 'end_date', 'match_format',
              'match_name', 'match_short_name', 'match_title', 'tour_abbrev', 'is_tournament', 'tour_name', 
              'home_team', 'away_team', 'is_home_national', 'is_away_national', 'batting_first_team', 
              'winner', 'innings1', 'innings2', 'ground', 'scorecard_link']

df['match_start_date'] = df.full_date.apply(pd.to_datetime).dt.date
df['match_start_time'] = df.full_date.apply(pd.to_datetime).dt.time
df['match_end_date'] = df.end_date.apply(pd.to_datetime).dt.date