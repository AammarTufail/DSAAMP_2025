# Google News AI Scraper

A robust Google News scraper specialized for collecting and analyzing AI-related news articles.

## Features

- **Targeted AI News Collection**: Focuses on artificial intelligence news from Google News
- **Advanced Rate Limiting**: Random delays between requests to avoid detection
- **User-Agent Rotation**: Cycles through different browser signatures
- **Respectful Scraping**: Honours robots.txt rules (optional)
- **Error Handling**: Sophisticated retry mechanism
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Data Export**: Save results in both JSON and CSV formats
- **News Analysis**: Extracts insights and patterns from collected articles
- **Data Visualization**: Generates word clouds and timeline charts

## Setup

1. Install required dependencies:

```bash
pip install requests beautifulsoup4 fake-useragent nltk matplotlib wordcloud
```

2. Download required NLTK resources (first time only):

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

3. Run the script:

```bash
python google_news_scraper.py
```

## Usage

1. Enter a search query when prompted (default: "artificial intelligence news")
2. Specify the maximum number of pages to scrape (default: 3)
3. The script will search for articles, extract details, analyze the content, and save the results

## Output

The script generates multiple files for each search:
- JSON file with complete article data
- CSV file with article data in tabular format
- Analysis JSON file with insights about publishers, keywords, and publication patterns
- Word cloud image visualizing the most common terms
- Timeline chart showing publication frequency over time

## Scraped Information

For each article, the scraper attempts to extract:

- Title
- URL link to the original article
- Publisher name
- Publication time
- Article snippet/description
- Thumbnail image URL

## Analysis Features

The news analysis provides valuable insights:

- **Publisher Distribution**: Which sources are publishing the most AI content
- **Publication Timeline**: When articles are being published
- **Common Keywords**: Most frequently mentioned terms
- **Emerging Topics**: Common phrases and potential trending topics
- **Historical Range**: Oldest and newest articles in the dataset

## Visualizations

The scraper generates two types of visualizations:

1. **Word Cloud**: Visual representation of the most common terms in article titles and snippets
2. **Timeline Chart**: Bar chart showing the distribution of articles over time

## Best Practices Implemented

This scraper follows ethical scraping practices:

1. **Mimics human behavior** with random delays between requests
2. **Uses rotating user agents** to appear as different browsers
3. **Respects robots.txt** rules when configured to do so
4. **Handles errors gracefully** with intelligent retry logic
5. **Provides comprehensive logging** for monitoring and debugging

## Limitations

- Google News structure may change, requiring selector updates
- The timeline analysis is limited by the time format Google provides
- Word frequency analysis is basic compared to advanced NLP techniques
- The scraper doesn't click through to original articles for full content

## Disclaimer

This tool is provided for educational purposes only. Web scraping may violate Google's Terms of Service. Use responsibly and at your own risk.
