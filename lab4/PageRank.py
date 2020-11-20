import logging
import requests
import math
import operator
import pandas as panda
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from itertools import islice

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
    return internal_links, links_id


def find_id(graph, node):
    index = 0
    for nd in graph.nodes:
        if node == nd:
            return index
        index += 1


def jacobi_method(B):
    e = 0.001
    solve_vector = []
    new_vector = []
    for i in range(0, len(B)):
        solve_vector.append(B[i][len(B)])
    eps = 1
    while eps > e:
        for i in range(0, len(B)):
            sum = 0
            for j in range(0, len(solve_vector)):
                sum += + solve_vector[i] * B[i][j]
            sum += + B[i][len(B)]
            new_vector.append(sum)
        eps = 0
        for i in range(0, len(solve_vector)):
            eps = eps + math.fabs(new_vector[i] - solve_vector[i])

        solve_vector = new_vector.copy()
        new_vector.clear()
    final_dict = dict()
    for i in range(0, len(solve_vector)):
        final_dict[i] = solve_vector[i]
    final_dict = sorted(final_dict.items(), key=operator.itemgetter(1), reverse=True)
    return final_dict


def main():
    logging.info("Start parsing site")
    page = requests.get(URL)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    domain_name = urlparse(URL).netloc
    links = parsing_site(URL, soup, domain_name)
    data_frame = panda.DataFrame(links[0], columns=["from", "to"])
    graph = nx.from_pandas_edgelist(data_frame, source="from", target="to")
    nx.draw(graph, with_labels=False)
    plt.show()

    d = 0.5

    dict_link = dict()
    for key, value in links[0]:
        if value in dict_link.keys():
            dict_link[value] = dict_link[value] + 1
        else:
            dict_link[value] = 1

    dict_count_link = dict()
    for key, value in links[0]:
        if key in dict_count_link.keys():
            dict_count_link[key] = dict_count_link[key] + 1
        else:
            dict_count_link[key] = 1

    B = [[0 for x in range(len(graph.nodes) + 1)] for y in range(len(graph.nodes))]

    for i in graph.edges:
        B[find_id(graph, i[1])][find_id(graph, i[0])] = d / dict_count_link[i[0]]

    for i in range(0, len(B)):
        B[i][len(B)] = 1 - d

    solution = jacobi_method(B)

    for key, value in list(islice(solution, 10)):
        print(links[1][key], value)


if __name__ == '__main__':
    main()
