import requests
from bs4 import BeautifulSoup
import re
import sender
import datetime
import os

base_address = 'https://news.naver.com/'


def get(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


soup = get(base_address + 'main/home.nhn')

sections = soup.find_all('div', {'class': 'main_component droppable'})


def get_section_name(section):
    return section.find('h4').text


def get_articles(section):
    entries = section.find_all('li')
    links = [entry.find('a') for entry in entries]
    articles = {}
    for link in links:
        title = link.text.strip()
        url = link['href']
        articles[title] = url
    return articles


def get_overview(section, expanded=False):
    section_name = get_section_name(section)
    articles = get_articles(section)
    separator = '\n-------------------\n'
    return section_name + separator + '\n'.join(articles.keys()) + '\n'


overview = []
for section in sections:
    overview.append(get_overview(section))


def get_body_text(article, chars=300):
    html = str(article.find('div', {'id': 'articleBodyContents'}))
    edited_html = re.sub('<br/>', '\n', html)
    article_contents = BeautifulSoup(edited_html, 'html.parser').text
    formatted = re.sub('\n', ' ', article_contents)
    formatted = re.sub('\t', '', formatted)
    formatted = re.sub(' +', ' ', formatted)
    formatted = re.sub(r'\.\s', r'.\n', formatted)

    return formatted[:chars].strip()


def get_details(section):
    articles = get_articles(section)
    details = []
    for title in articles:
        url = articles[title]
        article = get(base_address + url)
        details.append('----------------------------')
        details.append(f"[{title}]")
        details.append(get_body_text(article) + '\n')
    return '\n'.join(details)


overview_output = '\n'.join(overview)
headline_section = sections[0]
headlines_details_output = get_details(headline_section)

now = datetime.datetime.now()
rslt1 = sender.send(f'[NEWS-RELAY] NEWS OVERVIEW ({now.date()})', overview_output)
rslt2 = sender.send(f'[NEWS-RELAY] ARTICLE SNIPPETS ({now.date()})', headlines_details_output)


if not os.path.isdir('log'):
    os.mkdir('log')
with open('log/executions.txt', 'a') as f:
    f.write(f"{now}: {rslt1}, {rslt2}\n")
with open(f'log/{now.date()}_overview.txt', 'w') as f:
    f.write(overview_output)
with open(f'log/{now.date()}_details.txt', 'w') as f:
    f.write(headlines_details_output)
