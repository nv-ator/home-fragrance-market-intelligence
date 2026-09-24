# Home Fragrance Market Intelligence — Executive Demo Talking Points

This document provides concise, natural talking points for demonstrating the Home Fragrance Market Intelligence platform. The language is conversational yet analytically rigorous, designed for a screen recording or live stakeholder presentation (Target: 8–9 minutes).

---

## A. Opening (30 seconds)

> "Hello everyone. Today I'm presenting an end-to-end Market Intelligence and Brand Positioning platform for the Indian Home Fragrance and Air Care market.
> 
> We benchmark five major brands across the competitive landscape: AromaPure, Odonil, Godrej aer, Air Wick, and Ambi Pur.
> 
> Everything you will see today is driven by an automated data pipeline running from raw public listing collection all the way to a modern FastAPI backend and React analytics dashboard."

---

## B. Data Pipeline & Architecture (1 minute 30 seconds)

> "Before diving into the numbers, let's look at the engineering foundation.
> 
> Category managers often struggle with fragmented marketplace data, inconsistent pack sizes, and manual spreadsheets. To solve this, we built a fully automated, reproducible pipeline executable with a single command: `python main.py`.
> 
> Here's how it works:
> 1. **Collection**: We extracted 1,436 raw observations from public catalogue endpoints and marketplace listings with zero authentication bypass, preserving raw snapshots immutably with cryptographic SHA-256 manifests.
> 2. **Cleaning & Validation**: We applied strict scope filtering—removing car-only SKUs and non-ambient items—and deduplicated repeated search listings by ASIN and product variant keys. This yielded exactly 767 unique, validated home fragrance products.
> 3. **Transformation**: We standardized physical units into separate metrics—rupees per 100 grams for solids and rupees per 100 milliliters for liquids—without conflating mass and volume. Crucially, missing values are preserved as NULL rather than zero to prevent analytical distortion.
> 4. **Storage & Verification**: Data is loaded into an indexed SQLite database and served via FastAPI. Our automated quality gate validates 8 data health checks, backed by 44 automated unit and integration tests."

---

## C. Market Overview (1 minute)

*(Navigate to `/` — Market Overview)*

> "Let's turn to the dashboard. The Market Overview provides a top-level snapshot of the collected 767-product catalogue.
> 
> Across all five brands, we observe a mean price of ₹667.81 and a median price of ₹448.00. That noticeable gap tells us immediately that the distribution is positively skewed by higher-priced multi-packs and electric diffuser hardware.
> 
> Looking at the charts:
> - **Category Distribution**: Ambient Fragrance is the largest category with 430 products, followed by Scented Candle & Wax with 153 products and Reed Diffuser & Fragrance Oil with 81 products.
> - **Price Distribution**: Over 61% of all collected products list below ₹500 (181 under ₹250 and 288 between ₹250–₹499), with another 26% in the ₹500 to ₹1,000 range.
> - **Discount Depth**: Among the 545 products displaying promotional discounts, the average markdown is 39.5%.
> - **Review Volume**: We track 1,387 marketplace reviews across rated listings.
> 
> Importantly, our KPI cards explicitly state these figures represent observed public listings, not total consumer sales."

---

## D. Brand Comparison (1 minute)

*(Navigate to `/brands` — Brand Comparison)*

> "Moving to the Brand Comparison page, our objective here is symmetrical, neutral benchmarking. No brand is given preferential placement.
> 
> Looking at observed catalogue size:
> - AromaPure leads in collected catalogue depth with 360 unique SKUs, followed by Odonil with 145, Godrej aer with 129, Air Wick with 91, and Ambi Pur with 42.
> 
> In terms of pricing breadth:
> - Godrej aer exhibits an observed median price of ₹299.00, concentrating heavily in aerosol sprays and pocket blocks.
> - Air Wick shows a higher median price of ₹905.00, reflecting its focus on automated gadget starter kits and refill systems.
> - AromaPure spans an observed price range from ₹99.00 for single sachets to ₹4,899.00 for ultrasonic aroma diffuser machines.
> 
> We also observe varying category footprints: AromaPure spans 7 categories, Odonil and Ambi Pur span 5, Godrej aer spans 3, and Air Wick spans 2. We treat unobserved categories as catalogue gaps, not proof of total market absence."

---

## E. Price Positioning & Unit Economics (1 minute)

*(Navigate to `/pricing` — Price Positioning)*

> "On the Price Positioning page, we explore price distribution and unit economics without relying on arbitrary labels like 'Premium' or 'Budget'.
> 
> First, looking at the Price vs. Rating scatter plot:
> - Across the 364 products with public ratings, the Pearson correlation with price is a weak positive +0.24. Visually, products are widely dispersed between 1.0 and 5.0 stars across every price level from ₹50 to over ₹6,000. Customer satisfaction is not determined simply by price point.
> 
> Next, examining Unit Economics:
> - We strictly separate liquid and solid formats.
> - For liquid formulations like diffuser oils and spray refills, the average rate is ₹1,575.96 per 100ml across 271 products, ranging from ₹34.04 to ₹8,090.00.
> - For solid blocks and candles, the average rate is ₹411.30 per 100g across 30 products, ranging from ₹78.67 to ₹1,133.33.
> 
> Comparing unit rates rather than pack prices allows category managers to evaluate true consumer value independent of multi-pack sizing."

---

## F. Product Analysis (45 seconds)

*(Navigate to `/products` — Product Analysis)*

> "The Product Analysis tab provides granular, row-level transparency across all 767 products in the dataset.
> 
> Category managers can filter simultaneously across brand, category, format, platform, price ranges, and minimum rating thresholds.
> 
> For example, filtering by 'Scented Candle & Wax' instantly isolates all 153 relevant SKUs, showing their selling price, discount percentage, physical volume, calculated unit price, and review counts.
> 
> Every column includes sorting, pagination, and direct provenance attribution, ensuring stakeholders can trace any analytical observation back to its source record."

---

## G. Business Insights (1 minute 30 seconds)

*(Navigate to `/insights` — Business Insights)*

> "Now to the core strategic layer: Business Insights.
> 
> Rather than making speculative assertions, every card follows a strict four-part analytical framework:
> 1. **Factual Observation**: What does the data explicitly measure?
> 2. **Analytical Interpretation**: What might this pattern imply?
> 3. **Commercial Business Question**: What commercial question should management ask?
> 4. **Internal Validation Required**: What internal enterprise data is needed before taking action?
> 
> Let's review two key examples:
> 
> First, **Sub-₹500 Price Concentration**:
> - The data shows that 61.1% of all products list below ₹500 (469 of 767), with Odonil at 92.4% (134 of 145) and Godrej aer at 79.1% (102 of 129).
> - This reflects an intense battleground for impulse and everyday household replenishment.
> - The business question is: Can a brand achieve acceptable gross margins at sub-₹300 price points without compromising fragrance longevity?
> - Validation required: Internal unit BOM cost, freight expense, and trade margins.
> 
> Second, **Portfolio Footprint & Opportunity Gaps**:
> - If we select Godrej aer using the interactive brand selector, the dashboard highlights that Godrej aer is observed in 3 categories with zero presence in Candles, Reed Diffusers, or Essential Oils in this dataset.
> - We do not say 'Godrej aer should launch reed diffusers.'
> - Instead, we ask: Does Godrej aer have a commercially viable opportunity to enter decorative ambient fragrance, or does remaining focused on automated sprays yield superior operational efficiency?
> - Validation required: Manufacturing Capex, channel willingness, and gross margin hurdle rates."

---

## H. Limitations & Data Governance (40 seconds)

> "A core strength of this project is intellectual honesty regarding data boundaries:
> 1. **Catalogue Data vs. Total Market**: This dataset captures observed public listings on major e-commerce platforms. It does not measure physical retail off-take, kirana store distribution, or actual unit sales volume.
> 2. **Review Metrics**: Review counts reflect marketplace engagement on Amazon listings; they are not market share. AromaPure's official direct catalogue does not publish public review tallies, so those fields are preserved as 'Not available'.
> 3. **Promotions**: Discounts reflect instant promotional listings at snapshot time, not longitudinal net realized price."

---

## I. Closing & Strategic Summary (20 seconds)

> "In summary, this platform delivers an end-to-end, reproducible market intelligence solution.
> 
> By uniting automated Python data engineering, strict quality gates, a high-performance FastAPI backend, and an objective React analytics dashboard, we provide commercial leadership with clear, verifiable evidence to inform catalogue, pricing, and packaging decisions.
> 
> Thank you, and I look forward to your questions."
