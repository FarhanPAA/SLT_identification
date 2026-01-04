from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class SltResult:
    lower_limit: float
    x_bar: float
    sd: float
    responsive_indices: tuple[int, ...]
    accepted_indices: tuple[int, ...]
    winner_index: int | None


def _as_bool_sequence(values: Iterable[object], *, expected_len: int) -> list[bool]:
    out = [bool(v) for v in values]
    if len(out) != expected_len:
        raise ValueError("eligibility length must match tender_prices length")
    return out


def compute_slt(
    tender_prices: Sequence[float],
    estimated_price: float,
    nppi: float,
    eligibility: Iterable[object] | None = None,
    *,
    responsive_threshold_multiplier: float = 1.1,
) -> SltResult | None:
    """
    Compute the SLT lower limit and winning bidder.

    Responsive tenders are those that are eligible and below the threshold:
        price < responsive_threshold_multiplier * estimated_price

    Returns `None` when fewer than 2 responsive tenders exist.
    """
    if estimated_price < 0:
        raise ValueError("estimated_price must be >= 0")
    if nppi < 0:
        raise ValueError("nppi must be >= 0")
    if responsive_threshold_multiplier <= 0:
        raise ValueError("responsive_threshold_multiplier must be > 0")
    if not tender_prices:
        return None

    prices = [float(p) for p in tender_prices]
    if any(p <= 0 for p in prices):
        raise ValueError("all tender prices must be > 0")

    eligible = (
        [True] * len(prices)
        if eligibility is None
        else _as_bool_sequence(eligibility, expected_len=len(prices))
    )

    threshold = responsive_threshold_multiplier * estimated_price
    responsive_indices = tuple(
        i for i, (price, ok) in enumerate(zip(prices, eligible)) if ok and price < threshold
    )
    if len(responsive_indices) < 2:
        return None

    responsive_prices = [prices[i] for i in responsive_indices]
    mean_price = sum(responsive_prices) / len(responsive_prices)

    x_nppi = estimated_price * nppi
    x_bar = 0.5 * mean_price + 0.2 * estimated_price + 0.3 * x_nppi

    variance = sum((price - x_bar) ** 2 for price in responsive_prices) / len(responsive_prices)
    sd = sqrt(variance)
    lower_limit = x_bar - sd

    accepted_indices = tuple(i for i in responsive_indices if prices[i] >= lower_limit)
    winner_index = (
        None if not accepted_indices else min(accepted_indices, key=lambda i: prices[i])
    )

    return SltResult(
        lower_limit=lower_limit,
        x_bar=x_bar,
        sd=sd,
        responsive_indices=responsive_indices,
        accepted_indices=accepted_indices,
        winner_index=winner_index,
    )

