import datetime
import os
import json
import requests
from glob import glob
from random import random
from time import sleep
from geopy.geocoders import Nominatim


TINDER_URL = "https://api.gotinder.com"
geolocator = Nominatim(user_agent="auto-tinder")


class Person(object):

    def __init__(self, data, api):
        self._api = api
        self.data = data

        self.id = data["_id"]
        self.name = data.get("name", "Unknown")

        self.bio = data.get("bio", "")
        self.distance = data.get("distance_mi", 0) / 1.60934

        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]
        
        self.images = list(map(lambda photo: photo["url"], data.get("photos", [])))

        self.jobs = list(
            map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")}, data.get("jobs", [])))
        self.schools = list(map(lambda school: school["name"], data.get("schools", [])))

        if data.get("pos", False):
            self.location = geolocator.reverse(f'{data["pos"]["lat"]}, {data["pos"]["lon"]}')

    def __repr__(self):
        return f"{self.id}  -  {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"

    def like(self):
        return self._api.like(self.id)

    def dislike(self):
        return self._api.dislike(self.id)
    
    @property
    def path(self):
        return f'downloads/{self.id}_{self.name}'
    
    def download_images(self, sleep_max_for=0):
        for idx, image_url in enumerate(self.images):
            req = requests.get(image_url, stream=True)
            if req.status_code == 200:
                path = self.path + f'/{idx}.jpeg'
                print(path)
                with open(path, "wb") as f:
                    f.write(req.content)
            sleep(random() * sleep_max_for)
            
    def local_images(self):
        return glob(self.path + '/*.jpeg')
    
    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(self.path + '/data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        self.download_images(sleep_max_for=random() * 3)
