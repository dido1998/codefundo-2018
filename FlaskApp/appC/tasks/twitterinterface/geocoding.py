import urllib.request
import json
def geocode(address):
	response=urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key=AIzaSyC-WytuJY84cvqRxPC7JSJ2BuDUL6rWbpk')
	html=response.read()
	html=html.decode("utf-8") 
	res=json.loads(html)
	return res['results'][0]['geometry']['location']['lat'],res['results'][0]['geometry']['location']['lng']

def reversegeocode(lat,lon):
	response=urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lon)+'&key=AIzaSyC-WytuJY84cvqRxPC7JSJ2BuDUL6rWbpk')
	html=response.read()
	html=html.decode("utf-8") 
	res=json.loads(html)
	print(lat)
	print(lon)
	return res['results'][0]['formatted_address']

if __name__=='__main__':
	reversegeocode(40.714224,-73.961452)
