"""
Google News AI Scraper

This script scrapes AI-related news from Google News while implementing best practices:
- Random delays between requests
- Rotating user agents
- Respect for robots.txt
- Error handling and retries
- Rate limiting
- Logging
- Data export (JSON, CSV)
- News analysis

It's designed to collect the latest AI news articles, their publishers,
publication dates, article snippets, and links to the full articles.
"""

import requests
import time
import random
import logging
import os
import json
import csv
import re
from urllib.parse import urljoin, quote_plus
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from requests.exceptions import RequestException, Timeout, ConnectionError
import urllib.robotparser
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='google_news_scraper.log',
    filemode='a'
)
logger = logging.getLogger('google_news_scraper')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Constants
BASE_URL = "https://news.google.com"
SEARCH_URL = "https://news.google.com/search?q={}&hl=en-US&gl=US&ceid=US:en"
OUTPUT_DIR = "google_news_data"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 10

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def ensure_nltk_resource(resource_name):
    """Ensure the NLTK resource is available, download if missing."""
    try:
        nltk.data.find(f'corpora/{resource_name}')
    except LookupError:
        nltk.download(resource_name)

class GoogleNewsScraper:
    """Class to scrape Google News for AI-related news articles"""
    
    def __init__(self, respect_robots=True, delay_range=(1, 3)):
        """
        Initialize the scraper with configuration options
        
        Args:
            respect_robots (bool): Whether to respect robots.txt
            delay_range (tuple): Range for random delays between requests (min, max) in seconds
        """
        self.respect_robots = respect_robots
        self.delay_range = delay_range
        self.session = requests.Session()
        self.robot_parser = None
        
        # Setup user agents
        try:
            self.ua = UserAgent()
        except:
            # Fallback user agents if fake_useragent fails
            self.ua = None
            self.user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
            ]
        
        # Setup robots.txt parser
        if respect_robots:
            self.setup_robots_parser()
    
    def setup_robots_parser(self):
        """Initialize the robots.txt parser"""
        self.robot_parser = urllib.robotparser.RobotFileParser()
        self.robot_parser.set_url(f"{BASE_URL}/robots.txt")
        try:
            self.robot_parser.read()
            logger.info("Successfully parsed robots.txt")
        except Exception as e:
            logger.warning(f"Failed to parse robots.txt: {e}")
            self.robot_parser = None
    
    def get_random_user_agent(self):
        """Get a random user agent"""
        if self.ua:
            return self.ua.random
        else:
            return random.choice(self.user_agents)
    
    def get_request_headers(self):
        """Generate headers for the HTTP request"""
        user_agent = self.get_random_user_agent()
        
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def can_fetch(self, url):
        """Check if URL can be fetched according to robots.txt"""
        if not self.respect_robots or not self.robot_parser:
            return True
        
        user_agent = self.get_random_user_agent()
        try:
            can_fetch = self.robot_parser.can_fetch(user_agent, url)
            if not can_fetch:
                logger.warning(f"robots.txt disallows: {url}")
            return can_fetch
        except:
            return True
    
    def make_request(self, url, retries=MAX_RETRIES):
        """
        Make an HTTP request with retries
        
        Args:
            url (str): URL to request
            retries (int): Number of retry attempts
            
        Returns:
            tuple: (success, response_or_error)
        """
        if not self.can_fetch(url):
            return False, "Blocked by robots.txt"
        
        # Random delay before request
        time.sleep(random.uniform(*self.delay_range))
        
        for attempt in range(retries):
            headers = self.get_request_headers()
            
            try:
                logger.info(f"Request to {url} (Attempt {attempt+1}/{retries})")
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    return True, response
                
                logger.warning(f"HTTP Error: {response.status_code}")
            
            except (ConnectionError, Timeout, RequestException) as e:
                logger.warning(f"Request failed: {str(e)}")
            
            # Longer delay after a failure
            time.sleep(random.uniform(*[x*2 for x in self.delay_range]))
        
        logger.error(f"All {retries} attempts failed for {url}")
        return False, f"Failed after {retries} attempts"
    
    def search_news(self, query, max_pages=3):
        """
        Search for news on Google News
        
        Args:
            query (str): Search query
            max_pages (int): Maximum number of result pages to scrape
            
        Returns:
            list: List of article dictionaries
        """
        articles = []
        encoded_query = quote_plus(query)
        search_url = SEARCH_URL.format(encoded_query)
        
        success, response = self.make_request(search_url)
        
        if not success:
            logger.error(f"Failed to retrieve search page: {response}")
            return articles
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple selectors for robustness
        article_elements = soup.select('div[class*="NiLAwe"]')
        if not article_elements:
            article_elements = soup.find_all('article')
        if not article_elements:
            article_elements = soup.select('h3 a, h4 a')
        logger.info(f"Found {len(article_elements)} articles on search page")
        
        for article_elem in article_elements[:max_pages * 30]:  # Limit to ~30 articles per page
            try:
                # Extract article data
                article = self.extract_article_data(article_elem)
                if article:
                    articles.append(article)
            except Exception as e:
                logger.warning(f"Error extracting article data: {e}")
        
        return articles
    
    def extract_article_data(self, article_elem):
        """
        Extract data from an article element
        
        Args:
            article_elem (BeautifulSoup element): The article HTML element
            
        Returns:
            dict: Article data or None if failed
        """
        try:
            article = {
                'scraped_at': datetime.now().isoformat(),
            }
            
            # Title and link
            title_elem = article_elem.select_one('h3 a, h4 a')
            if title_elem:
                article['title'] = title_elem.get_text(strip=True)
                article['url'] = urljoin(BASE_URL, title_elem.get('href', ''))
            
            # Publisher
            publisher_elem = article_elem.select_one('a[data-n-tid]')
            if publisher_elem:
                article['publisher'] = publisher_elem.get_text(strip=True)
            
            # Time published
            time_elem = article_elem.select_one('time')
            if time_elem:
                article['published_time'] = time_elem.get_text(strip=True)
                article['published_datetime'] = self.parse_time_ago(time_elem.get_text(strip=True))
            
            # Snippet/Description
            description_elem = article_elem.select_one('.xBbh9')
            if description_elem:
                article['snippet'] = description_elem.get_text(strip=True)
            
            # Thumbnail image
            image_elem = article_elem.select_one('img[src^="https://"]')
            if image_elem and image_elem.has_attr('src'):
                article['thumbnail_url'] = image_elem['src']
            
            return article
        
        except Exception as e:
            logger.error(f"Error extracting article details: {e}")
            return None
    
    def parse_time_ago(self, time_ago_text):
        """
        Parse a 'time ago' text into a datetime
        
        Args:
            time_ago_text (str): Time ago text (e.g., "2 hours ago")
            
        Returns:
            str: ISO format datetime or original text if parsing fails
        """
        now = datetime.now()
        
        try:
            if 'min' in time_ago_text:
                minutes = int(re.search(r'(\d+)', time_ago_text).group(1))
                return (now - timedelta(minutes=minutes)).isoformat()
            elif 'hour' in time_ago_text:
                hours = int(re.search(r'(\d+)', time_ago_text).group(1))
                return (now - timedelta(hours=hours)).isoformat()
            elif 'day' in time_ago_text:
                days = int(re.search(r'(\d+)', time_ago_text).group(1))
                return (now - timedelta(days=days)).isoformat()
            elif 'week' in time_ago_text:
                weeks = int(re.search(r'(\d+)', time_ago_text).group(1))
                return (now - timedelta(weeks=weeks)).isoformat()
            else:
                return time_ago_text  # Return original if can't parse
        except:
            return time_ago_text
    
    def analyze_news(self, articles):
        """
        Analyze collected news articles
        
        Args:
            articles (list): List of article dictionaries
            
        Returns:
            dict: Analysis results
        """
        if not articles:
            return {"error": "No articles found"}
        # Ensure NLTK resources
        ensure_nltk_resource('stopwords')
        ensure_nltk_resource('punkt')
        analysis = {
            "total_articles": len(articles),
            "publishers": {},
            "publication_timeline": {},
            "common_keywords": {},
            "topics": [],
            "oldest_article": None,
            "newest_article": None,
            "most_active_publishers": []
        }
        
        # Process text for analysis
        all_text = ""
        publisher_counter = Counter()
        publication_days = Counter()
        
        for article in articles:
            # Count publishers
            if 'publisher' in article:
                publisher = article['publisher']
                publisher_counter[publisher] += 1
            
            # Track publication timeline
            if 'published_datetime' in article and article['published_datetime'] != article.get('published_time'):
                try:
                    article_date = datetime.fromisoformat(article['published_datetime'])
                    day_key = article_date.strftime('%Y-%m-%d')
                    publication_days[day_key] += 1
                except:
                    pass
            
            # Collect text for keyword analysis
            if 'title' in article:
                all_text += " " + article['title']
            if 'snippet' in article:
                all_text += " " + article['snippet']
        
        # Sort and prepare publishers data
        analysis["publishers"] = dict(publisher_counter)
        analysis["most_active_publishers"] = publisher_counter.most_common(5)
        
        # Sort and prepare timeline data
        analysis["publication_timeline"] = dict(sorted(publication_days.items()))
        
        # Extract keywords
        stop_words = set(stopwords.words('english'))
        additional_stops = {"news", "says", "new", "according", "could", "may", "also", "first", "one"}
        stop_words.update(additional_stops)
        
        try:
            # Tokenize and clean text
            word_tokens = word_tokenize(all_text.lower())
            filtered_words = [w for w in word_tokens if w.isalpha() and w not in stop_words and len(w) > 3]
            
            # Get keyword frequencies
            word_freq = Counter(filtered_words)
            analysis["common_keywords"] = dict(word_freq.most_common(20))
            
            # Topic extraction (simple approach - could be improved with NLP models)
            bigrams = self.extract_ngrams(filtered_words, 2)
            analysis["topics"] = bigrams[:10]  # Top 10 bigrams as topics
        except Exception as e:
            logger.error(f"Error in keyword analysis: {e}")
            analysis["common_keywords"] = {"error": str(e)}
        
        # Oldest and newest articles
        try:
            dated_articles = [a for a in articles if 'published_datetime' in a 
                            and a['published_datetime'] != a.get('published_time')]
            
            if dated_articles:
                dated_articles.sort(key=lambda x: x['published_datetime'])
                analysis["oldest_article"] = {
                    "title": dated_articles[0]["title"],
                    "publisher": dated_articles[0].get("publisher", "Unknown"),
                    "date": dated_articles[0]["published_datetime"]
                }
                analysis["newest_article"] = {
                    "title": dated_articles[-1]["title"],
                    "publisher": dated_articles[-1].get("publisher", "Unknown"),
                    "date": dated_articles[-1]["published_datetime"]
                }
        except Exception as e:
            logger.error(f"Error analyzing article dates: {e}")
        
        return analysis
    
    def extract_ngrams(self, word_list, n=2):
        """Extract n-grams from a list of words"""
        ngrams = []
        for i in range(len(word_list) - n + 1):
            ngrams.append(' '.join(word_list[i:i+n]))
        
        # Count and sort
        ngram_counter = Counter(ngrams)
        return ngram_counter.most_common(20)
    
    def generate_wordcloud(self, articles, filename):
        """
        Generate a word cloud from article content
        
        Args:
            articles (list): List of article dictionaries
            filename (str): Output filename for the word cloud image
        """
        try:
            # Ensure NLTK resources
            ensure_nltk_resource('stopwords')
            all_text = ""
            for article in articles:
                if 'title' in article:
                    all_text += " " + article['title']
                if 'snippet' in article:
                    all_text += " " + article['snippet']
            
            # Clean text
            stop_words = set(stopwords.words('english'))
            additional_stops = {"news", "says", "new", "according", "could", "may", "also", "first", "one"}
            stop_words.update(additional_stops)
            
            # Create and save wordcloud
            wordcloud = WordCloud(
                width=800, 
                height=400, 
                background_color='white',
                stopwords=stop_words,
                max_words=100,
                contour_width=3
            ).generate(all_text)
            
            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300)
            plt.close()
            
            logger.info(f"Generated word cloud: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error generating word cloud: {e}")
            return False
    
    def plot_timeline(self, analysis, filename):
        """
        Plot article publication timeline
        
        Args:
            analysis (dict): Analysis dictionary containing timeline data
            filename (str): Output filename for the timeline chart
        """
        try:
            timeline = analysis.get("publication_timeline", {})
            if not timeline:
                return False
            
            # Create the plot
            plt.figure(figsize=(12, 6))
            x = list(timeline.keys())
            y = list(timeline.values())
            
            plt.bar(x, y, color='skyblue')
            plt.xlabel('Date')
            plt.ylabel('Number of Articles')
            plt.title('AI News Publication Timeline')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300)
            plt.close()
            
            logger.info(f"Generated timeline chart: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error generating timeline chart: {e}")
            return False
    
    def save_to_json(self, data, filename):
        """Save data to a JSON file"""
        if not data:
            logger.warning("No data to save")
            return
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved data to {filepath}")
    
    def save_to_csv(self, articles, filename):
        """Save articles to a CSV file"""
        if not articles:
            logger.warning("No articles to save")
            return
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Get all possible fields
        all_fields = set()
        for article in articles:
            all_fields.update(article.keys())
        
        # Convert to list and sort
        fieldnames = sorted(list(all_fields))
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for article in articles:
                writer.writerow(article)
        
        logger.info(f"Saved {len(articles)} articles to {filepath}")
    
    def selenium_search_news(self, query, max_articles=30, headless=True):
        """
        Use Selenium to fetch Google News search results, bypassing consent wall.
        
        Args:
            query (str): Search query
            max_articles (int): Maximum number of articles to fetch
            headless (bool): Run browser in headless mode
            
        Returns:
            list: List of article dictionaries
        """
        articles = []
        encoded_query = quote_plus(query)
        search_url = SEARCH_URL.format(encoded_query)
        
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_argument('--user-agent=' + self.get_random_user_agent())
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(search_url)
        try:
            # Try to click any visible consent/accept button
            try:
                WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH, '//button'))
                )
                buttons = driver.find_elements(By.XPATH, '//button')
                for btn in buttons:
                    if btn.is_displayed() and ("accept" in btn.text.lower() or "agree" in btn.text.lower()):
                        btn.click()
                        break
            except Exception:
                pass  # Consent not present or already handled
            
            # Wait longer for articles to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'article'))
            )
            # Save screenshot for debugging
            driver.save_screenshot('selenium_debug_screenshot.png')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            article_elements = soup.find_all('article')
            for article_elem in article_elements[:max_articles]:
                try:
                    article = self.extract_article_data(article_elem)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.warning(f"Error extracting article data: {e}")
        finally:
            driver.quit()
        logger.info(f"Selenium: Found {len(articles)} articles on search page")
        return articles

def main():
    """Main function to run the scraper"""
    logger.info("Starting Google News scraper for AI news")
    
    # Create scraper
    scraper = GoogleNewsScraper(respect_robots=False)
    
    # Default search query for AI news
    default_query = "artificial intelligence news"
    search_query = input(f"Enter search query (default: '{default_query}'): ") or default_query
    
    max_pages = int(input("Maximum number of pages to scrape (default: 3): ") or "3")
    
    # Scrape news articles using Selenium
    logger.info(f"Searching for: {search_query}")
    articles = scraper.selenium_search_news(search_query, max_articles=max_pages*30, headless=True)
    
    if articles:
        # Generate filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_query = re.sub(r'[^\w]', '_', search_query.lower())
        json_filename = f"{sanitized_query}_{timestamp}.json"
        csv_filename = f"{sanitized_query}_{timestamp}.csv"
        wordcloud_filename = f"{sanitized_query}_wordcloud_{timestamp}.png"
        timeline_filename = f"{sanitized_query}_timeline_{timestamp}.png"
        analysis_filename = f"{sanitized_query}_analysis_{timestamp}.json"
        
        # Save results
        scraper.save_to_json(articles, json_filename)
        scraper.save_to_csv(articles, csv_filename)
        
        # Analyze articles
        analysis = scraper.analyze_news(articles)
        scraper.save_to_json(analysis, analysis_filename)
        
        # Generate visualizations
        scraper.generate_wordcloud(articles, wordcloud_filename)
        scraper.plot_timeline(analysis, timeline_filename)
        
        print(f"\nScraping completed successfully!")
        print(f"Found {len(articles)} articles about {search_query}")
        print(f"Results saved to:")
        print(f"  - {os.path.join(OUTPUT_DIR, json_filename)}")
        print(f"  - {os.path.join(OUTPUT_DIR, csv_filename)}")
        print(f"  - {os.path.join(OUTPUT_DIR, analysis_filename)}")
        print(f"  - {os.path.join(OUTPUT_DIR, wordcloud_filename)}")
        print(f"  - {os.path.join(OUTPUT_DIR, timeline_filename)}")
        
        # Display top publishers and recent news
        print("\nTop 5 Publishers:")
        for publisher, count in analysis["most_active_publishers"]:
            print(f"  - {publisher}: {count} articles")
        
        print("\nMost Recent AI News:")
        recent_articles = sorted(articles, 
                                key=lambda x: x.get('published_datetime', ''), 
                                reverse=True)[:5]
        for i, article in enumerate(recent_articles):
            print(f"{i+1}. {article.get('title', 'Untitled')}")
            print(f"   Source: {article.get('publisher', 'Unknown')}")
            print(f"   Published: {article.get('published_time', 'Unknown')}")
            print(f"   Link: {article.get('url', '')}")
            print()
    else:
        print("\nNo articles found or scraping failed")

if __name__ == "__main__":
    main()
