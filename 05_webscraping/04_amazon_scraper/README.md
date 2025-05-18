# Amazon Product Scraper

A robust Amazon product data scraper that implements best practices to avoid being blocked while providing comprehensive data analysis.

## Features

- **Advanced Rate Limiting**: Random delays between requests to avoid detection
- **User-Agent Rotation**: Cycles through different browser signatures
- **Proxy Rotation**: Automatically fetches and validates free proxies (optional)
- **Respectful Scraping**: Honours robots.txt rules (optional)
- **Error Handling**: Sophisticated retry mechanism with exponential backoff
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Data Export**: Save results in both JSON and CSV formats
- **Search Results Analysis**: Automatically analyzes product data to extract insights

## Setup

1. Install required dependencies:

```bash
pip install requests beautifulsoup4 fake-useragent
```

2. Run the script:

```bash
python amazon_scraper.py
```

## Usage

1. Enter a search query when prompted (e.g., "wireless headphones")
2. Specify the maximum number of search result pages to scrape (1-20)
3. Specify the maximum number of products to scrape (or leave blank to scrape all found)
4. The script will search for products, extract details, and save the results in the `amazon_data` directory

## Output

The script generates three files for each search:
- A JSON file with the complete product data structure
- A CSV file with flattened data for easy importing into spreadsheets
- An analysis JSON file with insights about the scraped products

## Analysis Features

The scraper now includes powerful analysis capabilities:

- **Top-Rated Products**: Identifies and displays the 5 highest-rated products
- **Price Range Analysis**: Calculates minimum, maximum and average prices
- **Rating Distribution**: Shows how ratings are distributed across products
- **Common Features**: Identifies frequently mentioned product features and specifications

After scraping is complete, the analysis summary is displayed in the console and saved to a JSON file for further review.

## Scraped Information

For each product, the scraper attempts to extract:

- Product title
- Current price
- Availability
- Customer rating (out of 5 stars)
- Number of reviews
- Detailed features
- Product description
- Product specifications
- Image URLs

## Example Analysis Output

When the scraping is complete, you'll see a summary of top products directly in the console:

```
Top 5 ranked products for this search:
1. Sony WH-1000XM4 Wireless Noise Canceling Overhead Headphones
   Rating: 4.7 ⭐ (34,592 reviews)
   Price: $348.00

2. Bose QuietComfort 45 Bluetooth Wireless Headphones
   Rating: 4.6 ⭐ (12,789 reviews)
   Price: $329.00

...
```

The full analysis is saved to a JSON file that includes:
- Complete listing of top-rated products
- Statistical breakdown of prices
- Rating distribution across all products
- Common features and specifications

## Best Practices Implemented

This scraper follows these best practices:

1. **Mimics human behavior** with random delays between requests
2. **Uses rotating user agents** to appear as different browsers
3. **Implements proxy rotation** to distribute requests across different IPs
4. **Respects robots.txt** rules when configured to do so
5. **Handles errors gracefully** with intelligent retry logic
6. **Provides comprehensive logging** for monitoring and debugging
7. **Avoids excessive requests** by implementing rate limiting

## Limitations

- Amazon's website structure changes frequently, so selectors may need updating
- Using free proxies can be unreliable, as they may be slow or stop working
- CAPTCHAs may still appear if Amazon detects scraping patterns
- The script does not handle product variations or "See all buying options"

## Disclaimer

This tool is provided for educational purposes only. Web scraping may violate Amazon's Terms of Service. Use responsibly and at your own risk.
