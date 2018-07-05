import scrapy
import urlparse
import time
import googlemaps
import hashlib
import requests
import json
import requests_toolbelt
import os
from os.path import splitext
from datetime import datetime

class TrailRunnerComSpider(scrapy.Spider):
    name = "photouploader"
    allowed_domains = ["trailburning.com"]
    start_urls = [
       "https://api.trailburning.com/v2/search?limit=1"
    ]


    def parse(self, response):
      
        # fake parser to upload all race pictures from dropbox folder
        trailburning_endpoint = "https://api.trailburning.com/v2/raceevents/"

        directory = "/home/ubuntu/racebase/crawler-photo"
       
        for filename in os.listdir(directory):
             if filename.lower().endswith(".jpg"): 
                tb_event_id = splitext(filename)[0]
                print('Uploading picture ' + os.path.join(directory, filename))
                print('Race matching is ' + tb_event_id)

               # check if event exists
                media_endpoint = trailburning_endpoint + tb_event_id
                tb_resp = requests.get(media_endpoint)
                if tb_resp.status_code == 404:
                    print('Race Event not found for id ' + tb_event_id)
                    os.rename(os.path.join(directory, filename), os.path.join(directory + '/failed', filename))
                    continue

                # check if there are photos already
                # delete every photo before proceeding, we replace with new one
                tb_resp_json = json.loads(tb_resp.text)
                for media in tb_resp_json['body']['raceevents'][0]['medias']:
                     print('Media id to be deleted : ' + media['id']) 
                     media_endpoint = trailburning_endpoint + tb_event_id + "/media/" + media['id']
                     tb_resp = requests.delete(media_endpoint)

                # cleanup completed

                media_endpoint = trailburning_endpoint + tb_event_id + "/media"
                print(' API endpoint is ' + media_endpoint)
                files={'media': (filename, open(os.path.join(directory, filename),'rb'))}
                tb_resp = requests.post(media_endpoint, files=files)

                if tb_resp.status_code == 201:

                      media_endpoint = trailburning_endpoint + tb_event_id
                      tb_resp = requests.get(media_endpoint)
                      tb_resp_json = json.loads(tb_resp.text)
                      mediaId = tb_resp_json['body']['raceevents'][0]['medias'][0]['id']
                      print("Publish media " + mediaId)
                      media_endpoint = trailburning_endpoint + tb_event_id + "/media/" + mediaId
                      payload = {'publish':'true'}
                      tb_resp = requests.post(media_endpoint, payload)
                     
                      print("Removing picture " + filename)
                      print(tb_resp.text)

                      os.remove(os.path.join(directory, filename))
                else:
                      print(tb_resp.text)
                continue
             else:
                print('Filename not supported ' + os.path.join(directory, filename))
                continue


