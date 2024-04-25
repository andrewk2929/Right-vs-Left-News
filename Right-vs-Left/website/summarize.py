from newspaper import Article
import nltk

url = 'https://www.nytimes.com/2022/10/27/technology/elon-musk-twitter-deal-complete.html'

article = Article(url)
article.download()
article.parse()
article.nlp()

# print(f"Title: {article.title}")
# print(f"Authors: {article.authors}")
# print(f"Publication Date: {article.publish_date}")
# print(f"Summary: {article.summary}")