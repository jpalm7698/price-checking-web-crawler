# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field 
from enum import Enum

# TODO: Add enum for storing rating_score per class name

# Items have a dict-like API
class AmazonProduct(Item):

    star_rating = {
        'a-star-1': 1.0,
        'a-star-1-5': 1.5,
        'a-star-2': 2.0,
        'a-star-2-5': 2.5,
        'a-star-3': 3.0,
        'a-star-3-5': 3.5,
        'a-star-4': 4.0,
        'a-star-4-5': 4.5,
        'a-star-5': 5.0
    }

    
 
    

    # TODO: Add additional fields if necessary?
    title = Field()
    image_url = Field()
    price = Field()
    rating_score = Field()
    num_ratings = Field()
    last_updated = Field(serializer=str)