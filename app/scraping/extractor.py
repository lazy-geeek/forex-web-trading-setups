import yaml
import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def run_scraping():
    with open("app/scraping/site_config.yaml", "r") as f:
        config = yaml.safe_load(f)

    options = Options()
    options.headless = True
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")

    driver = webdriver.Chrome(options=options)
    all_data = []
    try:
        for site in config["sites"]:
            try:
                driver.get(site["url"])
                time.sleep(3)  # Wait for JavaScript to load
                html = driver.page_source
                print("Debug: HTML length for", site["name"], ":", len(html))
                soup = BeautifulSoup(html, "html.parser")
                articles = soup.select(site["selectors"]["article"])
                for article in articles:
                    try:
                        title = article.select_one(
                            site["selectors"]["title"]
                        ).text.strip()
                        content = article.select_one(
                            site["selectors"]["content"]
                        ).text.strip()
                        all_data.append(
                            {"site": site["name"], "title": title, "content": content}
                        )
                    except AttributeError:
                        continue
            except Exception as e:
                print(f"Error scraping {site['name']}: {e}")
                continue
    finally:
        driver.quit()
    return all_data
