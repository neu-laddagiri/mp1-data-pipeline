"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv --config config/config.yaml
    python pipeline.py --input data.csv --output clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys
from pprint import pprint

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a data processing pipeline."
    )

    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--config", "-c", required=True,
                        help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose logging")

    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, "
        f"output={args.output}, config={args.config}"
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    if not isinstance(config, dict):
        logger.error(f"Config file must contain YAML settings: {args.config}")
        sys.exit(1)

    validation = config.get("validation") or {}
    if not isinstance(validation, dict):
        logger.error(f"Config section 'validation' must contain settings, got {validation!r}")
        sys.exit(1)

    required_columns = validation.get("required_columns") or []
    numeric_columns = validation.get("numeric_columns") or []

    rows_before_validation = len(data)

    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)

    logger.info(f"Validation complete: {rows_before_validation} → {len(data)} rows")

    original_data = data.copy()

    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(original_data, data)

    logger.info(
        f"Processing complete: {report['rows_before']} → {report['rows_after']} rows"
    )

    try:
        output_path = save_data(data, args.output)
    except ValueError:
        sys.exit(1)

    logger.info(f"Saved cleaned data to {output_path}")

    print("\nCleaning report:")
    pprint(report, sort_dicts=False)


if __name__ == "__main__":
    main()