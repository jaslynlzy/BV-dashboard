#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

# Load the CSV file, skipping the first two rows and treating "NaN" as missing values
df = pd.read_csv("CYP DASHBOARD updated 10_07_2023 - CYP_CSB(in).csv", skiprows=2, na_values="NaN")

# Forward fill the 'Date - Year' column where there are NaN values to carry the last valid value forward
df['Date - Year'] = df['Date - Year'].fillna(method='ffill')

# Drop any rows that still contain NaN values after forward filling
df = df.dropna()

# Group the data by 'Date - Year' and sum the 'SUM of CYP_Oral' values for each year
oral_totals = df.groupby("Date - Year")["SUM of CYP_Oral"].sum().reset_index()
# Rename the 'SUM of CYP_Oral' column to 'Yearly Oral total' for clarity
oral_totals.rename(columns={"SUM of CYP_Oral": "Yearly Oral total"}, inplace=True)

# Merge the yearly oral totals back into the original DataFrame
df = pd.merge(df, oral_totals, on="Date - Year")

# For rows with duplicate 'Date - Year' values (except the first occurrence), set 'Yearly Oral total' to NaN
df.loc[df.duplicated(subset=['Date - Year']), 'Yearly Oral total'] = np.nan

# Repeat the same process for 'SUM of CYP_Injection'
injection_totals = df.groupby("Date - Year")["SUM of CYP_Injection"].sum().reset_index()
injection_totals.rename(columns={"SUM of CYP_Injection": "Yearly Injection total"}, inplace=True)
df = pd.merge(df, injection_totals, on="Date - Year")
df.loc[df.duplicated(subset=['Date - Year']), 'Yearly Injection total'] = np.nan

# Repeat the same process for 'SUM of CYP_Implanon'
implanon_totals = df.groupby("Date - Year")["SUM of CYP_Implanon"].sum().reset_index()
implanon_totals.rename(columns={"SUM of CYP_Implanon": "Yearly Implanon total"}, inplace=True)
df = pd.merge(df, implanon_totals, on="Date - Year")
df.loc[df.duplicated(subset=['Date - Year']), 'Yearly Implanon total'] = np.nan

# Repeat the same process for 'SUM of CYP_IUD'
iud_totals = df.groupby("Date - Year")["SUM of CYP_IUD"].sum().reset_index()
iud_totals.rename(columns={"SUM of CYP_IUD": "Yearly IUD total"}, inplace=True)
df = pd.merge(df, iud_totals, on="Date - Year")
df.loc[df.duplicated(subset=['Date - Year']), 'Yearly IUD total'] = np.nan

# Group the data by 'Date - Year' and calculate the sum of 'SUM of CYP_Total' for each year
yearly_totals = df.groupby("Date - Year")["SUM of CYP_Total"].sum().reset_index()
# Rename the column 'SUM of CYP_Total' to 'Yearly total' for clarity
yearly_totals.rename(columns={"SUM of CYP_Total": "Yearly total"}, inplace=True)

# Merge the yearly totals back into the original DataFrame based on the 'Date - Year' column
df = pd.merge(df, yearly_totals, on="Date - Year")

# For rows with duplicate 'Date - Year' values (except the first occurrence), set 'Yearly total' to NaN
df.loc[df.duplicated(subset=['Date - Year']), 'Yearly total'] = np.nan

# Export the final DataFrame to a new CSV file
df.to_csv("processed_CYP_data.csv", index=False)

# Display the final DataFrame
df

