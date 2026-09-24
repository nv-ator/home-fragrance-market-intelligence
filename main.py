import os
import sys
import argparse
import yaml
from typing import Dict, Any

from src.utils.logger import setup_logger
from src.pipeline.orchestrator import PipelineOrchestrator
from src.pipeline.quality_gate import DataQualityGate, QualityGateError
from src.transformation.transformer import AnalyticalTransformer
from src.database.database import DatabaseLoader

logger = setup_logger("main_cli")

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_latest_raw_candidates_file(raw_base_dir: str = "data/raw") -> str:
    candidates_files = [
        os.path.join(raw_base_dir, f)
        for f in os.listdir(raw_base_dir)
        if f.startswith("all_raw_candidates_") and f.endswith(".json")
    ]
    if not candidates_files:
        raise FileNotFoundError(f"No aggregated raw candidates file found in {raw_base_dir}")
    candidates_files.sort(reverse=True)
    return candidates_files[0]

def main():
    parser = argparse.ArgumentParser(
        description="Home Fragrance Market Intelligence — End-to-End Pipeline & Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Execution Modes:
  python main.py                  Run complete pipeline end-to-end (Collect -> Clean -> Transform -> Database -> Validate)
  python main.py --stage all      Run complete pipeline end-to-end
  python main.py --stage collect  Run only raw data collection stage
  python main.py --stage clean    Run cleaning and validation on existing raw data
  python main.py --stage transform Run transformation on cleaned data
  python main.py --stage database Build/rebuild SQLite analytical database from clean dataset
  python main.py --stage validate Run final automated data quality gates
        """
    )
    parser.add_argument(
        "--stage",
        type=str,
        default="all",
        choices=["all", "collect", "clean", "transform", "database", "validate"],
        help="Pipeline stage to execute (default: all)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration YAML file (default: config/config.yaml)"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild SQLite database from scratch (applicable to database stage)"
    )

    args = parser.parse_args()
    config = load_config(args.config)
    orchestrator = PipelineOrchestrator(config=config)

    try:
        if args.stage == "all":
            orchestrator.execute_full_pipeline()

        elif args.stage == "collect":
            run_id = orchestrator.runs_dir
            orchestrator.run_collection_stage(run_id="manual_collect")

        elif args.stage == "clean":
            raw_path = get_latest_raw_candidates_file()
            orchestrator.run_cleaning_stage(raw_path)

        elif args.stage == "transform":
            clean_path = "data/processed/products_clean.csv"
            orchestrator.run_transformation_stage(clean_path)

        elif args.stage == "database":
            clean_path = "data/processed/products_clean.csv"
            orchestrator.run_database_stage(clean_path, rebuild=args.rebuild)

        elif args.stage == "validate":
            gate = DataQualityGate()
            gate.run_checks()

    except Exception as e:
        logger.error(f"[PIPELINE FAILED]: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
