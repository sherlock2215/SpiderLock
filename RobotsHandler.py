from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin,urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class RobotsHandler:
    def __init__(self,base_url, user_agent="SimplePythonWebCrawler/1.0"):
        parsed_url = urlparse(base_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.user_agent = user_agent
        robots_url=urljoin(self.base_url,"/robots.txt")
        self.rp=RobotFileParser()
        self.rp.set_url(robots_url)
        logging.info(f"Attempting to read robots.txt from: {robots_url}")
        try:
            self.rp.read()
            logging.info(f"Successfully read robots.txt for {self.base_url}")
        except Exception as e:
            logging.error(f"Failed to read robots.txt from {robots_url}. Proceeding with default permissive rules. Error: {e}")

    def can_fetch(self,url):
        return self.rp.can_fetch(self.user_agent, url)