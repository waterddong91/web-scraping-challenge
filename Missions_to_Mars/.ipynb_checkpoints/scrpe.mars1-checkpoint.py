{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies and Setup\n",
    "from splinter import Browser \n",
    "from bs4 import BeautifulSoup as bs\n",
    "import pandas as pd\n",
    "import time \n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "#executable_path = {'executable_path': \"chromedriver.exe\"} #ChromeDriverManager().install()}\n",
    "#browser = Browser('chrome', **executable_path, headless=False)\n",
    "\n",
    "# Set Executable Path & Initialize Chrome Browser \n",
    "def init_browser():\n",
    "    executable_path = {\"executable_path\": \"chromedriver.exe\"}\n",
    "    return Browser(\"chrome\", **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "###### NASA Mars News ######\n",
    "\n",
    "browser = init_browser()\n",
    "\n",
    "# NASA Mars News Site\n",
    "url = \"https://mars.nasa.gov/news/\"\n",
    "browser.visit(url)\n",
    "\n",
    "time.sleep(3)\n",
    "\n",
    "# Scrape Page (Parse Results HTML with BeautifulSoup)\n",
    "html = browser.html\n",
    "soup = bs(html, \"html.parser\")\n",
    "\n",
    "# News\n",
    "news = soup.find_all('div', class_=\"list_text\")[0]\n",
    "\n",
    "# Scrape the Latest News Title\n",
    "news_title = news.find(class_=\"content_title\").text\n",
    "\n",
    "# Scrape the Latest Paragraph Text\n",
    "news_p = news.find(class_=\"article_teaser_body\").text\n",
    "\n",
    "# Date\n",
    "news_date = news.find(class_='list_date').text\n",
    "\n",
    "# Store As Dictionary\n",
    "news_data= {\n",
    "    \"News Date\": news_date,\n",
    "    \"News Title\": news_title,\n",
    "    \"News Paragraph\" : news_p\n",
    "}\n",
    "    \n",
    "      \n",
    "browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "##### JPL Mars Space Images - Featured Image #####\n",
    "\n",
    "browser = init_browser()\n",
    "\n",
    "# JPL Site\n",
    "url_jpl = \"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars\"\n",
    "browser.visit(url_jpl)\n",
    "\n",
    "time.sleep(3)\n",
    "\n",
    "# Scrape Page (Parse Results HTML with BeautifulSoup)\n",
    "html= browser.html\n",
    "soup= bs(html, \"html.parser\")\n",
    "\n",
    " # Featured Image\n",
    "featured_image = soup.find('article', class_=\"carousel_item\")['style']\n",
    "\n",
    "# Image Name \n",
    "featured_image_name= (featured_image.split(\"wallpaper/\")[1]).split(\".jpg\")[0]\n",
    "\n",
    "# Use Base URL to Create Absolute URL\n",
    "jpl_url = \"https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg\"\n",
    "image_url= jpl_url + featured_image_name + \".jpg\"\n",
    "\n",
    "\n",
    "browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "##### Mars Facts #####\n",
    "\n",
    "url_facts =\"https://space-facts.com/mars/\"\n",
    "\n",
    "# Visit the Mars Facts Site Using Pandas to Read\n",
    "table = pd.read_html(url_facts)\n",
    "fact_table = pd.DataFrame(table[0])\n",
    "\n",
    "fact_table = fact_table.rename(columns={\n",
    "    0 : \"Description\",\n",
    "    1 : \"Value\"\n",
    "})\n",
    "\n",
    "fact_table.set_index(\"Description\", inplace = True)\n",
    "\n",
    "# Table to HTML\n",
    "table_html = fact_table.to_html()\n",
    "table_html= table_html.replace('\\n',\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "##### Mars Hemisphere #####\n",
    "\n",
    "browser = init_browser()\n",
    "\n",
    "# Scrape Mars Hemispheres From USGS\n",
    "hemisphere_url = \"https://astrogeology.usgs.gov\"\n",
    "hemisphere_img = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "browser.visit(hemisphere_img)\n",
    "\n",
    "time.sleep(3)\n",
    "\n",
    "# Scrape Page\n",
    "html= browser.html\n",
    "soup= bs(html, \"html.parser\")\n",
    "\n",
    "# URL\n",
    "url_list= []\n",
    "for x in range (8):\n",
    "    if (x % 2) == 0:\n",
    "        url_img = soup.find('div', class_=\"collapsible results\").find_all('a')[x]['href']\n",
    "        url_full = hemisphere_url + url_img\n",
    "        url_list.append(url_full)\n",
    "\n",
    "browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Title & URLs\n",
    "hemisphere_url = \"https://astrogeology.usgs.gov\"\n",
    "\n",
    "final_output = []\n",
    "\n",
    "# URL & Title \n",
    "for url in url_list:\n",
    "    browser = init_browser()\n",
    "    browser.visit(url)\n",
    "\n",
    "    time.sleep (3)\n",
    "\n",
    "    # Scrape Page\n",
    "    html = browser.html\n",
    "    soup = bs(html, \"html.parser\")\n",
    "\n",
    "    # URL of Each Image \n",
    "    src_image = soup.find('img', class_=\"wide-image\")['src']\n",
    "    final_image = hemisphere_url + src_image\n",
    "\n",
    "    # Title of Each Image \n",
    "    title_of_image = soup.find('h2', class_=\"title\").get_text()\n",
    "\n",
    "    # Dictionary \n",
    "    dic = {\"Title\": title_of_image ,\n",
    "          \"Image_URL\": final_image}\n",
    "\n",
    "    final_output.append(dic)\n",
    "\n",
    "    browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Last Dictionary Containing All Discovered Info.\n",
    "hemisphere_image_urls = {\n",
    "    \"News Date\": news_date,\n",
    "    \"News Title\": news_title,\n",
    "    \"News Paragraph\": news_p,\n",
    "    \"Featured Image URL\": image_url,\n",
    "    \"Fact Table\": table_html,\n",
    "    \"Hemisphere_Image_Title_1\": final_output[0][\"Title\"],\n",
    "    \"Hemisphere_Image_URL_1\": final_output[0][\"Image_URL\"],\n",
    "    \"Hemisphere_Image_Title_2\": final_output[1][\"Title\"],\n",
    "    \"Hemisphere_Image_URL_2\": final_output[1][\"Image_URL\"],\n",
    "    \"Hemisphere_Image_Title_3\": final_output[2][\"Title\"],\n",
    "    \"Hemisphere_Image_URL_3\": final_output[2][\"Image_URL\"],\n",
    "    \"Hemisphere_Image_Title_4\": final_output[3][\"Title\"],\n",
    "    \"Hemisphere_Image_URL_4\": final_output[3][\"Image_URL\"] \n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}