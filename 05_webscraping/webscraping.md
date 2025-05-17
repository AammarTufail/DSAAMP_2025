# Web screaping with Python

Web scraping is the process of extracting data from websites. It can be done using various libraries in Python, such as:
- `pandas`: scraping data from HTML tables and storing it in DataFrames.
- `requests`: for making HTTP requests to fetch web pages.
- `BeautifulSoup`: for parsing HTML and XML documents.
- `scrapy`: for building web crawlers and scraping large amounts of data.
- `selenium`: for automating web browsers and scraping dynamic content.
- `lxml`: for parsing XML and HTML documents.
- `html5lib`: for parsing HTML documents.

> In this guide, we will focus on using each of these libraries to scrape data from a website. We will cover the following topics:

> - Scraping and storing data with `pandas`
> - Making HTTP requests with `requests`
> - Parsing HTML with `BeautifulSoup`
> - Scraping dynamic content with `selenium`
> - Building a web crawler with `scrapy`
> - Best practices for web scraping
> - Legal and ethical considerations
> - Common pitfalls and how to avoid them
> - Conclusion and further resources

# Installation for web scraping libraries

Create a new conda/virtual environment and install the required libraries using pip:

```bash
# create a new conda environment
conda create -n webscraping_env python=3.10 -y
# activate the environment
conda activate webscraping_env
# install the required libraries
pip install pandas requests beautifulsoup4 scrapy selenium openpyxl lxml html5lib 
# must install libraries 
pip install ipykernel pipreqs seaborn matplotlib plotly
```
> Note: You can also use `pip install -r requirements.txt` if you have a `requirements.txt` file with the list of libraries.

You can also create the required environmentx.txt file using the following command:

```bash
# create a requirements.txt file
pip freeze > requirements.txt
```
> or you can install pipreqs library to create the requirements.txt file automatically:

```bash
# install pipreqs
pip install pipreqs
# create a requirements.txt file having all the libraries used in the project scanning all the files in the project
pipreqs <path_to_your_project>
```
> Note: You can also use `pip install -r requirements.txt` if you have a `requirements.txt` file with the list of libraries.

## 1. Scraping and storing data with `pandas`
`pandas` is a powerful library for data manipulation and analysis. It can also be used to scrape data from HTML tables and store it in DataFrames. Here's how to do it:

> This notebook will cover the web scraping with pandas library. Here is the link: 

1. > [Web Scraping with Pandas](./01_pandas/01_pandas_webscraping.ipynb) 
2. > [News Scraping from BBC](./02_news_scraping/01_bbc.ipynb)
3. > [News Scraping from CNN](./02_news_scraping/02_cnn.ipynb)
4. > [Data Scraping using API from workbank](./03_APIs/01_wbdata.ipynb)
5. > [Data Scraping using API from faostats](./03_APIs/02_faostat.ipynb)
6. > [Data Scraping using API from eurostat](./03_APIs/03_eurostat.ipynb)
7. > [Data Scraping using API from yfinance](./03_APIs/04_yfinance.ipynb)
8. > [Web scrapper for Amazon](./04_amazon_scraper/README.md)
9. > [Web scrapper for google news](./05_google_news_scraper/README.md)
10. > [Web scrapper for Google playstore scrapper](./06_google_play_scraper/README.md)


# Disclaimer
> This project is for educational purposes only. The author is not responsible for any misuse of the code or any legal issues that may arise from using it. Always check the website's terms of service before scraping data and ensure that you are not violating any laws or regulations. Use this code at your own risk.
> The author is not responsible for any legal issues that may arise from using this code. Always check the website's terms of service before scraping data and ensure that you are not violating any laws or regulations. Use this code at your own risk.


---