# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Mobile_Score_Item(scrapy.Item):
    Phone_Name = scrapy.Field()
    Price= scrapy.Field()
    Antutu8_Score = scrapy.Field()
    Geekbench5_Single_Core_Score = scrapy.Field()
    Geekbench5_Multi_Core_Score = scrapy.Field()
    Display_Score = scrapy.Field()
    Performance_Score = scrapy.Field()
    Software_Score= scrapy.Field()
    Battery_Score = scrapy.Field()
    Camera_Score = scrapy.Field()
    Overall_Score = scrapy.Field()
    Connectivity_Score= scrapy.Field()
    Sound_Score= scrapy.Field()
    pass
class Processor_Item(scrapy.Item):
    Processor = scrapy.Field()
    Manufacturer = scrapy.Field()
    Rating_score = scrapy.Field()
    Rating_grade = scrapy.Field()
    Cores = scrapy.Field()
    Clock_frequency = scrapy.Field()
    GPU = scrapy.Field()
    pass 
