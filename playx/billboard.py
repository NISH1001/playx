"""Simple API to access Billboard charts."""


import requests
from bs4 import BeautifulSoup
import re
import os

"""
__author__ = Deepjyoti Barman
__github__ = github.com/deepjyoti30

"""


class song():
    """Class to store song details."""

    def __init__(self):
        self.title = ""
        self.artist = ""
        self.rank = 0


class Billboard():
    """Class to store billboard charts."""

    def __init__(self, URL):
        """Initiate the basic stuff."""
        self.baseurl = "https://www.billboard.com/charts/"
        self.URL = self.baseurl + URL
        self.soup = self.get_soup()
        self.chart = []
        self.chart_name = ""
        self.get_name_of_chart()
        self.get_number_one()
        self.get_remaining_list()
        self.replace_symbols()

    def get_soup(self):
        """Return the soup for the response."""
        response = requests.get(self.URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def replace_symbols(self):
        """Replace symbols like &amp with &"""
        for i in self.chart:
            i.title = re.sub(r'&amp', '&', i.title)
            i.artist = re.sub(r'&amp', '&', i.artist)

    def get_name_of_chart(self):
        """Get the name of the chart from the webpage."""
        name = self.soup.findAll('h1',
                                attrs={'class': 'chart-detail-header__chart-name'})
        name = re.sub(r'\n', '', str(name))
        try:
            name = re.sub(
                        r'img alt=|"', '',
                        re.findall(r'img alt=".*?"', str(name))[0]
                        )
        except IndexError:
            name = re.sub(
                        r'[></]', '',
                        re.findall(r'>.*?</', str(name))[0]
                        )
        self.chart_name = name

    def get_number_one(self):
        """The number one of the chart needs to be extracted seperately."""
        number_one = song()
        soup = self.soup

        # Some extraction related to number one
        chart_number_one_title = soup.findAll(
                                    'div',
                                    attrs={'class': 'chart-number-one__title'}
                                    )[0]
        number_one.title = re.sub(
                            r'[<>]', '',
                            re.findall(r'>.*?<', str(chart_number_one_title))[0]
                            )

        chart_number_one_artist = str(soup.findAll(
                                    'div',
                                    attrs={'class': 'chart-number-one__artist'}
                                    )[0])
        chart_number_one_artist = chart_number_one_artist.replace("\n", '')
        chart_number_one_artist = re.findall(
                                    r'a href=.*?>.*?</a',
                                    str(chart_number_one_artist)
                                    )[0]
        number_one.artist = re.sub(
                                r'[<>/]', '',
                                re.findall(r'>.*?</', chart_number_one_artist)[0]
                                )

        number_one.rank = 1

        self.chart.append(number_one)

    def get_remaining_list(self):
        soup = self.soup.findAll('div', attrs={'class': 'chart-list-item'})
        for i in soup:
            songObj = song()
            songObj.artist = re.sub(
                                r'data-artist=|["]', '',
                                re.findall(r'data-artist=".*?"', str(i))[0]
                                )
            songObj.title = re.sub(
                                r'data-title=|["]', '',
                                re.findall(r'data-title=".*?"', str(i))[0]
                                )
            songObj.rank = re.sub(
                                r'data-rank=|["]', '',
                                re.findall(r'data-rank=".*?"', str(i))[0]
                                )
            self.chart.append(songObj)

def get_chart_names_online(url="https://www.billboard.com/charts"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=re.compile(r'.*/charts/.+'))
    chart_names = set()
    for link in links:
        href = link['href']
        name = href.split("/")[-1]
        if name:
            chart_names.add(name.lower())
    return chart_names

def get_chart_names(filename):
    path = os.path.expanduser(filename)
    return [ name.strip() for name in open(path).readlines()]

def dump_to_file(names):
    path = '~/.playx/logs/billboard'
    path = os.path.expanduser(path)
    print("Dumping billboard chart names to :: {}".format(path))
    with open(path, 'w') as f:
        f.write('\n'.join(names).strip())

if __name__ == "__main__":
    # Chart = Billboard("youtube")
    # for i in Chart.chart:
    #     # print(i.title)
    #     print("{}: {} by {}".format(i.rank, i.title, i.artist))
    chart_names = get_chart_names_online()
    dump_to_file(chart_names)
    print(get_chart_names('~/.playx/logs/billboard'))
