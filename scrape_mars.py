# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    browser = init_browser()

    # NASA MARS NEWS
    # -------------------------------------------------------------------------------------------------------------------------------------
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    for x in range(5):
        try:
            browser.click_link_by_partial_text('MORE')
        except:
            print("Scraping Complete")

    html = browser.html
    soup = bs(html,"html.parser")       
    results = soup.find_all('li',class_='slide')
    list_mars_news =[]
    for result in results:
        # Error handling
        try:
            news_title = result.find('div',class_='content_title').text.lstrip().rstrip()
            news_p = result.find('div',class_='article_teaser_body').text.lstrip().rstrip()
            # print(news_title)
            # print(news_p)
            dict_result ={
                "news_title" : news_title,
                "news_p" : news_p
            }
            list_mars_news.append(dict_result)
        except AttributeError as e:
            print(e)


    # JPL MARS SPACE IMAGES - FEATURED IMAGE
    # -------------------------------------------------------------------------------------------------------------------------------------
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html,"html.parser")
    results = "https://www.jpl.nasa.gov" + soup.find('div', class_='carousel_items').article.footer.a["data-fancybox-href"]

    list_mars_images = []
    list_mars_images.append(results)

    # for x in range(5):
    #     try:
    #         browser.click_link_by_partial_text('MORE')
    #     except:
    #         print("Scraping Complete")

    # html = browser.html
    # soup = bs(html,"html.parser")
    # article = soup.find('ul', class_='articles')
    # results = article.find_all('li', class_='slide')
    # list_mars_images =[]
    # for result in results:
    #     try:
    #         featured_image_url = result.a["data-fancybox-href"]
    #         if (featured_image_url):
    #             featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    #             # print(featured_image_url)
    #             list_mars_images.append(featured_image_url)
    #     except AttributeError as e:
    #         print('Error:',e)


    # MARS WEATHER
    # -------------------------------------------------------------------------------------------------------------------------------------
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text,"html.parser")
    print(soup.prettify())

    results = soup.find_all('div', class_='js-tweet-text-container')
    # print(" ".join(results[0].p.text.split()[:-1]) + " hPa")
    mars_weather = " ".join(results[0].p.text.split()[:-1]) + " hPa"


    # MARS FACTS
    # -------------------------------------------------------------------------------------------------------------------------------------

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    html_table = []
    for item, row in tables[0].iterrows():
        dict_xy = {
            "element": row.iloc[0],
            "value": row.iloc[1]
        }
        html_table.append(dict_xy)

    # html_table={
    #     "elements": list_elements,
    #     "values": list_values
    # }


    # df = tables[0]
    # df.columns = ['Elements', 'Values']
    # df.set_index('Elements', inplace=True)

    # html_table = df.to_html()

    # html_table = html_table.replace('\n', '')

    # df.to_html('table.html')

    


    # MARS HEMISPHERES
    # -------------------------------------------------------------------------------------------------------------------------------------    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = bs(html,"html.parser")
    results = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    for result in results:
        try:
            x = result.find('div', class_='description')
            hemisphere = x.a.text

            browser.click_link_by_partial_text(hemisphere)        
            html_x = browser.html

            soup_x = bs(html_x,"html.parser")
            link = soup_x.find('div', class_='downloads').find('li').a["href"]
            title = soup_x.find('h2', class_='title').text
    
            hemisphere_image_urls_dict = {
                "title": title, 
                "img_url":link
            }
            hemisphere_image_urls.append(hemisphere_image_urls_dict) 
    
            # print(title)
            # print(link)
            # print("-----------------------------------------------------------------------------------------------------------")        
        
            browser.visit(url)
        
        except AttributeError as e:
            print('Error:',e)

    browser.quit()

     # CREATE A DICTIONARY WITH ALL THE DATA ACQUIRED
    # -------------------------------------------------------------------------------------------------------------------------------------   

    mars_dict = {
        "mars_news" : list_mars_news,
        "mars_images" : list_mars_images,
        "mars_weather" : mars_weather,
        "html_table" : html_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    return mars_dict