import scrapy
from scrapy.crawler import CrawlerProcess

class Processor_Item(scrapy.Item):
    Processor = scrapy.Field()
    Manufacturer = scrapy.Field()
    Rating_score = scrapy.Field()
    Rating_grade = scrapy.Field()
    Cores = scrapy.Field()
    Clock_frequency = scrapy.Field()
    GPU = scrapy.Field()
    pass 

class Processor_Spider(scrapy.Spider):
    name= "processor_data"
    start_urls=['https://nanoreview.net/en/soc-list/rating']

    def parse(self, response):
        items= Processor_Item()
        items['Processor'] = None
        items['Manufacturer'] = None
        items['Rating_score'] = None
        items['Rating_grade'] = None
        items['Cores']= None
        items['Clock_frequency']= None
        items['GPU']= None
        for p in response.css('table.table-list tbody tr'):
            Processor= p.css('td:nth-child(2) a::text').get().split(' (')[0]
            items['Processor'] = Processor

            Manufacturer= p.css('td:nth-child(2)>span::text').get()
            items['Manufacturer'] = Manufacturer

            Rating_score= p.css('td:nth-child(3) div.table-list-score-box::text').get()
            items['Rating_score'] = Rating_score

            Rating_grade= p.css('td:nth-child(3)>span::text').get()
            items['Rating_grade'] = Rating_grade

            Cores=p.css('td:nth-child(6)>div::text').get()
            items['Cores']= Cores

            Clock_frequency=p.css('td:nth-child(7)::text').get()
            items['Clock_frequency']= Clock_frequency

            GPU=p.css('td:nth-child(8)>div::text').get()
            items['GPU']= GPU

            
            yield items

Processor_process = CrawlerProcess({
    'FEED_FORMAT': 'json', 
    'FEED_URI': '../../Processor_data.json',
})
Processor_process.crawl(Processor_Spider)
Processor_process.start()