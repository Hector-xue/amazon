from pathlib import Path

from amazon_ops_agent.ads_analysis import analyze_ads_report


def test_ads_analysis_classifies_sample_report() -> None:
    root = Path(__file__).resolve().parents[1]
    result = analyze_ads_report(root / "examples" / "sample_ads_report.csv")

    assert result["summary"]["rows"] == 5
    assert result["summary"]["orders"] == 122
    assert any(item["term"] == "cheap plastic bottle" for item in result["high_spend_low_conversion"])
    assert any(item["term"] == "coffee mug" for item in result["negative_keyword_candidates"])
    assert any(item["term"] == "stainless steel water bottle" for item in result["low_acos_winners"])

