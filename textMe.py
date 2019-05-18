#####################################################
#                                                   #
#                                                   #
#                 textme.py V2                      #
#               Author: RParkerE                    #
#               Date: 1/18/2016                     #
#                                                   #
#                                                   #
#####################################################

from weatherV2 import getWeather
from sunTimesV2 import sunTimes
from emailCheckV2 import read
from email.mime.text import MIMEText
import smtplib

def text(numstring, carrier, host, user, password):
	# Initialize variables
	hi, lo = getWeather()
	rise, set = sunTimes()
	msgs = read(host, user, password)
	ext = getCarrierExt(carrier)
	
	# Make message to sned
	message = "Today's High: " + hi + ", Today's Low: " + lo + ", Sunrise is at: " + rise + ", Sunset is at: " + set + ", You have " + msgs + " unread messages"
	# Create MIME object
	message = MIMEText(message)
	# Create email address
	email = user + '@' + host
	# Create email for phone number
	phone = str(numstring) + '@' + ext
	message['From'] = email
	message['To'] = phone
	
	# Get SMTP server for the host
	host = "smtp." + host.lower()
	# Connect to the SMTP server
	server = smtplib.SMTP(host, 587)
	# Start TLS communication
	server.starttls()
	# Login to given account 
	server.login(user, password)
	# Send email to phone from given account
	server.sendmail(email, phone, message.as_string())
	# End connection to the server
	server.quit()

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
		if carrier.title() in key:
			return (val)
