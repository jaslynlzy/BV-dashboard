import streamlit as st
import pandas as pd
import plotly.express as px
from millify import millify
import plotly.graph_objects as go
from impact_cleaning import ImpactFormat

st.set_page_config(layout="wide")

# Creating a container for the title of the dashboard
cont1 = st.container()
with cont1:
    st.markdown("<h1 style='text-align: center;'>Child Mortality Dashboard</h1>", unsafe_allow_html=True)
    st.write("")

# Load CSV file
df = st.file_uploader("Choose a file", type=["csv"])
if df is not None:
    df = ImpactFormat(df)
    df = pd.read_csv(df)
    dataframe = df.fillna(0)
    dataframe["Child mortality rate (children under 5 years)\nCHWs+CSB"] = dataframe[
        "Child mortality rate (children under 5 years)\nCHWs+CSB"].str.rstrip('%').astype('float')
    dataframe["Proportion of women giving birth under a skilled attendant\nCSB only"] = dataframe[
        "Proportion of women giving birth under a skilled attendant\nCSB only"].str.rstrip('%').astype('float')
    dataframe["Proportion of women retained in care (HIV treatment)"] = dataframe[
        "Proportion of women retained in care (HIV treatment)"].str.rstrip('%').astype('float')

    with st.sidebar:
        st.title('Yearly CYP Trends Dashboard')
        year_list = sorted(dataframe['Years'].unique(), reverse=True)
        selected_years = st.multiselect('Select years', year_list, default=year_list)
        df_selected_years = dataframe[dataframe['Years'].isin(selected_years)]

    if len(selected_years) == 0:
        st.info('No years selected. Please select a year.')

    elif len(selected_years) == 1:
        recent_year = selected_years[0]
        prev_year_index = year_list.index(recent_year) + 1
        prev_year = year_list[prev_year_index]

        recent_data = dataframe[dataframe['Years'] == recent_year]
        previous_data = dataframe[dataframe['Years'] == prev_year]

        icol_avg = recent_data["Child mortality rate (children under 5 years)\nCHWs+CSB"].mean()
        jcol_avg = recent_data["Number of child deaths (absolute number)\nCHWs+CSB"].mean()
        kcol_avg = recent_data["Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"].mean()
        lcol_avg = recent_data["Proportion of women giving birth under a skilled attendant\nCSB only"].mean()
        mcol_avg = recent_data["Proportion of women retained in care (HIV treatment)"].mean()
        ncol_avg = recent_data["Number of Service Delivery points added/strengthened(Children under five and mother)"].mean()

        icol_avg_delta = icol_avg - previous_data["Child mortality rate (children under 5 years)\nCHWs+CSB"].mean()
        jcol_avg_delta = jcol_avg - previous_data["Number of child deaths (absolute number)\nCHWs+CSB"].mean()
        kcol_avg_delta = kcol_avg - previous_data["Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"].mean()
        lcol_avg_delta = lcol_avg - previous_data["Proportion of women giving birth under a skilled attendant\nCSB only"].mean()
        mcol_avg_delta = mcol_avg - previous_data["Proportion of women retained in care (HIV treatment)"].mean()
        ncol_avg_delta = ncol_avg - previous_data["Number of Service Delivery points added/strengthened(Children under five and mother)"].mean()

        jcol_totals = recent_data["Number of child deaths (absolute number)\nCHWs+CSB"].sum()
        ncol_totals = recent_data["Number of Service Delivery points added/strengthened(Children under five and mother)"].sum()

        jcol_tot_delta = jcol_totals - previous_data["Number of child deaths (absolute number)\nCHWs+CSB"].sum()
        ncol_tot_delta = ncol_totals - previous_data["Number of Service Delivery points added/strengthened(Children under five and mother)"].sum()

        cont2 = st.container()
        with cont2:
            st.markdown("<h2 style='text-align: center;'>CSB Only</h2>", unsafe_allow_html=True)
            st.write("")

        cont3 = st.container()
        with cont3:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Avg. rate of HIV +ve mothers", value=f"{kcol_avg: .2f}%",
                           delta=f"{kcol_avg_delta: .2f}%", delta_color = "inverse")
                fig = px.pie(values=[kcol_avg, (100 - kcol_avg)], names=["Prevalent", "Not Prevalent"], color_discrete_sequence=px.colors.sequential.dense)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.metric(label="Avg. Prop. of births under a skilled attendant", value=f"{lcol_avg: .2f}%",
                           delta=f"{lcol_avg_delta: .2f}%")
                fig = px.pie(values=[lcol_avg, (100 - lcol_avg)], names=["Prevalent", "Not Prevalent"], color_discrete_sequence=px.colors.sequential.dense)
                st.plotly_chart(fig, use_container_width=True)

        cont4 = st.container()
        with cont4:
            st.markdown("<h2 style='text-align: center;'>CSB and CHWs</h2>", unsafe_allow_html=True)
            st.write("")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Avg. Child Mortality rate", value=f"{icol_avg: .2f}%",
                           delta=f"{icol_avg_delta: .2f}%", delta_color = "inverse")

            with col2:
                st.metric(label="Total Num. of Child Deaths", value=millify(jcol_totals, precision=2),
                           delta=millify(jcol_tot_delta, precision=2), delta_color = "inverse")

            with col3:
                st.metric(label="Avg. Numb. of Child Deaths", value=millify(jcol_avg, precision=2),
                           delta=millify(jcol_avg_delta, precision=2), delta_color = "inverse")

        cont5 = st.container()
        with cont5:
            st.markdown("<h2 style='text-align: center;'>Others</h2>", unsafe_allow_html=True)
            st.write("")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Avg. Prop. of Women in HIV care", value=f"{mcol_avg: .2f}%",
                           delta=f"{mcol_avg_delta: .2f}%")

            with col2:
                st.metric(label="Total Numb. of service delivery points added/strengthened", value=millify(ncol_totals, precision=2),
                           delta=millify(ncol_tot_delta, precision=2))

            with col3:
                st.metric(label="Avg. Numb. of service delivery points added/strengthened", value=millify(ncol_avg, precision=2),
                           delta=millify(ncol_avg_delta, precision=2))

    else:
        recent_year = max(selected_years)
        prev_year = max(year for year in selected_years if year < recent_year)

        recent_data = dataframe[dataframe['Years'] == recent_year]
        previous_data = dataframe[dataframe['Years'] == prev_year]

        icol_avg = recent_data["Child mortality rate (children under 5 years)\nCHWs+CSB"].mean()
        jcol_avg = recent_data["Number of child deaths (absolute number)\nCHWs+CSB"].mean()
        kcol_avg = recent_data["Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"].mean()
        lcol_avg = recent_data["Proportion of women giving birth under a skilled attendant\nCSB only"].mean()
        mcol_avg = recent_data["Proportion of women retained in care (HIV treatment)"].mean()
        ncol_avg = recent_data[
            "Number of Service Delivery points added/strengthened(Children under five and mother)"].mean()

        icol_avg_delta = icol_avg - previous_data["Child mortality rate (children under 5 years)\nCHWs+CSB"].mean()
        jcol_avg_delta = jcol_avg - previous_data["Number of child deaths (absolute number)\nCHWs+CSB"].mean()
        kcol_avg_delta = kcol_avg - previous_data[
            "Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"].mean()
        lcol_avg_delta = lcol_avg - previous_data[
            "Proportion of women giving birth under a skilled attendant\nCSB only"].mean()
        mcol_avg_delta = mcol_avg - previous_data["Proportion of women retained in care (HIV treatment)"].mean()
        ncol_avg_delta = ncol_avg - previous_data[
            "Number of Service Delivery points added/strengthened(Children under five and mother)"].mean()

        jcol_totals = recent_data["Number of child deaths (absolute number)\nCHWs+CSB"].sum()
        ncol_totals = recent_data[
            "Number of Service Delivery points added/strengthened(Children under five and mother)"].sum()

        jcol_tot_delta = jcol_totals - previous_data["Number of child deaths (absolute number)\nCHWs+CSB"].sum()
        ncol_tot_delta = ncol_totals - previous_data[
            "Number of Service Delivery points added/strengthened(Children under five and mother)"].sum()

        cont2 = st.container()
        with cont2:
            st.markdown("<h2 style='text-align: center;'>CSB Only</h2>", unsafe_allow_html=True)
            st.write("")

        cont3 = st.container()
        with cont3:
            st.subheader("Yearly Average Prevalence of HIV among children whose mothers are HIV+ve")
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(values=[kcol_avg, (100 - kcol_avg)], names=["Prevalent", "Not Prevalent"],
                             color_discrete_sequence=px.colors.sequential.dense)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                yearly_average = []
                for year in selected_years:
                    avg = df_selected_years[df_selected_years["Years"] == year][
                        "Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"].mean()
                    yearly_average.append(avg)

                # Create a DataFrame for plotting
                plot_df = pd.DataFrame({
                    "Years": selected_years,
                    "Yearly Average (%)": yearly_average
                })

                # Sort DataFrame by Years
                plot_df.sort_values(by="Years", inplace=True)

                # Plot the data
                fig = px.bar(plot_df, x="Years", y="Yearly Average (%)")

                fig.update_layout(
                    height=275  # Set a specific height in pixels
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig)
                st.metric(label="Avg. rate of HIV +ve mothers", value=f"{kcol_avg: .2f}%",
                          delta=f"{kcol_avg_delta: .2f}%", delta_color="inverse")


        cont4 = st.container()
        with cont4:
            st.subheader("Yearly Average Prop. of women giving birth under a skilled attendant")
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(values=[lcol_avg, (100 - lcol_avg)], names=["Prevalent", "Not Prevalent"],
                             color_discrete_sequence=px.colors.sequential.dense)
                st.plotly_chart(fig, use_container_width=True)

                with col2:
                    yearly_average = []
                    for year in selected_years:
                        avg = df_selected_years[df_selected_years["Years"] == year][
                            "Proportion of women giving birth under a skilled attendant\nCSB only"].mean()
                        yearly_average.append(avg)

                    # Create a DataFrame for plotting
                    plot_df = pd.DataFrame({
                        "Years": selected_years,
                        "Yearly Average (%)": yearly_average
                    })

                    # Sort DataFrame by Years
                    plot_df.sort_values(by="Years", inplace=True)

                    # Plot the data
                    fig = px.bar(plot_df, x="Years", y="Yearly Average (%)")

                    fig.update_layout(
                        height=275  # Set a specific height in pixels
                    )

                    # Display the plot in Streamlit
                    st.plotly_chart(fig)

                    st.metric(label=f"{recent_year} Average", value=f"{lcol_avg: .2f}%",
                              delta=f"{lcol_avg_delta: .2f}%")

        cont5 = st.container()
        with cont5:
            st.markdown("<h2 style='text-align: center;'>CSB and CHWs</h2>", unsafe_allow_html=True)
            st.write("")

            col1, col2 = st.columns(2)
            with col1:
                yearly_average = []
                for year in selected_years:
                    avg = df_selected_years[df_selected_years["Years"] == year][
                        "Child mortality rate (children under 5 years)\nCHWs+CSB"].mean()
                    yearly_average.append(avg)

                # Create a DataFrame for plotting
                plot_df = pd.DataFrame({
                    "Years": selected_years,
                    "Yearly Average (%)": yearly_average
                })

                # Sort DataFrame by Years
                plot_df.sort_values(by="Years", inplace=True)

                # Plot the data
                fig = px.bar(plot_df, x="Years", y="Yearly Average (%)", title="Child mortality rate (children under 5 years)")

                # Display the plot in Streamlit
                st.plotly_chart(fig)

            with col2:
                yearly_average = []
                for year in selected_years:
                    avg = df_selected_years[df_selected_years["Years"] == year][
                        "Number of child deaths (absolute number)\nCHWs+CSB"].mean()
                    yearly_average.append(avg)

                yearly_total = []
                for year in selected_years:
                    totals = df_selected_years[df_selected_years["Years"] == year][
                        "Number of child deaths (absolute number)\nCHWs+CSB"
                    ].sum()
                    yearly_total.append(totals)

                # Create a DataFrame for plotting
                combined_df = pd.DataFrame({
                    "Years": selected_years,
                    "Yearly Average": yearly_average,
                    "Yearly Total": yearly_total
                })

                # Sort DataFrame by Years
                combined_df.sort_values(by="Years", inplace=True)

                # Plot the data on the same graph
                fig = go.Figure()

                # Add trace for Couple Years Protection (CYP) CSB
                fig.add_trace(go.Scatter(x=combined_df["Years"], y=combined_df["Yearly Average"], mode='lines+markers',
                                         name='Yearly Average'))

                # Add trace for Population reached with improved access to health services
                fig.add_trace(
                    go.Scatter(x=combined_df["Years"], y=combined_df["Yearly Total"], mode='lines+markers',
                               name='Yearly Total'))

                # Customize layout
                fig.update_layout(
                    title="Number of child deaths",
                    xaxis_title="Years",
                    yaxis_title="Number of child deaths",
                    legend_title="Metrics",
                    hovermode="x unified",
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig, use_container_width=True)

        cont6 = st.container()
        with cont6:
            st.markdown("<h2 style='text-align: center;'>Others</h2>", unsafe_allow_html=True)
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                yearly_average = []
                for year in selected_years:
                    avg = df_selected_years[df_selected_years["Years"] == year][
                        "Proportion of women retained in care (HIV treatment)"].mean()
                    yearly_average.append(avg)

                # Create a DataFrame for plotting
                plot_df = pd.DataFrame({
                    "Years": selected_years,
                    "Yearly Average (%)": yearly_average
                })

                # Sort DataFrame by Years
                plot_df.sort_values(by="Years", inplace=True)

                # Plot the data
                fig = px.bar(plot_df, x="Years", y="Yearly Average (%)", title = "Avg. Prop. of women retained in care (HIV treatment)")

                # Display the plot in Streamlit
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                yearly_average = []
                for year in selected_years:
                    avg = df_selected_years[df_selected_years["Years"] == year][
                        "Number of Service Delivery points added/strengthened(Children under five and mother)"
                    ].mean()
                    yearly_average.append(avg)

                yearly_totals = []
                for year in selected_years:
                    totals = df_selected_years[df_selected_years["Years"] == year][
                        "Number of Service Delivery points added/strengthened(Children under five and mother)"
                    ].sum()
                    yearly_totals.append(totals)

                combined_df = pd.DataFrame({
                    "Years": selected_years,
                    "Yearly Average (%)": yearly_average,
                    "Yearly Totals": yearly_totals
                })

                # Sort DataFrame by Years
                combined_df.sort_values(by="Years", inplace=True)

                # Plot the data on the same graph
                fig = go.Figure()

                # Add trace for Couple Years Protection (CYP) CSB
                fig.add_trace(go.Scatter(x=combined_df["Years"], y=combined_df["Yearly Average (%)"],
                                         mode='lines+markers',
                                         name='Yearly Average (%)'))

                # Add trace for Population reached with improved access to health services
                fig.add_trace(
                    go.Scatter(x=combined_df["Years"], y=combined_df["Yearly Totals"],
                               mode='lines+markers',
                               name='Yearly Total'))

                # Customize layout
                fig.update_layout(
                    title="Number of Service Delivery points added/strengthened (Children under five and mother)",
                    xaxis_title="Years",
                    yaxis_title="Number of Service Delivery points added/strengthened",
                    legend_title="Metrics",
                    hovermode="x unified",
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig, use_container_width=True)














else:
    st.info("Please upload a CSV file.")
