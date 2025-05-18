"""
Google Play Store Scraper

This script scrapes app information from the Google Play Store while implementing best practices:
- Random delays between requests
- Rotating user agents
- Respect for robots.txt
- Error handling and retries
- Rate limiting
- Logging
- Data export (JSON, CSV)
- App analysis and visualization

It's designed to collect comprehensive app data including title, developer,
rating, reviews, category, pricing, and additional metadata.
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
from datetime import datetime
from fake_useragent import UserAgent
from requests.exceptions import RequestException, Timeout, ConnectionError
import urllib.robotparser
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='play_store_scraper.log',
    filemode='a'
)
logger = logging.getLogger('play_store_scraper')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Constants
BASE_URL = "https://play.google.com"
SEARCH_URL = "https://play.google.com/store/search?q={}&c=apps"
CATEGORY_URL = "https://play.google.com/store/apps/category/{}"
OUTPUT_DIR = "play_store_data"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 10

# App categories
APP_CATEGORIES = {
    "ART_AND_DESIGN": "ART_AND_DESIGN",
    "AUTO_AND_VEHICLES": "AUTO_AND_VEHICLES",
    "BEAUTY": "BEAUTY",
    "BOOKS_AND_REFERENCE": "BOOKS_AND_REFERENCE",
    "BUSINESS": "BUSINESS",
    "COMICS": "COMICS",
    "COMMUNICATION": "COMMUNICATION",
    "DATING": "DATING",
    "EDUCATION": "EDUCATION",
    "ENTERTAINMENT": "ENTERTAINMENT",
    "EVENTS": "EVENTS",
    "FINANCE": "FINANCE",
    "FOOD_AND_DRINK": "FOOD_AND_DRINK",
    "HEALTH_AND_FITNESS": "HEALTH_AND_FITNESS",
    "HOUSE_AND_HOME": "HOUSE_AND_HOME",
    "LIBRARIES_AND_DEMO": "LIBRARIES_AND_DEMO",
    "LIFESTYLE": "LIFESTYLE",
    "MAPS_AND_NAVIGATION": "MAPS_AND_NAVIGATION",
    "MEDICAL": "MEDICAL",
    "MUSIC_AND_AUDIO": "MUSIC_AND_AUDIO",
    "NEWS_AND_MAGAZINES": "NEWS_AND_MAGAZINES",
    "PARENTING": "PARENTING",
    "PERSONALIZATION": "PERSONALIZATION",
    "PHOTOGRAPHY": "PHOTOGRAPHY",
    "PRODUCTIVITY": "PRODUCTIVITY",
    "SHOPPING": "SHOPPING",
    "SOCIAL": "SOCIAL",
    "SPORTS": "SPORTS",
    "TOOLS": "TOOLS",
    "TRAVEL_AND_LOCAL": "TRAVEL_AND_LOCAL",
    "VIDEO_PLAYERS": "VIDEO_PLAYERS",
    "WEATHER": "WEATHER"
}

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class PlayStoreScraper:
    """Class to scrape Google Play Store app information"""
    
    def __init__(self, respect_robots=True, delay_range=(2, 5)):
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
            'Referer': 'https://play.google.com/',
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
    
    def search_apps(self, query, max_apps=50):
        """
        Search for apps on Google Play Store
        
        Args:
            query (str): Search query
            max_apps (int): Maximum number of apps to retrieve
            
        Returns:
            list: List of app URLs
        """
        app_urls = []
        encoded_query = quote_plus(query)
        search_url = SEARCH_URL.format(encoded_query)
        
        success, response = self.make_request(search_url)
        
        if not success:
            logger.error(f"Failed to retrieve search page: {response}")
            return app_urls
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find app elements - Google Play Store uses complex structure
        # Selectors may need adjustment as the site changes
        app_elements = soup.select('div[data-uitype="500"] a[href^="/store/apps/details"]')
        
        for app_elem in app_elements:
            if len(app_urls) >= max_apps:
                break
                
            try:
                app_url = urljoin(BASE_URL, app_elem['href'])
                if app_url not in app_urls:
                    app_urls.append(app_url)
            except Exception as e:
                logger.warning(f"Error extracting app URL: {e}")
        
        logger.info(f"Found {len(app_urls)} app URLs")
        return app_urls
    
    def get_apps_by_category(self, category, max_apps=50):
        """
        Get apps from a specific category
        
        Args:
            category (str): Category ID from APP_CATEGORIES
            max_apps (int): Maximum number of apps to retrieve
            
        Returns:
            list: List of app URLs
        """
        app_urls = []
        category_url = CATEGORY_URL.format(category)
        
        success, response = self.make_request(category_url)
        
        if not success:
            logger.error(f"Failed to retrieve category page: {response}")
            return app_urls
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find app elements within the category page
        app_elements = soup.select('div[data-uitype="500"] a[href^="/store/apps/details"]')
        
        for app_elem in app_elements:
            if len(app_urls) >= max_apps:
                break
                
            try:
                app_url = urljoin(BASE_URL, app_elem['href'])
                if app_url not in app_urls:
                    app_urls.append(app_url)
            except Exception as e:
                logger.warning(f"Error extracting app URL: {e}")
        
        logger.info(f"Found {len(app_urls)} app URLs for category {category}")
        return app_urls
    
    def extract_app_details(self, url):
        """
        Extract details from an app page
        
        Args:
            url (str): App URL
            
        Returns:
            dict: App details or None if failed
        """
        success, response = self.make_request(url)
        
        if not success:
            logger.error(f"Failed to retrieve app page: {response}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        try:
            app = {
                'url': url,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract app ID from URL
            app_id_match = re.search(r'id=([^&]+)', url)
            if app_id_match:
                app['app_id'] = app_id_match.group(1)
            
            # App title
            title_elem = soup.select_one('h1[itemprop="name"]')
            if title_elem:
                app['title'] = title_elem.text.strip()
            
            # Developer name
            dev_elem = soup.select_one('a[href^="/store/apps/dev"]')
            if dev_elem:
                app['developer'] = dev_elem.text.strip()
                app['developer_url'] = urljoin(BASE_URL, dev_elem['href'])
            
            # Rating
            rating_elem = soup.select_one('div[role="img"][aria-label*="stars"]')
            if rating_elem:
                rating_text = rating_elem.get('aria-label', '')
                rating_match = re.search(r'([\d.]+) stars', rating_text)
                if rating_match:
                    app['rating'] = float(rating_match.group(1))
            
            # Number of ratings
            ratings_count_elem = soup.select_one('div[aria-label*="ratings"]')
            if ratings_count_elem:
                count_text = ratings_count_elem.text.strip().replace(',', '')
                count_match = re.search(r'([\d,]+)', count_text)
                if count_match:
                    app['ratings_count'] = count_match.group(1)
            
            # Price
            price_elem = soup.select_one('meta[itemprop="price"]')
            if price_elem and price_elem.has_attr('content'):
                app['price'] = price_elem['content']
                app['is_free'] = (price_elem['content'] == '0')
            
            # Category
            category_elem = soup.select_one('a[href^="/store/apps/category"]')
            if category_elem:
                app['category'] = category_elem.text.strip()
                
                # Extract category ID from URL
                cat_url = category_elem.get('href', '')
                cat_id_match = re.search(r'category/([^/]+)', cat_url)
                if cat_id_match:
                    app['category_id'] = cat_id_match.group(1)
            
            # Content rating
            content_rating_elem = soup.select_one('[content-desc*="Content rating"] ~ div')
            if content_rating_elem:
                app['content_rating'] = content_rating_elem.text.strip()
            
            # Description
            desc_elem = soup.select_one('meta[itemprop="description"]')
            if desc_elem and desc_elem.has_attr('content'):
                app['description'] = desc_elem['content']
            
            # Screenshots
            screenshots = []
            screenshot_elems = soup.select('img[alt="Screenshot Image"][srcset]')
            for img in screenshot_elems:
                if img.has_attr('srcset'):
                    # Extract highest resolution image from srcset
                    srcset = img['srcset']
                    highest_res = srcset.split(',')[-1].strip().split(' ')[0]
                    screenshots.append(highest_res)
            
            app['screenshots'] = screenshots
            
            # Icon
            icon_elem = soup.select_one('img[itemprop="image"][src]')
            if icon_elem and icon_elem.has_attr('src'):
                app['icon_url'] = icon_elem['src']
            
            # Installation size
            size_elem = soup.select_one('[content-desc*="Size"] ~ div')
            if size_elem:
                app['size'] = size_elem.text.strip()
            
            # Current version
            version_elem = soup.select_one('[content-desc*="Current Version"] ~ div')
            if version_elem:
                app['version'] = version_elem.text.strip()
            
            # Required Android version
            android_version_elem = soup.select_one('[content-desc*="Requires Android"] ~ div')
            if android_version_elem:
                app['required_android_version'] = android_version_elem.text.strip()
            
            # In-app purchases
            iap_elem = soup.select_one('[content-desc*="In-app purchases"] ~ div')
            if iap_elem:
                app['has_iap'] = True
                app['iap_range'] = iap_elem.text.strip()
            else:
                app['has_iap'] = False
            
            # Updated date
            updated_elem = soup.select_one('[content-desc*="Updated on"] ~ div')
            if updated_elem:
                app['updated_date'] = updated_elem.text.strip()
            
            # Downloads count
            downloads_elem = soup.select_one('[content-desc*="Downloads"] ~ div')
            if downloads_elem:
                app['downloads'] = downloads_elem.text.strip()
            
            return app
        
        except Exception as e:
            logger.error(f"Error extracting app details: {e}")
            return None
    
    def analyze_apps(self, apps):
        """
        Analyze collected app data
        
        Args:
            apps (list): List of app dictionaries
            
        Returns:
            dict: Analysis results
        """
        if not apps:
            return {"error": "No apps found"}
        
        analysis = {
            "total_apps": len(apps),
            "categories": {},
            "free_vs_paid": {
                "free": 0,
                "paid": 0
            },
            "rating_distribution": {},
            "price_statistics": {
                "min": None,
                "max": None,
                "average": None
            },
            "developers": {},
            "content_ratings": {},
            "android_version_requirements": {},
            "top_rated_apps": [],
            "most_downloaded_apps": []
        }
        
        # Process app data
        category_counter = Counter()
        content_rating_counter = Counter()
        dev_counter = Counter()
        android_version_counter = Counter()
        prices = []
        
        for app in apps:
            # Count categories
            if 'category' in app:
                category_counter[app['category']] += 1
            
            # Free vs Paid
            if 'is_free' in app:
                if app['is_free']:
                    analysis["free_vs_paid"]["free"] += 1
                else:
                    analysis["free_vs_paid"]["paid"] += 1
            
            # Rating distribution
            if 'rating' in app:
                # Round to nearest 0.5
                rating = round(app['rating'] * 2) / 2
                rating_key = str(rating)
                if rating_key not in analysis["rating_distribution"]:
                    analysis["rating_distribution"][rating_key] = 0
                analysis["rating_distribution"][rating_key] += 1
            
            # Price statistics for paid apps
            if 'price' in app and app.get('is_free') is False:
                try:
                    price_value = float(app['price'])
                    prices.append(price_value)
                except:
                    pass
            
            # Count developers
            if 'developer' in app:
                dev_counter[app['developer']] += 1
            
            # Content ratings
            if 'content_rating' in app:
                content_rating_counter[app['content_rating']] += 1
            
            # Android version requirements
            if 'required_android_version' in app:
                android_version_counter[app['required_android_version']] += 1
        
        # Process collected data for analysis
        analysis["categories"] = dict(category_counter.most_common())
        analysis["developers"] = dict(dev_counter.most_common(10))
        analysis["content_ratings"] = dict(content_rating_counter.most_common())
        analysis["android_version_requirements"] = dict(android_version_counter.most_common())
        
        # Price statistics
        if prices:
            analysis["price_statistics"]["min"] = min(prices)
            analysis["price_statistics"]["max"] = max(prices)
            analysis["price_statistics"]["average"] = sum(prices) / len(prices)
        
        # Get top rated apps
        rated_apps = [a for a in apps if 'rating' in a and a['rating']]
        rated_apps.sort(key=lambda x: x['rating'], reverse=True)
        
        for app in rated_apps[:5]:
            analysis["top_rated_apps"].append({
                "title": app.get('title', 'Unknown'),
                "developer": app.get('developer', 'Unknown'),
                "rating": app.get('rating', 'N/A'),
                "category": app.get('category', 'Unknown'),
                "url": app.get('url', '')
            })
        
        return analysis
    
    def scrape_apps(self, query=None, category=None, max_apps=50):
        """
        Search for and scrape apps from Google Play Store
        
        Args:
            query (str): Search query (optional)
            category (str): Category ID from APP_CATEGORIES (optional)
            max_apps (int): Maximum number of apps to scrape
            
        Returns:
            list: List of app details
        """
        app_urls = []
        
        if query:
            logger.info(f"Searching for apps with query: {query}")
            app_urls = self.search_apps(query, max_apps)
        elif category:
            logger.info(f"Getting apps from category: {category}")
            app_urls = self.get_apps_by_category(category, max_apps)
        else:
            logger.error("Either query or category must be provided")
            return []
        
        logger.info(f"Found {len(app_urls)} app URLs")
        
        # Scrape app details
        apps = []
        for i, url in enumerate(app_urls):
            logger.info(f"Scraping app {i+1}/{len(app_urls)}: {url}")
            app = self.extract_app_details(url)
            if app:
                apps.append(app)
        
        return apps
    
    def generate_visualizations(self, apps, analysis, prefix):
        """
        Generate visualizations from app data
        
        Args:
            apps (list): List of app dictionaries
            analysis (dict): Analysis dictionary
            prefix (str): Filename prefix for generated images
        
        Returns:
            list: Paths to generated visualization files
        """
        viz_files = []
        try:
            # Create a directory for visualizations
            viz_dir = os.path.join(OUTPUT_DIR, "visualizations")
            os.makedirs(viz_dir, exist_ok=True)
            
            # 1. Rating Distribution
            if analysis["rating_distribution"]:
                plt.figure(figsize=(10, 6))
                ratings = [float(k) for k in analysis["rating_distribution"].keys()]
                counts = list(analysis["rating_distribution"].values())
                
                plt.bar(ratings, counts, color='skyblue', width=0.4)
                plt.xlabel('Rating')
                plt.ylabel('Number of Apps')
                plt.title('App Rating Distribution')
                plt.xticks([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                
                ratings_file = os.path.join(viz_dir, f"{prefix}_rating_distribution.png")
                plt.savefig(ratings_file, dpi=300, bbox_inches='tight')
                plt.close()
                viz_files.append(ratings_file)
            
            # 2. Category Distribution
            if analysis["categories"]:
                plt.figure(figsize=(12, 8))
                # Sort categories by count
                categories = dict(sorted(analysis["categories"].items(), 
                                  key=lambda x: x[1], reverse=True)[:10])
                
                y_pos = range(len(categories))
                plt.barh(y_pos, categories.values(), color='lightgreen')
                plt.yticks(y_pos, categories.keys())
                plt.xlabel('Number of Apps')
                plt.title('Top 10 App Categories')
                plt.tight_layout()
                
                categories_file = os.path.join(viz_dir, f"{prefix}_category_distribution.png")
                plt.savefig(categories_file, dpi=300, bbox_inches='tight')
                plt.close()
                viz_files.append(categories_file)
            
            # 3. Free vs Paid
            plt.figure(figsize=(8, 8))
            free_count = analysis["free_vs_paid"]["free"]
            paid_count = analysis["free_vs_paid"]["paid"]
            
            plt.pie([free_count, paid_count], 
                   labels=['Free', 'Paid'], 
                   autopct='%1.1f%%',
                   colors=['#66b3ff', '#ff9999'],
                   startangle=90,
                   explode=(0.1, 0))
            plt.title('Free vs Paid Apps')
            plt.axis('equal')
            
            pricing_file = os.path.join(viz_dir, f"{prefix}_free_vs_paid.png")
            plt.savefig(pricing_file, dpi=300, bbox_inches='tight')
            plt.close()
            viz_files.append(pricing_file)
            
            # 4. Content Rating Distribution
            if analysis["content_ratings"]:
                plt.figure(figsize=(10, 6))
                # Sort by count
                content_ratings = dict(sorted(analysis["content_ratings"].items(), 
                                      key=lambda x: x[1], reverse=True))
                
                plt.bar(content_ratings.keys(), content_ratings.values(), color='coral')
                plt.xlabel('Content Rating')
                plt.ylabel('Number of Apps')
                plt.title('Content Rating Distribution')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                content_file = os.path.join(viz_dir, f"{prefix}_content_ratings.png")
                plt.savefig(content_file, dpi=300, bbox_inches='tight')
                plt.close()
                viz_files.append(content_file)
            
            logger.info(f"Generated {len(viz_files)} visualization files")
            return viz_files
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            return viz_files
    
    def save_to_json(self, data, filename):
        """Save data to a JSON file"""
        if not data:
            logger.warning("No data to save")
            return
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved data to {filepath}")
    
    def save_to_csv(self, apps, filename):
        """Save apps to a CSV file"""
        if not apps:
            logger.warning("No apps to save")
            return
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Get all possible fields
        all_fields = set()
        for app in apps:
            all_fields.update(app.keys())
        
        # Remove list/dict fields that will need special handling
        for field in ['screenshots']:
            if field in all_fields:
                all_fields.remove(field)
        
        # Convert to list and sort
        fieldnames = sorted(list(all_fields))
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for app in apps:
                # Prepare a version of the app dict that's safe for CSV
                safe_app = {k: v for k, v in app.items() if k != 'screenshots'}
                
                # Handle screenshots as comma-separated string
                if 'screenshots' in app:
                    safe_app['screenshot_urls'] = ', '.join(app['screenshots'])
                
                writer.writerow(safe_app)
        
        logger.info(f"Saved {len(apps)} apps to {filepath}")

def main():
    """Main function to run the scraper"""
    logger.info("Starting Google Play Store scraper")
    
    # Create scraper
    scraper = PlayStoreScraper(respect_robots=True)
    
    # Present options to the user
    print("\nSelect search method:")
    print("1. Search by keyword")
    print("2. Browse by category")
    choice = input("Enter your choice (1 or 2): ")
    
    max_apps = int(input("\nMaximum number of apps to scrape (default: 20): ") or "20")
    
    apps = []
    search_method = ""
    search_term = ""
    
    if choice == "1":
        # Search by keyword
        query = input("\nEnter search query: ")
        search_method = "search"
        search_term = query
        apps = scraper.scrape_apps(query=query, max_apps=max_apps)
    elif choice == "2":
        # Browse by category
        print("\nAvailable Categories:")
        for i, (category_id, name) in enumerate(sorted(APP_CATEGORIES.items())):
            print(f"{i+1}. {name.replace('_', ' ').title()}")
        
        category_choice = input("\nEnter category number: ")
        try:
            category_idx = int(category_choice) - 1
            category_ids = sorted(APP_CATEGORIES.keys())
            category = category_ids[category_idx]
            
            search_method = "category"
            search_term = category.replace('_', ' ').lower()
            
            apps = scraper.scrape_apps(category=category, max_apps=max_apps)
        except (ValueError, IndexError):
            print("Invalid category selection.")
            return
    else:
        print("Invalid choice.")
        return
    
    if apps:
        # Generate filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_term = re.sub(r'[^\w]', '_', search_term.lower())
        file_prefix = f"{search_method}_{sanitized_term}_{timestamp}"
        
        json_filename = f"{file_prefix}.json"
        csv_filename = f"{file_prefix}.csv"
        analysis_filename = f"{file_prefix}_analysis.json"
        
        # Save results
        scraper.save_to_json(apps, json_filename)
        scraper.save_to_csv(apps, csv_filename)
        
        # Analyze apps
        analysis = scraper.analyze_apps(apps)
        scraper.save_to_json(analysis, analysis_filename)
        
        # Generate visualizations
        viz_files = scraper.generate_visualizations(apps, analysis, file_prefix)
        
        print(f"\nScraping completed successfully!")
        print(f"Found {len(apps)} apps")
        print(f"Results saved to:")
        print(f"  - {os.path.join(OUTPUT_DIR, json_filename)}")
        print(f"  - {os.path.join(OUTPUT_DIR, csv_filename)}")
        print(f"  - {os.path.join(OUTPUT_DIR, analysis_filename)}")
        
        if viz_files:
            print(f"  - Generated {len(viz_files)} visualization files in {os.path.join(OUTPUT_DIR, 'visualizations')}")
        
        # Display top apps
        print("\nTop 5 Rated Apps:")
        for i, app in enumerate(analysis["top_rated_apps"]):
            print(f"{i+1}. {app['title']}")
            print(f"   By: {app['developer']}")
            print(f"   Rating: {app['rating']} ⭐")
            print(f"   Category: {app['category']}")
            print()
        
        # Display category distribution
        print("\nCategory Distribution:")
        for category, count in list(analysis["categories"].items())[:5]:
            print(f"  - {category}: {count} apps")
    else:
        print("\nNo apps found or scraping failed")

if __name__ == "__main__":
    main()
