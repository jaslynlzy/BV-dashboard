import streamlit as st
import pandas as pd
from DataCleaning import data_cleaning
import plotly.express as px

st.set_page_config(layout="wide")

def visualise(data):
    st.sidebar.title("Visualization Options")
    option = st.sidebar.selectbox("Select Indicator level", ["Impacts", "Outcomes"])

    indicators = data[data["Indicator Level"].str.contains(r'(?i).*' + option + r'.*', na=False)]['Indicator and Definition'].unique()

    if indicators.size > 0:
        selected_category = st.sidebar.selectbox("Select Indicator", indicators)
        filtered_data = data[data['Indicator and Definition'] == selected_category]

        if not filtered_data.empty:
            st.write(f"### {selected_category}")
            target_value = filtered_data["Overall Target"].iloc[0]
            baseline_value = filtered_data["Baseline Value"].iloc[0]

            # Bar Chart
            long_data = filtered_data.melt(id_vars='Year', value_vars=['Actual', 'Target', 'Overall Target'],
                                           var_name='Type', value_name='Value')

            color_map = {'Actual': 'darkblue', 'Target': 'blueviolet', 'Overall Target': 'cornflowerblue'}
            fig_bar = px.bar(long_data, x='Year', y='Value', color='Type', color_discrete_map=color_map,
                             labels={'Value': 'Value', 'Year': 'Year'},
                             title="Indicator Performance Over Time (Bar Chart)")
            fig_bar.update_layout(barmode='group', legend_title='Performance Type')
            st.plotly_chart(fig_bar)

            # Line Chart
            fig_line = px.line(filtered_data, x='Year', y='Actual',
                               labels={'Actual': 'Actual Value', 'Year': 'Year'},
                               title='Actual Performance Over Time')
            fig_line.update_traces(mode='lines+markers', line=dict(color='darkblue', width=2),
                                   marker=dict(size=8))
            fig_line.add_shape(type='line', x0=filtered_data['Year'].min(), x1=filtered_data['Year'].max(),
                               y0=target_value, y1=target_value, line=dict(color='cornflowerblue', width=2, dash='dash'))
            fig_line.add_shape(type='line', x0=filtered_data['Year'].min(), x1=filtered_data['Year'].max(),
                               y0=baseline_value, y1=baseline_value, line=dict(color='green', width=2, dash='dot'))
            fig_line.add_annotation(x=filtered_data['Year'].max(), y=target_value, text='Overall Target',
                                    showarrow=False, yshift=10, font=dict(color='cornflowerblue', size=12))
            fig_line.add_annotation(x=filtered_data['Year'].max(), y=baseline_value, text='Baseline Value',
                                    showarrow=False, yshift=10, font=dict(color='green', size=12))
            st.plotly_chart(fig_line)

            #Box Plot (Distribution of Values)
            fig_box = px.box(long_data, x='Type', y='Value', color='Type', title="Distribution of Performance Values",
                             labels={'Value': 'Value', 'Type': 'Performance Type'})
            fig_box.update_traces(marker=dict(size=10))
            st.plotly_chart(fig_box)

        else:
            st.write("No data available for the selected indicator.")
    else:
        st.write("No indicators found for the selected level.")
    #if not filtered_data.empty:

st.title("Indicator Performance Dashboard")
uploaded_files = st.file_uploader("Upload CSV files", accept_multiple_files=True)
combined_data = pd.DataFrame()

if uploaded_files:
    for uploaded_file in uploaded_files:
        data = data_cleaning(uploaded_file)
        if not data.empty:
            combined_data = pd.concat([combined_data, data], ignore_index=True)

    if not combined_data.empty:
        visualise(combined_data)
    else:
        st.write("No data available for visualization.")
else:
    st.write("Please upload CSV files to proceed.")