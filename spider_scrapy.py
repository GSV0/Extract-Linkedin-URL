"""
Scrapy spider for extracting linkedin urls from any website.
Developer: Ghanshyam S. Vachhani || Email: gsvachhani7@gmail.com
required "input.xlsx" file in same directory,
"input.xlsx" file need to have column of list of web site with header name "Website"
"""


import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess


class SocialLinksSpider(scrapy.Spider):

    name = 'SocialLinks'

    def start_requests(self):

        df = pd.read_excel('input.xlsx', engine='openpyxl')
        websites = list(enumerate(df['Website']))
        for website in websites:
            yield scrapy.Request(url=website[1], meta={'website': website[1], 'index': website[0]})

    def parse(self, response, **kwargs):

        yield {
            'Index': response.meta['index'],
            'Website': response.meta['website'],
            'Linkedin': ' | '.join(set(response.xpath('//a[contains(@href, "linkedin")]/@href').extract()))
        }


if __name__ == '__main__':

    process = CrawlerProcess(
        settings={
            'FEED_FORMAT': 'csv',
            'FEED_URI': 'output.csv',
        }
    )
    process.crawl(SocialLinksSpider)
    process.start()