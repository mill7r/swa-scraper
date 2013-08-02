from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector.lxmlsel import HtmlXPathSelector
from scrapy import log
from datetime import datetime, timedelta
from dateutil.parser import parse as dateParse
import re

class Util(object):
	@classmethod
	def parseFlight(_class, string):
		""" General format:
		Departing flight    123(/456)   $0000    12:30AM depart    7:25AM arrive     (Non/1/2)stop    (Change planes in XXX)
		[always]			[flt1/2]    [price]  [departure]       [arrival]   		 [# stops] 		  [connection]
		"""

		removeKeywords = ['Departing flight', 'depart', 'arrive', 'Change Planes in', 'stop', 'stops', 'Plane Change']
		regex = '|'.join(removeKeywords)
		infoList = filter(lambda el: el!="", re.sub(regex, "", string).split(' '))

		stops = int(infoList[4]) if infoList[4] != 'Non' else 0	

		connectingArpts = infoList[5].split('/') if stops > 0 and infoList[5] != "No" else None

		flight = {
			'flight': infoList[0].split('/'),
			'price': infoList[1],
			'depart': infoList[2],
			'arrive': infoList[3],
			'stops': stops,
			'connectingArpts': connectingArpts
		}

		return flight

class SWAFareSpider(BaseSpider):
	"""A spider to scrape the Southwest site for fare pricing."""
	
	FORMNAME = "buildItineraryForm"
	name = 'southwest.com'
	start_urls = ['http://www.southwest.com/flight/search-flight.html']
	cities = ['GSP', 'FNT', 'BOS', 'OAK', 'LIT', 'BOI', 'SAN', 'DCA', 'LBB', 'BWI', 
	'PIT', 'RIC', 'SAT', 'JAX', 'IAD', 'JAN', 'HRL', 'CHS', 'EYW', 'BNA',
	'PHL', 'SNA', 'SFO', 'PHX', 'LAX', 'MAF', 'LAS', 'CRP', 'CMH', 'FLL', 
	'DEN', 'DTW', 'BUR', 'ROC', 'GEG', 'BUF', 'GRR', 'BDL', 'DSM', 'EWR', 
	'MHT', 'PBI', 'RNO', 'OKC', 'IND', 'ATL', 'ISP', 'SMF', 'BKG', 'PVD', 
	'SEA', 'ECP', 'ICT', 'MDW', 'RDU', 'PDX', 'CLE', 'SJU', 'AUS', 'CLT', 
	'SJC', 'ELP', 'OMA', 'MEM', 'TUS', 'ALB', 'TUL', 'ORF', 'MKE', 'MSY', 
	'MSP', 'CAK', 'TPA', 'DAL', 'DAY', 'ONT', 'STL', 'ABQ', 'HOU', 'SLC', 
	'MCO', 'RSW', 'BHM', 'MCI', 'PNS', 'LGA', 'AMA', 'SDF', 'PWM']
	
	def __init__(self, fromCity, date, toCity, *args, **kwargs):
		super(SWAFareSpider, self).__init__(**kwargs)
		self.origin = fromCity
		self.outDate = dateParse(date)
		self.destination = toCity
		
	@classmethod
	def lookupCity(_class, cityCode):
		if cityCode in _class.cities:
			return cityCode
		else:
			raise Exception("Invalid city specified.")	

			
	def buildQuery(self):
		"""Build the POST query string for searching flights."""
		queryData = {}
		
		queryData["twoWayTrip"] = "false"
		queryData["adultPassengerCount"] = "1"
		queryData["outboundTimeOfDay"] = "ANYTIME"
		queryData["fareType"] = "DOLLARS"
		
		queryData["originAirport"] = self.lookupCity(self.origin)
		queryData["destinationAirport"] = self.lookupCity(self.destination)
		queryData["outboundDateString"] = self.outDate.strftime("%m/%d/%Y")
			
		queryData["returnAirport"] = ""
		
		return queryData
		
	def parse(self, response):	
		queryData = self.buildQuery()

		return [FormRequest.from_response(response, formdata=queryData, formname=self.FORMNAME, callback=self.scrapeFlights)]
		

	def scrapeFlights(self, response):
		"""Scrape the flights into a Fare() object."""
		
		html = HtmlXPathSelector(response)

		# if ( "errors" in response.body ) :
		# 	theError = html.select("//ul[@id='errors']/li/text()")
		# 	self.log("Error: %s" % theError , level=log.ERROR)
		# 	return

		xpath = '//div[@class="productPricing"]/div/input/@title'
		
		flightList = html.select(xpath).extract()
		allFares = Route()
		allFares['fareList'] = list()
		
		for flightString in flightList:
			if ( flightString[0] == 'D' ):
				flightData = Util.parseFlight(flightString)
				self.log("Found: %s" % flightString)
				flight = Fare()		
				
				for	key in flightData:
					flight[key] = flightData[key]
				flight['origin'] = self.origin
				flight['destination'] = self.destination
				flight['date'] = self.outDate
				
				allFares['fareList'].append(flight)
				self.log('Added')
			else:
				return	
		return allFares
