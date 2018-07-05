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
    name = "fixtrailtag"
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
                   name = ev['name'].lower().encode('utf-8')
                   racekeyword = 'trail'
                   evType = ev.get('type')
                   if evType == "road_run":
                       print ev['id'].encode('utf-8') + ' ' + name
                       if racekeyword in name:
                           evToUpdate = tb_url_update_event + ev['id']
                           tb_event_data = {"type" : "trail_run"}
                           # tb_event_data = {"type" : "road_run"}
                           requests.put(evToUpdate,tb_event_data)

                                                
 #          item = RacebasetestItem()
 #          yield item
