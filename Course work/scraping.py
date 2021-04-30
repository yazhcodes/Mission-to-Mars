# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_teaser = mars_news(browser)
    scraped_data = {
      "news_title": news_title,
      "news_teaser": news_teaser,
      "featured_image": featured_image(browser),
      "facts": mars_earth_facts(),
      "last_modified": dt.datetime.now()
    }
    print(scraped_data)
    browser.quit()
    return scraped_data

def mars_news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_teaser = slide_elem.find('div', class_='article_teaser_body').get_text()
        return news_title, news_teaser
    except AttributeError():
        return None,None

def featured_image(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.find_by_tag('button')[1].click()
    html = browser.html
    img_soup = soup(html,'html.parser')
    try:
        img_url = img_soup.find('img',class_='fancybox-image')['src']
        img_url = url + img_url
        return img_url
    except AttributeError():
        return None

def mars_earth_facts():
    url = 'https://galaxyfacts-mars.com/'
    try:
        facts_df = pd.read_html(url)[0]
    except AttributeError():
        return None
    facts_df.columns=['description', 'Mars', 'Earth']
    facts_df.set_index('description', inplace=True)
    facts_df = facts_df.iloc[1:]
    return facts_df.to_html()

if __name__ == "__main__":
    print(scrape_all())