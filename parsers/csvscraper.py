import scrapy
import urlparse
import time
import googlemaps
import hashlib
import requests
import csv

from racebasetest.items import RacebasetestItem
from datetime import datetime

class TrailRunnerComSpider(scrapy.Spider):
    name = "csv"
    allowed_domains = ["www.arsenio.it"]
    start_urls = [
        "http://www.arsenio.it"
    ]


    def parse(self, response):
      
      # fake parser to process a predefined CSV file with records such as
      # date, location, name, distance1-distance2,url
      # 2016-08-13,Whatever Hong Kong,Midsummer Race,10000-20000,http://xterace.com
      with open('/home/ubuntu/racebase/csv/xxxx', 'rb') as f:
          reader = csv.reader(f)
          for row in reader:
			# Race name
			race_name = row[0]

			# post the race event
			tb_raceevents_data = {"name": race_name, "website": race_url, "email": raceEmail, "coords": "(" + str(longitude) + "," + str(latitude) + ")" }
			tb_resp = requests.post(tb_url_racevents, tb_raceevents_data)

			# need the Location to post the race
			if tb_resp.status_code == 201:
			# we just need the final ID, not the path
				tb_raceevent_id = tb_resp.headers['Location']
				tb_url_races = "https://api.trailburning.com" + tb_raceevent_id + "/races"
				# looping on distances
					# Separate on comma.
				dists = race_distances.split("-")

				for dist in dists:
					tb_race_data = {"name" : race_name, "date": race_date, "distance": dist}
					tb_resp = requests.post(tb_url_races,tb_race_data)

                                item = RacebasetestItem()
				item['race'] = race_name
				item['url'] = race_url
				item['date'] = race_date
				item['distance'] = race_distances
				item['lat'] = latitude
				item['lng'] = longitude


			 	yield item
