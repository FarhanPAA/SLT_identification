import streamlit as st

from main import slt


def parse_float_list(value):
    items = [v.strip() for v in value.split(",") if v.strip()]
    return [float(v) for v in items]


def parse_bool_list(value):
    items = [v.strip().lower() for v in value.split(",") if v.strip()]
    return [v in {"true", "t", "1", "yes", "y"} for v in items]


st.set_page_config(page_title="SLT Calculator", layout="centered")
st.title("Single Lowest Tender (SLT) Calculator")
st.write("Enter inputs to compute the SLT lower limit.")

default_tender_prices = "100000, 95000, 105000, 98000"
default_estimated_price = "99000"
default_nppi = "0.85"
default_eligibility = "False, True, True, True"

col1, col2 = st.columns(2)

with col1:
    tender_prices_input = st.text_input("Tender prices (comma-separated)", default_tender_prices)
    estimated_price_input = st.text_input("Estimated price", default_estimated_price)

with col2:
    nppi_input = st.text_input("NPPI", default_nppi)
    eligibility_input = st.text_input("Eligibility flags (comma-separated)", default_eligibility)

if st.button("Calculate SLT"):
    try:
        tender_prices = parse_float_list(tender_prices_input)
        estimated_price = float(estimated_price_input)
        nppi = float(nppi_input)
        eligibility = parse_bool_list(eligibility_input)

        if len(tender_prices) != len(eligibility):
            st.error("Tender prices and eligibility must have the same number of entries.")
        else:
            result = slt(tender_prices, estimated_price, nppi, eligibility)
            if result is None:
                st.warning("No eligible tender prices (need at least 2 after filtering).")
            else:
                st.success(f"SLT lower limit: {result:.2f}")
    except ValueError as exc:
        st.error(f"Invalid input: {exc}")
