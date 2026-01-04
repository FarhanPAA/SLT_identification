from __future__ import annotations

from slt import compute_slt


def slt(
    tender_prices: list[float],
    estimated_price: float,
    nppi: float,
    eligibility: list[bool] | None = None,
) -> float | None:
    """
    Backwards-compatible wrapper returning only the SLT lower limit.
    """
    result = compute_slt(tender_prices, estimated_price, nppi, eligibility)
    return None if result is None else result.lower_limit


if __name__ == "__main__":
    sample_prices = [34057525, 36537500, 38254655, 41145689, 44876900, 36004268, 37789320]
    sample_estimated = 40000000
    sample_nppi = 0.9168
    sample_eligibility = [True, True, True, True, True, False, True]
    print(slt(sample_prices, sample_estimated, sample_nppi, sample_eligibility))

