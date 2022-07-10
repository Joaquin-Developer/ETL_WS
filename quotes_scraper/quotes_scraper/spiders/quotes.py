from typing import List, Optional
import scrapy
from scrapy.http import Response


class QuotesSpider(scrapy.Spider):
    """Quotes spider controller"""

    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com/page/1/"
    ]

    custom_settings: Optional[dict] = {
        "FEED_URI": "quotes.json",
        "FEED_FORMAT": "json"
    }

    def parse_only_quotes(self, response, **kwargs):
        """parse a one quote"""

        if kwargs:
            quotes: List = kwargs["quotes"]
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()')).getall()

        next_page_xpath = '//ul[@class="pager"]//li[@class="next"]/a/@href'
        next_page_btn_link = response.xpath(next_page_xpath).get()

        if next_page_btn_link:
            cb_kwargs = {"quotes": quotes}
            yield response.follow(next_page_btn_link,
                                  callback=self.parse_only_quotes,
                                  cb_kwargs=cb_kwargs)
        else:
            yield {
                "quotes": quotes
            }

    def parse(self, response, **kwargs):
        """ type: response: scrapy.http.Response"""

        title = response.xpath("//h1/a/text()").get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()

        top_ten_tags_xpath = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'
        top_ten_tags = response.xpath(top_ten_tags_xpath).getall()

        yield {
            "title": title,
            "top_ten_tags": top_ten_tags
        }

        next_page_xpath = '//ul[@class="pager"]//li[@class="next"]/a/@href'
        next_page_btn_link = response.xpath(next_page_xpath).get()

        if next_page_btn_link:
            cb_kwargs = {"quotes": quotes}
            yield response.follow(next_page_btn_link, callback=self.parse_only_quotes, cb_kwargs=cb_kwargs)
