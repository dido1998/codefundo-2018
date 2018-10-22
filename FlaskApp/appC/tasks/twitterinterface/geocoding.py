import urllib.request
import json
def geocode(address):
	response=urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key=AIzaSyA2Fn0J57CMn5od7EHQQWlOoEAGxKK8kqo')
	html=response.read()
	html=html.decode("utf-8") 
	res=json.loads(html)
	return res['results'][0]['geometry']['location']['lat'],res['results'][0]['geometry']['location']['lng']

if __name__=='__main__':
	geocode('undri,pune')