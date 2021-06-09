from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import pandas as pd
import pymongo

def scrape_mars():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # time.sleep(1)
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.Nasa
    collection = db.mars_data

    collection.drop()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    articles=soup.find_all("div",class_="col-md-12")[1:]

    for article in articles:

        try:
            news_title=article.find("div",class_="content_title").text
            news_p=article.find("div",class_="article_teaser_body").text
            featured_image_url=article.find("img")['src']

            print('-----------------')
            print(news_title)
            print(news_p)
            print(featured_image_url)


            data={
                "title":news_title,
                "paragraph":news_p,
                "image_url":featured_image_url
            }

            # scraped_data.append(data)
            collection.insert_one(data)
                            

        except Exception as e:
            print(e)

        # print(scraped_data)

    browser.quit()
    return ("Data Updated!")



# ## Mars Facts

mars_facts_url="https://galaxyfacts-mars.com/"
mars_facts=pd.read_html(mars_facts_url)[1]
mars_facts=mars_facts.rename(columns = {0:"Variable",1:"Value"})
mars_facts.to_html("Mars_facts.html")


hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg"},
]

