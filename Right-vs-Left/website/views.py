from flask import *
from newspaper import Article
from os import path
import nltk
from googlesearch import search
import random
from urllib.parse import urlparse
import sys
import threading
import time
import validators
from bs4 import BeautifulSoup
import requests

views = Blueprint("views", __name__)

@views.route("/") 
def home(methods = ['GET', 'POST']):

    if request.method == 'GET':

        # reference variables

        right_bias = []
        left_bias = []
        neutral = []

        number = 0

        def scraper(query, num_links):
            links = []

            found_results = False # check if there are results
            # search the engine
            for url in search(query, num_results=num_links):
                if validators.url(url):
                    found_results = True
                    links.append(url)
                
            print(links)

            if not found_results: # check if there are any results with corresponding topic
                flash(f"{topic} has no sites found.", category = 'error')
                return redirect(url_for("views.home"))
                print("no sites found")
            else:
                print('sites found')
                # print(len(links))
                mainstream_right = ["oan news", "washington times news"]
                mainstream_left = ["cnn news", "msnbc news"]
                mainstream_neutral = ["abc news", "bbc news"]

                random_right = random.choice(mainstream_right)
                random_left = random.choice(mainstream_left)
                random_neutral = random.choice(mainstream_neutral)

                # keyphrase = ["foxnews.com", "breitbart.com", 'huffpost.com', 
                # 'theamericanconservative.com', 'oann.com', 'newsmax.com', 
                # 'www.foxbusiness.com', 'wsj.com', 'rep-am.com']

                # sort links
                for i in range(len(links)):
                    # links[i].click() # click on link (only works for selenium)
                    # check for right-biased sites
                    if any(domain in links[i] for domain in ["breitbart.com", 'huffpost.com', 
                    'theamericanconservative.com', 'oann.com', 'newsmax.com', 
                    'wsj.com', 'rep-am.com', 'washingtontimes.com', 'dailymail.co.uk']):
                        right_bias.append(links[i])
                    # check for left-biased sites
                    if any(domain in links[i] for domain in ['buzzfeednews.com', 'cnn.com', 
                    'democracynow.org', 'msnbc.com', 'nytimes.com']):
                        left_bias.append(links[i])
                    # check for neutral sites
                    if any(domain in links[i] for domain in ["apnews.com", "bbc.com", 
                    "abcnews.go.com", "abc15.com"]):
                        neutral.append(links[i])
                    else:
                        pass

                # make sure all type of sites are scraped
                if len(right_bias) and len(left_bias) and len(neutral) == 0:
                    flash("Not a current news topic", category = "error")
                if len(right_bias) == 0:
                    scraper(f"{topic} {random_right}", 3)
                if len(left_bias) == 0:
                    scraper(f"{topic} {random_left}", 3)
                if len(neutral) == 0:
                    scraper(f"{topic} {random_neutral}", 3) # minimize num_links for optimization
                print(f'{right_bias} {left_bias} {neutral}')

        scraper(f"{topic}", 10)

        # url = 'https://www.cnn.com/2022/11/20/tech/twitter-elon-musk-trump/index.html' # sample url

        left_url = f'{left_bias[0]}'

        left_article = Article(left_url)

        left_article.download()
        left_article.parse()
        left_article.nlp()

        # scraping article data
        # art_author = article.author
        # art_summary = article.summary

        art_date_published = str(left_article.publish_date)
        left_art_modify_date = art_date_published[:-9] # remove last 9 characters from date (hours, mins, seconds)

        # use bs4 for title
        left_page = requests.get(left_url).text
        left_doc = BeautifulSoup(left_page, 'html.parser')
        left_art_title = left_doc.find('title')
        left_art_str_title = str(left_art_title)

        left_art_modify_title = BeautifulSoup(left_art_str_title, 'html.parser').text

        # art_title = str(left_article.title)
        # left_art_modify_title = art_title[9:] # remove first 9 characters from title (Analysis:)

        left_art_modify_summary = left_article.summary
        left_art_authors_1 = left_article.authors
        left_art_modify_authors = left_art_authors_1

        # return render_template("search.html", art = article, art_summary = art_modify_summary,
        # art_title = art_modify_title, art_publish = art_modify_date)
        
        # return render_template("home.html", left_art = left_article, left_art_summary = left_art_modify_summary, 
        # left_art_title = left_art_modify_title, left_art_publish = left_art_modify_date)

        # url = 'https://www.cnn.com/2022/11/20/tech/twitter-elon-musk-trump/index.html' # sample url

        right_url = f'{right_bias[0]}'

        right_article = Article(right_url)

        right_article.download()
        right_article.parse()
        right_article.nlp()

        # scraping article data
        # art_author = article.author
        # art_summary = article.summary

        art_date_published = str(right_article.publish_date)
        right_art_modify_date = art_date_published[:-9] # remove last 9 characters from date (hours, mins, seconds)

        # use bs4 for the title
        right_page = requests.get(right_url).text
        right_doc = BeautifulSoup(right_page, 'html.parser')
        right_art_title = right_doc.find('title')
        right_art_str_title = str(right_art_title)

        right_art_modify_title = BeautifulSoup(right_art_str_title, 'html.parser').text

        # art_title = str(right_article.title)
        # right_art_modify_title = art_title[9:] # remove first 9 characters from title (Analysis:)

        right_art_modify_summary = right_article.summary
        right_art_authors_1 = right_article.authors
        right_art_modify_authors = right_art_authors_1

        # return render_template("search.html", art = article, art_summary = art_modify_summary,
        # art_title = art_modify_title, art_publish = art_modify_date)


        neutral_url = f'{neutral[0]}'

        neutral_article = Article(neutral_url)

        neutral_article.download()
        neutral_article.parse()
        neutral_article.nlp()

        # scraping article data
        # art_author = article.author
        # art_summary = article.summary

        art_date_published = str(neutral_article.publish_date)
        neutral_art_modify_date = art_date_published[:-9] # remove last 9 characters from date (hours, mins, seconds)

        # use bs4 for title
        neutral_page = requests.get(neutral_url).text
        neutral_doc = BeautifulSoup(neutral_page, 'html.parser')
        neutral_art_title = neutral_doc.find('title')
        neutral_art_str_title = str(neutral_art_title)

        neutral_art_modify_title = BeautifulSoup(neutral_art_str_title, 'html.parser').text

        # art_title = str(neutral_article.title)
        # neutral_art_modify_title = art_title[9:] # remove first 9 characters from title (Analysis:)

        neutral_art_modify_summary = neutral_article.summary
        neutral_art_authors_1 = neutral_article.authors
        neutral_art_modify_authors = neutral_art_authors_1

        # return render_template("search.html", art = article, art_summary = art_modify_summary,
        # art_title = art_modify_title, art_publish = art_modify_date)

        return render_template("search.html", usr_topic = topic, right_art = right_article, 
        right_art_summary = right_art_modify_summary, right_art_title = right_art_modify_title, 
        right_art_publish = right_art_modify_date, 
        neutral_art = neutral_article, neutral_art_summary = neutral_art_modify_summary, 
        neutral_art_title = neutral_art_modify_title, neutral_art_publish = neutral_art_modify_date, 
        left_art = left_article, left_art_summary = left_art_modify_summary, 
        left_art_title = left_art_modify_title, left_art_publish = left_art_modify_date, 
        left_art_authors = left_art_modify_authors,
        right_art_authors = right_art_modify_authors, neutral_art_authors = neutral_art_modify_authors,
        left_art_url = left_url, right_art_url = right_url, neutral_art_url = neutral_url)


    return render_template("home.html")


@views.route("/topic", methods = ['GET', 'POST'])
def topic():

    topic = request.form.get("topic")

    print("made it to topic")
    print(topic)

    # reference variables

    right_bias = []
    left_bias = []
    neutral = []

    number = 0

    if not topic:
        flash("Please enter text", category = "warning")
        return redirect(url_for("home.html"))
        print("No topic error")
    else:
        def scraper(query, num_links):
            links = []

            found_results = False # check if there are results
            # search the engine
            for url in search(query, num_results=num_links):
                if validators.url(url):
                    found_results = True
                    links.append(url)
                
            print(links)

            if not found_results: # check if there are any results with corresponding topic
                flash(f"{topic} has no sites found.", category = 'error')
                return redirect(url_for("views.home"))
                print("no sites found")
            else:
                print('sites found')
                # print(len(links))
                mainstream_right = ["oan news", "washington times news"]
                mainstream_left = ["cnn news", "msnbc news"]
                mainstream_neutral = ["abc news", "bbc news"]

                random_right = random.choice(mainstream_right)
                random_left = random.choice(mainstream_left)
                random_neutral = random.choice(mainstream_neutral)

                # keyphrase = ["foxnews.com", "breitbart.com", 'huffpost.com', 
                # 'theamericanconservative.com', 'oann.com', 'newsmax.com', 
                # 'www.foxbusiness.com', 'wsj.com', 'rep-am.com']

                # sort links
                for i in range(len(links)):
                    # links[i].click() # click on link (only works for selenium)
                    # check for right-biased sites
                    if any(domain in links[i] for domain in ["breitbart.com", 'huffpost.com', 
                    'theamericanconservative.com', 'oann.com', 'newsmax.com', 
                    'wsj.com', 'rep-am.com', 'washingtontimes.com', 'dailymail.co.uk']):
                        right_bias.append(links[i])
                    # check for left-biased sites
                    if any(domain in links[i] for domain in ['buzzfeednews.com', 'cnn.com', 
                    'democracynow.org', 'msnbc.com', 'nytimes.com']):
                        left_bias.append(links[i])
                    # check for neutral sites
                    if any(domain in links[i] for domain in ["apnews.com", "bbc.com", 
                    "abcnews.go.com", "abc15.com"]):
                        neutral.append(links[i])
                    else:
                        pass

                # make sure all type of sites are scraped
                if len(right_bias) and len(left_bias) and len(neutral) == 0:
                    flash("Not a current news topic", category = "error")
                if len(right_bias) == 0:
                    scraper(f"{topic} {random_right}", 3)
                if len(left_bias) == 0:
                    scraper(f"{topic} {random_left}", 3)
                if len(neutral) == 0:
                    scraper(f"{topic} {random_neutral}", 3) # minimize num_links for optimization
                print(f'{right_bias} {left_bias} {neutral}')

        scraper(f"{topic}", 10)

        # url = 'https://www.cnn.com/2022/11/20/tech/twitter-elon-musk-trump/index.html' # sample url

        left_url = f'{left_bias[0]}'

        left_article = Article(left_url)

        left_article.download()
        left_article.parse()
        left_article.nlp()

        # scraping article data
        # art_author = article.author
        # art_summary = article.summary

        art_date_published = str(left_article.publish_date)
        left_art_modify_date = art_date_published[:-9] # remove last 9 characters from date (hours, mins, seconds)

        # use bs4 for title
        left_page = requests.get(left_url).text
        left_doc = BeautifulSoup(left_page, 'html.parser')
        left_art_title = left_doc.find('title')
        left_art_str_title = str(left_art_title)

        left_art_modify_title = BeautifulSoup(left_art_str_title, 'html.parser').text

        # art_title = str(left_article.title)
        # left_art_modify_title = art_title[9:] # remove first 9 characters from title (Analysis:)

        left_art_modify_summary = left_article.summary
        left_art_authors_1 = left_article.authors
        left_art_modify_authors = left_art_authors_1

        # return render_template("search.html", art = article, art_summary = art_modify_summary,
        # art_title = art_modify_title, art_publish = art_modify_date)
        
        # return render_template("home.html", left_art = left_article, left_art_summary = left_art_modify_summary, 
        # left_art_title = left_art_modify_title, left_art_publish = left_art_modify_date)

        # url = 'https://www.cnn.com/2022/11/20/tech/twitter-elon-musk-trump/index.html' # sample url

        right_url = f'{right_bias[0]}'

        right_article = Article(right_url)

        right_article.download()
        right_article.parse()
        right_article.nlp()

        # scraping article data
        # art_author = article.author
        # art_summary = article.summary

        art_date_published = str(right_article.publish_date)
        right_art_modify_date = art_date_published[:-9] # remove last 9 characters from date (hours, mins, seconds)

        # use bs4 for the title
        right_page = requests.get(right_url).text
        right_doc = BeautifulSoup(right_page, 'html.parser')
        right_art_title = right_doc.find('title')
        right_art_str_title = str(right_art_title)

        right_art_modify_title = BeautifulSoup(right_art_str_title, 'html.parser').text

        # art_title = str(right_article.title)
        # right_art_modify_title = art_title[9:] # remove first 9 characters from title (Analysis:)

        right_art_modify_summary = right_article.summary
        right_art_authors_1 = right_article.authors
        right_art_modify_authors = right_art_authors_1

        # return render_template("search.html", art = article, art_summary = art_modify_summary,
        # art_title = art_modify_title, art_publish = art_modify_date)


        neutral_url = f'{neutral[0]}'

        neutral_article = Article(neutral_url)

        neutral_article.download()
        neutral_article.parse()
        neutral_article.nlp()

        # scraping article data
        # art_author = article.author
        # art_summary = article.summary

        art_date_published = str(neutral_article.publish_date)
        neutral_art_modify_date = art_date_published[:-9] # remove last 9 characters from date (hours, mins, seconds)

        # use bs4 for title
        neutral_page = requests.get(neutral_url).text
        neutral_doc = BeautifulSoup(neutral_page, 'html.parser')
        neutral_art_title = neutral_doc.find('title')
        neutral_art_str_title = str(neutral_art_title)

        neutral_art_modify_title = BeautifulSoup(neutral_art_str_title, 'html.parser').text

        # art_title = str(neutral_article.title)
        # neutral_art_modify_title = art_title[9:] # remove first 9 characters from title (Analysis:)

        neutral_art_modify_summary = neutral_article.summary
        neutral_art_authors_1 = neutral_article.authors
        neutral_art_modify_authors = neutral_art_authors_1

        # return render_template("search.html", art = article, art_summary = art_modify_summary,
        # art_title = art_modify_title, art_publish = art_modify_date)

        # can't use image due to copyright issues
        # # use bs4 for image
        # neutral_art_img = neutral_doc.find('img')
        
        # # check if there's an img
        # if neutral_art_img:
        #     neutral_art_modify_img = neutral_art_img['src'] # get the src from the img tag
        # else:
        #     neutral_art_modify_img = "" # enter img src

        return render_template("search.html", usr_topic = topic, right_art = right_article, 
        right_art_summary = right_art_modify_summary, right_art_title = right_art_modify_title, 
        right_art_publish = right_art_modify_date, 
        neutral_art = neutral_article, neutral_art_summary = neutral_art_modify_summary, 
        neutral_art_title = neutral_art_modify_title, neutral_art_publish = neutral_art_modify_date, 
        left_art = left_article, left_art_summary = left_art_modify_summary, 
        left_art_title = left_art_modify_title, left_art_publish = left_art_modify_date, 
        left_art_authors = left_art_modify_authors,
        right_art_authors = right_art_modify_authors, neutral_art_authors = neutral_art_modify_authors,
        left_art_url = left_url, right_art_url = right_url, neutral_art_url = neutral_url)


    return render_template("search.html", usr_topic = topic)

# @views.route("/search")
# def test():
#     topic = "a"
#     return redirect(f"/news/{topic}")



# selenium google scraping code:
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# print("hello world ###0")
#         def scraper(query, num_links):
#             print("hello world ###1")
#             PATH = r'instance\chromedriver_win32/chromedriver.exe'

#             # Launch a browser
#             driver = webdriver.Chrome(PATH)

#             # Navigate to the Google search page
#             driver.get("https://www.google.com/")

#             # Find the search input box and enter the query
#             search_box = driver.find_element_by_name("q")
#             search_box.send_keys(query)
#             search_box.send_keys(Keys.RETURN)

#             # Wait for the search results to load
#             driver.implicitly_wait(1)

#             # Extract the URLs of the search results
#             links = []
#             print("hello world")
#             results = driver.find_elements_by_css_selector("div.r > a")
#             print(results)
#             for result in range(min(num_links, len(results))):
#                 link = result.get_attribute("href")
#                 if link.startswith("http"):
#                     links.append(link)

#             print("hello world 2")
#             if len(links) == 0: # check if there are any links with corresponding topic
#                 flash(f"{topic} has no sites found.", category = 'error')
#                 return render_template("home.html")
#                 print("no sites found")
#             else:
#                 print('sites found')
#                 mainstream_right = ["fox news", "fox news", "oan news"] # oan isn't as mainstream as fox news
#                 mainstream_left = ["cnn news", "msnbc news"]
#                 mainstream_neutral = ["abc news", "bbc news"]

#                 random_right = random.choice(mainstream_right)
#                 random_left = random.choice(mainstream_left)
#                 random_neutral = random.choice(mainstream_neutral)

#                 # sort links
#                 for link in range(len(links)):
#                     # links[i].click()
#                     if ["foxnews.com", "breitbart.com", 'huffpost.com', 'theamericanconservative.com', 'oann.com',
#                     'newsmax.com', 'www.foxbusiness.com', 'wsj.com', 'rep-am.com'] in links[num_links]:
#                         right_bias.append(links[num_links])
#                     if ['buzzfeednews.com', 'cnn.com', 'democracynow.org', 'msnbc.com', 'nytimes.com'] in links[num_links]:
#                         left_bias.append(links[num_links])
#                     if ["apnews.com", "bbc.com", "abcnews.go.com", "abc15.com"] in links[num_links]:
#                         neutral.append(links[num_links])
#                     else:
#                         pass

#                 # make sure all type of sites are scraped
#                 if len(right_bias) and len(left_bias) and len(neutral) == 0:
#                     flash("Not a current news topic", category = "error")
#                 if len(right_bias) == 0:
#                     scraper(f"{topic} {random_right}", 3)
#                 if len(left_bias) == 0:
#                     scraper(f"{topic} {random_left}", 3)
#                 if len(neutral) == 0:
#                     scraper(f"{topic} {random_neutral}", 3) # minimize num_links for optimization
#                 print(f'{right_bias} {left_bias} {neutral}')
#             # close the web browser
#             driver.quit()
#             print("finished!")

#         scraper(f"{topic}", 10)