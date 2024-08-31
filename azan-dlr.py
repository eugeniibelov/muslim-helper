#!/usr/bin/env python3

import sys, os, re, tempfile, argparse
from libazan import *

PROG_NAME = 'azan_dlr.py'
VERSION = '0.0.4-1'
CACHE_DIR = os.path.join(os.path.dirname(__file__), '.cache')
DELAY = 5

l_title_link_pattern = re.compile(p_l_title_link)
course_title_pattern = re.compile(p_course_title)
l_title_pattern = re.compile(p_l_title)
l_link_pattern = re.compile(p_l_link)
page_pattern = re.compile(p_page)

if os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)
parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description='Downloader of audio lessons from Azan.ru and Azan.kz'
        )

parser.add_argument('urls', action='extend', nargs="+", type=str, help='Get file with urls or list of urls')
parser.add_argument('--version', action='version', version=f'VERSION: v{VERSION}')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose info messages', default=False)
parser.add_argument('-d', '--dry-run', action='store_true', help='Emulate downloading')
parser.add_argument('-p', '--path', action='store', type=str, help='Set path for downloaded lessons', default='.')

args = parser.parse_args()

URLS = get_urls(args.urls)

clear()
# Для каждого url из списка
for url in URLS:
    page = 1            # Текущая страница
    pages = 1           # Количество страниц
    course_title = ''   # Название курса
    links = dict()      # Словарь для названий и ссылок
    l_title = ''   # Вспомогательные переменные для 
    l_link = ''    # Заполнения словаря

    # Временный файл для хранения содержимого страницы
    tmp = tempfile.NamedTemporaryFile()

    # Пока не достигнем последней страницы
    while page <= pages:
        # Полный адрес текущей страницы
        link = url + f'?page={page}'

        if args.verbose:
            print(s_download_url.format(link), end='')
        else:
            print(s_download_url.format(page), end='')

        # Скачиваем и сохраняем страницу во временный файл
        save_file(tmp.name, get_file(link, DELAY))

        # Открываем временный файл
        # Построчно читаем его
        # И узнаем количество страниц для перехода
        file = open(tmp.name, 'r')

        if pages == 1:
            for line in file:
                match = page_pattern.search(line)
                if match:
                    pages = int(match[1])

            # Возвращаемся в начало файла
            file.seek(0)

        # Опять построчно читаем файл
        # И находим название курса
        for line in file:
            if len(course_title) == 0:
                match = course_title_pattern.search(line)
                if match:
                    course_title = match[1]
                    course_title = remove_bad_symbols(match[1])

            #  В каждой строчке ищем название урока 
            #  или ссылку для скачивание
            if len(l_title) == 0:
                match = l_title_pattern.search(line)
                if match:
                    l_title = match[1]
                    l_title = remove_bad_symbols(match[1])

            if len(l_link) == 0 and len(l_title) > 0:
                match = l_link_pattern.search(line)
                if match:
                    l_link = url[:15] + match[1]

            #  Заносим ссылку и сбрасываем названия
            if len(l_title) > 0 and len(l_link) > 0:
                l_title = str(len(links) + 1).zfill(2) + '. ' + l_title + '.mp3'
                links[l_title] = l_link

                l_title = ''
                l_link =  ''

        # Переходим на следующую страницу
        page += 1

    # Закрываем файл
    file.close()
    tmp.close()


    # На этом этапе файл все файлы закрыты
    # Далее работаем со словарем, содержащим ссылки 
    course_path = os.path.join(args.path, course_title)

    print(s_download_course_title.format(course_title), end='')

    if not args.dry_run:
        if not os.path.exists(course_path):
            os.mkdir(course_path)

    for title, link in links.items():
        file_path = os.path.join(course_path, title)
        rv = -1

        if args.verbose:
            print(s_download_title.format(link, file_path), end='')
        else:
            print(s_download_title_short.format(title), end='')

        if not args.dry_run:
            if not os.path.exists(file_path):
                save_file(file_path, get_file(link, DELAY))
        else:
            print()
    print()
