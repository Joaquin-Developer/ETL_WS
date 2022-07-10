from typing import Optional
import scrapy
from scrapy.http import Response


class CiaSpider(scrapy.Spider):
    name = "cia"
    start_urls = [
        "https://www.cia.gov/library/readingroom/historical-collections"
    ]

    custom_settings: Optional[dict] = {
        "FEED_URI": "cia.json",
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8"
    }

    def parse(self, response, **kwargs):
        xpath_links_expr = '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href'
        links_desclassified = response.xpath(xpath_links_expr).getall()

        for link in links_desclassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={
                "url": response.urljoin(link)
            })

    def parse_link(self, response, **kwargs):
        link = kwargs["url"]
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        paragraph = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get()

        yield {
            "url": link,
            "title": title,
            "body": paragraph
        }
