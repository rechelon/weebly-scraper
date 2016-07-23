import urllib2
from bs4 import BeautifulSoup
import requests
import os
import urllib
import datetime
import sys

class WeeblyScraper():

    def scrape(weebly, pages):
        post_urls = []
        for page in range(1,11):
            print "scraping page #"+str(page)
            try:
                url = urllib2.urlopen(weebly+"articles/previous/"+str(page))
                html_doc = url.read()
                soup = BeautifulSoup(html_doc, 'html.parser')
                if soup.find(id="blogTable") is not  None:
                    for post in soup.findAll("a", { "class" : "blog-title-link" }):
                        post_url = post.get('href')
                        post_urls.append(post_url)
            except:
                print "page not found, you don't have that many posts"
        print post_urls

        for post_url in post_urls:
            url = urllib2.urlopen(post_url)
            html_doc = url.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            title = soup.findAll("a", { "class" : "blog-title-link" })
            title = title[0].get_text().encode("ascii", "ignore")
            print title
            date = soup.findAll("p", { "class" : "blog-date" })
            date = date[0].get_text().encode("ascii", "ignore").strip()
            date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
            content = soup.findAll("div", { "class" : "blog-content" })
            content = content[0].prettify().encode("utf8", "ignore")
            url = post_url.replace(WEEBLY_URL, '').encode("ascii", "ignore")
            filename = url.replace("articles/", "")
            filename = filename[:120]
            post_md = open("content/"+date+'-'+filename+".md", 'w+')
            print "writing "+date+filename+".md"
            post_md.write("---\ntitle: '"+title+"'\ndate: "+date+"\nurl: "+url+"\n\n---\n"+content)
            post_md.close()


if __name__== "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s <weebly url> <number of pages>" % sys.argv[0]
        sys.exit(1)
        scraper = WeeblyScraper()
        scraper.scrape(sys.argv[1], sys,argv[2])
