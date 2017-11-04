#!/usr/bin/env python

import sys
from get_dataframe import df


class LiveScores:
	'''Displays list of live scores from CI.'''
	def __init__(self):
		pass

	def get_all_scores(self):
		print 'LIVE MATCHES: \n'
		for match in df.itertuples():
			print "{} - {}, {}".format(match.match_name, match.match_title, match.tour_abbrev)
			print match.match_summary + '\n'

	def get_scores_by_format(self, format):
		print 'LIVE {} MATCHES: \n'.format(format.upper())
		for match in df[df.match_format == format].itertuples():
			print "{} - {}, {}".format(match.match_name, match.match_title, match.tour_abbrev)
			print match.match_summary + '\n'

	def get_scores_by_team(self):
		pass

def main():
	scores = LiveScores()
	if len(sys.argv) == 1:
		scores.get_all_scores()
	if 'Test' in sys.argv:
		scores.get_scores_by_format('Test')
	if 'ODI' in sys.argv:
		scores.get_scores_by_format('ODI')

if __name__ == '__main__':
	main()