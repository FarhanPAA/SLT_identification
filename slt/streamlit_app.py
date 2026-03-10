from __future__ import annotations

import streamlit as st

from .calculator import compute_slt


def run() -> None:
    st.set_page_config(
        page_title="Significantly Low Priced Tenderers Identification",
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(14, 116, 144, 0.14), transparent 28%),
                linear-gradient(180deg, #f4f8fb 0%, #eef4f7 100%);
        }
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero-card, .section-card, .result-card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            padding: 1.2rem 1.3rem;
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.35rem;
        }
        .hero-caption {
            color: #355468;
            font-size: 1rem;
            margin: 0;
        }
        .metric-label {
            color: #486273;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.2rem;
        }
        .metric-value {
            color: #0f172a;
            font-size: 1.35rem;
            font-weight: 700;
            margin: 0;
        }
        div[data-testid="stNumberInput"], div[data-testid="stTextInput"], div[data-testid="stSelectbox"] {
            background: #fbfdff;
            border-radius: 12px;
            padding: 0.25rem 0.35rem;
        }
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
            border: none;
            min-height: 2.8rem;
        }
        .result-heading {
            color: #0f172a;
            font-size: 1.15rem;
            font-weight: 700;
            margin: 0 0 0.85rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Significantly Low Priced Tenderers Identification</div>
            <p class="hero-caption">
                Enter the estimate, NPPI, and tender details to identify responsive bids and the winning bidder.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    summary_col1, summary_col2, summary_col3 = st.columns([1.2, 1.2, 1])
    with summary_col1:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="metric-label">Tenderers</div>
                <p class="metric-value">{st.session_state.tenderer_count}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with summary_col2:
        st.markdown(
            """
            <div class="section-card">
                <div class="metric-label">Evaluation Rule</div>
                <p class="metric-value">SLT Lower Limit</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with summary_col3:
        st.markdown(
            """
            <div class="section-card">
                <div class="metric-label">Threshold</div>
                <p class="metric-value">110% of estimate</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Project Inputs")
    col1, col2 = st.columns(2)
    with col1:
        estimated_price = st.number_input(
            "Estimated price",
            min_value=0.0,
            value=None,
            step=1.0,
            format="%.2f",
            placeholder="Enter estimated price",
        )
    with col2:
        nppi = st.number_input(
            "NPPI",
            min_value=0.0,
            value=None,
            step=0.0001,
            format="%.4f",
            help="Non-Performing Price Index factor.",
            placeholder="Enter NPPI",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Tenderers")
    tenderer_names: list[str] = []
    tender_prices: list[float | None] = []
    eligibility: list[bool] = []

    for tenderer_index in range(st.session_state.tenderer_count):
        name_col, price_col, eligible_col = st.columns([2.4, 2, 1.1])

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
                    value=None,
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
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("Calculate SLT", use_container_width=True):
        if estimated_price is None or nppi is None or any(price is None for price in tender_prices):
            st.warning("Please enter Estimated price, NPPI, and a price for every tenderer before calculating.")
            return

        if any(price <= 0 for price in tender_prices if price is not None):
            st.error("All tender prices must be greater than 0.")
            return

        try:
            result = compute_slt(
                [price for price in tender_prices if price is not None],
                float(estimated_price),
                float(nppi),
                eligibility,
            )
        except ValueError as exc:
            st.error(str(exc))
            return

        if result is None:
            st.warning("No responsive tenders (need at least 2 after filtering).")
            return

        winner_name = (
            "No winning bidder"
            if result.winner_index is None
            else tenderer_names[result.winner_index]
        )
        winner_price = (
            "-"
            if result.winner_index is None
            else f"{tender_prices[result.winner_index]:,.2f}"
        )

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-heading">Evaluation Summary</div>', unsafe_allow_html=True)
        st.table(
            [
                {"Item": "SLT Lower Limit", "Value": f"{result.lower_limit:,.2f}"},
                {"Item": "X_BAR", "Value": f"{result.x_bar:,.2f}"},
                {"Item": "Standard Deviation", "Value": f"{result.sd:,.2f}"},
                {"Item": "Winning Bidder", "Value": winner_name},
                {"Item": "Winning Tender Price", "Value": winner_price},
            ]
        )
        st.markdown("</div>", unsafe_allow_html=True)

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
