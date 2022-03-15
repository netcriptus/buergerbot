#! /usr/bin/env python3
import os
import time

import requests

import bs4
from pyshorteners import Shortener
# TODO: fix playsound for linux
# from playsound import playsound

url = "https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]=120686&dienstleisterlist=122210,122217,327316,122219,327312,122227,327314,122231,122243,327348,122252,329742,122260,329745,122262,329748,122254,329751,122271,327278,122273,327274,122277,327276,330436,122280,327294,122282,327290,122284,327292,327539,122291,327270,122285,327266,122286,327264,122296,327268,150230,329760,122301,327282,122297,327286,122294,327284,122312,329763,122314,329775,122304,327330,122311,327334,122309,327332,122281,327352,122279,329772,122276,327324,122274,327326,122267,329766,122246,327318,122251,327320,122257,327322,122208,327298,122226,327300&herkunft=http%3A%2F%2Fservice.berlin.de%2Fdienstleistung%2F120686%2F"
termin_url = "http://service.berlin.de"

shortener = Shortener()
services = ["chilpit", "clckru", "dagd", "isgd", "tinyurl"]
global_link_counter = 0
retry_time = 10


def mount_url(date_link):
    return "{}{}".format(url, date_link)

def get_month_name(html_month_tag):
    return html_month_tag.find("th", attrs={"class": "month"}).text


def shorten_url(long_url_tag):
    global global_link_counter
    service = global_link_counter % len(services)
    short_url = mount_url(long_url_tag["href"])
    global_link_counter += 1
    try:
        return getattr(shortener, services[service]).short(short_url)
    except (requests.exceptions.ReadTimeout, TypeError):
        return short_url


def main():
    session = requests.Session()
    while True:
        os.system('cls||clear')
        print("#" * 80)
        print("Fetching available dates\n")
        response = session.get(url)
        if response.status_code != 200:
            exit(f"Something went wrong, status code {response.status_code}, please try again")

        body = bs4.BeautifulSoup(response.content, "html.parser")
        months = body.select(".calendar-month-table")
        links_found = False
        for month in months:
            links = month.select("td.buchbar a")
            if links:
                links_found = True
                print(f"\t\t{get_month_name(month)}\n")
                for link in links:
                    day_url = shorten_url(link)
                    print("\t{} -> {}".format(link.text, day_url))
                    # URL shortener service will refuse the request if we go too fast.
                    time.sleep(0.1)
                print("\n\n")
        if not links_found:
            print("\tNo available dates found this time.")

        # TODO: fix playsound for linux
        # else:
        #     playsound("./found_sound.wav")
        print("#" * 80)
        print(f"Retrying in {retry_time} seconds...")
        time.sleep(retry_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit("\nHave a nice day at the Buergeramt!\n")
