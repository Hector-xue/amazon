from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


COLUMN_ALIASES = {
    "campaign": ["campaign", "campaign name"],
    "ad_group": ["ad group", "ad group name"],
    "term": ["customer search term", "search term", "keyword", "targeting"],
    "impressions": ["impressions"],
    "clicks": ["clicks"],
    "spend": ["spend", "cost"],
    "sales": ["sales", "7 day total sales", "14 day total sales"],
    "orders": ["orders", "7 day total orders", "14 day total orders", "purchases"],
    "ctr": ["ctr", "click-through rate"],
    "cpc": ["cpc", "cost per click"],
    "acos": ["acos", "advertising cost of sales"],
    "roas": ["roas", "return on ad spend"],
}


def analyze_ads_report(path: str | Path) -> dict[str, Any]:
    df = _read_report(path)
    df = _normalize_columns(df)
    df = _coerce_metrics(df)
    df = _calculate_metrics(df)

    high_spend_threshold = max(float(df["spend"].quantile(0.75)), 30.0)
    low_acos_threshold = 0.25
    negative_spend_threshold = max(float(df["spend"].median()), 20.0)

    high_spend_low_conversion = df[
        (df["spend"] >= high_spend_threshold) & ((df["orders"] <= 1) | (df["acos"] >= 0.7))
    ]
    low_acos_winners = df[(df["orders"] >= 2) & (df["acos"] > 0) & (df["acos"] <= low_acos_threshold)]
    negative_candidates = df[(df["spend"] >= negative_spend_threshold) & (df["orders"] == 0)]
    budget_candidates = df[(df["orders"] >= 3) & (df["roas"] >= 4.0)]

    return {
        "summary": _summary(df),
        "high_spend_low_conversion": [
            _action(row, "High spend with weak conversion.", "Lower bid, isolate the term, or review listing relevance.")
            for _, row in high_spend_low_conversion.iterrows()
        ],
        "low_acos_winners": [
            _action(row, "Efficient sales at low ACOS.", "Increase bid gradually or move into exact match campaign.")
            for _, row in low_acos_winners.iterrows()
        ],
        "negative_keyword_candidates": [
            _action(row, "Spend without orders.", "Add as negative phrase/exact after manual relevance review.")
            for _, row in negative_candidates.iterrows()
        ],
        "budget_adjustment_candidates": [
            _action(row, "Strong ROAS and order volume.", "Consider budget increase and keyword expansion.")
            for _, row in budget_candidates.iterrows()
        ],
        "rows": df.to_dict(orient="records"),
    }


def _read_report(path: str | Path) -> pd.DataFrame:
    report_path = Path(path)
    if report_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(report_path)
    return pd.read_csv(report_path)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized = {str(column).strip().lower(): column for column in df.columns}
    renamed: dict[str, str] = {}
    for target, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                renamed[normalized[alias]] = target
                break
    return df.rename(columns=renamed)


def _coerce_metrics(df: pd.DataFrame) -> pd.DataFrame:
    for column in ["impressions", "clicks", "spend", "sales", "orders", "ctr", "cpc", "acos", "roas"]:
        if column not in df:
            df[column] = 0
        df[column] = (
            df[column]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)
    if "term" not in df:
        df["term"] = "UNKNOWN"
    if "campaign" not in df:
        df["campaign"] = None
    if "ad_group" not in df:
        df["ad_group"] = None
    return df


def _calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df["ctr"] = df.apply(lambda row: row["ctr"] / 100 if row["ctr"] > 1 else row["ctr"], axis=1)
    df["acos"] = df.apply(lambda row: row["acos"] / 100 if row["acos"] > 1 else row["acos"], axis=1)
    df.loc[df["ctr"] == 0, "ctr"] = df["clicks"] / df["impressions"].replace(0, pd.NA)
    df.loc[df["cpc"] == 0, "cpc"] = df["spend"] / df["clicks"].replace(0, pd.NA)
    df.loc[df["acos"] == 0, "acos"] = df["spend"] / df["sales"].replace(0, pd.NA)
    df.loc[df["roas"] == 0, "roas"] = df["sales"] / df["spend"].replace(0, pd.NA)
    return df.fillna(0)


def _summary(df: pd.DataFrame) -> dict[str, Any]:
    spend = float(df["spend"].sum())
    sales = float(df["sales"].sum())
    clicks = int(df["clicks"].sum())
    impressions = int(df["impressions"].sum())
    return {
        "rows": int(len(df)),
        "impressions": impressions,
        "clicks": clicks,
        "spend": round(spend, 2),
        "sales": round(sales, 2),
        "orders": int(df["orders"].sum()),
        "ctr": round(clicks / impressions, 4) if impressions else 0,
        "cpc": round(spend / clicks, 2) if clicks else 0,
        "acos": round(spend / sales, 4) if sales else 0,
        "roas": round(sales / spend, 2) if spend else 0,
    }


def _action(row: pd.Series, reason: str, recommendation: str) -> dict[str, Any]:
    return {
        "term": str(row.get("term", "")),
        "campaign": row.get("campaign"),
        "ad_group": row.get("ad_group"),
        "reason": reason,
        "metrics": {
            "impressions": int(row["impressions"]),
            "clicks": int(row["clicks"]),
            "spend": round(float(row["spend"]), 2),
            "sales": round(float(row["sales"]), 2),
            "orders": int(row["orders"]),
            "ctr": round(float(row["ctr"]), 4),
            "cpc": round(float(row["cpc"]), 2),
            "acos": round(float(row["acos"]), 4),
            "roas": round(float(row["roas"]), 2),
        },
        "recommendation": recommendation,
    }
