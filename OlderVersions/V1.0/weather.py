import urllib
import csv
import json
from xml.dom import minidom

locale = []
weatherInfo = []
def getLoc():
	latUrl = 'http://ip-api.com/csv/?fields=lat'
	lonUrl = 'http://ip-api.com/csv/?fields=lon'
	latHtml = urllib.urlopen(latUrl)
	lonHtml = urllib.urlopen(lonUrl)
	latReader = csv.reader(latHtml)
	lonReader = csv.reader(lonHtml)
	for row in latReader:
		locale.append(row[0])
	for row in lonReader:
		locale.append(row[0])
	return locale
def getWeather():
	getLoc()
	lati = locale[0]
	longi = locale[1]
	url = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php?lat=' + lati + "&lon=" + longi + '&format=24+hourly&numDays=7'
	html = urllib.urlopen(url)
	xmldoc = minidom.parseString(html.read())
	names = xmldoc.getElementsByTagName('name')
	values = xmldoc.getElementsByTagName('value')
	weatherInfo.append(values[0].firstChild.nodeValue)
	weatherInfo.append(values[7].firstChild.nodeValue)
