import sys

from bs4 import BeautifulSoup
import requests
import os
import subprocess
from bs4.element import Comment
import urllib.request
import time


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


offset = sys.argv[1]
os.environ['NO_PROXY'] = '127.0.0.1'
url = "http://127.0.0.1:800" + offset + '/warehouse_log'
# subprocess.call(" python server_stresser.py 1", shell=True)
req = requests.get(url)

soup = BeautifulSoup(req.text, 'html.parser')
texts = soup.findAll(text=True)

visible_texts = filter(tag_visible, texts)
u" ".join(t.strip() for t in visible_texts)

soup_list = soup.text.split('\n')
file = open("../warehouse_logfiles/warehouse_" + sys.argv[1] + ".data")
line_list = file.readlines()
for x, elem in enumerate(line_list):
    line_list[x] = elem.replace('\n', '')

soup_list = soup_list[::2]
cache = True
for x, elem in enumerate(line_list):
    if elem == soup_list[x]:
        continue
    else:
        print("Error, there was a problem detected at the following packet:")
        print("warehouse log: " + elem)
        print("http-server Log: " + soup_list[x])
        cache = False
        break
if cache:
    print("contents are identical")
