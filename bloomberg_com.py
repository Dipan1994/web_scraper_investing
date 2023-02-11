from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_article(data):
    return dict(
        headline = data.get_text(),
        link = 'https://www.bloomberg.com/' + data['href']
    )


def bloomber_com():

    resp = requests.get('https://www.bloomberg.com/fx-center')
    soup = BeautifulSoup(resp.content,'html-parser')

    headline = soup.select_one(".single-story-module_headline-link")
    grid_articles = soup.select(".grid-module-story-module_headline-link")
    side_articles = soup.select(".story-list-story_info_headline-link")

    all_links = []
    all_links.append(get_article(headline))
    [all_links.append(get_article(x)) for x in grid_articles]
    [all_links.append(get_article(x)) for x in side_articles]

    return all_links

