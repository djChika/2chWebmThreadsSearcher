import json
import re
import urllib.request
import webbrowser

from bs4 import BeautifulSoup

MAIN_URL = 'https://2ch.hk/b/threads.json'
BASEURL = 'http://2ch.hk/b/res/'
INCLUDE_KEYWORDS = r'([Ww][Ee][Bb][Mm])|([Цц][Уу][Ии][Ьь])|([ВвШш][Ее][Бб][Мм])|([Mm][Pp][4])|([Ьь][Зз][4])'
EXCLUDE_KEYWORDS = r'([Фф][Аа][Пп])|([Ff][Aa][Pp])'


def build_url_to_thread(num):
    return BASEURL + str(num) + ".html"


with urllib.request.urlopen(MAIN_URL) as url:
    board = json.loads(url.read().decode())

threads = board['threads']
urls_list = []

for thread in threads:
    thread_comment = thread['comment']
    soup = BeautifulSoup(thread_comment, "html.parser").get_text()
    comment_length = len(soup)
    thread_posts_count = thread['posts_count']
    if re.findall(INCLUDE_KEYWORDS, thread_comment) \
            and not re.findall(EXCLUDE_KEYWORDS, thread_comment) \
            and thread_posts_count > 20 \
            and comment_length < 200:
        num = thread['num']
        url = build_url_to_thread(num)
        urls_list.append(url)

print("Totally found " + str(len(urls_list)) + " WEBM thread(s):")
for url in urls_list:
    print(url)

if len(urls_list) > 0:
    print("Open...")
    for url in urls_list:
        webbrowser.open(url)
else:
    print("No WEBM threads found:(")
