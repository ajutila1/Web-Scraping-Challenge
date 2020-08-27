from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    
    browser = init_browser()

    # Set url for scraping news and scrape into soup
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Grab text of news title and paragraph blurb
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find('div', class_ ='article_teaser_body').text
    
    #-----------------------------------------------------

    # Set url for scraping featured image and scrape into soup
    url_jpeg = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpeg)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Grab text containing url and strip the string to just the url
    img_url = soup.find('div', class_='carousel_container').find('article')['style']
    stripped_url = img_url[23:]
    stripped_url = stripped_url[:-3]
    featured_image_url = "https://www.jpl.nasa.gov" + stripped_url

    #-----------------------------------------------------

    # Set url for scraping facts table
    url_tables = 'https://space-facts.com/mars/'

    # Use pandas to transform the table and convert back to HTML
    tables = pd.read_html(url_tables)
    mars_facts = tables[0]
    mars_facts.rename(columns = {list(mars_facts)[0]: 'Description', list(mars_facts)[1]: 'Mars'}, inplace=True)
    mars_facts.set_index('Description', inplace=True)
    mars_facts_html = mars_facts.to_html()
    mars_facts_html.replace('\n', '')

    #-----------------------------------------------------

    # Set base url for future url building and url to begin scraping from for hemi data
    url_base = "https://astrogeology.usgs.gov"
    url_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Scrape items containing hemi data
    browser.visit(url_hemi)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='item')

    # Set up list to collect data from loop
    hemisphere_image_urls = []

    # Loop through items to pull title and corresponding image
    for result in results:
        title = result.find('div', class_='description').find('h3').text
        img_route = result.find('a', class_='itemLink product-item')['href']
        browser.visit(url_base + img_route)
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        img_url = url_base + soup.find('img', class_='wide-image')['src']
        mars_dict = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(mars_dict)
        browser.back()
        time.sleep(2)

    # Create dictionary containing all info to be used in index.html
    mars_web_info = {'news_title': news_title, 'news_p': news_p, 'featured_image_url': featured_image_url, "mars_facts_html": mars_facts_html, 'hemisphere_image_urls': hemisphere_image_urls}

    return mars_web_info


