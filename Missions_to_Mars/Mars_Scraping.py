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

    url = "https://redplanetscience.com/"
    browser.visit(url)

    client = pymongo.MongoClient('mongodb://localhost:27017')
    client.Nasa.mars_data.drop()

    #Get Mars News and Image  
    html = browser.html
    soup = bs(html, "html.parser")

    articles=soup.find_all("div",class_="col-md-12")[1:]
    for article in articles:
        try:
            news_title=article.find("div",class_="content_title").text
            news_p=article.find("div",class_="article_teaser_body").text
            featured_image_url=article.find("img")['src']

            data={
                "title":news_title,
                "paragraph":news_p,
                "image_url":featured_image_url
            }
            client.Nasa.mars_data.insert_one(data)                     
        except Exception as e:
            print(e)
   

    #Get Mars Facts Table 
    tables = pd.read_html('https://galaxyfacts-mars.com/')
    df = tables[0]
    df.columns = df.iloc[0]
    comparison = df[1:]
    comparison.set_index('Mars - Earth Comparison')
    html_table = comparison.to_html()
    html_table.replace('\n', '')

    #Get Mars Hemispheres
    browser.visit('https://marshemispheres.com/')
    html = browser.html
    soup = bs(html, 'html.parser')

    names = soup.find_all('div', class_='item')

    hemisphere = []

    for x in names: 
        itemtitle = x.find('div', class_='description').find('a').find('h3').text
        baseurl = x.find('a')['href']
        image_url = 'https://marshemispheres.com/' + baseurl
        browser.visit(image_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        image = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        final_image = 'https://marshemispheres.com/' + image
        hemisphere.append({'title':itemtitle, 'img_url':final_image})
        
    browser.quit()
    
    mars_data = {
        'mars_facts': html_table,
        'hemisphere_images': hemisphere
    }
    
    client.Nasa.planet_data.drop()
    client.Nasa.planet_data.insert_one(mars_data)

    return mars_data
