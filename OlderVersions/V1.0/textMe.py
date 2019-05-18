from weather import getWeather, weatherInfo
from sunTimes import sunRise, sunSet, sunTimes
from emailCheck import read, unread
from email.mime.text import MIMEText
import smtplib

extension = []

def send_text(numstring, carrier, host, user, password):
	getInfo(host, user, password)
	getCarrierExt(carrier)
	
	message = "Today's High: " + str(weatherInfo[0]) + ", Today's Low: " + str(weatherInfo[1]) + ", Sunrise is at: " + sunTimes[0] + ", Sunset is at: " + sunTimes[1] + ", You have " + str(unread[0]) + " unread messages"
	message = MIMEText(message)
	email = user + '@' + host
	phone = numstring + '@' + extension[0]
	message['From'] = email
	message['To'] = phone

	host = "smtp." + host
	server = smtplib.SMTP(host, 587)
	server.starttls()
	server.login(user, password)
	server.sendmail(email, phone, message.as_string())
	server.quit()

def getInfo(host, usr, pas):
	getWeather()
	sunRise()
	sunSet()
	read(host, usr, pas)

def getCarrierExt(carrier):
	carrierExts = {
		'Alltel' : 'message.alltel.com',
		'AT&T' : 'txt.att.net',
		'Boost Mobile' : 'myboostmobile.com',
		'Cingular' : 'cingularme.com',
		'Metro PCS' : 'MyMetroPcs.com',
		'Nextel' : 'messaging.nextel.com',
		'Powertel' : 'ptel.net',
		'Sprint' : 'messaging.sprintpcs.com',
		'SunCom' : 'tms.suncom.com',
		'T-Mobile' : 'tmomail.net',
		'US Cellular' : 'email.uscc.net',
		'Verizon' : 'vtext.com',
		'Virgin Mobile' : 'vmobl.com'
		}
	for key, val in carrierExts.items():
		if carrier in key:
			extension.append(val)
