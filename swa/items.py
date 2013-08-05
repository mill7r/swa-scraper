# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Fare(Item):
	origin = Field()
	destination = Field()
	date = Field()
	flight = Field()
	arrive = Field()
	depart = Field()
	faretype = Field()
	price = Field()
	stops = Field()
	connectingArpts = Field()
	fareValidityDate = Field() 
	
