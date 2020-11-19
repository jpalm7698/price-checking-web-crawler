# Numerous Dataclass Models for Products Scraped from Shopping Websites
# See https://doc.scrapy.org/en/latest/topics/items.html for more details

from scrapy.item import dataclass

@dataclass
class AmazonProduct(Item):
    # TODO: Add additional fields if necessary?
    # Note: Field types are not enforced at run time.
    title: str
    price: float
    rating_score: float
    num_ratings: int 