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
    name = "blacklist"
    allowed_domains = ["www.arsenio.it"]
    start_urls = [
        "http://www.arsenio.it"
    ]


    def parse(self, response):
      
      # fake parser to process a predefined CSV file with records such as
      # date, location, name, distance1-distance2,url
      # 2016-08-13,Whatever Hong Kong,Midsummer Race,10000-20000,http://xterace.com
      tb_url_search  = "https://api.trailburning.com/v2/search"
      tb_url_racevents = "https://api.trailburning.com/v2/raceevents"

      with open('/home/ubuntu/Dropbox/Race Photos/blacklist/blacklist.txt', 'rb') as f:
          reader = csv.reader(f)
          for row in reader:
			# Race name
			race_name = row[0]

                        payload = {'q': race_name}
                        tb_resp_event = requests.get(tb_url_search, params=payload)
                        tb_resp_json = json.loads(tb_resp_event.text)
                        tb_json_size = tb_resp_json['meta']['count']

                        # echo tb_json_size

                        # need to look on the events array
                        if ( tb_json_size < 1):
                           continue

                        for ev in tb_resp_json['body']['raceevents']:                       

                           if ( ev['name'] == race_name ):
                                  time.sleep(1)
                                  tb_raceevent_delete = tb_url_racevents + "/" + ev['id']                                 
                                  requests.delete(tb_raceevent_delete)
                                  continue 

