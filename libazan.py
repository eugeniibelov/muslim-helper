import requests, os, time

l = os.get_terminal_size()[0]
def clear(): print('\033[H\033[2J', end='')

BAD_SYMBOLS = '«»?\/"'
s_download_all = 'Скачивание:'
s_download_url = "Получаем страницу: {}"
s_download_title = "\n'{}'\n-> '{}'"
s_download_title_short = "\n'{}'"
s_download_course_title = '-' * l + "\n'{}'\n" + '-' * l

p_course_title = r'<title>(.+)</title>'
p_page = r'href="\/durus\/.+?page=(\d+)"'
p_l_link = r'href="(\/audio\/download\/\d+)"'
p_l_title = r'(?:(?:player__)|(?:audio-))title">.*\d+[:.]\s?(.+)<\/div>'

p_l_title_link = r'(?:(?:player__)|(?:audio-))title">(.+)(?:</div>)[\s\w<>="\/\-:]+href="([\/\w]+)"'


#  Получаем urls из командной строки или из файла
def get_urls(url_list):
    urls = []
    for arg in url_list:
        #  Если аргумент - существующий файл
        #  то это файл со списком urls
        if os.path.exists(arg):
            file = open(arg, 'r')
            for url in file:
                #  Читаем его и выбираем строки
                urls.append(url.strip())
        else:
            #  Иначе расцениваем аргументы как адреса
            urls.append(arg)

    return urls


def remove_bad_symbols(s):
    #  for l in s:
        #  if l not it BAD_SYMBOLS:
    return ''.join([l for l in s if l not in BAD_SYMBOLS])

def save_file(title, data):
    with open(title, 'wb') as file:
        file.write(data)
    file.close()

def get_file(link, delay):
    r = ''
    rv = -1
    while rv != 0:
        try:
            r = requests.get(link)
            if r.status_code == 200:
                rv = 0
        except:
            rv = -1

        if rv == 0:
            print('...готово')
        else:
            print(f'...повтор через {delay}с')
            time.sleep(delay)
            delay += 2

    return r.content
