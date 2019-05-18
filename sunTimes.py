#####################################################
#                                                   #
#                                                   #
#                sunTimes.py V2                     #
#               Author: RParkerE                    #
#               Date: 1/18/2016                     #
#                                                   #
#                                                   #
#####################################################

from weatherV2 import getLoc
from datetime import date
from math import *

def sunTimes():
	# Initialize your coordinates
	lati, longi = getLoc()
	
	# See if it is daylight savings time or not
	daylight = isDaylightSavings()
    
	#################################################### BEGIN NOAA SUNRTIMES ALGORITHIM ###########################################################
	D2R = pi/180
	R2D = 180/pi
    
	A = date.today().year/100
	B = A/4
	C = 2-A+B
	E = 365.25*(date.today().year+4716)
	F = 30.6001*(date.today().month+1)
	JD = C+date.today().day+E+F-1524.5
	JC = (JD-2451545)/36525
	longSun = int(280.46646+JC*(36000.76983+JC*0.0003032))%360
	anomSun = 357.52911+JC*(35999.05029-0.0001537*JC)
	eOrbit = 0.016708634-JC*(0.000042037+0.0000001267*JC)
	sunEqCtr = sin(D2R*(anomSun))*(1.914602-JC*(0.004817+0.000014*JC))+sin(D2R*(2*anomSun))*(0.019993-0.000101*JC)+sin(D2R*(3*anomSun))*0.000289
	trueLongSun = longSun+sunEqCtr
	trueAnomSun = anomSun+sunEqCtr
	sunRadVector = (1.000001018*(1-eOrbit*eOrbit))/(1+eOrbit*cos(D2R*(trueAnomSun)))
	sunAppLong = trueLongSun-0.00569-0.00478*sin(D2R*(125.04-1934.136*JC))
	obliqEcliptic = 23+(26+((21.448-JC*(46.815+JC*(0.00059-JC*0.001813))))/60)/60
	obliqCorr = obliqEcliptic+0.00256*cos(D2R*(125.04-1934.136*JC))
	sunAscen = R2D*(atan2(cos(D2R*(sunAppLong)), cos(D2R*(obliqCorr))*sin(D2R*(sunAppLong))))
	sunDeclin = R2D*(asin(sin(D2R*(obliqCorr))*sin(D2R*(sunAppLong))))
	varY = tan(D2R*(obliqCorr/2))*tan(D2R*(obliqCorr / 2))
	eqTime = 4*R2D*(varY*sin(2*D2R*(longSun))-2*eOrbit*sin(D2R*(anomSun))+4*eOrbit*varY*sin(D2R*(anomSun))*cos(2*D2R*(longSun))-0.5*varY*varY*sin(4*D2R*(longSun))-1.25*eOrbit*eOrbit*sin(2*D2R*(anomSun)))
	haSunrise = R2D*(acos(cos(D2R*(90.833))/(cos(D2R*(float(lati)))*cos(D2R*(sunDeclin)))-tan(D2R*(float(lati)))*tan(D2R*(sunDeclin))))
	if(daylight == True):
		solarNoon = (720-4*float(longi)-eqTime+(-5*60))/1440 #TODO: Change -5 to a method for finding timezone
		solarNoon = solarNoon+.041667
	else:
		solarNoon = (720-4*float(longi)-eqTime+(-5*60))/1440 #TODO: Change -5 to a method for finding timezone
	localRiseTime = (solarNoon*1440-haSunrise*4)/1440
	localSetTime = (solarNoon*1440+haSunrise*4)/1440
	##################################################### END NOAA SUNTIMES ALGORITHIM ############################################################
	# Convert the number returned by NOAA's algorithim into standard 24:00 time
	riseTime = convertToTime(localRiseTime)
	setTime = convertToTime(localSetTime)
	# Return local sunrise and sunset times
	return (riseTime, setTime)
	
def convertToTime(n):
	tmp = n*24
	newHour = floor(tmp)
	tmp = tmp-newHour
	tmp = tmp*60
	newMinute = floor(tmp)
	if(newMinute<10):
		convertedTime = str(int(newHour))+":0"+str(int(newMinute))
	else:
		convertedTime = str(int(newHour))+":"+str(int(newMinute))
	return convertedTime
	
def isDaylightSavings():
	marchSecondSunday = 0
	novFirstSunday = 0
	i = 8
	n = 1
    
	cent = floor(date.today().year/100)

	while(i<=14):
		i+=1
		if(marchSecondSunday!=0):
			marchSecondSunday = int((i+floor(2.6*3-0.2)-2*cent+date.today().year+floor(date.today().year/4)+floor(cent/4)))%7
		break
	while(n<=7):
		n+=1
		if(novFirstSunday!=0):
			novFirstSunday = int((i+floor(2.6*11-0.2)-2*cent+date.today().year+floor(date.today().year/4)+floor(cent/4)))%7
		break

	if (date.today().month==3):
		if (date.today().day>=i):
			daylight = True
	elif(date.today().month==11):
		if(date.today().day<=n):
			daylight = True
	elif(date.today().month>3):
		daylight = True
	elif(date.today().month<11):
		daylight = True
	else:
		daylight = False
	return daylight
