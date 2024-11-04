import requests
from bs4 import BeautifulSoup

class BaseScraper:
    def fetch_page(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse_html(self, html):
        return BeautifulSoup(html, "html.parser")
