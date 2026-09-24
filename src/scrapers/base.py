from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
import requests
from src.utils.logger import setup_logger

logger = setup_logger("base_scraper")

class BaseScraper(ABC):
    """Abstract base class for all source scrapers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.req_settings = config.get("request_settings", {})
        self.timeout = self.req_settings.get("timeout", 15)
        self.user_agent = self.req_settings.get(
            "user_agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        self.retry_count = self.req_settings.get("retry_count", 3)
        self.backoff_factor = self.req_settings.get("backoff_factor", 2.0)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def fetch_url(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        """Performs a polite GET request with configurable retries and exponential backoff."""
        req_headers = headers or {}
        attempt = 0
        while attempt < self.retry_count:
            attempt += 1
            try:
                logger.info(f"Fetching URL (Attempt {attempt}/{self.retry_count}): {url}")
                response = self.session.get(url, headers=req_headers, timeout=self.timeout)
                if response.status_code == 200:
                    return response
                elif response.status_code in [429, 503, 500, 502, 504]:
                    sleep_time = self.backoff_factor ** attempt
                    logger.warning(f"HTTP {response.status_code} received from {url}. Backing off {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"HTTP {response.status_code} received from {url}. No retry for client error.")
                    return response
            except requests.RequestException as e:
                sleep_time = self.backoff_factor ** attempt
                logger.warning(f"Request failed on attempt {attempt}: {str(e)}. Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)

        logger.error(f"Exceeded max retries ({self.retry_count}) for URL: {url}")
        return None

    @abstractmethod
    def collect(self) -> Dict[str, Any]:
        """Collects raw candidate records and raw content responses. Must return summary and records."""
        pass
