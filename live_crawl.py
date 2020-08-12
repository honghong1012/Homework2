from bs4 import BeautifulSoup
from mongoengine import *
import requests
import time
import pprint

response = requests.get("http://search.dangdang.com/?key=%C8%AB%B2%BF&act=input")
pprint.pprint(response.text)