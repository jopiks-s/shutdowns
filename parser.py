from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import urllib.parse



chromedriver = r"chromedriver\chromedriver.exe"

address = "Куренівська вул"
house_number = "14а"


# TODO replace time.sleep() to asyncio.sleep()
def get_schedule(address, house_number):
    endpoint = urllib.parse.urlparse("https://www.dtek-kem.com.ua")
    opts = Options()
    opts.add_argument(
        r"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
    # TODO replace context manager to async version
    with webdriver.Chrome(executable_path=chromedriver, chrome_options=opts) as driver:
        try:
            driver.get(domain)
            time.sleep(30)
            street = driver.find_element(By.ID, "street")
            house_num = driver.find_element(By.ID, "house_num")

            street.send_keys(address)
            time.sleep(1.5)
            street.send_keys(Keys.ENTER)
            time.sleep(1)
            house_num.send_keys(house_number)
            time.sleep(1.5)
            house_num.send_keys(Keys.ENTER)
            time.sleep(3)
            source = driver.page_source

            soup = BeautifulSoup(source, "html.parser")
            rows = soup.find_all("tr")[1:]
        except Exception as e:
            print(e)
            print("Can't load information from site!")
            return None

        week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        schedule = {}
        for day in week:
            schedule[day] = []

        shutdowns_periods = [[]]

        for i, row in enumerate(rows):
            time_range = row.find_next().find("div").text.replace(" – ", "-").split("-")
            shutdowns_periods[i].append(int(time_range[0].split(":")[0]))
            shutdowns_periods[i].append(int(time_range[1].split(":")[0]))
            shutdowns_periods.append([])
        shutdowns_periods.pop()

        for y, row in enumerate(rows):
            col = row.find_next().find("div").find_next()
            for x in range(7):
                if col["class"][0] == "cell-scheduled":
                    schedule[week[x]].append(shutdowns_periods[y])
                col = col.find_next()

        return schedule
