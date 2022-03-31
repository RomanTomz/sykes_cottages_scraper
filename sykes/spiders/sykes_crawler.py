# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime 


class SykesCrawlerSpider(CrawlSpider):
    name = 'sykes_crawler'
    allowed_domains = ['sykescottages.co.uk']
    start_urls = ['https://www.sykescottages.co.uk/search.html?country=england&region=&location=&location_long=&locationdist=10&num_sleeps=2&num_pets=-1&startlabel=20%2F08%2F2022&start=20%2F08%2F2022&periodStart=&periodEnd=&duration=7&fuzziness=3&sort=&show=&page=&cardstyle=&pets=&referrer=landing&search_preferences_enabled=0']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='inner-controls']/ul/li[@class='next']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for cottage in response.xpath("//article"):
            yield {
                'title':cottage.xpath(".//div[@class='prop-head-container ']/a/hgroup/h2/text()").get(),
                'price_from':cottage.xpath(".//div/div[2]/p/em/text()").get().replace('£',''),
                'wasPrice':cottage.xpath(".//div/div[2]/p/strike/text()").get(),
                'location':cottage.xpath("normalize-space(.//div[@class='center-column']/div/a[2]/span/text())").get(),
                'sleeps':cottage.xpath("normalize-space(.//div[@class='center-column']/ul/li/em/text())").get(),
                'bedrooms':cottage.xpath("normalize-space(.//div[@class='center-column']/ul/li[2]/em/text())").get(),
                'pets':cottage.xpath("normalize-space(.//div[@class='center-column']/ul/li[3]/em/text())").get(),
                'customer_ratings':cottage.xpath(".//div[@class='center-column']/ul[@class='prop-info ']/div[@class='customer_rating17321']/p/text()").get(),
                'hot_tub':cottage.xpath(".//div[@class='property-primary from-map-1607']/div[2]/div[@class='kep-4614']/ul/li[@data-type='Hot Tub']/text()").get(),
                'provider':'Sykes',
                'date_scraped': datetime.date.today()

            }
