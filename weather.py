#####################################################
#                                                   #
#                                                   #
#                weather.py V2                      #
#               Author: RParkerE                    #
#               Date: 1/18/2016                     #
#                                                   #
#                                                   #
#####################################################

import urllib
import csv
import json
from xml.dom import minidom
from xml.etree import cElementTree

#Method for getting your current location
def getLoc():
	# Calls API
	url = 'http://ip-api.com/csv/?fields=lat,lon'
	http_connection = urllib.urlopen(url)
	value_array = http_connection.readline().decode().split(',')
	# Close API connection
	http_connection.close()
	# API uses your IP adress and returns your coordinates
	lat = float(value_array[0])
	lon = float(value_array[1])
	# Close API connection
	http_connection.close()
	# Return coordinates
	return (lat,lon)
		
def getWeather():
	# Initialize your coordinates
	lat, lon = getLoc()
	# Call API
	url_base = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php?lat={lat}&lon={lon}&format=24+hourly&numDays=7'
	url = url_base.format(lat=lat, lon=lon)
	print(url)
	http_connection = urllib.urlopen(url)
	# Parse XML file returned by API
	tree = cElementTree.parse(http_connection)
	# Close API connection
	http_connection.close()
	doc = tree.getroot()
	# Search XML document for temperatures
	temps = doc.findall('.//temperature/value')
	# Return the days high and low temperatures
	return (temps[0].text,temps[7].text)
