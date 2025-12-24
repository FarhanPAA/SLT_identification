# Sample data

tender_prices = [34057525, 36537500, 38254655, 41145689, 44876900, 36004268, 37789320]
estimated_price = 40000000
NPPI = 0.9168
eligibility = [True, True, True, True, True, False, True]
def slt(tender_prices, estimated_price, NPPI, eligibility):
    """
    Calculate the Single Lowest Tender (SLT) price based on tender prices,
    estimated price, NPPI, and eligibility criteria.

    Parameters:
    tender_prices (list of float): List of tender prices submitted.
    estimated_price (float): The estimated price for the tender.
    NPPI (float): The Non-Performing Price Index.
    eligibility (bool): Eligibility criteria for SLT calculation.

    Returns:
    float: Lower limit of acceptable price
    """
    tender_prices = [price for price, eligible in zip(tender_prices, eligibility) if eligible and price < 1.1*estimated_price]

    if len(tender_prices) < 2:
        return None  # No eligible tender prices

    mean_price = sum(tender_prices) / len(tender_prices)
    print(f"Mean tender price: {mean_price}")
    X_NPPI = estimated_price * NPPI
    print(f"X_NPPI: {X_NPPI}")

    x_bar = 0.5*mean_price + 0.2*estimated_price + 0.3*X_NPPI
    print(f"x_bar: {x_bar}")

    sd = (sum((price - x_bar) ** 2 for price in tender_prices) / len(tender_prices)) ** 0.5

    return x_bar - sd

lower_limit = slt(tender_prices, estimated_price, NPPI, eligibility)
print(f"SLT lower limit: {lower_limit}")
