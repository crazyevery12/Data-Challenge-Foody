# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodyItem(scrapy.Item):
    Name = scrapy.Field()
    Quality = scrapy.Field()
    Position = scrapy.Field()
    Price = scrapy.Field()
    Service = scrapy.Field()
    Space = scrapy.Field()
    ZAvg_Score = scrapy.Field()

    pass
