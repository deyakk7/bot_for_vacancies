import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as BS
from decouple import config
from telebot import TeleBot

bot = TeleBot(config('TOKEN', ''))
channel_id = config('CHANNEL_ID', '')

djinni_url = config('DJINNI_URL', '')
work_ua_url = config('WORK_UA_URL', '')

BASE_URL_DJINNI = "https://djinni.co/"
BASE_WORK_UA_URL = 'https://www.work.ua/'


TO_STOP = False


@bot.message_handler(commands=['start'])
def start(message):
    latest_post_id_djinni = '0'
    latest_post_id_work_ua = '0'
    bot.send_message(message.chat.id, 'Started')
    while True:
        global TO_STOP
        if TO_STOP:
            time.sleep(2)
            TO_STOP = False
            break

        # Djinni
        data_post_djinni = parser_djinni(latest_post_id_djinni)
        if data_post_djinni[1] is not None:
            bot.send_message(channel_id, data_post_djinni[1])
        time.sleep(3)

        latest_post_id_djinni = data_post_djinni[0]

        # Work.ua

        data_post_work_ua = parser_work_ua(latest_post_id_work_ua)
        if data_post_work_ua[1] is not None:
            bot.send_message(channel_id, data_post_work_ua[1])
        time.sleep(3)
        latest_post_id_work_ua = data_post_work_ua[0]


@bot.message_handler(commands=['stop'])
def stop(message):
    global TO_STOP
    TO_STOP = True
    bot.send_message(message.chat.id, 'Stopped')


def parser_work_ua(latest_post_id):
    # Get to work.ua
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 "
                      "Safari/537.36",
    }
    r = requests.get(work_ua_url, headers=headers)
    html = BS(r.content, 'html.parser')

    # Get list of jobs
    last_job = html.find('div', {'id': 'pjax-jobs-list'})
    post_id = last_job.find('a')['name'].strip()

    # Check working
    print(post_id)

    # Check that is a new post
    if post_id != latest_post_id:
        data = ''
        title = last_job.find('div', class_='job-link').find('a')
        url = title['href']
        title = title.text.strip()
        data += title + '\n\n'
        price = last_job.find('div', class_=None)

        if price is not None:
            price = price.text.strip()
            data += price + '\n'
        company = last_job.find('span', class_='add-right-xs').text.strip()
        data += company + '\n\n'
        description = last_job.find('p', class_='ellipsis ellipsis-line ellipsis-line-3 text-default-7 cut-bottom').text
        description = ' '.join(description.split())

        data += description + '\n\n'

        data += urljoin(BASE_WORK_UA_URL, url)
        return post_id, data

    return post_id, None


def parser_djinni(latest_post_id):
    # get to djinni
    r = requests.get(djinni_url)
    html = BS(r.content, 'html.parser')

    # find latest job post
    last_job = html.find('li', class_='list-jobs__item job-list__item')
    post_id = last_job['id'].strip()
    print(post_id)

    # Check that is a new post
    if latest_post_id != post_id:
        print('here we go')
        info = last_job.find(
            'div', class_='job-list-item__job-info font-weight-500').text.strip()

        title = last_job.find(
            'a', class_='h3 job-list-item__link'
        ).text.strip()

        post_url = urljoin(BASE_URL_DJINNI, last_job.find(
            'a', class_='h3 job-list-item__link', href=True,
        )['href'])

        data = title + '\n\n' + info + '\n\n' + post_url
        return post_id, data

    return post_id, None


if __name__ == '__main__':
    bot.infinity_polling()
