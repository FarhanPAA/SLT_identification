import streamlit as st

from main import slt


st.set_page_config(page_title="SLT Calculator", layout="centered")
st.title("Single Lowest Tender (SLT) Calculator")
st.write("Enter inputs to compute the SLT lower limit.")

default_tender_prices = []
default_estimated_price = ""
default_nppi = ""

if "tenderer_count" not in st.session_state:
    st.session_state.tenderer_count = 2


def add_tenderer():
    st.session_state.tenderer_count += 1


def remove_tenderer():
    if st.session_state.tenderer_count <= 2:
        return

    last_index = st.session_state.tenderer_count - 1
    st.session_state.pop(f"tender_name_{last_index}", None)
    st.session_state.pop(f"tender_price_{last_index}", None)
    st.session_state.pop(f"tender_eligible_{last_index}", None)
    st.session_state.tenderer_count -= 1

col1, col2 = st.columns(2)
with col1:
    estimated_price = st.text_input(
        "Estimated price",
        value=default_estimated_price,
        placeholder="Enter estimated price",
    )
with col2:
    nppi = st.text_input(
        "NPPI",
        value=default_nppi,
        placeholder="Enter NPPI factor",
    )

st.subheader("Tenderers")
for tenderer_index in range(st.session_state.tenderer_count):
    name_col, price_col, eligible_col = st.columns([2, 2, 1])

    with name_col:
        st.text_input(
            f"Tenderer {tenderer_index + 1} name",
            value=f"Tenderer No: {tenderer_index + 1}",
            key=f"tender_name_{tenderer_index}",
        )

    with price_col:
        price_key = f"tender_price_{tenderer_index}"
        if price_key in st.session_state and st.session_state[price_key] is not None:
            st.session_state[price_key] = str(st.session_state[price_key])

        st.text_input(
            f"Tenderer {tenderer_index + 1} price",
            value="",
            placeholder="Enter price",
            key=price_key,
        )

    with eligible_col:
        st.selectbox(
            f"Tenderer {tenderer_index + 1} eligible",
            options=[True, False],
            index=0,
            key=f"tender_eligible_{tenderer_index}",
        )

controls_col1, controls_col2 = st.columns([1, 1])
with controls_col1:
    st.button("Add tenderer", on_click=add_tenderer, use_container_width=True)
with controls_col2:
    st.button(
        "Remove tenderer",
        on_click=remove_tenderer,
        disabled=st.session_state.tenderer_count <= 2,
        use_container_width=True,
    )

if st.button("Calculate SLT"):
    tender_price_raw = [
        (st.session_state.get(f"tender_price_{i}", "") or "").strip()
        for i in range(st.session_state.tenderer_count)
    ]
    tenderer_names = [
        (st.session_state.get(f"tender_name_{i}") or f"Tenderer No: {i + 1}").strip()
        for i in range(st.session_state.tenderer_count)
    ]
    eligibility = [
        bool(st.session_state.get(f"tender_eligible_{i}", True))
        for i in range(st.session_state.tenderer_count)
    ]

    if any(not raw for raw in tender_price_raw):
        st.warning("Please enter a tender price for every tenderer before calculating.")
    elif not (estimated_price or "").strip() or not (nppi or "").strip():
        st.warning("Please enter both Estimated price and NPPI before calculating.")
    else:
        try:
            estimated_price_value = float((estimated_price or "").strip())
            nppi_value = float((nppi or "").strip())
            tender_prices = [float(raw) for raw in tender_price_raw]
        except ValueError as exc:
            st.error(f"Invalid numeric input: {exc}")
        else:
            if estimated_price_value < 0:
                st.error("Estimated price must be 0 or greater.")
            elif nppi_value < 0 or nppi_value > 10:
                st.error("NPPI must be between 0 and 10.")
            elif any(price <= 0 for price in tender_prices):
                st.error("All tender prices must be greater than 0.")
            else:
                result = slt(tender_prices, estimated_price_value, nppi_value, eligibility)
                if result is None:
                    st.warning("No eligible tender prices (need at least 2 after filtering).")
                else:
                    st.success(f"SLT lower limit: {result:.2f}")

                    responsive_indices = [
                        i
                        for i, (price, is_eligible) in enumerate(zip(tender_prices, eligibility))
                        if is_eligible and price < 1.1 * estimated_price_value
                    ]
                    accepted_indices = [
                        i for i in responsive_indices if tender_prices[i] >= float(result)
                    ]

                    if not accepted_indices:
                        st.warning("No winning bidder (all responsive bids are below the SLT lower limit).")
                    else:
                        winner_index = min(accepted_indices, key=lambda i: tender_prices[i])
                        st.info(
                            f"Winning bidder: {tenderer_names[winner_index]} "
                            f"— Tender price: {tender_prices[winner_index]:.2f}"
                        )
