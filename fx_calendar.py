from bs4 import BeautifulSoup
import pandas as pd
import requests
from dateutil import parser
import time
import datetime as dt

def get_date(c):
    ths = c.select_one("tr")
    for th in ths:
        if th.has_attr("colspan"):
            date_text = th.get_text().strip()
            return parser.parse(date_text)
    return None

def get_data_point(key,element):
    for e in ['span','a']:
        d = element.select_one(f"{e}#{key}")
        if d is not None:
            return d.get_text()
    return ''

def get_data_dict(item_date,table_rows):
    data = []

    for tr in table_rows:
        data.append(
            date = item_date,
            country = tr.attrs['data-country'],
            category = tr.attrs['data-category'],
            event = tr.attrs['data-event'],
            symbol = tr.attrs['data-symbol'],
            actual = get_data_point('actual',tr),
            previous = get_data_point('previous',tr),
            forecast = get_data_point('forecast',tr)
        )

    return data

def get_fx_calendar(from_date):

    session = requests.session()

    fr_d_str = dt.datetime.strftime(from_date,"%Y-%m-%d 00:00:00")

    to_date = from_date + dt.timedelta(days=6)
    to_d_str = dt.datetime.strftime(to_date,"%Y-%m-%d 00:00:00")   
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Cookie": f"calendar-importance=3; cal-custom-range={fr_d_str}|{to_d_str}; cal-timezone-offset=330; TEServer=TEIIS2"
    }
    resp = session.get('https://www.tradingeconomics.com/calendar',headers=header)
    soup = BeautifulSoup(resp.content,'html.parser')

    table = soup.select_one("table#calendar")

    last_header_date = None
    trs = {}
    final_data = []

    for c in table.children:
        if c.name == 'thead':
            if 'class' in c.attrs and 'hidden-head' in c.attrs['class']:
                continue
            last_header_date = get_date(c)
            trs[last_header_date] = []
        elif c.name == "tr":
            trs[last_header_date].append(c)

    for item_date,table_rows in trs.items:
        final_data += get_data_dict(item_date,table_rows)

    return final_data


def fx_calendar():
    final_data = []

    start = parser.parse("2022-03-07T00:00:00Z")
    end = parser.parse("2022-03-25T00:00:00Z")

    while start<end:
        final_data += get_fx_calendar(start)
        start = start + dt.timedelta(days=7)
        time.sleep(1)

    
