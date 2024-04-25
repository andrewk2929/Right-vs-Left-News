# import the necessary modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# define your search query and the number of links to click
query = "python automation"
num_links = 3

# create a webdriver object for interacting with a web browser
driver = webdriver.Chrome()

# navigate to the Google search page
driver.get("https://www.google.com")

# find the search input element and enter the search query
search_input = driver.find_element_by_name("q")
search_input.send_keys(query)

# submit the search query
search_input.send_keys(Keys.RETURN)

# find the links in the search results
links = ['d', 'h', 'z']

right_bias = []
left_bias = []

# click on the specified number of links
for link in range(links):
  # links[i].click()
  if ["foxnews.com", "breitbart.com", 'huffpost.com', 'theamericanconservative.com', 'oann.com',
  'newsmax.com', 'www.foxbusiness.com'] in links[i]:
    right_bias.append(links[i])
  if ['buzzfeednews.com', 'cnn.com', 'democracynow.org', 'msnbc.com', 'nytimes.com'] in links[i]:
    left_bias.append(links[i])
  else:
    pass

# close the web browser
driver.close()
