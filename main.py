import json
import re
import urllib.request
import webbrowser


# SETTINGS
MAIN_URL = 'https://2ch.hk/b/threads.json'

BASEURL = 'http://2ch.hk/b/res/'

INCLUDE_KEYWORDS = r'([Ww][Ee][Bb][Mm])|' \
                   r'([Цц][Уу][Ии][Ьь])|' \
                   r'([ВвШш][Ее][Бб][Мм])|' \
                   r'([Mm][Pp][4])|' \
                   r'([Ьь][Зз][4])|' \
                   r'([Тт][Аа][Нн][Цц])'

EXCLUDE_KEYWORDS = r'([Фф][Аа][Пп])|' \
                   r'([Ff][Aa][Pp])|' \
                   r'([Dd][Aa][Rr][Kk])|' \
                   r'([Дд][Аа][Рр][Кк])|' \
                   r'([Bb][Ll][Aa][Cc][Kk])|' \
                   r'([Ww][Aa][Rr])|' \
                   r'([Вв][Аа][Рр])'

MAX_OP_POST_LENGTH = 200

MIN_POSTS_COUNT = 30


#SETTINGS


def build_url_to_thread(num):
    return BASEURL + str(num) + ".html"


with urllib.request.urlopen(MAIN_URL) as url:
    board = json.loads(url.read().decode())

threads = board['threads']
urls_list = []

for thread in threads:
    op_post = thread['subject']
    op_post_length = len(op_post)
    thread_posts_count = thread['posts_count']
    if re.findall(INCLUDE_KEYWORDS, op_post) \
            and not re.findall(EXCLUDE_KEYWORDS, op_post) \
            and thread_posts_count > MIN_POSTS_COUNT \
            and op_post_length < MAX_OP_POST_LENGTH:
        thread_num = thread['num']
        url = build_url_to_thread(thread_num)
        urls_list.append(url)

if len(urls_list):
    print("Totally found " + str(len(urls_list)) + " WEBM thread(s):")
    for url in urls_list:
        print(url)

    print("Open...")
    for url in urls_list:
        webbrowser.open(url)
else:
    print("No WEBM threads found :(")
