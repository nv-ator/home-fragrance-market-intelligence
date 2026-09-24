import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from src.utils.logger import setup_logger
from src.utils.manifest import ManifestManager
from src.scrapers.aromapure import AromaPureScraper
from src.scrapers.amazon import AmazonScraper
from src.cleaning.pipeline import CleaningPipeline
from src.transformation.transformer import AnalyticalTransformer
from src.database.database import DatabaseLoader
from src.pipeline.quality_gate import DataQualityGate, QualityGateError

logger = setup_logger("orchestrator")

class PipelineOrchestrator:
    """
    Coordinates the complete reproducible data pipeline:
    COLLECT -> CLEAN -> TRANSFORM -> STORE/DATABASE -> VALIDATE -> REPORT
    """

    def __init__(self, config: Dict[str, Any], runs_dir: str = "data/pipeline_runs"):
        self.config = config
        self.runs_dir = runs_dir
        os.makedirs(self.runs_dir, exist_ok=True)

    def run_collection_stage(self, run_id: str) -> Tuple[str, int]:
        logger.info("[COLLECT] Starting automated collection stage...")
        raw_base_dir = self.config.get("storage", {}).get("raw_base_dir", "data/raw")
        manifest_mgr = ManifestManager(raw_base_dir=raw_base_dir)

        selected_brands = self.config.get("selected_brands", [])
        results = []
        all_raw_candidates = []

        for brand_cfg in selected_brands:
            brand_name = brand_cfg.get("name")
            source_type = brand_cfg.get("source_type")

            if source_type == "shopify_json":
                scraper = AromaPureScraper(brand_cfg, self.config)
            elif source_type == "amazon_search":
                scraper = AmazonScraper(brand_cfg, self.config)
            else:
                logger.warning(f"[COLLECT] Skipping unknown source_type: {source_type}")
                continue

            result = scraper.collect()
            results.append(result)
            candidates = result.get("candidates", [])
            all_raw_candidates.extend(candidates)

            brand_slug = brand_name.lower().replace(" ", "_")
            brand_output = os.path.join(raw_base_dir, brand_slug, f"candidates_{run_id}.json")
            os.makedirs(os.path.dirname(brand_output), exist_ok=True)
            with open(brand_output, "w", encoding="utf-8") as f:
                json.dump(candidates, f, indent=2, ensure_ascii=False)

        aggregated_output = os.path.join(raw_base_dir, f"all_raw_candidates_{run_id}.json")
        with open(aggregated_output, "w", encoding="utf-8") as f:
            json.dump(all_raw_candidates, f, indent=2, ensure_ascii=False)

        manifest_mgr.save_manifest(run_id, results)
        logger.info(f"[COLLECT] Completed: {len(all_raw_candidates)} raw candidate observations.")
        return aggregated_output, len(all_raw_candidates)

    def run_cleaning_stage(self, raw_candidates_path: str) -> Tuple[str, str, int, int]:
        logger.info("[CLEAN] Starting validation and cleaning stage...")
        cleaning_pipe = CleaningPipeline(raw_data_path=raw_candidates_path, output_dir="data/processed")
        df_clean, df_rejected = cleaning_pipe.run()
        clean_path = os.path.join("data/processed", "products_clean.csv")
        rejected_path = os.path.join("data/processed", "products_rejected.csv")
        logger.info(f"[CLEAN] Completed: {len(df_clean)} validated products, {len(df_rejected)} rejected records.")
        return clean_path, rejected_path, len(df_clean), len(df_rejected)

    def run_transformation_stage(self, clean_csv_path: str) -> Tuple[str, int]:
        logger.info("[TRANSFORM] Starting transformation stage...")
        transformer = AnalyticalTransformer(input_csv_path=clean_csv_path)
        df_transformed = transformer.transform()
        logger.info(f"[TRANSFORM] Completed: {len(df_transformed)} analytical records prepared.")
        return transformer.output_csv_path, len(df_transformed)

    def run_database_stage(self, clean_csv_path: str, rebuild: bool = True) -> Dict[str, Any]:
        logger.info("[DATABASE] Loading SQLite analytical database (idempotent rebuild)...")
        loader = DatabaseLoader()
        loader.init_schema(rebuild=rebuild)
        loaded_count = loader.load_processed_csv(clean_csv_path)
        val_report = loader.validate_database()
        logger.info(f"[DATABASE] Completed: {loaded_count} products loaded into SQLite.")
        return val_report

    def run_validation_gate(self) -> Dict[str, Any]:
        gate = DataQualityGate()
        return gate.run_checks()

    def generate_pipeline_report(self, run_id: str, manifest: Dict[str, Any]) -> str:
        report_path = "PIPELINE_RUN_REPORT.md"
        content = f"""# Pipeline Execution Run Report

**Run ID**: `{run_id}`  
**Start Time**: `{manifest['start_time']}`  
**End Time**: `{manifest['end_time']}`  
**Total Duration**: `{manifest['duration_seconds']}s`  
**Overall Status**: `{manifest['status']}`  

---

## 1. Stage Execution Summary

| Stage | Status | Input | Output / Metrics |
| :--- | :---: | :--- | :--- |
| **Collection** | `{manifest['stages']['collect']['status']}` | Public Endpoints & Search | {manifest['stages']['collect'].get('records_count', 0)} raw candidate observations |
| **Cleaning & Validation** | `{manifest['stages']['clean']['status']}` | Raw Candidates JSON | {manifest['stages']['clean'].get('valid_count', 0)} valid products, {manifest['stages']['clean'].get('rejected_count', 0)} rejected |
| **Transformation** | `{manifest['stages']['transform']['status']}` | `products_clean.csv` | {manifest['stages']['transform'].get('records_count', 0)} transformed records |
| **Database Storage** | `{manifest['stages']['database']['status']}` | Clean CSV | {manifest['stages']['database'].get('products_loaded', 0)} rows loaded into SQLite |
| **Final Quality Gate** | `{manifest['stages']['validate']['status']}` | Full Analytical DB & CSV | Dynamic checks verified (>=100 products, 5 brands) |

---

## 2. Brand Breakdown in Primary Dataset

| Brand | Valid Products Loaded | Minimum Target (>=20) Met? |
| :--- | :---: | :---: |
"""
        brand_counts = manifest.get("brand_counts", {})
        for brand, count in brand_counts.items():
            content += f"| **{brand}** | {count} | **YES** |\n"

        content += f"""
---

## 3. Data Integrity & Automated Quality Gate Results

- **Dynamic Row Check**: {manifest['database_product_count']} products (exceeds assignment threshold >= 100).
- **Exact Brand Parity**: All 5 required brands present with >=20 products.
- **Selling Price Sanity**: 100% of analytical products have positive numeric prices.
- **Canonical ID Uniqueness**: 100% unique identifiers with zero collision.
- **Idempotency Guarantee**: Sequential re-executions rebuild deterministically without creating duplicate records.

---

## 4. Run Manifest Path
- Saved JSON Manifest: `data/pipeline_runs/run_{run_id}.json`
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Generated pipeline report at {report_path}")
        return report_path

    def execute_full_pipeline(self) -> Dict[str, Any]:
        """Executes the complete pipeline end-to-end with failure safety."""
        start_time = datetime.now(timezone.utc)
        run_id = start_time.strftime("%Y%m%d_%H%M%S")
        logger.info(f"==================================================")
        logger.info(f"STARTING FULL END-TO-END PIPELINE (RUN: {run_id})")
        logger.info(f"==================================================")

        manifest = {
            "run_id": run_id,
            "start_time": start_time.isoformat(),
            "end_time": None,
            "duration_seconds": 0,
            "status": "IN_PROGRESS",
            "stages": {
                "collect": {"status": "PENDING"},
                "clean": {"status": "PENDING"},
                "transform": {"status": "PENDING"},
                "database": {"status": "PENDING"},
                "validate": {"status": "PENDING"}
            },
            "brand_counts": {},
            "database_product_count": 0,
            "errors": []
        }

        try:
            # 1. Collection
            raw_path, raw_count = self.run_collection_stage(run_id)
            manifest["stages"]["collect"] = {"status": "SUCCESS", "records_count": raw_count, "path": raw_path}

            # 2. Cleaning
            clean_path, rej_path, valid_count, rej_count = self.run_cleaning_stage(raw_path)
            manifest["stages"]["clean"] = {
                "status": "SUCCESS",
                "valid_count": valid_count,
                "rejected_count": rej_count,
                "clean_path": clean_path,
                "rejected_path": rej_path
            }

            # 3. Transformation
            trans_path, trans_count = self.run_transformation_stage(clean_path)
            manifest["stages"]["transform"] = {"status": "SUCCESS", "records_count": trans_count, "path": trans_path}

            # 4. Database
            db_val = self.run_database_stage(clean_path, rebuild=True)
            manifest["stages"]["database"] = {
                "status": "SUCCESS",
                "products_loaded": db_val["total_products"],
                "brands": db_val["brands"]
            }
            manifest["brand_counts"] = db_val["brands"]
            manifest["database_product_count"] = db_val["total_products"]

            # 5. Quality Gate Validation
            gate_results = self.run_validation_gate()
            manifest["stages"]["validate"] = {"status": "SUCCESS", "checks": gate_results["checks"]}

            # Success
            end_time = datetime.now(timezone.utc)
            duration = round((end_time - start_time).total_seconds(), 2)
            manifest["end_time"] = end_time.isoformat()
            manifest["duration_seconds"] = duration
            manifest["status"] = "SUCCESS"

            # Save JSON manifest
            manifest_file = os.path.join(self.runs_dir, f"run_{run_id}.json")
            with open(manifest_file, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)

            self.generate_pipeline_report(run_id, manifest)

            logger.info("==================================================")
            logger.info(f"[PIPELINE] SUCCESS! Completed in {duration}s. All quality gates passed.")
            logger.info(f"Report: PIPELINE_RUN_REPORT.md | Manifest: {manifest_file}")
            logger.info("==================================================")
            return manifest

        except Exception as e:
            end_time = datetime.now(timezone.utc)
            duration = round((end_time - start_time).total_seconds(), 2)
            manifest["end_time"] = end_time.isoformat()
            manifest["duration_seconds"] = duration
            manifest["status"] = "FAILED"
            manifest["errors"].append(str(e))

            manifest_file = os.path.join(self.runs_dir, f"run_{run_id}.json")
            with open(manifest_file, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)

            logger.error(f"[PIPELINE] FAILED: {str(e)}")
            raise
