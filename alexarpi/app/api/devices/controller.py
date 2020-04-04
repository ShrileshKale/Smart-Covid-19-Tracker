# -*- coding: utf-8 -*-
from app import app
from flask import Response, request, render_template,redirect,url_for
from flask_ask import Ask, statement,question
import json
from bson import json_util
import RPi.GPIO as GPIO
import time
import sys
import os
from bs4 import BeautifulSoup
import requests
url ='https://www.worldometers.info/coronavirus/country/india/'
url1 ='https://www.worldometers.info/coronavirus/country/germany/'
state = True
arr=[] # to store the count value
ask = Ask(app, '/')
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
urls = [url,url1]
@ask.intent('ledcontrol')
def led(status):
	global covidIndia
	global covidGermany
	global state
	global arr
	try:
		if status == "on": # "status" is a slot in intent "ledcontrol and on is value of a slot"
			del arr[:] # deleting old values of count in timely manner
			for i in range (len(urls)):
				source = requests.get(urls[i]).text  # get 2 urls
				target=BeautifulSoup(source, 'lxml') #
				# web scrapping from worldometers.info website
				covidIndia = target.find_all('div', id_="maincounter-wrap")
				covidIndia = target.find('div', class_="maincounter-number").text.strip() # used strip() to discard blank lines
				covidIndia.encode('ascii', 'ignore')
				print ('CoronaVirus cases:-'+str(covidIndia))
				arr.append(str(covidIndia)) # appending count to arr array arr[0]=India's count ,arr[1]= Germany's count
				print 'arr'+str(arr)
		elif status == "off": # for slot value "off" 
			print ("in off state")
			return statement('Bye')
		state = False
		return statement('India has'+arr[0]+'Covid-19 positive patients'+'and Germany has'+arr[1]+'Covid-19 positive patients')

	except Exception as e:
		return statement('Error while fetching the data')

@app.route('/control-panel', methods=["GET"])
def controlPanel():
	global covidIndia
	global covidGermany
	global state
	global arr
	try:
		if state == False:
			print state
			if led("on"):
				print 'Inside Alexa front page'
				state = True
				return render_template('Alexa_main_page.html',val1=arr[0],val2=arr[1])
			else:
				return Response(json.dumps({
			"status": "failure-inside else part of led call",
			"message": "Invalid request:"
		}, default=json_util.default), mimetype="application/json")
		else:
			print ('Inside Waiting front page')
			return render_template('Alexa_waiting_page.html')
	except Exception, e:
		return Response(json.dumps({
			"status": "failure",
			"message": "Invalid request: %s" %e
		}, default=json_util.default), mimetype="application/json")




	
		





















