from urllib.parse import urlparse
import requests
import time
from PageParser import PageParser
from CrawlQueue import CrawlQueue
from RobotsHandler import RobotsHandler


class WebCrawler:
    def __init__(self, start_url, strategy="bfs", max_depth=2, allowed_domains=None, disallowed_extensions=None):
        parsed_url = urlparse(start_url)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        self.user_agent = 'SimplePythonWebCrawler/1.0'
        self.robots_handler = RobotsHandler(base_domain, user_agent=self.user_agent)
        self.queue = CrawlQueue(strategy)
        self.graph = {}

        self.max_depth = max_depth
        self.allowed_domains = allowed_domains or []
        self.disallowed_extensions = disallowed_extensions or []

    def fetch_page(self, url):
        if not self.robots_handler.can_fetch(url):
            print(f"Blocked by robots.txt: {url}")
            return None, {}

        time.sleep(1)

        headers = {'User-Agent': self.user_agent}
        metrics = {"status_code": None, "load_time": None, "page_size_kb": None, "error": None}

        try:
            start_time = time.time()
            response = requests.get(url, timeout=30, headers=headers)
            duration = time.time() - start_time

            metrics["status_code"] = response.status_code
            metrics["load_time"] = round(duration, 2)
            metrics["page_size_kb"] = round(len(response.content) / 1024, 2)
            response.raise_for_status()
            return response.text, metrics

        except requests.exceptions.Timeout:
            metrics["error"] = "Timeout"
        except requests.exceptions.ConnectionError:
            metrics["error"] = "Connection Error"
        except requests.exceptions.SSLError:
            metrics["error"] = "SSL Error"
        except requests.RequestException as e:
            metrics["error"] = str(e)
            metrics["status_code"] = getattr(e.response, 'status_code', 'N/A')
        except Exception as e:
            metrics["error"] = f"Unexpected: {e}"

        return None, metrics

    def _is_web_scheme(self, url):
        return urlparse(url).scheme in ("http", "https")

    def crawl(self, start_url):
        # Start with depth 0
        self.queue.push((start_url, 0))

        while not self.queue.is_empty():
            url, depth = self.queue.pop()
            if not self._is_web_scheme(url):
                print(f"Skipping non-web scheme: {url}")
                continue

            print(f"[{depth}] Visiting: {url}")
            html, metrics = self.fetch_page(url)
            if html is None:
                self.graph[url] = {"metrics": metrics, "links": [], "title": "", "h1": ""}
                continue

            # Parse page for links, title, h1
            parser = PageParser(html, url)
            links = parser.parse_links()
            filtered_links = parser.filter_links(
                links,
                allowed_domains=self.allowed_domains,
                disallowed_extensions=self.disallowed_extensions
            )

            page_title = parser.get_title() if hasattr(parser, "get_title") else ""
            page_h1 = parser.get_h1() if hasattr(parser, "get_h1") else ""

            self.graph[url] = {
                "metrics": metrics,
                "links": filtered_links,
                "title": page_title,
                "h1": page_h1
            }

            if self.max_depth is None or depth < self.max_depth:
                for link in filtered_links:
                    self.queue.push((link, depth + 1))

        # Categorize links after crawl
        self.graph = self.categorize_links(self.graph)
        print(f"\nCrawl complete. Visited {len(self.queue.seen_urls)} unique pages.")

    def categorize_links(self, crawl_graph):
        categorized_graph = {}

        for page, data in crawl_graph.items():
            categorized = {
                "http(s)_links": [],
                "mail_links": [],
                "video_links": [],
                "image_links": [],
                "other_links": []
            }

            for link in data.get("links", []):
                if link.startswith("mailto:"):
                    categorized["mail_links"].append(link)
                elif link.lower().endswith((".mp4", ".webm", ".avi")):
                    categorized["video_links"].append(link)
                elif link.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    categorized["image_links"].append(link)
                elif link.startswith("http://") or link.startswith("https://"):
                    categorized["http(s)_links"].append(link)
                else:
                    categorized["other_links"].append(link)

            categorized_graph[page] = {
                "metrics": data["metrics"],
                "title": data.get("title", ""),
                "h1": data.get("h1", ""),
                "categorized_links": categorized
            }

        return categorized_graph



