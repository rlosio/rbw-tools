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
    name = "dupremover"
    allowed_domains = ["trailburning.com"]
    start_urls = [
       "https://api.trailburning.com/v2/search?limit=10000&type=road_run",
       "https://api.trailburning.com/v2/search?limit=10000&type=trail_run"
    ]

    def parse(self, response):
      
      # fake parser to clean up database:
      # deleting races that where already exist one race with same date and same distance

            tb_url_delete_race = "https://api.trailburning.com/v2/races/"

            tb_resp_json = json.loads(response.text)
            now = datetime.now().strftime("%Y-%m-%d")
            for ev in tb_resp_json['body']['raceevents']:
                   raceList = list()                  
                   # we now loop on the races of every event and date
                   for race in ev['races']:
                       singleRace = str(race['distance']) + race['date'] 
                       # print singleRace
                       if singleRace in raceList:
                           raceToBeDeleted = tb_url_delete_race + race['id']
                           # calling now TB backend to delete the race
                           print raceToBeDeleted
                           requests.delete(raceToBeDeleted)
                              
                       else:
                           raceList.append(singleRace)
                                                
 #          item = RacebasetestItem()
 #          yield item
