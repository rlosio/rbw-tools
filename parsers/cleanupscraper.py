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
    name = "cleanup"
    allowed_domains = ["trailburning.com"]
    start_urls = [
       "https://api.trailburning.com/v2/search?limit=10000&type=road_run",
       "https://api.trailburning.com/v2/search?limit=10000&type=trail_run"
    ]


    def parse(self, response):
      
      # fake parser to clean up database:
      # deleting all races in the past for any event when at least one race is available in the future

            tb_url_delete_race = "https://api.trailburning.com/v2/races/"

            tb_resp_json = json.loads(response.text)
            now = datetime.now().strftime("%Y-%m-%d")
            for ev in tb_resp_json['body']['raceevents']:
                   # we now loop on the races of every event
                   # first we check if we should skip the event
                   futureRaces = None
                   for race in ev['races']:
                       if (race['date'] >= now):
                            futureRaces = True

                   # if we have at least one race in the future delete old ones
                   if futureRaces:
                           for race in ev['races']:
                                if (race['date'] < now):
                                    # we delete the race with the given id
                                    raceToBeDeleted = tb_url_delete_race + race['id'] 
                                    # calling now TB backend to delete the race
                                    print raceToBeDeleted
                                    requests.delete(raceToBeDeleted)        

                                                
 #          item = RacebasetestItem()
 #          yield item
