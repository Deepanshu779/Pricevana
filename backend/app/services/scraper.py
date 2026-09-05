import re
import time
import requests
import hashlib
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import current_app

from ..config import logger


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def scrape_flipkart(driver):
    title = None
    price = None

    title_selectors = [
        "span.VU-ZEz",
        "span.B_NuCI"
    ]

    price_selectors = [
        "div.Nx9bqj",
        "div._30jeq3._16Jk6d"
    ]

    for selector in title_selectors:
        try:
            title = driver.find_element(By.CSS_SELECTOR, selector).text
            if title:
                break
        except Exception:
            pass

    for selector in price_selectors:
        try:
            price_text = driver.find_element(By.CSS_SELECTOR, selector).text
            price = float(re.sub(r"[^\d]", "", price_text))
            if price:
                break
        except Exception:
            pass

    return title, price


def scrape_amazon(driver):
    title = None
    price = None

    title_selectors = ["#productTitle"]
    price_selectors = [
        ".a-price-whole",
        "#priceblock_ourprice",
        "#priceblock_dealprice"
    ]

    for selector in title_selectors:
        try:
            title = driver.find_element(By.CSS_SELECTOR, selector).text.strip()
            if title:
                break
        except Exception:
            pass

    for selector in price_selectors:
        try:
            price_text = driver.find_element(By.CSS_SELECTOR, selector).text
            price = float(re.sub(r"[^\d]", "", price_text))
            if price:
                break
        except Exception:
            pass

    return title, price


def extract_meta_image(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        html = response.text

        match = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if match:
            return match.group(1)

        match = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']', html, re.IGNORECASE)
        if match:
            return match.group(1)

        match = re.search(r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if match:
            return match.group(1)
    except Exception as e:
        logger.warning(f"Meta image extraction failed: {e}")
    return None


def generate_mock_product(url):
    parsed = urlparse(url)
    path = parsed.path

    segments = [s for s in path.split('/') if s]
    slug = ""
    for s in reversed(segments):
        if s.lower() in {'p', 'dp', 'product', 'gp'}:
            continue
        if s.lower().startswith('itm') and len(s) >= 10:
            continue
        if re.match(r'^[A-Z0-9]{10}$', s, re.IGNORECASE):
            continue
        if s.isdigit():
            continue
        slug = s
        break

    if not slug and segments:
        slug = segments[0]

    slug = slug.split('.')[0]
    slug = re.sub(r'^[ip]d[m|t]', '', slug)

    words = re.split(r'[-_]', slug)
    cleaned_words = [w.capitalize() for w in words if w]
    title = " ".join(cleaned_words)

    if not title:
        title = "Generic Tracked Product"

    title = re.sub(r'\b[A-Z0-9]{10}\b', '', title).strip()

    url_hash = int(hashlib.md5(url.encode('utf-8')).hexdigest(), 16)
    title_lower = title.lower()
    if any(k in title_lower for k in ["airdope", "earbud", "headphone", "earphone", "duopod", "pod", "sound", "audio"]):
        price = 499 + (url_hash % 2500)
    elif any(k in title_lower for k in ["phone", "mobile", "galaxy", "iphone", "s24", "oneplus"]):
        price = 12999 + (url_hash % 67000)
    elif any(k in title_lower for k in ["laptop", "macbook", "notebook", "computer"]):
        price = 29999 + (url_hash % 70000)
    elif any(k in title_lower for k in ["shirt", "tshirt", "jeans", "jacket", "socks", "clothing"]):
        price = 399 + (url_hash % 2600)
    else:
        price = 499 + (url_hash % 14500)

    image_url = extract_meta_image(url)

    return {
        "title": title,
        "price": float(price),
        "currency": "INR",
        "price_source": "mock_generator",
        "image_url": image_url
    }


def scrape_product_info(url):
    try:
        if current_app and current_app.config.get("TESTING"):
            return generate_mock_product(url), None
    except Exception:
        pass

    driver = None
    try:
        driver = create_driver()
        driver.set_page_load_timeout(10)
        driver.get(url)
        time.sleep(2)
        domain = urlparse(url).netloc.lower()
        title = None
        price = None

        if "flipkart" in domain:
            title, price = scrape_flipkart(driver)
        elif "amazon" in domain:
            title, price = scrape_amazon(driver)
        else:
            return generate_mock_product(url), None

        if not title or not price:
            logger.warning("Scraper failed to extract title/price, falling back to mock generator")
            return generate_mock_product(url), None

        image_url = extract_meta_image(url)

        return {
            "title": title,
            "price": price,
            "currency": "INR",
            "price_source": "live_scraping",
            "image_url": image_url
        }, None

    except Exception as e:
        logger.warning(f"Scraper error: {e}. Falling back to mock generator.")
        return generate_mock_product(url), None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
