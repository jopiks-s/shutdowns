from typing import Dict
import aiohttp
import asyncio
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import urllib.parse

address_t = "Куренівська вул"
house_number_t = "14а"

domain = urllib.parse.urlparse("https://www.dtek-kem.com.ua")

test_str = '"data":{"1":{"1":{"1":"no","2":"no","3":"no","4":"no","5":"yes","6":"yes","7":"maybe","8":"maybe","9":"maybe","10":"no","11":"no","12":"no","13":"no","14":"yes","15":"yes","16":"maybe","17":"maybe","18":"maybe","19":"no","20":"no","21":"no","22":"no","23":"yes","24":"yes"},"2":{"1":"maybe","2":"maybe","3":"maybe","4":"no","5":"no","6":"no","7":"no","8":"yes","9":"yes","10":"maybe","11":"maybe","12":"maybe","13":"no","14":"no","15":"no","16":"no","17":"yes","18":"yes","19":"maybe","20":"maybe","21":"maybe","22":"no","23":"no","24":"no"},"3":{"1":"no","2":"yes","3":"yes","4":"maybe","5":"maybe","6":"maybe","7":"no","8":"no","9":"no","10":"no","11":"yes","12":"yes","13":"maybe","14":"maybe","15":"maybe","16":"no","17":"no","18":"no","19":"no","20":"yes","21":"yes","22":"maybe","23":"maybe","24":"maybe"},"4":{"1":"no","2":"no","3":"no","4":"no","5":"yes","6":"yes","7":"maybe","8":"maybe","9":"maybe","10":"no","11":"no","12":"no","13":"no","14":"yes","15":"yes","16":"maybe","17":"maybe","18":"maybe","19":"no","20":"no","21":"no","22":"no","23":"yes","24":"yes"},"5":{"1":"maybe","2":"maybe","3":"maybe","4":"no","5":"no","6":"no","7":"no","8":"yes","9":"yes","10":"maybe","11":"maybe","12":"maybe","13":"no","14":"no","15":"no","16":"no","17":"yes","18":"yes","19":"maybe","20":"maybe","21":"maybe","22":"no","23":"no","24":"no"},"6":{"1":"no","2":"yes","3":"yes","4":"maybe","5":"maybe","6":"maybe","7":"no","8":"no","9":"no","10":"no","11":"yes","12":"yes","13":"maybe","14":"maybe","15":"maybe","16":"no","17":"no","18":"no","19":"no","20":"yes","21":"yes","22":"maybe","23":"maybe","24":"maybe"},"7":{"1":"no","2":"no","3":"no","4":"no","5":"yes","6":"yes","7":"maybe","8":"maybe","9":"maybe","10":"no","11":"no","12":"no","13":"no","14":"yes","15":"yes","16":"maybe","17":"maybe","18":"maybe","19":"no","20":"no","21":"no","22":"no","23":"yes","24":"yes"}},"2":{"1":{"1":"maybe","2":"maybe","3":"maybe","4":"no","5":"no","6":"no","7":"no","8":"yes","9":"yes","10":"maybe","11":"maybe","12":"maybe","13":"no","14":"no","15":"no","16":"no","17":"yes","18":"yes","19":"maybe","20":"maybe","21":"maybe","22":"no","23":"no","24":"no"},"2":{"1":"no","2":"yes","3":"yes","4":"maybe","5":"maybe","6":"maybe","7":"no","8":"no","9":"no","10":"no","11":"yes","12":"yes","13":"maybe","14":"maybe","15":"maybe","16":"no","17":"no","18":"no","19":"no","20":"yes","21":"yes","22":"maybe","23":"maybe","24":"maybe"},"3":{"1":"no","2":"no","3":"no","4":"no","5":"yes","6":"yes","7":"maybe","8":"maybe","9":"maybe","10":"no","11":"no","12":"no","13":"no","14":"yes","15":"yes","16":"maybe","17":"maybe","18":"maybe","19":"no","20":"no","21":"no","22":"no","23":"yes","24":"yes"},"4":{"1":"maybe","2":"maybe","3":"maybe","4":"no","5":"no","6":"no","7":"no","8":"yes","9":"yes","10":"maybe","11":"maybe","12":"maybe","13":"no","14":"no","15":"no","16":"no","17":"yes","18":"yes","19":"maybe","20":"maybe","21":"maybe","22":"no","23":"no","24":"no"},"5":{"1":"no","2":"yes","3":"yes","4":"maybe","5":"maybe","6":"maybe","7":"no","8":"no","9":"no","10":"no","11":"yes","12":"yes","13":"maybe","14":"maybe","15":"maybe","16":"no","17":"no","18":"no","19":"no","20":"yes","21":"yes","22":"maybe","23":"maybe","24":"maybe"},"6":{"1":"no","2":"no","3":"no","4":"no","5":"yes","6":"yes","7":"maybe","8":"maybe","9":"maybe","10":"no","11":"no","12":"no","13":"no","14":"yes","15":"yes","16":"maybe","17":"maybe","18":"maybe","19":"no","20":"no","21":"no","22":"no","23":"yes","24":"yes"},"7":{"1":"maybe","2":"maybe","3":"maybe","4":"no","5":"no","6":"no","7":"no","8":"yes","9":"yes","10":"maybe","11":"maybe","12":"maybe","13":"no","14":"no","15":"no","16":"no","17":"yes","18":"yes","19":"maybe","20":"maybe","21":"maybe","22":"no","23":"no","24":"no"}},"3":{"1":{"1":"no","2":"yes","3":"yes","4":"maybe","5":"maybe","6":"maybe","7":"no","8":"no","9":"no","10":"no","11":"yes","12":"yes","13":"maybe","14":"maybe","15":"maybe","16":"no","17":"no","18":"no","19":"no","20":"yes","21":"yes","22":"maybe","23":"maybe","24":"maybe"},"2":{"1":"no","2":"no","3":"no","4":"no","5":"yes","6":"yes","7":"maybe","8":"maybe","9":"maybe","10":"no","11":"no","12":"no","13":"no","14":"yes","15":"yes","16":"maybe","17":"maybe","18":"maybe","19":"no","20":"no","21":"no","22":"no","23":"yes","24":"yes"},"3":{"1":"maybe","2":"maybe","3":"maybe","4":"no","5":"no","6":"no","7":"no","8":"yes","9":"yes","10":"maybe","11":"maybe","12":"maybe","13":"no","14":"no","15":"no","16":"no","17":"yes","18":"yes","19":"maybe","20":"maybe","21":"maybe","22":"no","23":"no","24":"no"},"4":{"1":"no","2":"yes","3":"yes","4":"maybe","5":"maybe","6":"maybe","7":"no","8":"no","9":"no","10":"no","11":"yes","12":"yes","13":"maybe","14":"maybe","15":"maybe","16":"no","17":"no","18":"no","19":"no","20":"yes","21":"yes","22":"maybe","23":"maybe","24":"maybe"},"5":{"1":"no","2":"no","3":"no","4":"no","5":"yes","6":"yes","7":"maybe","8":"maybe","9":"maybe","10":"no","11":"no","12":"no","13":"no","14":"yes","15":"yes","16":"maybe","17":"maybe","18":"maybe","19":"no","20":"no","21":"no","22":"no","23":"yes","24":"yes"},"6":{"1":"maybe","2":"maybe","3":"maybe","4":"no","5":"no","6":"no","7":"no","8":"yes","9":"yes","10":"maybe","11":"maybe","12":"maybe","13":"no","14":"no","15":"no","16":"no","17":"yes","18":"yes","19":"maybe","20":"maybe","21":"maybe","22":"no","23":"no","24":"no"},"7":{"1":"no","2":"yes","3":"yes","4":"maybe","5":"maybe","6":"maybe","7":"no","8":"no","9":"no","10":"no","11":"yes","12":"yes","13":"maybe","14":"maybe","15":"maybe","16":"no","17":"no","18":"no","19":"no","20":"yes","21":"yes","22":"maybe","23":"maybe","24":"maybe"}}}'


async def site_pending(token: Dict) -> Dict | None:
    endpoint = domain._replace(path="/ua/shutdowns")
    data = {}

    # TODO replace print to logging
    async with aiohttp.ClientSession() as sess:
        sess.cookie_jar.update_cookies(token)
        attempt = 0
        while True:
            resp = await sess.get(endpoint.geturl())
            print(len(resp.headers))
            attempt += 1
            if attempt >= 30:
                print(f"Unable access endpoint: {endpoint.geturl()}, and update data!")
                return None
            if len(resp.headers) in [6, 8]:
                print(f"Failed request to: {endpoint.geturl()}. Request again...")
                await asyncio.sleep(1)
            else:
                break

        raw_data = await resp.text()
        data = json.loads(raw_data[raw_data.rfind('"data"'):raw_data.rfind('}}}}') + 3].replace('"data":', ''))

        return data


async def get_preset(token: Dict) -> Dict:
    from datetime import datetime
    from os.path import exists

    data = {}
    if not exists("preset_data.txt"):
        data = await site_pending(token)
        with open("preset_data.txt", "w") as file:
            data = {"preset": data, "update_date": datetime.now().strftime('%ed %Hh').strip()}
            json.dump(data, file, indent=4)
    else:
        with open("preset_data.txt") as file:
            file = json.load(file)
            last_update = file["update_date"]
            time_diff = datetime.now() - datetime.strptime(last_update, '%dd %Hh')
            print(time_diff)

    return {}


# TODO replace time.sleep() to asyncio.sleep()
def get_schedule(address, house_number):
    endpoint = domain._replace(path="ua/ajax")
    chromedriver = r"chromedriver\chromedriver.exe"
    # week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


asyncio.run(get_preset({"incap_ses_1104_2224657": "JQxxALeLHSRN9OUI7zJSD4RGuWMAAAAAEq7fd/+sV7bXS8SOVHUaFQ=="}))
