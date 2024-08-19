import streamlit as st
import tracemalloc
import datetime
import tempfile
import pandas as pd

st.set_page_config(layout="wide")

st.title("Outcome and Impact Data Overview")
tracemalloc.start()

# upload a csv file
uploaded_file = st.file_uploader("Please select a CSV file", type="csv")

if uploaded_file is not None:
    # use temp file to save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
        st.write("File successfully uploaded and saved to:", tmp_file_path)

    # @st.cache
    @st.cache_data
    # define a function to process the uploaded file and save the processed data
    def process_and_save_data(input_file_path):
        # load the .csv filedata
        df = pd.read_csv(input_file_path)

        # drop all rows with all NaN values
        df_cleared = df.dropna(how="all")

        df_cleared.reset_index(drop=True, inplace=True)
        df_cleared.index += 0

        # Convert percentage to number in the specified column if it exists
        if (
            "Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"
            in df_cleared.columns
        ):
            df_cleared[
                "Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"
            ] = df_cleared[
                "Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"
            ].apply(
                lambda x: (
                    int(float(str(x).replace("%", "")) / 100)
                    if "%" in str(x)
                    else x
                )
            )

        # Convert number to percentage in the specified column if it exists
        if (
            "Proportion of women retained in care (HIV treatment)"
            in df_cleared.columns
        ):
            df_cleared[
                "Proportion of women retained in care (HIV treatment)"
            ] = df_cleared[
                "Proportion of women retained in care (HIV treatment)"
            ].apply(
                lambda x: (
                    f"{float(x) * 100:.2f}%"
                    if pd.notna(x) and "%" not in str(x)
                    else x
                )
            )
        return df_cleared

    # invoking the function to process the data
    data = process_and_save_data(tmp_file_path)

    # filter the data by year, quarter, and indicators of realisation
    data_column_option = st.sidebar.multiselect(
        "Select Data Column", data.columns[2:]
    )
    year_option = st.sidebar.multiselect("Select Year", data["Years"].unique())
    site_option = st.sidebar.multiselect("Select Site", data["Site"].unique())

    # filtered data
    st.subheader("Filtered Data")
    filtered_data = data
    if year_option:
        filtered_data = filtered_data[filtered_data["Years"].isin(year_option)]
    # select by site
    if site_option:
        filtered_data = filtered_data[filtered_data["Site"].isin(site_option)]

    # show the filtered data
    if data_column_option:
        table_to_display = ["Years", "Site"] + data_column_option
        st.write(filtered_data[table_to_display])

    if "Couple Years Protection (CYP)AC" in data.columns:
        # Get the current year
        current_year = datetime.datetime.now().year

        # Filter the DataFrame for the years from 2021 to the current year
        df_sum = data[data["Years"].isin(range(2021, current_year + 1))]

        # Group by 'Years' and calculate the sum of the specified columns
        df_site_sum = df_sum.groupby("Years")[
            [
                "Couple Years Protection (CYP)AC",
                "Couple Years Protection (CYP)AC+LARC",
                "Couple Years Protection (CYP)CSB",
                "Number of Population reached with improved access to health services",
                "Number of Villages reached for Safidy",
            ]
        ].sum()

        # Reset the index to make 'Years' a column again
        df_site_sum.reset_index(inplace=True)

        st.subheader(f"Summed data of all sites, years 2021-{current_year}")
        # Display the dataframe on the Streamlit webpage
        st.write(df_site_sum)

    if "Population" in data.columns:
        # Get the current year
        current_year = datetime.datetime.now().year

        # Filter the DataFrame for the years from 2021 to the current year
        df_sum = data[data["Years"].isin(range(2021, current_year + 1))]

        # Group by 'Years' and calculate the sum of the specified columns
        df_site_sum = df_sum.groupby("Years")[
            [
                "Population",
                "Children under five",
                "Women of Reproductive Age (FAR) 15 - 49 years old",
                "Number of child deaths (absolute number)\nCHWs+CSB",
                "Number of Service Delivery points added/strengthened(Children under five and mother)",
            ]
        ].sum()

        # Reset the index to make 'Years' a column again
        df_site_sum.reset_index(inplace=True)

        st.subheader(f"Summed data of all sites, years 2021-{current_year}")
        # Display the dataframe on the Streamlit webpage
        st.write(df_site_sum)

else:
    st.write("Please upload a CSV file.")