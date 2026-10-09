# MP1 Data Pipeline

This project is a config-driven command-line pipeline that loads a CSV file, validates it, cleans it, and saves the result. `pipeline.py` is the entry point: it parses the `--input`, `--output`, `--config`, and `--verbose` arguments and coordinates each step, while the actual logic lives in the `src/` package. Data moves through the pipeline in order: `utils.py` sets up logging and confirms the input and config files exist, `data_loaders.py` reads the CSV and the YAML config, `data_validator.py` checks that the required columns are present and removes rows with non-numeric values in numeric columns, `data_processor.py` removes duplicate rows, missing values, and outliers based on the config, and `data_output.py` writes the cleaned data to a CSV file. `src/__init__.py` exposes these functions so `pipeline.py` can import everything from one place. All validation and cleaning settings come from `config/config.yaml`, so a different dataset can be cleaned by editing the config rather than the code. Every step logs what it did, including how many rows it removed, so a run can be audited afterward. At the end, the pipeline prints a cleaning report comparing the row and column counts before and after processing.

## Example

Run the pipeline on the provided sample data:

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
16:48:03 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
16:48:03 INFO     src.utils — Input file validated: fixtures/sample_data.csv
16:48:03 INFO     src.utils — Input file validated: config/config.yaml
16:48:03 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
16:48:03 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
16:48:03 WARNING  src.data_validator — Invalid numeric value in rating at row 94: 'not_available'
16:48:03 WARNING  src.data_validator — Invalid numeric value in rating at row 95: 'error'
16:48:03 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
16:48:03 DEBUG    src.data_validator — Validation: 100 → 98 rows (2 removed)
16:48:03 INFO     __main__ — Validation complete: 100 → 98 rows
16:48:03 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
16:48:03 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
16:48:03 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
16:48:03 INFO     __main__ — Processing complete: 98 → 92 rows
16:48:03 DEBUG    src.data_output — Saved 92 rows to output\clean.csv
16:48:03 INFO     __main__ — Saved cleaned data to output\clean.csv

Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}
```