# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from ..items import AmazonProduct

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = [
        'amazon.com'
    ]

    def start_requests(self):
        urls = [
            'https://www.amazon.com/Sony-MDRZX110-BLK-Stereo-Headphones/dp/B00NJ2M33I/ref=sr_1_3?dchild=1&keywords=headphones&qid=1604970532&sr=8-3&th=1',
            'https://www.amazon.com/Gildan-Fleece-Hooded-Sweatshirt-G18500/dp/B07MGYCGXF?pd_rd_w=OTmxE&pf_rd_p=64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_r=C57TDEBHK3A00G73Z5T3&pd_rd_r=f57e8b32-980e-4511-ac21-c932a11f19ed&pd_rd_wg=NgRR0&th=1',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        self.logger.info('Parse function called on %s', response.url)

        # Note: Python 3.8 is required to use the walrus operator
        if num_ratings := response.xpath('//*[(@id = "acrCustomerReviewText")]/text()').get():
            # num_ratings = '##,### ratings'
            # Parse all digits within text element and cast them into an integer
            num_ratings = int(''.join([i for i in re.findall(r'\d+', num_ratings)]))
        else:
            num_ratings = 0

        yield AmazonProduct(
            title=response.xpath(
                '//*[(@id = "productTitle")]/text()').get().strip(),
            image_url=response.xpath(
                '//img[(@id = "landingImage")]/@src').get(),
            price=response.xpath(
                '//*[(@id = "priceblock_ourprice")]/text()').get(),
            rating_score=AmazonProduct.star_rating[response.xpath(
                '//*[@id="acrPopover"]/span/a/i/@class').re(r'(a-star(-[1-5]){1,2})')[0]],
            num_ratings=num_ratings

        )


        # If another product containing the keyword is found, follow and parse that product.
        # https://docs.scrapy.org/en/latest/intro/tutorial.html?highlight=response.follow#a-shortcut-for-creating-requests
        next_product = response.xpath('//a[contains(div/text(), "Sweat") and starts-with(@href, "/")]/@href').get()
        if next_product is not None:
            self.logger.info(f"Following next product: {next_product}")
            # Error 503 is received after url GET Request. How to mitigate Amazon Bot detection?
            yield response.follow(next_product, callback=self.parse)
