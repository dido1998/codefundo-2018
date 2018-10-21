########### Python 3.6 #############
import requests
import twitterinterface.tweetextract
import app as db
def check(text):
	headers = {
	    # Request headers
	    'Ocp-Apim-Subscription-Key': '793c58a6a4d54c469c527b9e47516371',
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
	    r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/457e361c-3942-4caf-89f9-ce28f0c1ee57',headers=headers, params=params)
	    data=r.json()
	    return data['topScoringIntent']['intent']
	except Exception as e:
	    print("error")
	    return None

	

def analysetweet(tweet):

	pred=check(tweet['text'])
	print(tweet['text'])
	print(pred)
	print('-------------------')
	if pred=='DetectFlood':

		db.insertuser(tweet)
		tweetextract.gettweetbylocation(tweet)

if __name__=='__main__':
	check()
