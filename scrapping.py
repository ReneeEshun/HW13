import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time

def scrape_all():
    data={}

    data["jpl_image"]=scrapping_jpl()
    data["weather_tweet"]=scrapping_weather()
    data["mars_facts"]=scraping_mars_facts()
    data["hemispheres"]=scrapping_hemisphere()
    return data


def scrapping_jpl():
    response=requests.get("https://www.jpl.nasa.gov/spaceimages/index.php?category=Mars").text
    image_page=BeautifulSoup(response, "html.parser")
    image=image_page.find("article", class_="carousel_item")
    image_url=image["style"]
    clean_image_url="https://www.jpl.nasa.gov" + image_url.split("'")[1]
    return clean_image_url

def scrapping_weather():
    response=requests.get("https://twitter.com/MarsWxReport").text
    tweet=BeautifulSoup(response, "html.parser")
    first_tweet=tweet.find("p", class_="tweet-text")
    return first_tweet.text

def scraping_mars_facts():
    response=requests.get("https://space-facts.com/mars").text
    facts=BeautifulSoup(response, "html.parser")
    mars_table=facts.find("table", class_="tablepress")
    return str(mars_table)

def scrapping_hemisphere():
    executable_path = {'executable_path': 'chromedriver.exe'}

    # build our browser
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    div_description = soup.find_all("div", class_="description")

    hemispheres=[]

    for tags in div_description:
        a_tags = tags.find("a", class_="itemLink")
        
        # tell the browser to visit the url you scraped
        browser.visit("https://astrogeology.usgs.gov" + a_tags["href"])
        time.sleep(1)
        
        # grabs the a tag for the text containing "Sample"
        sample_elem = browser.find_link_by_text('Sample').first
        
        # this is the url to the picture
        image_url = sample_elem["href"]
        title = browser.find_by_css("h2.title").text
        hemispheres.append({
            "title": title,
            "image_url":image_url
        })
    
        # grab the title of the picture
        browser.back()
    return hemispheres