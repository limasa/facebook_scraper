from bs4 import BeautifulSoup
import requests
import datetime


def get_data(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    post_single_list = []
    post_list = []
    post_id_list = []
    post_dict = {}

    for post_div in soup.find_all('div', {'class': ['_1dwg _1w_m _q7o']}):
        for p in post_div.find_all('p'):
            post_single_list.append(p.text)
        post_list.append(post_single_list)
        post_single_list = []

    for id in soup.find_all('div', {'class': ['_5pcp _5lel _2jyu _232_']}):
        if len(id['id']) > 40:
            post_id_list.append(id['id'])

    for key in post_id_list:
        for value in post_list:
            post_dict[key] = ', '.join(value)
            post_list.remove(value)
            break

    return post_dict


def page_name(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    return soup.title.text.split('-')[0]


def get_time(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    id_list = []

    for tag in soup.find_all('div', class_="_5pcp _5lel _2jyu _232_"):
        if len(tag["id"]) > 40:
            id_list.append(tag["id"])

    time_list = []
    page_time_list = []

    for a in soup.find_all('div', class_="clearfix _42ef"):
        for abbr in a.select('abbr'):
            time_list.append(abbr.get("data-utime"))

    for time in time_list:
        page_time_list.append(datetime.datetime.fromtimestamp(int(time)
                                                              ).strftime('%d.%m.%Y %H:%M'))
    post_time = {}
    for key in id_list:
        for value in page_time_list:
            post_time[key] = ''.join(value)
            page_time_list.remove(value)
            break

    return post_time


def page_img_link(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    page_img_link = ''

    for a in soup.find_all("img"):
        page_img_link = a['src']
        break
    return page_img_link


def page_id(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    for id in soup.find_all('div', {'class': ['_5pcp _5lel _2jyu _232_']}):
        if len(id['id']) > 40:
            return id['id'].split('_')[2].split(';')[0]
