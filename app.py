
import streamlit as st
from agent import (
    retrieve_transactions,
    filter_transactions,
    categorize_transactions,
    calculate_total,
    detect_anomalies,
    generate_summary
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Banking Assistant Agent",
    page_icon="🏦",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("🏦 Banking Assistant Agent")
st.caption("AI-powered transaction analysis and spending insights")

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Analysis Settings")

threshold = st.sidebar.number_input(
    "Transaction Threshold (₹)",
    min_value=0,
    value=50000,
    step=5000
)

st.sidebar.info(
    "The agent analyzes expense transactions above the selected threshold."
)

# ---------------- INTRO ----------------
st.subheader("🔍 Transaction Analysis")

st.write(
    f"Find expense transactions above **₹{threshold:,.0f}** "
    "from last month and generate a spending summary."
)

# ---------------- ANALYZE BUTTON ----------------
if st.button("🚀 Analyze Transactions", width="stretch"):

    try:

        # 1. Retrieve Transactions
        with st.spinner("Retrieving transactions..."):
            df = retrieve_transactions()

        # 2. Filter Transactions
        filtered = filter_transactions(df, threshold)

        # 3. Categorize Transactions
        category_totals = categorize_transactions(filtered)

        # 4. Calculate Total
        total = calculate_total(filtered)

        # 5. Detect Anomalies
        anomalies = detect_anomalies(filtered)

        # ---------------- DASHBOARD ----------------
        st.markdown("## 📊 Analysis Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Transactions Found",
                len(filtered)
            )

        with col2:
            st.metric(
                "Total Spending",
                f"₹{total:,.2f}"
            )

        with col3:
            st.metric(
                "Possible Anomalies",
                len(anomalies)
            )

        st.markdown("---")

        # ---------------- TRANSACTIONS ----------------
        st.subheader(
            f"💳 Transactions Above ₹{threshold:,.0f}"
        )

        if filtered.empty:

            st.info(
                "No transactions were found above the selected threshold."
            )

        else:

            st.dataframe(
                filtered,
                width="stretch",
                hide_index=True
            )

            # ---------------- CATEGORY ----------------
            st.subheader("📊 Category-wise Spending")

            if not category_totals.empty:
                st.bar_chart(category_totals)

            # ---------------- ANOMALIES ----------------
            st.subheader("⚠️ Possible Anomalies")

            if anomalies.empty:

                st.success(
                    "✅ No unusual transactions detected."
                )

            else:

                st.warning(
                    f"{len(anomalies)} unusual transaction(s) detected."
                )

                st.dataframe(
                    anomalies,
                    width="stretch",
                    hide_index=True
                )

            # ---------------- SUMMARY ----------------
            st.subheader("📝 Spending Summary")

            summary = generate_summary(
                filtered,
                category_totals,
                total
            )

            st.info(summary)

            # ---------------- SUCCESS ----------------
            st.success(
                "✅ Transaction analysis completed successfully."
            )

    except FileNotFoundError:

        st.error(
            "❌ Transaction data file was not found. "
            "Please check the data folder."
        )

    except Exception as e:

        st.error(
            f"❌ Something went wrong: {e}"
        )

else:

    st.info(
        "👆 Click **Analyze Transactions** to start the analysis."
    )

