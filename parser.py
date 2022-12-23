from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests

url = "https://www.dtek-kem.com.ua/ua/shutdowns"
# cookies = {
#     "cookie": 'Domain=dtek-kem.com.ua; _language=1f011804d107a9f0f6fa36417ed49140e5bc2106c740e65666f3a94e857201cca:2:{i:0;s:9:"_language";i:1;s:2:"uk";}; _csrf-dtek-kem=593985e8da4221f688f2449a28a169f6a93c2b2af8cee543ab5c83dfbafcfe5ca:2:{i:0;s:14:"_csrf-dtek-kem";i:1;s:32:"igln4Z3fO2k5j7v_4xh9tmxfNGoc4-mD";}; visid_incap_2224657=4Ztj4DNvQ+eKgVezy+N73CqTZWMAAAAAQUIPAAAAAAAjGbP7I4Gk0Uwa1DfxQlaJ; nlbi_2224657=xJH+Le6boVtdgtZN8ri73wAAAAAVRlmCz7vnBTsrOtby5FtW; Domain=dtek-kem.com.ua; incap_ses_287_2224657=X8AAXQuYkXc6YU40WqH7AyeRcmMAAAAAalPViAbY+MmgdXG5UasSiw==; incap_ses_7228_2224657=pbq/MRQ1LhdEnvAXQARPZCtpc2MAAAAAEn4z2rhctmKqEsPZ/e57IA==; incap_ses_1613_2224657=wdNeIErkuCfdNxV/GYdiFthrc2MAAAAA3vEusQjpx5xreehwdMcA3A==; dtek-kem=kutoha4qf55mqiks18f3fpp39p; nlbi_2224657_2147483392=tQljPA6TgC/+tNwq8ri73wAAAAB+kh5pTuamlnm3CsSZmes+; reese84=3:Yt016O8sibPi4zx4G7uGyg==:Bo5hfOYejJvpCgAM3vgWs0+FZkHm6LAb7vUdHyy/flwk0yzk/AuvpOr5/0t83gzEoqtPhTKy+ZDxIU9rXxtJhAFBTrJT6z9+ZF29WYdHMlmLiL/WGtqcQdlV+3QfushDSzMybwEBNQPd22GMncmvnER2aMT0o4501bHwUuppk9ir9VltKA6yfQlAeQWOLSTv4Z5goIb0q8Nmg0Zi8IS5WqPu/6rZ0E/ylJtbV/6nmQkGHatWKEcpnwQImHtNeM6rZC6v3SZK8NBnrGgrS4l5QZUSzkw2FzVj7NO3LpuRMNdmLAv9U7DnQ9SSYydO8g4v8jX5OUux+SvDZAx49ZLjLydTf2MtpfmkftKz07qwvnKdfBya73BLLT6ftxIzpdErnDCbNYJjm4OdVloHbIfvGTAhLYxP/y0JjmVxxPTUaBOyYPjXkXX+8vL25tXwYIa/yqbbTwy1feyjJ+sqSQrImXnBLUj9tb6Y0rTc3LnNjms=:xo/xIthgNh+dO7BdhcsqBi1R00VyN7uJOdBMPd/nPGU='}

requests.get(url)

chromedriver = r"chromedriver\chromedriver.exe"

address = "Куренівська вул"
house_number = "14а"


# TODO replace time.sleep() to asyncio.sleep()
def get_schedule(address, house_number):
    opts = Options()
    opts.add_argument(
        r"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
    # TODO replace context manager to async version
    with webdriver.Chrome(executable_path=chromedriver, chrome_options=opts) as driver:
        try:
            driver.get(url)
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
