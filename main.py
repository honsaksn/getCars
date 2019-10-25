from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import traceback
import json 

import dbMgr
import getCarsDto

class getCars:

    def __init__(self):
        self.get_cars_dto = getCarsDto.getCarsDTO()

    def get_conn(self, url):
        try:
            html_doc = self.get_browser_info(url)

            soup = BeautifulSoup(html_doc, 'html.parser')
            result_tags = soup.findAll("li", {"class": "result-row"})
            for result in result_tags:
                # Check the date of the post to see if it is worth looking at

                post_date_info = self.get_post_date(result)
                post_valid_time = post_date_info.get("valid_time", "")
                post_time = post_date_info.get("post_date", "")

                if post_valid_time:

                    post_info = result.findAll("a", {"class":"hdrlnk"})
                    # Get the unique post id 
                    post_id = self.get_post_id(post_info)

                    new_post = self.get_cars_dto.check_post_id(post_id)
                    # Check if the post has been seen before
                    if new_post: 
                        # Get the link to the post 
                        post_link = self.get_post_link(post_info)
                        # Get the price of the post 
                        post_price = self.get_post_price(result)
                        
                        self.get_cars_dto.post_results(post_time, post_id, post_link, post_price)
        except Exception as e:
            print(e)
            traceback_message = traceback.format_exc()
            self.get_cars_dto.post_error(traceback_message)

    def get_browser_info(self, url):
        # Launch a browser and get the url page source code 
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_path = r'C:\Users\steven\Documents\GetCars\chromedriver.exe'

        browser = webdriver.Chrome(chrome_path, options=chrome_options)
        browser.get(url)
        html_doc = browser.page_source
        return html_doc

    def get_post_price(self, post_html): 
        # Get the posted price of the ad
        result_price = post_html.find("span", {"class": "result-price"})
        post_price = result_price.contents[0]
        return post_price

    def get_post_date(self, post_html): 
        # Get the date the ad was posted 
        post_date = post_html.find("time", {"class": "result-date"})
        post_date = str(post_date)
        post_date = self.split_post_date(post_date)
        valid_time = self.check_post_date(post_date)
        post_date_json = {"valid_time":valid_time, "post_date": post_date}
        return post_date_json

    def split_post_date(self, post_date): 
        # Format the inputted date 
        post_date = post_date.split("datetime=")
        post_date = post_date[1].split('"')
        post_date = datetime.strptime(post_date[1], '%Y-%m-%d %H:%M')
        return post_date

    def get_post_link(self, post_info):
        # split off additional text to get URL link to post 
        a_tag = post_info[0]

        a_tag = str(a_tag)
        href = a_tag.split("href=")

        link = href[1].split(">")
        post_link = link[0]
        return post_link

    def get_post_id(self, post_info): 
        # get the unique id on the post
        post_info = str(post_info[0])
        post_info = post_info.split("data-id=")
        post_info = post_info[1].split("href=")
        post_id = post_info[0]
        post_id = str(post_id)
        stripped_post_id = self.strip_data(post_id)
        return stripped_post_id

    def strip_data(self, input_string): 
        # Remove any quotes or spaces from the string 
        mod_string = input_string.replace('"', "")
        mod_string = mod_string.replace(' ', '')
        return mod_string

    def check_post_date(self, post_date):
        # Check to see if this post is new enough to be checked
        if post_date > (datetime.now() - timedelta(hours=1)):
            status = True
        else:
            status = False
        return status

    def main(self):
        # Get all the urls to access from the DB 
        urls = self.get_cars_dto.get_urls()
        if urls:
            url_dict = json.loads(urls)
            for url in url_dict:
                url_string = url.get("url", "")
                self.get_conn(url_string)

if __name__ == '__main__':
    get_cars = getCars()
    # get_cars.get_conn()
    get_cars.main()