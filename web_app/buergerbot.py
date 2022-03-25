#! /usr/bin/env python3
import asyncio
import os
import time

import requests

import bs4
from pyshorteners import Shortener

url = "https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]=120686&dienstleisterlist=122210,122217,327316,122219,327312,122227,327314,122231,122243,327348,122252,329742,122260,329745,122262,329748,122254,329751,122271,327278,122273,327274,122277,327276,330436,122280,327294,122282,327290,122284,327292,327539,122291,327270,122285,327266,122286,327264,122296,327268,150230,329760,122301,327282,122297,327286,122294,327284,122312,329763,122314,329775,122304,327330,122311,327334,122309,327332,122281,327352,122279,329772,122276,327324,122274,327326,122267,329766,122246,327318,122251,327320,122257,327322,122208,327298,122226,327300&herkunft=http%3A%2F%2Fservice.berlin.de%2Fdienstleistung%2F120686%2F"
termin_url = "http://service.berlin.de"

shortener = Shortener()
services = ["chilpit", "clckru", "dagd", "isgd", "tinyurl"]
global_link_counter = 0
retry_time = 10
session = requests.Session()
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

# session.headers.update(headers)

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

def fetch_months():
    response = session.get(url)
    if response.status_code != 200:
        exit(f"Something went wrong, status code {response.status_code}, please try again")

    body = bs4.BeautifulSoup(response.content, "html.parser")
    months = body.select(".calendar-month-table")
    return months

async def fetch_times(day_link):
    session = requests.Session()
    session.headers.update(headers)
    link = f"{termin_url}{day_link['href']}"
    print(f"Fetching time for {day_link.text} -> {link}")
    response = session.get(link)
    if response.status_code != 200:
        exit(f"Something went wrong, status code {response.status_code}, {response.content}")

    body = bs4.BeautifulSoup(response.content, "html.parser")
    table = body.find_all(".timetable")
    print(body)
    print(f"\t table: {table}")
    if not table:
        return []
    table = table[0].find_first("table")
    time_table = []
    appointment_time = ""

    for row in table.find_all("tr"):
        appointment_time = row.select(".buchbar")[0].text or appointment_time
        for cell in row.find_all("td"):
            location = cell.text
            link = cell.find("a")["href"]
            time_table.append((day_link.text, appointment_time, location, link))

    return time_table

def extract_links(month):
    links = month.select("td.buchbar a")
    return [(link.text, shorten_url(link)) for link in links]

async def await_day_links(day_links):
    return await asyncio.gather(*[fetch_times(link) for link in day_links])

def main():
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
                # experimental async feature
                day_links = asyncio.run(await_day_links(links))
                for link_tuple in day_links:
                    if link_tuple:
                        print("\t{} -> {}, {}, {}".format(link_tuple[0], link_tuple[1], link_tuple[2], link_tuple[3]))
                    else:
                        print("False alarm")
                print("\n\n")
        if not links_found:
            print("\tNo available dates found this time.")

        print("#" * 80)
        print(f"Retrying in {retry_time} seconds...")
        time.sleep(retry_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit("\nHave a nice day at the Buergeramt!\n")
