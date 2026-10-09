# data_processor.py
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    logger.debug(f"remove_duplicates: {before} → {after} rows")

    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis not in ("rows", "columns"):
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")

    if axis == "rows":
        before = len(df)
        df = df.dropna()
        after = len(df)
        logger.debug(f"handle_missing: {before} → {after} rows")
    else:
        before = df.shape[1]
        df = df.dropna(axis=1)
        after = df.shape[1]
        logger.debug(f"handle_missing: {before} → {after} columns")

    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ("iqr", "zscore"):
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for column in columns:
        if column not in df.columns:
            logger.warning(f"Column not found: {column}")
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            logger.warning(f"Column is not numeric: {column}")
            continue

        if method == "iqr":
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
        else:
            mean = df[column].mean()
            std = df[column].std()
            lower = mean - threshold * std
            upper = mean + threshold * std

        before = len(df)
        df = df[(df[column] >= lower) & (df[column] <= upper)].copy()
        removed = before - len(df)

        logger.debug(
            f"{column}: method={method}, threshold={threshold}, "
            f"lower={lower}, upper={upper}, removed={removed}"
        )

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config.get("processing", {})

    if settings.get("remove_duplicates", False):
        df = remove_duplicates(df)

    missing = settings.get("missing", {})
    if missing.get("enabled", False):
        df = handle_missing(df, missing.get("axis", "rows"))

    outliers = settings.get("outliers", {})
    if outliers.get("enabled", False):
        df = remove_outliers(
            df,
            outliers.get("columns", []),
            outliers.get("method"),
            outliers.get("threshold"),
        )

    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": df_before.shape[1],
        "columns_after": df_after.shape[1],
        "columns_removed": df_before.shape[1] - df_after.shape[1],
    }