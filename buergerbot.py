#! /usr/bin/env python3
import bs4
import requests
import time

from pyshorteners import Shortener

url = 'http://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&dienstleister%5B%5D=122210&dienstleister%5B%5D=122217&dienstleister%5B%5D=122219&dienstleister%5B%5D=122227&dienstleister%5B%5D=122231&dienstleister%5B%5D=122238&dienstleister%5B%5D=122243&dienstleister%5B%5D=122252&dienstleister%5B%5D=122260&dienstleister%5B%5D=122262&dienstleister%5B%5D=122254&dienstleister%5B%5D=122271&dienstleister%5B%5D=122273&dienstleister%5B%5D=122277&dienstleister%5B%5D=122280&dienstleister%5B%5D=122282&dienstleister%5B%5D=122284&dienstleister%5B%5D=122291&dienstleister%5B%5D=122285&dienstleister%5B%5D=122286&dienstleister%5B%5D=122296&dienstleister%5B%5D=150230&dienstleister%5B%5D=122301&dienstleister%5B%5D=122297&dienstleister%5B%5D=122294&dienstleister%5B%5D=122312&dienstleister%5B%5D=122314&dienstleister%5B%5D=122304&dienstleister%5B%5D=122311&dienstleister%5B%5D=122309&dienstleister%5B%5D=317869&dienstleister%5B%5D=324433&dienstleister%5B%5D=325341&dienstleister%5B%5D=324434&dienstleister%5B%5D=324435&dienstleister%5B%5D=122281&dienstleister%5B%5D=324414&dienstleister%5B%5D=122283&dienstleister%5B%5D=122279&dienstleister%5B%5D=122276&dienstleister%5B%5D=122274&dienstleister%5B%5D=122267&dienstleister%5B%5D=122246&dienstleister%5B%5D=122251&dienstleister%5B%5D=122257&dienstleister%5B%5D=122208&dienstleister%5B%5D=122226&anliegen%5B%5D=120686&herkunft=%2Fterminvereinbarung%2F'
termin_url = 'http://service.berlin.de/terminvereinbarung/termin'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1) ',
    'Accept-Encoding': ', '.join(('gzip', 'deflate')),
    'Accept': '*/*',
    'Connection': 'keep-alive',
}

services = ['Tinyurl', 'Isgd']

while True:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print('Something went wrong')
        break

    body = bs4.BeautifulSoup(response.content, 'html.parser')
    months = body.select('.calendar-month-table')
    for month in months:
        links = month.select('td.buchbar a')
        if links:
            print('\t\t{}\n'.format(month.find('th', attrs={'class': 'month'}).text))
            for i, link in enumerate(links):
                service = i % len(services)
                try:
                    day_url = Shortener(services[service]).short('{}/{}'.format(termin_url, link['href']))
                except requests.exceptions.ReadTimeout:
                    day_url = '{}/{}'.format(termin_url, link['href'])
                print('\t{} -> {}'.format(link.text, day_url))
                time.sleep(0.1)
            print('\n\n')
    print('#'*80)
    print('Retrying in 60 seconds...')

    time.sleep(60)
