# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Initiate ChromeDriverManager and Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# News Title & Teaser
url = 'https://redplanetscience.com'
browser.visit(url)
browser.is_element_present_by_css('div.list_text', wait_time=1)
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
news_title = slide_elem.find('div', class_='content_title').get_text()
news_teaser = slide_elem.find('div', class_='article_teaser_body').get_text()
print(f'\nNEWS TITLE: {news_title}\n\nNEWS TEASER: {news_teaser}\n')

# Featured Image
url = 'https://spaceimages-mars.com/'
browser.visit(url)
browser.find_by_tag('button')[1].click()
html = browser.html
img_soup = soup(html,'html.parser')
img_url = img_soup.find('img',class_='fancybox-image')['src']
img_url = url + img_url
print(f'IMAGE LINK: {img_url}\n')

# Mars/Earth Facts
url = 'https://galaxyfacts-mars.com/'
browser.visit(url)
table_soup = soup(browser.html,'html.parser')
facts_df = pd.read_html(url)[0]
facts_df.columns=['description', 'Mars', 'Earth']
facts_df.set_index('description', inplace=True)
facts_df = facts_df.iloc[1:]
print(f'MARS/EARTH FACTS: \n{facts_df}')

facts_df.to_html()

browser.quit()