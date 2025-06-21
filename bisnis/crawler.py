import requests
from bs4 import BeautifulSoup
from datetime import datetime
from bisnis.utils import save_to_json, clean_text, parse_iso_date
import time
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://www.bisnis.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_total_pages(date):
    formatted_date = date.strftime("%Y-%m-%d")
    url = f"{BASE_URL}/index?categoryId=0&type=indeks&date={formatted_date}&page=1"
    
    logger.info(f"🌐 Fetching total pages from: {url}")
    
    try:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"❌ Failed to fetch page: {e}")
        return 1

    soup = BeautifulSoup(resp.text, "html.parser")
    total_page_input = soup.find("input", {"id": "total_page"})
    
    if total_page_input:
        try:
            total = int(total_page_input["value"])
            logger.info(f"📄 Total pages found: {total}")
            return total
        except (ValueError, KeyError) as e:
            logger.warning(f"⚠️ Could not parse total_page value: {e}")
            return 1
    else:
        logger.warning("⚠️ total_page input not found, defaulting to 1")
        return 1

def fetch_article_links(date: datetime):
    formatted_date = date.strftime("%Y-%m-%d")
    total_pages = get_total_pages(date)
    links = []

    logger.info(f"🔍 Fetching article links for date: {formatted_date} across {total_pages} pages")

    for page in range(1, total_pages + 1):
        url = f"{BASE_URL}/index?categoryId=0&type=indeks&date={formatted_date}&page={page}"
        logger.info(f"🌐 Scraping page {page}: {url}")

        try:
            resp = requests.get(url, headers=HEADERS)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"❌ Failed to fetch page {page}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("div.artItem div.artContent a.artLink")

        logger.info(f"📰 Found {len(articles)} articles on page {page}")

        for art in articles:
            href = art.get("href")
            if href and not href.startswith("https://premium.bisnis.com"):
                full_url = href if href.startswith("http") else BASE_URL + href
                links.append(full_url)

    logger.info(f"✅ Total collected article links: {len(links)} for date {formatted_date}")
    return links

def fetch_article_content(article_url):
    logger.info(f"📥 Fetching content from: {article_url}")
    
    try:
        resp = requests.get(article_url, headers=HEADERS)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"❌ Failed to fetch article {article_url}: {e}")
        raise

    soup = BeautifulSoup(resp.text, "html.parser")

    # --- Extract title ---
    title_tag = soup.find("h1", class_="detailsTitleCaption")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"
    
    # --- Extract content ---
    content_div = soup.find("article", class_="detailsContent")
    content = clean_text(content_div.get_text(" ", strip=True)) if content_div else ""

    # --- Extract publish date ---
    date_meta = soup.find("meta", {"name": "publishdate"})
    date_str = date_meta["content"] if date_meta else datetime.now().isoformat()

    logger.info(f"✅ Article fetched: {title[:60]}...")

    return {
        "link": article_url,
        "judul": title,
        "isi": content,
        "tanggal_terbit": parse_iso_date(date_str)
    }

def crawl_by_date(start_date, end_date):
    articles = []
    current = start_date

    logger.info(f"🗓️ Starting backtrack crawl from {start_date.date()} to {end_date.date()}")

    while current <= end_date:
        date_str = current.strftime('%Y-%m-%d')
        logger.info(f"📅 Scraping articles for {date_str}")

        try:
            links = fetch_article_links(current)
        except Exception as e:
            logger.error(f"❌ Failed to fetch links for {date_str}: {e}")
            current += timedelta(days=1)
            continue

        logger.info(f"🔗 Found {len(links)} links on {date_str}")

        for link in links:
            try:
                article = fetch_article_content(link)
                articles.append(article)
            except Exception as e:
                logger.error(f"⚠️ Error fetching article {link}: {e}")

        logger.info(f"✅ Completed date: {date_str} ({len(articles)} total articles so far)")
        current += timedelta(days=1)

    logger.info(f"🏁 Finished crawling. Total articles collected: {len(articles)}")
    return articles

def crawl_latest(interval_sec):
    seen_links = set()
    logger.info(f"🟢 Starting crawl_latest with interval: {interval_sec} seconds")

    while True:
        now = datetime.now()
        logger.info(f"🔎 Scraping latest articles at {now.strftime('%Y-%m-%d %H:%M:%S')}")

        links = fetch_article_links(datetime.now())
        new_articles = []
        
        for link in links:
          if link not in seen_links:
            try:
                article = fetch_article_content(link)

                new_articles.append(article)
                seen_links.add(link)
                
                logger.info(f"✅ Fetched article: {link}")
            except Exception as e:
                logger.error(f"Error fetching artcile {link}: {e}")

        if new_articles:
            logger.info(f"💾 Saving {len(new_articles)} new articles to output/hasil_standard.json")
            save_to_json(new_articles, "output/hasil_standard.json")
        else:
            logger.info("ℹ️ No new articles found in this interval.")

        logger.info(f"⏳ Sleeping for {interval_sec} seconds...\n")
        time.sleep(interval_sec)

