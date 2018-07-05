import scrapy
import urlparse
import time
import googlemaps
import hashlib
import requests
import json

from racebasetest.items import RacebasetestItem
from datetime import datetime

class TrailRunnerComSpider(scrapy.Spider):
    name = "alltag"
    allowed_domains = ["trailburning.com"]
    start_urls = [
        "https://api.trailburning.com/v2/search?limit=10000"
    ]

    def parse(self, response):
      
      # fake parser to clean up database:
      # deleting races that where already exist one race with same date and same distance

            tb_url_update_event = "https://api.trailburning.com/v2/raceevents/"

            tb_resp_json = json.loads(response.text)
            now = datetime.now().strftime("%Y-%m-%d")
            for ev in tb_resp_json['body']['raceevents']:
                   name = ev['name'].encode('utf-8')
                   event_type = ev.get('type') 
                   print 'type: ' + str(event_type) + ' - ' + name
