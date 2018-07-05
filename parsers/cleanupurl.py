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
    name = "cleanupurl"
    allowed_domains = ["trailburning.com"]
    start_urls = [
       "https://api.trailburning.com/v2/search?limit=10000&type=trail_run",
       "https://api.trailburning.com/v2/search?limit=10000&type=road_run"
    ]


    def parse(self, response):
      
      # fake parser to clean up database:
      # deleting all races in the past for any event when at least one race is available in the future

            tb_url_racevents = "https://api.trailburning.com/v2/raceevents/"

            tb_resp_json = json.loads(response.text)
            buggy_url = "marathons.ahotu.com/http"
            for ev in tb_resp_json['body']['raceevents']:
                 if 'website' in ev:
                      ev_url = ev['website']
                      # print ev_url
                      ev_id = ev['id']
                   
                      if ev_url.find(buggy_url) > 0:
                           print ev_url
                           new_url = ev_url[27:]  
                           # time.sleep(1)
                           tb_url_data = { "website": new_url }
                           tb_resp = requests.put(tb_url_racevents + ev_id, tb_url_data)
 #          item = RacebasetestItem()
 #          yield item
