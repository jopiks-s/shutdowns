from os.path import exists
from datetime import datetime
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
site_access = False
token = {"incap_ses_1104_2224657": "ogkaDJHSnSfvQX0K7zJSD3j2u2MAAAAAaMfw8DCMaOuNZyqvNAd9+w=="}


async def site_pending() -> Dict | None:
    global site_access

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
                print(f"Unable access endpoint: {endpoint.geturl()}!")
                site_access = False
                return None
            if len(resp.headers) in [6, 7, 8]:
                print(f"Failed attempt n.{attempt}")
                print(f"Failed request to: {endpoint.geturl()}. Request again...")
                await asyncio.sleep(1)
            else:
                print(f"Successful request to: {endpoint.geturl()}")
                break

        raw_data = await resp.text()
        data = raw_data[raw_data.rfind('"data"'):raw_data.rfind('}}}}') + 3].replace('"data":', '')
        if len(data) == 0:
            print("Can`t find in response.text() DisconSchedule.preset['data']")
            site_access = False
            return None

        site_access = True
        return json.loads(data)

async def update_preset() -> bool:
    site_data = await site_pending()
    preset_exists = exists("preset_data.txt")
    curr_date = datetime.now().strftime("%Y/%m/%d %Hh")

    if site_data == None:
        print("Failed to update preset data!")
        if not preset_exists:
            with open("preset_data.txt", "w") as file:
                data = {"preset": {}, "update_date": curr_date}
                json.dump(data, file, indent=4)
        return False

    if not preset_exists:
        with open("preset_data.txt", "w") as file:
            data = {"preset": site_data, "update_date": curr_date}
            json.dump(data, file, indent=4)
    else:
        with open("preset_data.txt", "r+") as file:
            data: Dict = json.load(file)
            data["preset"] = site_data
            data["update_date"] = datetime.now().strftime("%Y/%m/%d %Hh")

            file.seek(0)
            json.dump(data, file, indent=4)
    print("Data updated successfully")
    return True


async def get_preset() -> Dict:

    data = {}
    if not exists("preset_data.txt"):
        await update_preset()
    with open("preset_data.txt", "r") as file:
        preset_data = json.load(file)
        last_update = datetime.strptime(preset_data["update_date"], "%Y/%m/%d %Hh")
        elapsed_h = int(str((datetime.now() - last_update)).split(":")[0])
        if elapsed_h > 12:
            await update_preset()

        file.seek(0)
        preset = json.load(file)["preset"]
        print(preset)
        return preset


# TODO replace time.sleep() to asyncio.sleep()
def get_schedule(address, house_number):
    endpoint = domain._replace(path="ua/ajax")
    chromedriver = r"chromedriver\chromedriver.exe"
    # week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


asyncio.run(get_preset())
