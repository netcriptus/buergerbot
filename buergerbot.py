#! /usr/bin/env python3
import time

import requests

import bs4
from pyshorteners import Shortener

url = """
https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]=120686&dienstleisterlist=122210,122217,122219,122227,122231,122243,122252,122260,122262,122254,122271,122273,122277,122280,122282,122284,122291,122285,122286,122296,327262,325657,150230,122301,122297,122294,122312,122314,122304,122311,122309,122281,122279,122276,122274,122267,122246,122251,122257,122208,122226&herkunft=http%3A%2F%2Fservice.berlin.de%2Fdienstleistung%2F120686%2F
"""
termin_url = "http://service.berlin.de/terminvereinbarung/termin"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1) ",  # noqa
    "Accept-Encoding": ", ".join(("gzip", "deflate")),
    "Accept": "*/*",
    "Connection": "keep-alive",
}

services = ["Tinyurl", "Isgd"]
global_link_counter = 0


def get_month_name(html_month_tag):
    return html_month_tag.find("th", attrs={"class": "month"}).text


def shorten_url(long_url_tag):
    global global_link_counter
    service = global_link_counter % len(services)
    try:
        short_url = Shortener(services[service]).short(
            "{}/{}".format(termin_url, long_url_tag["href"])
        )
    except (requests.exceptions.ReadTimeout, TypeError):
        short_url = "{}/{}".format(termin_url, long_url_tag["href"])
    global_link_counter += 1
    return short_url


def main():
    while True:
        print("#" * 80)
        print("Fetching available dates\n")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            exit("Something went wrong, please try again")

        body = bs4.BeautifulSoup(response.content, "html.parser")
        months = body.select(".calendar-month-table")
        links_found = False
        for month in months:
            links = month.select("td.buchbar a")
            if links:
                links_found = True
                print("\t\t{}\n".format(get_month_name(month)))
                for link in links:
                    day_url = shorten_url(link)
                    print("\t{} -> {}".format(link.text, day_url))
                    # URL shortener service will refuse the request if we go too fast.
                    time.sleep(0.1)
                print("\n\n")
        if not links_found:
            print("\tNo available dates found this time.")
        print("#" * 80)
        print("Retrying in 60 seconds...")
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            exit("\nHave a nice day at the Buergeramt!\n")


if __name__ == "__main__":
    main()
