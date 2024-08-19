import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging

st.set_page_config(layout="wide")

logging.basicConfig(filename='processing_log.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# data cleaning function
def process_and_save_data(df):
    try:
        # transpose dataframe
        df_transposed = df.T
        df_transposed = df_transposed.dropna(how='all')

        # drop specific rows
        df_transposed = df_transposed.drop(index=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'],
                                           errors='ignore')

        # extract new column names
        new_column_names = df_transposed.iloc[0].tolist()

        # set new column names for transposed dataframe
        df_transposed.columns = new_column_names
        df_transposed = df_transposed.drop(index=df_transposed.index[0])

        # rename first column
        df_transposed.rename(columns={df_transposed.columns[0]: 'Year'}, inplace=True)

        # reformat year column
        df_transposed[['Year', 'Quarter']] = df_transposed['Year'].str.split('-', expand=True)

        return df_transposed

    except Exception as e:
        logging.error(f"Error processing DataFrame: {e}")
        return pd.DataFrame()  # return empty on error


# summary function
def summary_page(df):
    st.title("CHW Activity Dashboard")

    # sidebar filters
    st.sidebar.header("Filters")

    years = df["Year"].unique()
    selected_years = st.sidebar.multiselect('Select Years', sorted(years), default=sorted(years))

    indicators = df["Indicators of realisation"].unique()
    selected_indicators = st.sidebar.multiselect('Select Indicators of Realisation', sorted(indicators),
                                                 default=sorted(indicators))

    # additional filters based on dynamic column names
    all_columns = df.columns[2:]
    selected_columns = st.sidebar.multiselect('Select Data Columns', sorted(all_columns), default=sorted(all_columns))

    # filter data based on the selected years and indicators
    df_selected = df[df["Year"].isin(selected_years) & df["Indicators of realisation"].isin(selected_indicators)]

    if not df_selected.empty and selected_columns:
        # ensure only selected columns that exist in dataframe are used
        columns_to_display = ["Year", "Indicators of realisation"] + selected_columns

        # filter to display only selected columns
        df_display = df_selected[columns_to_display].copy()

        # convert selected columns to numeric, forcing errors to NaN
        df_display[selected_columns] = df_display[selected_columns].apply(pd.to_numeric, errors='coerce')

        # show the filtered data as a table
        st.write("### Filtered Data")
        st.dataframe(df_display)

        # line chart visualisation
        st.write("### Trend Over Time")
        for column in selected_columns:
            plt.figure(figsize=(10, 5))
            plt.plot(df_display['Year'], df_display[column], marker='o', linestyle='-', label=column)
            plt.title(f'Trend of {column} Over Time')
            plt.xlabel('Year')
            plt.ylabel(column)
            plt.legend()
            plt.grid(True)
            st.pyplot(plt)
            plt.clf()

        # bar chart visualisation
        st.write("### Indicator Comparison by Location")
        df_indicator_sum = df_display.groupby("Indicators of realisation")[selected_columns].sum()

        df_indicator_sum.plot(kind='bar', figsize=(10, 6))
        plt.title('Sum of Selected Data Columns by Indicator')
        plt.xlabel("Indicator of Realisation")
        plt.ylabel("Sum")
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

    else:
        st.write("No data available for the selected filters.")


# main dashboard function
st.sidebar.title("CHW Activity Dashboard")
st.sidebar.info("Upload up to 5 CSV files to start analyzing CHW activities.")

# file uploader
uploaded_files = []
for i in range(5):
    uploaded_file = st.sidebar.file_uploader(f"Upload CSV file {i + 1}", type="csv", key=f"file_uploader_{i}")
    if uploaded_file:
        uploaded_files.append(uploaded_file)

if uploaded_files:
    processed_dataframes = []
    for uploaded_file in uploaded_files:
        # load uploaded file into a dataframe
        df = pd.read_csv(uploaded_file)

        # clean dataframe
        cleaned_df = process_and_save_data(df)

        # validate required columns exist in the dataframe
        required_columns = ["Year", "Indicators of realisation"]
        if all(col in cleaned_df.columns for col in required_columns):
            processed_dataframes.append(cleaned_df)
        else:
            st.error(
                f"The uploaded file {uploaded_file.name} must contain the following columns: {', '.join(required_columns)}")

    if processed_dataframes:
        # combine all cleaned dataframes into a single one
        combined_df = pd.concat(processed_dataframes, ignore_index=True)
        summary_page(combined_df)
    else:
        st.error("No valid data available after cleaning the uploaded files.")
else:
    st.write("Please upload CSV files to proceed.")
