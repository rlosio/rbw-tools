import scrapy
import urlparse
import time
import googlemaps
import hashlib
import requests
import csv
import json

from racebasetest.items import RacebasetestItem
from datetime import datetime

class TrailRunnerComSpider(scrapy.Spider):
    name = "csvtype"
    allowed_domains = ["www.arsenio.it"]
    start_urls = [
        "http://www.arsenio.it"
    ]


    def parse(self, response):
      
      # fake parser to process a predefined CSV file with records such as
      # date, location, name, distance1-distance2,url
      # 2016-08-13,Whatever Hong Kong,Midsummer Race,10000-20000,http://xterace.com
      with open('/home/ubuntu/racebase/csv/hongkong-20160805.csv', 'rb') as f:
          reader = csv.reader(f)
          for row in reader:
	         # Race name
		 raceName = row[2]
                 tb_url_racevents = "https://api.trailburning.com/v2/raceevents/"
                 tb_url_search  = "https://api.trailburning.com/v2/search"
                 payload = {'q': raceName}
                 tb_resp_event = requests.get(tb_url_search, params=payload)
                 tb_resp_json = json.loads(tb_resp_event.text)
                 tb_json_size = tb_resp_json['meta']['count']
			
                # if event exists we need the id
                 if ( tb_json_size > 0):
                     existing_event = tb_resp_json['body']['raceevents'][0]['id']
                     evToUpdate = tb_url_racevents + existing_event
                     tb_raceevents_data = {"type": "trail_run"}
                     requests.put(evToUpdate, tb_raceevents_data)
		
