import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse

class PageParser:
    def __init__(self,html,base_url):
        self.base_url=base_url
        self.soup=BeautifulSoup(html,'lxml' if 'lxml' in globals() else 'html.parser')

    def parse_links(self):
        links=[urljoin(self.base_url,a['href']) for a in self.soup.findAll('a',href=True)]
        links=[link.split('#')[0] for link in links]
        return links

    def filter_links(self,links,allowed_domains=None,disallowed_extensions=None):
        filtered = []
        allowed_domains_set = set(allowed_domains or [])
        disallowed_extensions_tuple = tuple(disallowed_extensions or [])
        for link in links:
            if allowed_domains_set:
                try:
                    domain = urlparse(link).netloc
                    # Check if the domain is NOT in the allowed list
                    if domain and domain not in allowed_domains_set:
                        continue
                except ValueError:
                    continue  # Skip malformed URLs

                    # 2. Extension Check (e.g., .pdf, .jpg)
            if disallowed_extensions_tuple and link.lower().endswith(disallowed_extensions_tuple):
                    # We skip files ending with the disallowed extensions (e.g., PDFs, images)
                continue

            filtered.append(link)

        return filtered

    def get_title(self):
        title_tag=self.soup.find('title')
        return title_tag.text.strip() if title_tag else ''

