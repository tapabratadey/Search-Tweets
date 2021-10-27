import csv

def read_file(filename, list_of_tweets):
	with open(filename, 'r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			list_of_tweets.append(row)
	return list_of_tweets