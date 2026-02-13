# importing necessary package
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup, NavigableString, Tag

# pandas dataframe to store the data
df = pd.DataFrame(columns = ['Title', 'URL', 'Section', 'Original Text'])

# loading the web driver
driver = webdriver.Firefox(executable_path = '/Applications/geckodriver')


'''
Extracting Text from the first article: 'The AI Revolution: The Road to Superintelligence' and 
storing it into the pandas dataframe df
'''
page_url = 'https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html'

try:
  driver.get(page_url)
  with open('article1.html', 'w', encoding = 'utf-8') as file:
    file.write(driver.page_source)
except Exception as e: 
  print(e)
else:

  # get the whole article
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  # get the article title
  header = soup.find('header', {'class': 'entry-header'})
  article_title = header.find('h1').get_text().strip()

  # get the article body
  article_body = soup.find('div', {'class': 'entry-content'})
  # with open('article1_body.html', 'w', encoding = 'utf-8') as file:
  #   file.write(str(article_body.prettify))
  
  temp_section_header = 'Introduction'      # Label first section as Introduction
  temp_section_text =  ''                   # Declare variable to store section text

  section_start = article_body.find('p', {'style': "text-align: center;"})  # Declare the start of the article as the first p tag element
  # print(section_start.prettify())

  for elem in section_start.next_siblings:      # For each sibling of p tag

    if elem.name == 'h2' or elem.text == 'That’s the topic of Part 2 of this post.':    # if the element is a header

      # stores the data as pandas series in the df dataframe and reset the section header and text 
      temp_row = pd.Series({'Title': article_title, 'URL': page_url, 'Section': temp_section_header, 'Original Text': temp_section_text})
      df = pd.concat([df, temp_row.to_frame().T], ignore_index = True)
      temp_section_header = elem.get_text().strip()
      temp_section_text = ''
      continue

    temp_section_text = temp_section_text + elem.get_text().strip()


'''
Extracting Text from the second article: 'Do Things That Don't Scale' and 
storing it into the pandas dataframe df
'''
page_url = 'http://www.paulgraham.com/ds.html'

try:
  driver.get(page_url)
  with open('article2.html', 'w', encoding = 'utf-8') as file:
    file.write(driver.page_source)
except Exception as e:
  print(e)
else:
  # get the whole article
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  # get the article title
  article_title = soup.title.get_text()

  # get the article body
  article_body = soup.p
  # with open('article2_body.html', 'w', encoding = 'utf-8') as file:
  #   file.write(str(article_body.prettify))

  temp_section_header = 'Introduction'    # Label first section as Introduction
  temp_section_text = ''                  # Empty variable to store section text

  # As the section text are separated by <br> tags find all <br> tags
  for br in article_body.findAll('br'):
    next_s = br.nextSibling           # For all next siblings of br tag

    # Upon encountering a b tag, store the previous section text in the df dataframe, get the new section header
    # reset section text
    if next_s.name == 'b':            
      temp_row = pd.Series({'Title': article_title, 'URL': page_url, 'Section': temp_section_header, 'Original Text': temp_section_text})
      df = pd.concat([df, temp_row.to_frame().T], ignore_index = True)
      temp_section_header = next_s.get_text().strip()
      temp_section_text = ''
      if next_s.get_text().strip() == 'Notes':
        break
    else:
      temp_section_text = temp_section_text + next_s.get_text().strip()

df.to_csv('article.csv')
driver.quit()
