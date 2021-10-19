#! /usr/bin/env python3
import time

import requests

import bs4
from pyshorteners import Shortener

url = "https://service.berlin.de/terminvereinbarung/termin/day/"
termin_url = "http://service.berlin.de/terminvereinbarung/termin"

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
    session = requests.Session()
    while True:
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
