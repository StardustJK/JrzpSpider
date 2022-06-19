# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JrzpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pos_name=scrapy.Field()
    salary_low_bound=scrapy.Field()
    salary_high_bound=scrapy.Field()
    salary_fee_months=scrapy.Field()
    pos_keyword=scrapy.Field()
    pos_domain=scrapy.Field()
    city=scrapy.Field()
    location=scrapy.Field()
    degree=scrapy.Field()
    exp=scrapy.Field()
    person_in_charge=scrapy.Field()
    charge_pos=scrapy.Field()
    pos_detail=scrapy.Field()
    enterprise=scrapy.Field()
    enterprise_scale=scrapy.Field()
    scale_mapping=scrapy.Field()
    create_time=scrapy.Field()
    url=scrapy.Field()
    pos_source=scrapy.Field()
    
    pass
