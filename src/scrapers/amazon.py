from typing import Dict, Any, List, Optional
import os
import re
import time
import random
from urllib.parse import quote_plus
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from src.scrapers.base import BaseScraper
from src.utils.logger import setup_logger

logger = setup_logger("amazon_scraper")

class AmazonScraper(BaseScraper):
    """Scraper for public Amazon India product search listings."""

    def __init__(self, brand_config: Dict[str, Any], global_config: Dict[str, Any]):
        super().__init__(global_config)
        self.brand_name = brand_config.get("name", "Unknown")
        self.search_queries = brand_config.get("search_queries", [f"{self.brand_name} air freshener"])
        self.max_pages = self.req_settings.get("max_pages_per_query", 2)
        self.delay_range = self.req_settings.get("delay_range", [1.5, 3.0])

        brand_slug = self.brand_name.lower().replace(" ", "_")
        self.raw_dir = os.path.join(
            global_config.get("storage", {}).get("raw_base_dir", "data/raw"),
            "amazon",
            brand_slug
        )
        os.makedirs(self.raw_dir, exist_ok=True)

    def _brand_matches_plausibly(self, title: str) -> bool:
        """Basic source-level brand validation check to avoid completely unrelated results."""
        t_lower = title.lower()
        b_lower = self.brand_name.lower()
        if b_lower in t_lower:
            return True
        # Specific brand aliases
        if b_lower == "godrej aer" and ("aer" in t_lower or "godrej" in t_lower):
            return True
        if b_lower == "air wick" and ("airwick" in t_lower or "air wick" in t_lower):
            return True
        if b_lower == "ambi pur" and ("ambipur" in t_lower or "ambi pur" in t_lower):
            return True
        if b_lower == "odonil" and "odonil" in t_lower:
            return True
        if b_lower == "aromapure" and ("aromahpure" in t_lower or "aromapure" in t_lower):
            return True
        return False

    def parse_search_html(self, html_content: str, raw_filepath: str, source_url: str) -> List[Dict[str, Any]]:
        """Parses product cards from Amazon search results HTML without dropping candidate info."""
        soup = BeautifulSoup(html_content, "html.parser")
        product_cards = soup.select('div[data-component-type="s-search-result"]')
        candidates = []
        scraped_at = datetime.now(timezone.utc).isoformat()

        for card in product_cards:
            asin = card.get("data-asin", "").strip()
            if not asin:
                continue

            # Product Title
            title_elem = card.select_one("h2 span") or card.select_one("h2 a")
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Check plausible brand match
            if not self._brand_matches_plausibly(title):
                # We skip obviously unrelated sponsored items that bleed into search results
                continue

            # Product URL
            link_elem = card.select_one("h2 a")
            href = link_elem.get("href", "") if link_elem else ""
            if href.startswith("/"):
                product_url = f"https://www.amazon.in{href}"
            else:
                product_url = href or f"https://www.amazon.in/dp/{asin}"

            # Pricing
            price_whole = card.select_one(".a-price-whole")
            price_raw = price_whole.get_text(strip=True).replace(",", "").replace(".", "") if price_whole else None

            mrp_elem = card.select_one(".a-price.a-text-price span.a-offscreen")
            mrp_raw = mrp_elem.get_text(strip=True).replace("₹", "").replace(",", "").strip() if mrp_elem else None

            # Ratings & Reviews
            rating_raw = None
            rating_elem = (
                card.find(attrs={"aria-label": lambda x: x and "out of 5 stars" in x.lower()}) or
                card.select_one("i.a-icon-star-small span.a-icon-alt") or 
                card.select_one("i.a-icon-star span.a-icon-alt") or
                card.find("i", class_=lambda cl: cl and "star" in cl)
            )
            if rating_elem:
                rating_text = rating_elem.get("aria-label") or rating_elem.get_text(strip=True) or ""
                m = re.search(r"(\d+(\.\d+)?)", rating_text)
                if m:
                    rating_raw = m.group(1)

            review_count_raw = None
            review_elem = (
                card.find("a", attrs={"aria-label": lambda x: x and "rating" in x.lower()}) or
                card.select_one('span[aria-label*="ratings"]') or 
                card.select_one('a[href*="#customerReviews"] span')
            )
            if review_elem:
                rev_text = (review_elem.get("aria-label") or review_elem.get_text(strip=True) or "").replace(",", "")
                m = re.search(r"\d+", rev_text)
                if m:
                    review_count_raw = m.group(0)

            # Availability / Badges
            badge_elem = card.select_one(".a-badge-text")
            badge_raw = badge_elem.get_text(strip=True) if badge_elem else None

            candidate = {
                "source": "Amazon India",
                "brand_query": self.brand_name,
                "source_url": source_url,
                "product_url": product_url,
                "product_id": asin,
                "asin": asin,
                "sku": None,
                "product_name": title,
                "brand": self.brand_name,
                "category_raw": None,
                "subcategory_raw": None,
                "product_type_raw": None,
                "tags_raw": [badge_raw] if badge_raw else [],
                "price_raw": price_raw,
                "mrp_raw": mrp_raw,
                "discount_raw": None,
                "pack_size_raw": None,
                "rating_raw": rating_raw,
                "review_count_raw": review_count_raw,
                "rating_source": "Amazon India" if rating_raw is not None else None,
                "review_source": "Amazon India" if review_count_raw is not None else None,
                "availability_raw": "In Stock",
                "seller_raw": None,
                "description_raw": None,
                "scraped_at": scraped_at,
                "raw_source_reference": raw_filepath
            }
            candidates.append(candidate)

        return candidates

    def collect(self) -> Dict[str, Any]:
        """Iterates over configured search queries and pages, archiving raw HTML responses."""
        all_candidates = []
        errors = []
        total_size = 0
        start_time = time.time()
        successful_requests = 0

        for query_idx, query in enumerate(self.search_queries, 1):
            for page in range(1, self.max_pages + 1):
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                raw_filename = f"search_q{query_idx}_p{page}_{timestamp}.html"
                raw_filepath = os.path.join(self.raw_dir, raw_filename)

                encoded_query = quote_plus(query)
                page_param = f"&page={page}" if page > 1 else ""
                url = f"https://www.amazon.in/s?k={encoded_query}{page_param}"

                headers = {
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                }

                # Polite initial delay before marketplace request
                time.sleep(random.uniform(self.delay_range[0], self.delay_range[1]))
                response = self.fetch_url(url, headers=headers)
                
                # Check for interstitial challenge HTML and retry once if triggered
                if response and "triggerInterstitialChallenge" in response.text:
                    logger.warning(f"Interstitial challenge encountered for {self.brand_name} (Query: {query}, Page: {page}). Waiting 5s and retrying...")
                    time.sleep(5.0)
                    response = self.fetch_url(url, headers=headers)

                if not response or response.status_code != 200 or "triggerInterstitialChallenge" in response.text:
                    status = response.status_code if response else 'None'
                    err_msg = f"Failed query '{query}' page {page} with status {status}"
                    logger.error(err_msg)
                    errors.append(err_msg)
                else:
                    successful_requests += 1
                    total_size += len(response.content)
                    with open(raw_filepath, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    logger.info(f"Saved raw HTML search for {self.brand_name} page {page} to {raw_filepath}")

                    page_candidates = self.parse_search_html(response.text, raw_filepath, url)
                    logger.info(f"Query '{query}' p.{page}: Found {len(page_candidates)} brand-matching candidates")
                    all_candidates.extend(page_candidates)

        elapsed = time.time() - start_time
        return {
            "brand": self.brand_name,
            "source": "Amazon India",
            "source_url": f"Amazon search queries ({len(self.search_queries)})",
            "http_status": 200 if successful_requests > 0 else 500,
            "response_size": total_size,
            "candidates_count": len(all_candidates),
            "candidates": all_candidates,
            "errors": errors,
            "elapsed_time_sec": elapsed,
            "raw_dir": self.raw_dir
        }
