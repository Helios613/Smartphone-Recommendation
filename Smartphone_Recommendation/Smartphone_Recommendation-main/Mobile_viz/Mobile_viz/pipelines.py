# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class MobileVizPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()
        

    def create_connection(self):
        self.conn = sqlite3.connect("Mobiles.db")
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute("""drop table if exists Mobile_data_table""")
        self.curr.execute("""create table Mobile_data_table (
            Phone_Name text,
            Price text,
            Display_Score text,
            Performance_Score text,
            Antutu8_Score text,
            Geekbench5_Single_Core_Score text,
            Geekbench5_Multi_Core_Score text,
            Software_Score text,
            Battery_Score text,
            Camera_Score text,
            Connectivity_Score text,
            Sound_Score text,
            Overall_Score text
        )""")

    def Mobile_data_store(self,item):
        self.curr.execute("""insert into Mobile_data_table values(?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
            item['Phone_Name'][0],
            item['Price'][0],
            item['Display_Score'][0],
            item['Performance_Score'][0],
            item['Antutu8_Score'][0],
            item['Geekbench5_Single_Core_Score'][0],
            item['Geekbench5_Multi_Core_Score'][0],
            item['Software_Score'][0],
            item['Battery_Score'][0],
            item['Camera_Score'][0],
            item['Connectivity_Score'][0],
            item['Sound_Score'][0],
        ))
        self.conn.commit()


    def process_item(self, item, spider):
        self.Mobile_data_store(item)
        return item
