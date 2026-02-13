## Synth Hiring Challenge: 

### As part of the task you need to:

1. Scrape text from
  - [https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html](https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html)
  - [http://www.paulgraham.com/ds.html](http://www.paulgraham.com/ds.html)
2. Summarize the articles by sections/sub headings using [https://huggingface.co/sshleifer/distilbart-cnn-6-6](https://huggingface.co/sshleifer/distilbart-cnn-6-6)
3. Store the summaries and design REST APIs to fetch
  - Section heads given the title of article
  - Summary given the section head
  - You can use Supabase and fastapi for this
    - [https://supabase.com/](https://supabase.com/)
    - [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

### Solution:

1. [Done] Used Selenium to get the text from the website using Firefox's *geckodiver* and used Beautifu Soup to navigate the DOM to store the article                 section-wise in the datframe. The code for scraping are in *scrap_script.py* and the dataframe of article is *article.csv*.    
2. [Done] Used hugginface inference API to get the summary of each section and stored it in the original dataframe. The code for inference is                        *inference.ipynb* and the dataframe of articles with summary section-wise is *article_summary.csv*.
3. [Yet To Do]

