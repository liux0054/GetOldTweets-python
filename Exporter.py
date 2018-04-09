# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
# import argparse, json, datetime, uuid, 
# import tweepy
from textblob import TextBlob 
# from searchtweets import ResultStream, gen_rule_payload, load_credentials
import pandas as pd 
# from nltk import word_tokenize
import re, string


if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print f.read()
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "output_got.csv"

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--output':
				outputFileName = arg
				
		outputFile = codecs.open(outputFileName, "w+", "utf-8")

		outputFile.write('username,date,retweets,favorites,text,geo,mentions,hashtags,id,permalink,polarity,subjectivity')

		print('Searching...\n')

		def receiveBuffer(tweets):
			for t in tweets:
				# t.text= re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", t.text)
				content = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", t.text)
				content=content.split()

				# to remove http......
				if 'http' in content:
					http_index=content.index('http')
					content=content[:http_index]
				content=" ".join(content)
				
				analysis=TextBlob(content)
				sentiment=analysis.sentiment
				# sentiment_score.append(analysis.sentiment)
				t.polarity = sentiment.polarity
				t.subjectivity=sentiment.subjectivity
				outputFile.write(('\n%s,%s,%d,%d,"%s",%s,%s,%s,"%s",%s,%s,%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink, t.polarity, t.subjectivity)))


				


			outputFile.flush()
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
