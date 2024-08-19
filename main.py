import streamlit as st

pages = {
        "📗 CHW Activity Dashboard": [
                st.Page("pages/chw_activity.py", title = "📖 CHW Activity")
        ],
        "📕 Impact and Outcomes Dashboard": [
                st.Page("pages/impact_outcome_overview.py", title = "📖 Outcome and Impact Data Overview"),
        ],
        "📘 Indicator Performance Dashboard": [
                st.Page("pages/indicator_perf.py", title = "📖 Indicator Performance")
        ],
        "📚 General Trends": [
                st.Page("pages/year_child.py", title="📖 Child Mortality Dashboard"),
                st.Page("pages/year_cyp.py", title="📖 CYP Dashboard"),
                st.Page("pages/year_disease.py", title="📖 Diseases Dashboard")
]
}

pg = st.navigation(pages)
pg.run()