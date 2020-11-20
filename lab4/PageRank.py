import logging
import requests
import pandas as panda
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from bs4 import BeautifulSoup


URL = "https://genome.eu"


def parsing_site(url, soup, domain_name):
    links = []
    internal_links = []
    links_id = []
    visited = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href == url or href in links or href == "" or href is None or domain_name not in href:
            continue
        links.append(href)
        links_id.append(href)
        internal_links.append([url, href])

    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        for line in soup.find_all('a'):
            href = line.get('href')
            if href == url or href in links or href == "" or href is None or domain_name not in href:
                continue
            visited.append(href)
            internal_links.append([link, href])
            links_id.append(href)
    return internal_links


def main():
    logging.info("Start parsing site")
    page = requests.get(URL)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    domain_name = urlparse(URL).netloc
    internal_links = parsing_site(URL, soup, domain_name)
    df = panda.DataFrame(internal_links, columns=["from", "to"])
    G = nx.from_pandas_edgelist(df, source="from", target="to")
    nx.draw(G, with_labels=False)
    plt.show()

# input('Enter site: ')
# site = input('Enter site: ')


if __name__ == '__main__':
    main()
