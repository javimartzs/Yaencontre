from selenium import webdriver
from bs4 import BeautifulSoup
import requests

url = 'https://www.yaencontre.com/alquiler/pisos'

driver = webdriver.Chrome()
driver.get(url)

cookies = driver.get_cookies()

s = requests.Session()
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])

input()