import streamlit as st
import pandas as pd
import plotly.express as px
from LARC_CHWs_Cleaning import larc_chw_cleaning

st.set_page_config(layout="wide")

# Creating a container for the title of the dashboard
cont1 = st.container()
with cont1:
    st.markdown("<h1 style='text-align: center;'>Yearly CYP Dashboard</h1>", unsafe_allow_html=True)
    st.write("")

# Streamlit code to upload and process the file
df_file = st.file_uploader("Choose a file", type=["csv"])

if df_file is not None:
    cleaned_csv_path = larc_chw_cleaning(df_file)

    # Read the cleaned DataFrame (optional, just for display)
    dataframe = pd.read_csv(cleaned_csv_path)

    # Include options to choose years on sidebar
    with st.sidebar:
        st.title('Yearly CYP Trends Dashboard')
        year_list = sorted(dataframe['Year'].unique(), reverse=True)
        selected_years = st.multiselect('Select years', year_list, default=year_list)
        df_selected_years = dataframe[dataframe['Year'].isin(selected_years)]

        # Select the methods they would like to look at
        method_list = ["CYP pills", "CYP injection", "CYP Implant", "CYP IUD"]
        selected_method_list = st.multiselect('Select methods', method_list, default=method_list)

        # Aggregate data
        df_aggregated = df_selected_years.groupby('Year')[selected_method_list].sum().reset_index()
        df_aggregated.sort_values(by="Year", inplace=True)

        # Create bar graph showing all trends for the selected years and methods
    fig = px.bar(df_aggregated, x="Year", y=selected_method_list,
                 labels={"value": "Total", "variable": "Method"},
                 barmode="group",
                 color_discrete_sequence=["#050C9C", "#3572EF", "#3ABEF9", "#A7E6FF"])

    # Ensure the hover template shows the correct totals
    fig.update_traces(hovertemplate='%{y:.2f}')

    st.plotly_chart(fig)

    #Create columns for metrics cards to me aligned
    col1, col2, col3, col4 = st.columns(4)

    # Calculate total CYP counts for each method for the selected years
    total_cyp_pills = df_selected_years["CYP pills"].sum()
    total_cyp_injection = df_selected_years["CYP injection"].sum()
    total_cyp_implant = df_selected_years["CYP Implant"].sum()
    total_cyp_iud = df_selected_years["CYP IUD"].sum()

    if len(selected_years) > 1:
        #For delta
        recent_year = max(selected_years)
        previous_year = max(year for year in selected_years if year < recent_year)

        recent_data = dataframe[dataframe['Year'] == recent_year]
        previous_data = dataframe[dataframe['Year'] == previous_year]

        #total sum of the most recent year
        total_cyp_pills_new = recent_data["CYP pills"].sum()
        total_cyp_injection_new = recent_data["CYP injection"].sum()
        total_cyp_implant_new = recent_data["CYP Implant"].sum()
        total_cyp_iud_new = recent_data["CYP IUD"].sum()

        delta_pills = total_cyp_pills_new-previous_data["CYP pills"].sum()
        delta_injection = total_cyp_injection_new-previous_data["CYP injection"].sum()
        delta_implant = total_cyp_implant_new-previous_data["CYP Implant"].sum()
        delta_iud = total_cyp_iud_new-previous_data["CYP IUD"].sum()

        #Include metrics cards for each method
        col1.metric(label="Total CYP Pills", value=f"{total_cyp_pills_new:.2f}", delta=f"{delta_pills:.2f}")
        col2.metric(label="Total CYP Injections", value=f"{total_cyp_injection_new:.2f}", delta=f"{delta_injection:.2f}")
        col3.metric(label="Total CYP Implants", value=f"{total_cyp_implant_new:.2f}", delta=f"{delta_implant:.2f}")
        col4.metric(label="Total CYP IUDs", value=f"{total_cyp_iud_new:.2f}", delta=f"{delta_iud:.2f}")

    else:
        # Include metrics cards for each method
        col1.metric(label="Total CYP Pills", value=f"{total_cyp_pills:.2f}")
        col2.metric(label="Total CYP Injections", value=f"{total_cyp_injection:.2f}")
        col3.metric(label="Total CYP Implants", value=f"{total_cyp_implant:.2f}")
        col4.metric(label="Total CYP IUDs", value=f"{total_cyp_iud:.2f}")

else:
    st.info("Please upload a CSV file.")





