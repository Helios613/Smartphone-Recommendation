import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
import time
import csv,sqlite3
import os
from datetime import date

today=date.today()
path=os.getcwd()
path=path.replace("\\","/")
path=path.rsplit('/',1)[0]
path_csvfile=path+"/Mobile_phone_scores.csv"

if os.path.exists(path_csvfile):
    os.remove(path_csvfile)

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
    Update_Date= scrapy.Field()
    pass

class Mobile_data(scrapy.Spider):
    name= "mobile_scores_dataset"
    start_urls=['https://nanoreview.net/en/phone-list/antutu-rating']

    def parse(self, response):
        for p in response.css('table.table-list tbody tr'):
            p.css('td:nth-child(2) a::attr(href)').get()
            PhoneURL= p.css('td:nth-child(2) a::attr(href)').get()
            if PhoneURL is not None:
                yield response.follow(PhoneURL, callback=self.parse_Specs) 

    def parse_Specs(self, response):
            items= Mobile_Score_Item()
            items['Phone_Name']=None
            items['Price']=None
            items['Display_Score']=None
            items['Performance_Score']=None
            items['Antutu8_Score']=None
            items['Geekbench5_Single_Core_Score']=None
            items['Geekbench5_Multi_Core_Score']=None
            items['Software_Score']=None
            items['Battery_Score']=None
            items['Camera_Score']=None
            items['Connectivity_Score']=None
            items['Sound_Score']=None
            items['Overall_Score']=None
            items['Phone_Name']=response.css('div.card h1.title-h1::text').get(),
            if response.css('div.card:nth-child(1) table.specs-table tbody tr:nth-child(4) td.cell-h::text').get()=='Launch price':
                items['Price']=int(response.css('div.card:nth-child(1) table.specs-table tbody tr:nth-child(4) td.cell-s::text').get().split('~ ')[1].split(' USD')[0])
            else :
                items['Price']=None

            for benchmark in response.css('article#the-app>div:nth-child(6)> div:nth-of-type(3) div.two-columns-item.mb'):
                if benchmark.css('div.score-bar div.score-bar-name::text').get()=='\n\t\t\t\tAnTuTu Benchmark 8\n\t\t\t\t\n\t\t\t':
                    items['Antutu8_Score']=int(benchmark.css('div.score-bar div.score-bar-result span::text').get())

                elif benchmark.css('div.score-bar div.score-bar-name::text').get()=='\n\t\t\t\tGeekbench 5 (Single-Core)\n\t\t\t\t\n\t\t\t':
                    items['Geekbench5_Single_Core_Score']=int(benchmark.css('div.score-bar div.score-bar-result span::text').get())

                elif benchmark.css('div.score-bar div.score-bar-name::text').get()=='\n\t\t\t\tGeekbench 5 (Multi-Core)\n\t\t\t\t\n\t\t\t':
                    items['Geekbench5_Multi_Core_Score']=int(benchmark.css('div.score-bar div.score-bar-result span::text').get())

            items['Display_Score']= int(response.css('article#the-app> div:nth-of-type(3) div.card-block.bb-light.pb.flex.flex-wrap div.card-heading-box::text').get())
            items['Performance_Score']=int(response.css('article#the-app> div:nth-of-type(6) div.card-block.bb-light.pb.flex.flex-wrap div.card-heading-box::text').get())
            items['Software_Score']=int(response.css('article#the-app> div:nth-of-type(7) div.card-block.bb-light.pb.flex.flex-wrap div.card-heading-box::text').get())
            items['Battery_Score']=int(response.css('article#the-app> div:nth-of-type(8) div.card-block.bb-light.pb.flex.flex-wrap div.card-heading-box::text').get())
            items['Camera_Score']=int(response.css('article#the-app> div:nth-of-type(9) div.card-block.bb-light.pb.flex.flex-wrap div.card-heading-box::text').get())
            items['Connectivity_Score']=int(response.css('article#the-app> div:nth-of-type(10) div.card-block.bb-light.pb.flex.flex-wrap div.card-heading-box::text').get())
            items['Sound_Score']=int(response.css('article#the-app> div:nth-of-type(11) div.card-block.bb-light.pb.flex.flex-wrap div.card-heading-box::text').get())
            items['Overall_Score']=float("{:.2f}".format((0.85*items['Battery_Score']+0.85*items['Camera_Score']+0.75*items['Connectivity_Score']+0.70*items['Display_Score']+0.80*items['Performance_Score']+0.80*items['Software_Score']+0.75*items['Sound_Score'])/5.5))
            items['Update_Date']=str(today.strftime("%Y-%m-%d"))
            yield items


Mobile_data_crawler_process = CrawlerProcess({
    'FEED_FORMAT': 'csv', 
    'FEED_URI': '../Mobile_phone_scores.csv',
})

Mobile_data_crawler_process.crawl(Mobile_data)
Mobile_data_crawler_process.start()

pathdb=path+"/Mobiles.db"
conn= sqlite3.connect(pathdb)
curr= conn.cursor()
curr.execute("drop table if exists temp_mobile")
curr.execute("CREATE TABLE temp_mobile (Antutu8_Score int,Battery_Score int,Camera_Score int,Connectivity_Score int,Display_Score int,Geekbench5_Multi_Core_Score int,Geekbench5_Single_Core_Score int,Overall_Score int,Performance_Score int,Phone_Name text,Price int,Software_Score int,Sound_Score int, Update_Date date)") 

pathcsv=path+"/Mobile_phone_scores.csv"
with open(pathcsv,'r') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['Antutu8_Score'], i['Battery_Score'],i['Camera_Score'], i['Connectivity_Score'], i['Display_Score'], i['Geekbench5_Multi_Core_Score'], i['Geekbench5_Single_Core_Score'], i['Overall_Score'], i['Performance_Score'], i['Phone_Name'], i['Price'], i['Software_Score'], i['Sound_Score'], i['Update_Date']) for i in dr]


curr.executemany("INSERT INTO temp_mobile (Antutu8_Score,Battery_Score,Camera_Score,Connectivity_Score,Display_Score,Geekbench5_Multi_Core_Score,Geekbench5_Single_Core_Score,Overall_Score,Performance_Score,Phone_Name,Price,Software_Score,Sound_Score,Update_Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?);", to_db)

curr.execute ("CREATE TABLE IF NOT EXISTS SmartPhones (Antutu8_Score int,Battery_Score int,Camera_Score int,Connectivity_Score int,Display_Score int,Geekbench5_Multi_Core_Score int,Geekbench5_Single_Core_Score int,Overall_Score int,Performance_Score int,Phone_Name text,Price int,Software_Score int,Sound_Score int, Update_Date date);")

curr.execute("INSERT INTO SmartPhones SELECT * FROM temp_mobile WHERE Phone_Name NOT IN (SELECT Phone_Name FROM SmartPhones);")
curr.execute("""

update smartphones
set Antutu8_Score = (
    select temp_mobile.Antutu8_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Battery_Score = (
    select temp_mobile.Battery_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Camera_Score = (
    select temp_mobile.Camera_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Connectivity_Score = (
    select temp_mobile.Connectivity_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Display_Score = (
    select temp_mobile.Display_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Geekbench5_Multi_Core_Score = (
    select temp_mobile.Geekbench5_Multi_Core_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Geekbench5_Single_Core_Score = (
    select temp_mobile.Geekbench5_Multi_Core_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Overall_Score = (
    select temp_mobile.Overall_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Performance_Score = (
    select temp_mobile.Performance_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Price = (
    select temp_mobile.Price
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Software_Score = (
    select temp_mobile.Software_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Sound_Score = (
    select temp_mobile.Sound_Score
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
),
Update_Date = (
    select temp_mobile.Update_Date
    from temp_mobile
    where smartphones.Phone_Name = temp_mobile.Phone_Name
) where Phone_Name in (select Phone_Name from temp_mobile where smartphones.phone_name= temp_mobile.phone_name);""")
conn.commit()
conn.close()
