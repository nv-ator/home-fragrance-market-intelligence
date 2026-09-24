from typing import Dict, Any, List, Optional
import os
import json
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.scrapers.base import BaseScraper
from src.utils.logger import setup_logger

logger = setup_logger("aromapure_scraper")

class AromaPureScraper(BaseScraper):
    """Scraper for AromaPure public catalogue endpoint (Shopify JSON API)."""

    def __init__(self, brand_config: Dict[str, Any], global_config: Dict[str, Any]):
        super().__init__(global_config)
        self.brand_config = brand_config
        self.catalogue_url = brand_config.get("catalogue_url", "https://aromahpure.com/products.json")
        self.page_limit = brand_config.get("page_limit", 250)
        self.raw_dir = os.path.join(global_config.get("storage", {}).get("raw_base_dir", "data/raw"), "aromapure")
        self.page_raw_dir = os.path.join(self.raw_dir, "product_pages")
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.page_raw_dir, exist_ok=True)

    @staticmethod
    def _review_fields_from_html(html_content: str) -> Dict[str, Optional[str]]:
        """Extract only explicitly published aggregate review fields from a public PDP."""
        soup = BeautifulSoup(html_content, "html.parser")
        rating_raw = None
        review_count_raw = None
        seller_raw = None

        for script in soup.select('script[type="application/ld+json"]'):
            try:
                payload = json.loads(script.string or script.get_text())
            except (TypeError, json.JSONDecodeError):
                continue
            records = payload if isinstance(payload, list) else [payload]
            for record in records:
                if not isinstance(record, dict):
                    continue
                aggregate = record.get("aggregateRating")
                if isinstance(aggregate, dict):
                    rating_value = aggregate.get("ratingValue")
                    review_value = aggregate.get("reviewCount", aggregate.get("ratingCount"))
                    if rating_value is not None:
                        rating_raw = str(rating_value)
                    if review_value is not None:
                        review_count_raw = str(review_value)
        visible_text = soup.get_text(" ", strip=True)
        if review_count_raw is None:
            if re.search(r"\bno\s+reviews?\b", visible_text, re.IGNORECASE):
                review_count_raw = "0"
            else:
                review_match = re.search(
                    r"(?:based on|from|of|reviews?\s*[:\-]?)\s*([\d,]+(?:\.\d+)?\s*[kK]?)\s+reviews?",
                    visible_text,
                    re.IGNORECASE,
                )
                if review_match:
                    review_count_raw = review_match.group(1)

        return {
            "rating_raw": rating_raw,
            "review_count_raw": review_count_raw,
            "seller_raw": seller_raw,
        }

    def enrich_product_pages(self, candidates: List[Dict[str, Any]]) -> Dict[str, int]:
        """Fetch public official PDPs and enrich candidates without changing product identity."""
        stats = {"attempted": 0, "with_rating": 0, "with_review_count": 0, "with_seller": 0, "failed": 0}
        candidates_by_url: Dict[str, List[Dict[str, Any]]] = {}
        for candidate in candidates:
            product_url = candidate.get("product_url")
            if product_url:
                candidates_by_url.setdefault(product_url, []).append(candidate)

        for product_url, url_candidates in candidates_by_url.items():
            stats["attempted"] += 1
            try:
                response = self.fetch_url(product_url)
            except Exception as exc:
                logger.warning(f"Could not fetch public AromaPure PDP {product_url}: {exc}")
                stats["failed"] += 1
                continue
            if not response or response.status_code != 200:
                stats["failed"] += 1
                continue
            page_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(url_candidates[0].get("product_id", "unknown"))) + ".html"
            page_path = os.path.join(self.page_raw_dir, page_name)
            with open(page_path, "w", encoding="utf-8") as page_file:
                page_file.write(response.text)
            fields = self._review_fields_from_html(response.text)
            for candidate in url_candidates:
                candidate["raw_page_reference"] = page_path
                if fields["rating_raw"] is not None:
                    candidate["rating_raw"] = fields["rating_raw"]
                    candidate["rating_source"] = "AromaPure Official"
                if fields["review_count_raw"] is not None:
                    candidate["review_count_raw"] = fields["review_count_raw"]
                    candidate["review_source"] = "AromaPure Official"
                if fields["seller_raw"] is not None:
                    candidate["seller_raw"] = fields["seller_raw"]
            if fields["rating_raw"] is not None:
                stats["with_rating"] += 1
            if fields["review_count_raw"] is not None:
                stats["with_review_count"] += 1
            if fields["seller_raw"] is not None:
                stats["with_seller"] += 1
        return stats

    def parse_raw_products(self, data: Dict[str, Any], raw_filename: str) -> List[Dict[str, Any]]:
        """Parses raw JSON products into standardized raw record candidates without dropping data."""
        raw_candidates = []
        products = data.get("products", [])
        scraped_at = datetime.now(timezone.utc).isoformat()

        for prod in products:
            prod_id = str(prod.get("id", ""))
            title = prod.get("title", "")
            handle = prod.get("handle", "")
            vendor = prod.get("vendor", "")
            product_type = prod.get("product_type", "")
            tags = prod.get("tags", [])
            body_html = prod.get("body_html", "")
            product_url = f"https://aromahpure.com/products/{handle}" if handle else ""

            variants = prod.get("variants", [])
            if not variants:
                # Handle single entry without variant
                candidate = {
                    "source": "AromaPure Official",
                    "brand_query": "AromaPure",
                    "source_url": self.catalogue_url,
                    "product_url": product_url,
                    "product_id": prod_id,
                    "asin": None,
                    "sku": None,
                    "product_name": title,
                    "brand": vendor or "AromaPure",
                    "category_raw": product_type,
                    "subcategory_raw": None,
                    "product_type_raw": product_type,
                    "tags_raw": tags,
                    "price_raw": None,
                    "mrp_raw": None,
                    "discount_raw": None,
                    "pack_size_raw": None,
                    "rating_raw": None,
                    "review_count_raw": None,
                    "availability_raw": None,
                    "seller_raw": None,
                    "description_raw": body_html,
                    "scraped_at": scraped_at,
                    "raw_source_reference": raw_filename
                }
                raw_candidates.append(candidate)
            else:
                for variant in variants:
                    v_id = str(variant.get("id", ""))
                    sku = variant.get("sku", "")
                    price = variant.get("price")
                    compare_at_price = variant.get("compare_at_price")
                    available = variant.get("available")
                    grams = variant.get("grams")
                    variant_title = variant.get("title", "")

                    full_name = f"{title} - {variant_title}" if variant_title and variant_title != "Default Title" else title

                    candidate = {
                        "source": "AromaPure Official",
                        "brand_query": "AromaPure",
                        "source_url": self.catalogue_url,
                        "product_url": product_url,
                        "product_id": f"{prod_id}_{v_id}",
                        "asin": None,
                        "sku": sku,
                        "product_name": full_name,
                        "brand": vendor or "AromaPure",
                        "category_raw": product_type,
                        "subcategory_raw": None,
                        "product_type_raw": product_type,
                        "tags_raw": tags,
                        "price_raw": str(price) if price is not None else None,
                        "mrp_raw": str(compare_at_price) if compare_at_price is not None else None,
                        "discount_raw": None,
                        "pack_size_raw": f"{grams}g" if grams and grams > 0 else variant_title,
                        "rating_raw": None,
                        "review_count_raw": None,
                        "availability_raw": "In Stock" if available is True else ("Out of Stock" if available is False else None),
                        "seller_raw": None,
                        "description_raw": body_html,
                        "scraped_at": scraped_at,
                        "raw_source_reference": raw_filename
                    }
                    raw_candidates.append(candidate)

        return raw_candidates

    def collect(self) -> Dict[str, Any]:
        """Collects the full public catalogue JSON and saves the raw response immutably."""
        start_time = time.time()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        raw_filename = f"products_{timestamp}.json"
        raw_filepath = os.path.join(self.raw_dir, raw_filename)

        url = f"{self.catalogue_url}?limit={self.page_limit}"
        response = self.fetch_url(url)

        elapsed = time.time() - start_time
        if not response or response.status_code != 200:
            logger.error(f"Failed to fetch AromaPure catalogue from {url}")
            return {
                "brand": "AromaPure",
                "source": "AromaPure Official",
                "source_url": url,
                "http_status": response.status_code if response else None,
                "response_size": len(response.content) if response else 0,
                "candidates_count": 0,
                "candidates": [],
                "errors": [f"HTTP request failed with status {response.status_code if response else 'None'}"],
                "elapsed_time_sec": elapsed,
                "raw_file": None
            }

        # Save raw JSON content immutably
        with open(raw_filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        logger.info(f"Saved raw AromaPure catalogue response to {raw_filepath} ({len(response.text)} bytes)")

        try:
            data = response.json()
            candidates = self.parse_raw_products(data, raw_filepath)
            enrichment = self.enrich_product_pages(candidates)
            logger.info(f"Extracted {len(candidates)} raw candidate records for AromaPure")
            return {
                "brand": "AromaPure",
                "source": "AromaPure Official",
                "source_url": url,
                "http_status": response.status_code,
                "response_size": len(response.content),
                "candidates_count": len(candidates),
                "candidates": candidates,
                "enrichment": enrichment,
                "errors": [],
                "elapsed_time_sec": elapsed,
                "raw_file": raw_filepath
            }
        except Exception as e:
            logger.exception(f"Error parsing AromaPure JSON: {e}")
            return {
                "brand": "AromaPure",
                "source": "AromaPure Official",
                "source_url": url,
                "http_status": response.status_code,
                "response_size": len(response.content),
                "candidates_count": 0,
                "candidates": [],
                "errors": [str(e)],
                "elapsed_time_sec": elapsed,
                "raw_file": raw_filepath
            }
