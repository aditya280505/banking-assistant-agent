import streamlit as st
from agent import (
    retrieve_transactions,
    filter_transactions,
    categorize_transactions,
    calculate_total,
    detect_anomalies,
    generate_summary
)

st.set_page_config(
    page_title="Banking Assistant Agent",
    page_icon="🏦"
)

st.title("🏦 Banking Assistant Agent")
st.write(
    "Show transactions above ₹50,000 from last month "
    "and summarize my spending."
)

if st.button("Analyze Transactions"):

    try:
        # 1. Retrieve
        df = retrieve_transactions()

        # 2. Filter
        filtered = filter_transactions(df)

        # 3. Categorize
        category_totals = categorize_transactions(filtered)

        # 4. Calculate
        total = calculate_total(filtered)

        # 5. Detect anomalies
        anomalies = detect_anomalies(filtered)

        # Results
        st.subheader("💳 Transactions Above ₹50,000")

        if filtered.empty:
            st.info("No matching transactions found.")
        else:
            st.dataframe(filtered)

            st.metric(
                "Total Spending",
                f"₹{total:,.2f}"
            )

            st.subheader("📊 Category-wise Spending")
            st.bar_chart(category_totals)

            st.subheader("⚠️ Possible Anomalies")

            if anomalies.empty:
                st.success("No unusual transactions detected.")
            else:
                st.dataframe(anomalies)

            # 6. Summary
            st.subheader("📝 Spending Summary")

            summary = generate_summary(
                filtered,
                category_totals,
                total
            )

            st.write(summary)

    except Exception as e:
        st.error(
            f"❌ Something went wrong: {e}"
        )