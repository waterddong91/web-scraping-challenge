# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt
import pandas as pd
import json


#### Main Web Scraping Bot #####

def scrape_all():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    '''
    img_url = featured_image(browser)
    
    #mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()
    '''
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
        }

    #Quit browser and return    
    browser.quit()
    return data 

'''
# Set Executable Path & Initialize Chrome Browser
def init_browser():
    executable_path = {"executable_path": "./chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
'''


#### NASA Mars News ####

# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Get First List Item & Wait Half a Second If Not Immediately Present
    #browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    
    html = browser.html
    news_soup = BeautifulSoup(html, "lxml")

    # Parse Results HTML with BeautifulSoup
    # Find Everything Inside:
    #   <ul class="item_list">
    #     <li class="slide">
    try:
        #slide_element = news_soup.find('li',class_="slide").find('div', class_='content_title').text
        #slide_element_p = news_soup.find('div', class_='article_teaser_body').text

        # Scrape the Latest News Title
        # Use Parent Element to Find First <a> Tag and Save it as news_title
        news_title = news_soup.find('li',class_="slide").find('div', class_='content_title').text
        news_paragraph = news_soup.find('div', class_='article_teaser_body').text
    except AttributeError:
        return None, 
    return news_title, news_paragraph



##### JPL Mars Space Images - Featured Image #####

# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(0.5)

    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    time.sleep(0.5)

    # Find "More Info" Button and Click It
    #browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()
    time.sleep(0.5)

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "lxml")

    # Find featured_image_url large size 
    try:
        img_url = image_soup.find('figure', class_='lede').a['href']
        
    except AttributeError:
        return None 
   # Use Base URL to Create Absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url



##### Mars Facts #####

# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    facts_url = 'http://space-facts.com/mars/'
    facts_df=pd.read_html(facts_url)[0]
    facts_df.columns = ['Description','Mars']
    facts_df['Description']=facts_df['Description'].str.replace(':','')
    facts_df.set_index('Description', inplace=True)
    # Convert the data into a HTML table
    facts_df.to_html()
    # Format HTML table with bootstrap
    return facts_df.to_html(classes="table table-striped")
    


##### Mars Hemispheres #####
# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = 'https://astrogeology.usgs.gov'
    url_convert = url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_convert)

    # Read/show the data using BeautifulSoup
    html = browser.html
    soup = bs(html,'lxml')

    # Extracted the titles and the image browser url
    image_urls = [(a.text, a['href']) for a in browser.find_by_css('div[class="description"] a')]

    #Initialize the list
    hemisphere_image_urls = []
    for title,url in image_urls:
    # Used a Python dictionary to store the data
        temp = {}
        temp['title'] = title
        # Visit the url to look for image url
        browser.visit(url)
        img_url = browser.find_by_css('img[class="wide-image"]')['src']
        temp['img_url'] = img_url
        #print(temp)
    # Appended each hemisphere info of all hemipheres to the list
        hemisphere_image_urls.append(temp)
    #print(hemisphere_image_urls)
    # Displayed titles and image links
    hemisphere_image_urls
    # Navigate back
    browser.back()
    return hemisphere_image_urls

'''
# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere
'''

if __name__ == "__main__":
    print(scrape_all())