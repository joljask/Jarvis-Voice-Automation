import requests
from jarvis_voiceassistant import speak
import inflect
import re

from database import append_csv


from pprint import pprint
def weather_data(query):
	res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric')
	return res.json()
def print_weather(result,city):
	p = inflect.engine()
	temperature = str("{}'s temperature {}°Celcius ".format(city,result['main']['temp']))
	t = str(temperature)
	temp = re.findall(r'\d+', t)
	res = list(map(int, temp))
	ntw = "temperature is " + p.number_to_words(res[0])

	speak(ntw)
	append_csv(ntw)
	#print("Wind speed: {} m/s".format(result['wind']['speed']))
	#print("Description: {}".format(result['weather'][0]['description']))
	#print("Weather: {}".format(result['weather'][0]['main']))
def main():
	city="bangalore"
	print()
	try:
	  query='q='+city
	  w_data=weather_data(query)
	  print_weather(w_data, city)
	  print()
	except:
	  print('City not found...')
if __name__=='__main__':
	main()
