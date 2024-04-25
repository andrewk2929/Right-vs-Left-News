from textblob import TextBlob
from newspaper import Article
from bs4 import BeautifulSoup
import requests

articles = [
'https://en.wikipedia.org/wiki/Mathematics',
'https://www.foxnews.com/media/elon-musk-pokes-fun-cbs-short-lived-twitter-hiatus-network-resumes-tweeting-48-hours-later',
'https://www.cnn.com/2022/11/20/tech/twitter-elon-musk-trump/index.html',
'https://www.bbc.com/news/uk-61585886',
'https://www.bbc.com/news/uk-england-london-52963555'
]
i = len(articles)

print("Welcome to Andrew's Article Sentiment Analysis!")

for article in range(i):
    url = articles[article]

    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    title = doc.find('title')

    article = Article(url)

    article.download()
    article.parse()
    article.nlp()

    text = article.summary # article.text for full text

    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    title_txt = title.string

    if sentiment < -0.6:
        emotion = "very sad"
    if -0.6 < sentiment < -0.3:
        emotion = "sad"
    if  -0.3 < sentiment < 0:
        emotion = "slightly sad"

    if 0 < sentiment < 0.3:
        emotion = "neutral"
    if 0.3 < sentiment < 0.6:
        emotion = "happy"
    if 0.6 < sentiment:
        emotion = "overjoyed"

    print(f"Article: {title_txt} Sentiment: {emotion}({sentiment})\n")