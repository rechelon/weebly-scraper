#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen


MAX_FILE_NAME = 120
DATE_FORMAT = 'en'  # Put 'fr' here if your dates fit the format '%d/%m/%Y'


class WeeblyScraper():

    def scrape(self, weebly, nbPages):
        post_urls = []

        for pageNumber in range(1, abs(int(nbPages)) + 1):
            address = weebly + 'previous/' + str(pageNumber)
            print("Scraping page (" + address + ')')

            try:
                url = urlopen(address)
                soup = BeautifulSoup(url.read(), 'html.parser')

                if soup.find(id='blogTable') is not None:
                    for post in soup.findAll('a', {'class': 'blog-title-link'}):
                        post_urls.append(post.get('href'))

            except:
                print("Page not found, you don\'t have that many posts.")

        for post_url in post_urls:
            url = urlopen(post_url)
            soup = BeautifulSoup(url.read(), 'html.parser')

            title = soup.findAll('a', {'class': 'blog-title-link'})
            title = title[0].get_text().encode('utf-8', 'ignore')

            date = soup.findAll('p', {'class': 'blog-date'})
            date = date[0].get_text().encode('utf-8', 'ignore').strip()
            date = datetime.datetime.strptime(date.decode('utf-8'), '%d/%m/%Y' if DATE_FORMAT == 'fr' else '%m/%d/%Y').strftime('%Y-%m-%d')

            content = soup.findAll('div', {'class': 'blog-content'})
            content = content[0].prettify().encode('utf-8', 'ignore')

            url = post_url.replace(weebly, '').encode('utf-8', 'ignore')
            filename = url.decode('utf-8').replace('articles/', '')[:MAX_FILE_NAME]
            print("... writing " + date + '-' + filename + '.md')
            post_md = open('content/' + date + '-' + filename + '.md', 'w+')
            post_md.write('---\ntitle: ' + '\"' + title.decode('utf-8').replace('\"', '\\\"') + '\"' + '\ndate: ' + date + "\nurl: " + url.decode('utf-8') + '\n---\n\n' + content.decode('utf-8').replace('  <', ' <'))
            post_md.close()


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("\nUsage: `" + sys.argv[0] + " <Weebly URL posts\' page> <Number of pages containing posts>`\n")

    else:
        WeeblyScraper().scrape(sys.argv[1], sys.argv[2])

    sys.exit(0)
