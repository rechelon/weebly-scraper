# Weebly Blog Post Scraper

Weebly provides the option to "back up" a site, but not the actual posts or content made to it. Which is predatory bullshit designed to prey upon clients who don't have any technical skills or understanding and then lock them into their service.

This is a very simple script to scrape a weebly site's blog posts into markdown files that can be used in things like Hugo or Jekyl, or just be viewed by hand. To import markdown files to wordpress see https://tyler.io/importing-jekyll-posts-into-wordpress/

To use run this script with python on the commandline with the first argument being the website address (the weebly.com version) and the second being the number of pages of blog posts to attempt to scrape (if you don't know how many pages try a large number):`
```shell
python weebly-scraper.py http://example.weebly.com 20
```

Requirements: Python, Beautiful Soup
