
#Read and write (Access level)

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import twitterinterface.detectflood as detectflood
import database as db
#Variables that contains the user credentials to access Twitter API 
access_token = "813274164492529665-wPAJPScMbuU8oOKlvoHO3m4kK14pL0z"
access_token_secret = "jMD3lboNidIti6RoygcLH32OrTem2uddgWKE8ZuHY0AMv"
consumer_key = "dvgZ3nJuemHAV7gY7v2IPpPEZ"
consumer_secret = "LL8E0WYTg8iKh12IKbCAeQ63xyZsi48GXDq9GLb7AoaCAgxGpb"
import tweepy

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self,t):
        self.c1=0
        self.c=t
    def on_data(self, data):
        jsondata=json.loads(data)
        self.c1+=1

        with open('data.json', 'w+') as outfile:
            detectflood.analysetweet(jsondata)
            json.dump(data, outfile)
        if self.c1<self.c:
            return True
        else:
            print("streaming stopped")
            return False

    def on_error(self, status):
        print (status)


def gettweetbytag():
    #This handles Twitter authetification and the connection to Twitter Streaming API

    l = StdOutListener(30)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['flood','#flood','#floods','floods','rain','rains'])

def gettweetbylocation(tweet):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets = api.search(q='geocode:'+tweet['coordinates']['coordinates'][0]+','+tweet['coordinates']['coordinates'][1]+',50km')
    for t in tweets:
        if detectflood.check(t['text'])=='DetectFlood':
            db.insertuser(t)
    db.checkusertable()


if __name__=='__main__':
    gettweetbytag()


