########### Python 3.6 #############
import requests
import tweetextract
import FlaskApp.app as db
def check(text):
	headers = {
	    # Request headers
	    'Ocp-Apim-Subscription-Key': '',
	}

	params ={
	    # Query parameter
	    'q': text,
	    # Optional request parameters, set to default values
	    'timezoneOffset': '0',
	    'verbose': 'false',
	    'spellCheck': 'false',
	    'staging': 'false',
	}

	try:
	    r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/<enter key>',headers=headers, params=params)
	    data=r.json()

	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return data['topScoringIntent']['intent']

def analysetweet(tweet):

	pred=check(tweet['text'])
	print(tweet['text'])
	print(pred)
	print('-------------------')
	if pred=='DetectFlood':

		db.insertintotable(tweet)
		tweetextract.gettweetbylocation(tweet)

if __name__=='__main__':
	check()
