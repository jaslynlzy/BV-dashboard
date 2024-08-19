import pandas as pd
import numpy as np
import re

def larc_chw_cleaning(input_file):
    # Load the CSV file, skipping the first two rows and treating "NaN" as NaN values
    df = pd.read_csv(input_file, skiprows=2, na_values="NaN")

    # Function to clean and split the "Quarter" column into "Year" and "Quarter"
    def clean_quarter_column(quarter_str):
        if pd.isna(quarter_str):
            return np.nan, np.nan
        # Define regex patterns to capture various formats
        patterns = [
            r"(?P<Year>\d{4})[-/\s]*(?P<Quarter>Q[1-4])",  # Matches "2023-Q1", "2023/Q1", "2023 Q1"
            r"(?P<Quarter>Q[1-4])[-/\s]*(?P<Year>\d{4})",  # Matches "Q1-2023", "Q1/2023", "Q1 2023"
            r"(?P<Year>\d{4})[-/\s]*(?P<Month>[A-Za-z]+)",  # Matches "2023-Jan", "2023 January"
        ]
        for pattern in patterns:
            match = re.match(pattern, quarter_str)
            if match:
                match_dict = match.groupdict()
                # If we matched a month instead of a quarter, map months to quarters
                if 'Month' in match_dict:
                    month = match_dict['Month'].lower()[:3]  # Get first three letters, lowercase
                    month_to_quarter = {
                        'jan': 'Q1', 'feb': 'Q1', 'mar': 'Q1',
                        'apr': 'Q2', 'may': 'Q2', 'jun': 'Q2',
                        'jul': 'Q3', 'aug': 'Q3', 'sep': 'Q3',
                        'oct': 'Q4', 'nov': 'Q4', 'dec': 'Q4'
                    }
                    match_dict['Quarter'] = month_to_quarter.get(month, np.nan)
                    match_dict.pop('Month')  # Remove 'Month' from dict
                return match_dict.get('Year'), match_dict.get('Quarter')
        return np.nan, np.nan

    # Apply the cleaning function to split the "Quarter" column
    df['Year'], df['Quarter'] = zip(*df['Quarter'].apply(clean_quarter_column))

    # Drop rows with any NaN values after splitting
    df = df.dropna(subset=['Year', 'Quarter', 'CYP total'])

    # Group the data by "Year" and calculate the sum of "CYP total" for each year
    yearly_totals = df.groupby('Year')['CYP total'].sum().reset_index()

    # Rename the column "CYP total" to "Yearly total" in the yearly totals DataFrame
    yearly_totals.rename(columns={'CYP total': 'Yearly total'}, inplace=True)

    # Merge the yearly totals back into the original DataFrame based on the "Year" column
    df = pd.merge(df, yearly_totals, on='Year')

    # For rows with duplicate "Year" values (except the first occurrence), set "Yearly total" to NaN
    df.loc[df.duplicated(subset=['Year'], keep='first'), 'Yearly total'] = np.nan

    # Optionally reset the index for cleanliness
    df.reset_index(drop=True, inplace=True)

    # After processing, save the DataFrame to a CSV file
    output_file = "cleaned_data.csv"  # Save to a temporary directory or any other desired location
    df.to_csv(output_file, index=False)

    # Return the path to the saved CSV file
    return output_file





