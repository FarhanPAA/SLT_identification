from __future__ import annotations

import streamlit as st

from .calculator import compute_slt


def run() -> None:
    st.set_page_config(page_title="SLT Calculator", layout="centered")
    st.title("Single Lowest Tender (SLT) Calculator")
    st.caption("Enter inputs to compute the SLT lower limit and identify the winning bidder.")

    if "tenderer_count" not in st.session_state:
        st.session_state.tenderer_count = 2

    def add_tenderer() -> None:
        st.session_state.tenderer_count += 1

    def remove_tenderer() -> None:
        if st.session_state.tenderer_count <= 2:
            return
        last_index = st.session_state.tenderer_count - 1
        st.session_state.pop(f"tender_name_{last_index}", None)
        st.session_state.pop(f"tender_price_{last_index}", None)
        st.session_state.pop(f"tender_eligible_{last_index}", None)
        st.session_state.tenderer_count -= 1

    col1, col2 = st.columns(2)
    with col1:
        estimated_price = st.number_input(
            "Estimated price",
            min_value=0.0,
            value=0.0,
            step=1.0,
            format="%.2f",
        )
    with col2:
        nppi = st.number_input(
            "NPPI",
            min_value=0.0,
            value=0.0,
            step=0.0001,
            format="%.4f",
            help="Non-Performing Price Index factor.",
        )

    st.subheader("Tenderers")
    tenderer_names: list[str] = []
    tender_prices: list[float] = []
    eligibility: list[bool] = []

    for tenderer_index in range(st.session_state.tenderer_count):
        name_col, price_col, eligible_col = st.columns([2, 2, 1])

        with name_col:
            tenderer_names.append(
                st.text_input(
                    f"Tenderer {tenderer_index + 1} name",
                    value=f"Tenderer No: {tenderer_index + 1}",
                    key=f"tender_name_{tenderer_index}",
                ).strip()
            )

        with price_col:
            tender_prices.append(
                st.number_input(
                    f"Tenderer {tenderer_index + 1} price",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    format="%.2f",
                    key=f"tender_price_{tenderer_index}",
                )
            )

        with eligible_col:
            eligibility.append(
                st.selectbox(
                    f"Tenderer {tenderer_index + 1} eligible",
                    options=[True, False],
                    index=0,
                    key=f"tender_eligible_{tenderer_index}",
                )
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

    st.divider()

    if st.button("Calculate SLT", use_container_width=True):
        try:
            result = compute_slt(tender_prices, estimated_price, nppi, eligibility)
        except ValueError as exc:
            st.error(str(exc))
            return

        if result is None:
            st.warning("No responsive tenders (need at least 2 after filtering).")
            return

        st.success(f"SLT lower limit: {result.lower_limit:,.2f}")
        st.write(f"x̄: {result.x_bar:,.2f}  •  SD: {result.sd:,.2f}")

        if result.winner_index is None:
            st.warning("No winning bidder (all responsive bids are below the SLT lower limit).")
        else:
            st.info(
                f"Winning bidder: {tenderer_names[result.winner_index]} — "
                f"Tender price: {tender_prices[result.winner_index]:,.2f}"
            )

        rows = []
        for i, (name, price, ok) in enumerate(zip(tenderer_names, tender_prices, eligibility)):
            rows.append(
                {
                    "Tenderer": name,
                    "Price": price,
                    "Eligible": ok,
                    "Responsive": i in result.responsive_indices,
                    "Accepted (>= SLT)": i in result.accepted_indices,
                    "Winner": i == result.winner_index,
                }
            )
        st.dataframe(rows, use_container_width=True, hide_index=True)

