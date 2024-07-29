import cloudscraper
from bs4 import BeautifulSoup
import logging
from flask import current_app
import random

def create_browser_session():
    user_agent = (
        f"Mozilla/5.0 (Android {current_app.config['ANDROID_VERSION']}; Mobile; rv:{current_app.config['BROWSER_VERSION']}) "
        f"Gecko/{current_app.config['BROWSER_VERSION']} Firefox/{current_app.config['BROWSER_VERSION']} "
        f"KAIOS/{current_app.config['BROWSER_VERSION']}"
    )
    
    return cloudscraper.create_scraper(
        browser={
            'browser': current_app.config['BROWSER_NAME'],
            'platform': current_app.config['BROWSER_PLATFORM'],
            'mobile': current_app.config['BROWSER_MOBILE'],
            'custom': user_agent
        },
        delay=current_app.config['REQUEST_DELAY']
    )

def fetch_content(url):
    session = create_browser_session()
    try:
        headers = {
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers',
        }
        
        if current_app.config['USE_PROXY'] and current_app.config['PROXY_URL']:
            proxies = {'http': current_app.config['PROXY_URL'], 'https': current_app.config['PROXY_URL']}
        else:
            proxies = None

        response = session.get(
            url, 
            timeout=current_app.config['REQUEST_TIMEOUT'],
            proxies=proxies,
            headers=headers
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        logging.error(f"Error fetching content: {str(e)}")
        return None

def parse_chapter_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # This is a placeholder. Adjust the selector based on the actual structure of the websites.
    chapter_links = soup.select('a.chapter-link')
    return [link['href'] for link in chapter_links]

def set_custom_cookies(session, cookies):
    for cookie_name, cookie_value in cookies.items():
        session.cookies.set(cookie_name, cookie_value, domain='.example.com')  # Replace with actual domain

def simulate_human_behavior(session):
    # Simulate scrolling
    scroll_amount = random.randint(500, 1500)
    session.get(f"javascript:window.scrollBy(0,{scroll_amount})")
    
    # Simulate random clicks (you'd need to implement this based on the site's structure)
    # session.get("javascript:document.querySelector('a.random-link').click()")
    
    # Add a random delay between actions
    import time
    time.sleep(random.uniform(1, 5))
    
from urllib.parse import urljoin
from urllib.parse import urlparse
import logging
logging.basicConfig(level=logging.DEBUG)

# Then in your function:


def parse_all_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    regular_links = []
    books = {}
    pagination_links = []

    # Parse books from table
    table = soup.find('table', {'class': 'table'})
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        book = {
            'bookTitle': cols[1].text.strip(),
            'bookurl': cols[1].find('a')['href'],
            'latestChapterTitle': cols[2].find('a').text.strip(),
            'latestChapterUrl': cols[2].find('a')['href'],
            'author': cols[3].text.strip()
        }
        books[book['bookurl']] = book  # Use bookurl as key for easy lookup

    # Parse regular links and pagination links
    all_links = soup.find_all('a', href=True)
    for a in all_links:
        if a.find_parent('ul', {'class': 'pagination', 'id': 'pagelink'}) is None:
            text = a.text.strip()
            url = urljoin(base_url, a['href'])
            parsed_url = urlparse(url)
            if 'book' not in parsed_url.path and 'book' not in parsed_url.query:
                regular_links.append({'text': text, 'url': url})

    # Parse pagination links (li tags in ul tags)
    pagination_ul = soup.find('ul', {'class': 'pagination', 'id': 'pagelink'})
    if pagination_ul:
        for li in pagination_ul.find_all('li'):
            for a in li.find_all('a', href=True):
                text = a.text.strip()
                url = urljoin(base_url, a['href'])
                pagination_links.append({'text': text, 'url': url})

    return {'regular_links': regular_links, 'books': list(books.values()), 'pagination_links': pagination_links}


