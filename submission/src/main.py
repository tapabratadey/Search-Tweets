
import read_file as csv
import TweetIndex as TweetIndex
from pygments import console

example_file = '../data/examples.csv'
small_file = '../data/small.csv'
tweets_file = '../data/tweets.csv'

def init(list_of_tweets):
	# list_of_tweets = csv.read_file(example_file, list_of_tweets)
	# list_of_tweets = csv.read_file(small_file, list_of_tweets)
	list_of_tweets = csv.read_file(tweets_file, list_of_tweets)
	return list_of_tweets

def search(tweet):
	# ===============================================================================
	
	print('\n\n------------------')
	print('   TEST 1 - 5     ')
	print('------------------')
	
	assert tweet.search('neeva') == [('0', 'out if what that neeva say'), ('1', 'as his at she neeva be'), ('2', 'other special this neeva know into'), ('3', 'my out that special when neeva'), ('4', 'have out we me use will neeva')]
	print('Test 1:', console.colorize("green", "Passed!"))
	
	assert tweet.search('neeva & special') == [('2', 'other special this neeva know into'), ('3', 'my out that special when neeva'), ('6', 'have only of special neeva'), ('11', 'i go special like him she neeva'), ('18', 'one by special neeva our who')]
	print('Test 2:', console.colorize("green", "Passed!"))
	
	assert tweet.search('neeva & !special') == [('0', 'out if what that neeva say'), ('1', 'as his at she neeva be'), ('4', 'have out we me use will neeva'), ('5', 'all many first neeva'), ('7', 'one see neeva our would')]
	print('Test 3:', console.colorize("green", "Passed!"))
	
	assert tweet.search('neeva | special') == [('0', 'out if what that neeva say'), ('1', 'as his at she neeva be'), ('2', 'other special this neeva know into'), ('3', 'my out that special when neeva'), ('4', 'have out we me use will neeva')]
	print('Test 4:', console.colorize("green", "Passed!"))
	
	assert tweet.search('neeva & special & (think | when) & !my') == [('32', 'of think special neeva'), ('45', 'think want special neeva'), ('49', 'special when tell neeva'), ('57', 'come special now very when this neeva a'), ('70', 'think special neeva')]
	print('Test 5:', console.colorize("green", "Passed!"))
	
	# ===============================================================================
	
	print('\n\n------------------')
	print('   TEST 5 - 10    ')
	print('------------------')
	
	assert tweet.search("neeva & special & ((think & go) | (first & this))") == [('36', 'my only go special her from neeva think look'), ('84', 'way special this neeva first'), ('824', 'the go special find and neeva our think know'), ('1904', 'can just special find this neeva first into'), ('5275', 'i about even special this neeva get first he')]
	print('Test 6:', console.colorize("green", "Passed!"))

	assert tweet.search('is') == "No results found"
	print('Test 7:', console.colorize("green", "Passed!"))

	assert tweet.search("neeva & is & (man | (thing & two))") == [('27', 'man neeva'), ('28', 'many we me neeva man'), ('35', 'neeva one man which'), ('71', 'man some neeva'), ('82', 'by on them so neeva give man')]
	print('Test 8:', console.colorize("green", "Passed!"))

	assert tweet.search("") == "No results found"
	print('Test 9:', console.colorize("green", "Passed!"))

	assert tweet.search("neeva & think & (come | go)") == [('36', 'my only go special her from neeva think look'), ('100', 'come we special her these neeva think but'), ('309', 'take can come well neeva think could'), ('824', 'the go special find and neeva our think know'), ('1608', 'his come how in neeva think first')]
	print('Test 10:', console.colorize("green", "Passed!"))


	# ===============================================================================

	print('\n\n------------------')
	print('   TEST 11 - 15   ')
	print('------------------')


	assert tweet.search("neeva & is & think | special & man") == "Invalid Query"
	print('Test 11:', console.colorize("green", "Passed!"))

	assert tweet.search("take & day & !special") == [('530', 'our day take neeva'), ('907', 'take way day than neeva'), ('2632', 'take use day neeva other'), ('3563', 'take do day will neeva'), ('3719', 'take my if day very this neeva')]
	print('Test 12:', console.colorize("green", "Passed!"))

	assert tweet.search("take & day") == [('530', 'our day take neeva'), ('907', 'take way day than neeva'), ('2632', 'take use day neeva other'), ('2916', 'take up that special day neeva would'), ('3563', 'take do day will neeva')]
	print('Test 13:', console.colorize("green", "Passed!"))

	assert tweet.search("go & want | ((take & well) & (thing & say))") == [('2158', 'want one what go out even we do special her neeva get at'), ('2263', 'want go very here neeva be'), ('2814', 'want go we so this neeva'), ('3001', 'want their go him neeva with then'), ('3091', 'want go just those neeva our for')]
	print('Test 14:', console.colorize("green", "Passed!"))

	assert tweet.search("neeva & say") == [('0', 'out if what that neeva say'), ('8', 'say about or neeva'), ('17', 'what not very those neeva say tell a'), ('41', 'your how and those she neeva say know'), ('73', 'on that be to neeva say know which')]
	print('Test 15:', console.colorize("green", "Passed!"))


def process_and_search(list_of_tweets):
	tweet = TweetIndex.TweetIndex()
	tweet.process_tweets(list_of_tweets)
	search(tweet)

if __name__ == '__main__':
	list_of_tweets = []
	list_of_tweets = init(list_of_tweets)
	process_and_search(list_of_tweets)
