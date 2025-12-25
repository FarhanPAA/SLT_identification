# Sample data

tender_prices = [34057525, 36537500, 38254655, 41145689, 44876900, 36004268, 37789320]
estimated_price = 40000000
NPPI = 0.9168
eligibility = [True, True, True, True, True, False, True]

# Function to calculate SLT
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
    # Filter tender prices based on eligibility and 10% threshold
    tender_prices = [price for price, eligible in zip(tender_prices, eligibility) if eligible and price < 1.1*estimated_price]

    # Formula only applies if there are at least 2 eligible tender prices
    if len(tender_prices) < 2:
        return None  # No eligible tender prices

    # Calculate mean price of responsive tenders
    mean_price = sum(tender_prices) / len(tender_prices)
    
    # Calculate X_NPPI based on estimated price and NPPI from eProcurement
    X_NPPI = estimated_price * NPPI

    # Calculate x_bar from the formula
    x_bar = 0.5*mean_price + 0.2*estimated_price + 0.3*X_NPPI
    
    # Calculate standard deviation of tender prices using x_bar
    sd = (sum((price - x_bar) ** 2 for price in tender_prices) / len(tender_prices)) ** 0.5

    # Return the lower limit
    return x_bar - sd

print("Lower limit of acceptable price (SLT):", slt(tender_prices, estimated_price, NPPI, eligibility))