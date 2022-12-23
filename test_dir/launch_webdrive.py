import selenium
from selenium import webdriver

if __name__ == "__main__":
    with webdriver.Chrome(executable_path=r"../chromedriver/chromedriver.exe") as chrome:
        input("close? ")