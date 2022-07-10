import scrapy


class QuotesSpider(scrapy.Spider):
    """Quotes spider controller"""

    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com/page/1/"
    ]

    def parse(self, response: scrapy.http.Response, **kwargs):

        title = response.xpath("//h1/a/text()").get()
        print(f"Titulo: {title} \n\n")

        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        print("Citas: ")
        for quote in quotes:
            print(f"- {quote}")

        top_ten_tags_xpath = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'
        top_ten_tags = response.xpath(top_ten_tags_xpath).getall()

        print("Top ten tags:")
        for tag in top_ten_tags:
            print(f"- {tag}")
