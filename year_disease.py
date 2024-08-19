import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from millify import millify
import plotly.graph_objects as go
import numpy as np
from outcome_cleaning import OutcomesSave

st.set_page_config(layout="wide")

# Creating a container for the title of the dashboard
cont1 = st.container()
with cont1:
    st.markdown("<h1 style='text-align: center;'>Diseases Dashboard</h1>", unsafe_allow_html=True)
    st.write("")

# Load CSV file
df = st.file_uploader("Choose a file", type=["csv"])
if df is not None:
    df = OutcomesSave(df)
    dataframe_old = pd.read_csv(df)
    dataframe = dataframe_old.fillna(0)
    dataframe['Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level'] = dataframe['Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level'].str.rstrip('%').astype('float')
    dataframe['Proportion of children under five years receiving appropriate treatment for diarrhea'] = dataframe[
        'Proportion of children under five years receiving appropriate treatment for diarrhea'].str.rstrip('%').astype(
        'float')
    dataframe['Proportion of children under five years receiving appropriate treatment for malaria'] = dataframe[
        'Proportion of children under five years receiving appropriate treatment for malaria'].str.rstrip('%').astype(
        'float')
    dataframe['Proportion of children under five years receiving appropriate treatment for pneumonia'] = dataframe[
        'Proportion of children under five years receiving appropriate treatment for pneumonia'].str.rstrip('%').astype(
        'float')

    # Include options to choose years on sidebar
    with st.sidebar:
        st.title('Yearly CYP Trends Dashboard')
        year_list = sorted(dataframe['Years'].unique(), reverse=True)
        selected_years = st.multiselect('Select years', year_list, default=year_list)
        df_selected_years = dataframe[dataframe['Years'].isin(selected_years)]

    if len(selected_years) == 0:
        st.info('No years selected. Please select a year.')

    elif len(selected_years) == 1:
        recent_year = max(selected_years)
        prev_year = year_list[selected_years.index(recent_year) + 1]

        recent_data = dataframe[dataframe['Years'] == recent_year]
        previous_data = dataframe[dataframe['Years'] == prev_year]

        avg_fcol = recent_data['Couple Years Protection (CYP)CSB'].mean()
        avg_kcol = recent_data['Number of Population reached with improved access to health services'].mean()

        avg_delta_fcol = avg_fcol - previous_data['Couple Years Protection (CYP)CSB'].mean()
        avg_delta_kcol = avg_kcol - previous_data['Number of Population reached with improved access to health services'].mean()

        fcol_total = df_selected_years["Couple Years Protection (CYP)CSB"].sum()
        kcol_total = df_selected_years["Number of Population reached with improved access to health services"].sum()

        delta_fcol_total = fcol_total - previous_data['Couple Years Protection (CYP)CSB'].sum()
        delta_kcol_total = kcol_total - previous_data['Number of Population reached with improved access to health services'].sum()

        cont2 = st.container()
        with cont2:
            st.header("CYP CSB and Improved Healthcare Access")
            st.subheader(f"Average and Totals in {recent_year}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label=f"Avg. CYP CSB ({recent_year})",
                          value=millify(avg_fcol, precision=2),
                          delta=millify(avg_delta_fcol, precision=2))
                st.metric(label=f"Total CYP CSB ({recent_year})",
                          value=millify(fcol_total, precision=2),
                          delta=millify(delta_fcol_total, precision=2))

                style_metric_cards(border_left_color="#050C9C")

            with col2:
                st.metric(label=f"Avg. Pop. with Improved Healthcare Access ({recent_year})",
                          value=millify(avg_kcol, precision=2),
                          delta=millify(avg_delta_kcol, precision=2))
                st.metric(label=f"Total Pop. with Improved Healthcare Access ({recent_year})",
                          value=millify(kcol_total, precision=2),
                          delta=millify(delta_kcol_total, precision=2))

                style_metric_cards(border_left_color="#3ABEF9")

            with col3:
                # Create a bar chart using Plotly
                fig = go.Figure(data=[
                    go.Bar(name="CYP CSB", x=["Total", "Average"], y=[fcol_total, avg_fcol]),
                    go.Bar(name="Improved Healthcare Access", x=["Total", "Average"], y=[kcol_total, avg_kcol])
                ])

                fig.update_layout(
                    title="Totals and Averages",
                    legend_title="Metrics",
                    barmode='group'  # Group bars next to each other
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig, use_container_width=True)

        cont3 = st.container()
        with cont3:
            st.header("Proportions Trends")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                mean_value = df_selected_years["Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_gcol = mean_value - previous_data['Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level'].mean()

                min_value = df_selected_years["Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].min()
                max_value = df_selected_years["Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].max()

                st.metric(label=f"Average Proportion Neonatal Death ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_gcol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average Proportion of Neonatal Death"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#050C9C"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

            with col2:
                mean_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for diarrhea"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_hcol = mean_value - previous_data['Proportion of children under five years receiving appropriate treatment for diarrhea'].mean()

                min_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for diarrhea"].min()
                max_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for diarrhea"].max()

                st.metric(label=f"Average Proportions receiving treatment for diarrhea ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_hcol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average Proportion of children receiving treatment for Diarrhea"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#3572EF"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

            with col3:
                mean_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for malaria"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_icol = mean_value - previous_data['Proportion of children under five years receiving appropriate treatment for malaria'].mean()

                min_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for malaria"].min()
                max_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for malaria"].max()

                st.metric(label=f"Average Proportions receiving treatment for malaria ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_icol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average Proportion of children receiving treatment for Malaria"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#3ABEF9"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

            with col4:
                mean_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for pneumonia"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_jcol = mean_value - previous_data['Proportion of children under five years receiving appropriate treatment for pneumonia'].mean()

                min_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for pneumonia"].min()
                max_value = df_selected_years["Proportion of children under five years receiving appropriate treatment for pneumonia"].max()

                st.metric(label=f"Average Proportions receiving treatment for pneumonia ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_jcol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average Proportion of children receiving treatment for Pneumonia"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#A7E6FF"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

        cont4 = st.container()
        with cont4:
            st.subheader("Total Proportions")

            gcol_total = df_selected_years["Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].sum()
            hcol_total = df_selected_years["Proportion of children under five years receiving appropriate treatment for diarrhea"].sum()
            icol_total = df_selected_years["Proportion of children under five years receiving appropriate treatment for malaria"].sum()
            jcol_total = df_selected_years["Proportion of children under five years receiving appropriate treatment for pneumonia"].sum()

            fig = go.Figure(data=[
                go.Bar(name="Proportions", x=["Neonatal Death", "Diarrhea Treatment", "Malaria Treatment", "Pneumonia Treatment"],
                      y=[gcol_total, hcol_total, icol_total, jcol_total])
            ])

            fig.update_layout(
                title="Total Proportions",
                legend_title="Metrics"
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        recent_year = max(selected_years)
        prev_year = max(year for year in selected_years if year < recent_year)

        recent_data = dataframe[dataframe['Years'] == recent_year]
        previous_data = dataframe[dataframe['Years'] == prev_year]

        avg_fcol = recent_data['Couple Years Protection (CYP)CSB'].mean()
        avg_kcol = recent_data['Number of Population reached with improved access to health services'].mean()

        avg_delta_fcol = avg_fcol - previous_data['Couple Years Protection (CYP)CSB'].mean()
        avg_delta_kcol = avg_kcol - previous_data[
            'Number of Population reached with improved access to health services'].mean()

        fcol_total = df_selected_years["Couple Years Protection (CYP)CSB"].sum()
        kcol_total = df_selected_years["Number of Population reached with improved access to health services"].sum()

        delta_fcol_total = fcol_total - previous_data['Couple Years Protection (CYP)CSB'].sum()
        delta_kcol_total = kcol_total - previous_data[
            'Number of Population reached with improved access to health services'].sum()

        cont2 = st.container()
        with cont2:
            st.header("CYP CSB and Improved Healthcare Access")
            st.subheader(f"Average and Totals in {recent_year}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label=f"Avg. CYP CSB ({recent_year})",
                          value=millify(avg_fcol, precision=2),
                          delta=millify(avg_delta_fcol, precision=2))
                st.metric(label=f"Total CYP CSB ({recent_year})",
                          value=millify(fcol_total, precision=2),
                          delta=millify(delta_fcol_total, precision=2))

                style_metric_cards(border_left_color="#050C9C")

            with col2:
                st.metric(label=f"Avg. Pop. with Improved Healthcare Access ({recent_year})",
                          value=millify(avg_kcol, precision=2),
                          delta=millify(avg_delta_kcol, precision=2))
                st.metric(label=f"Total Pop. with Improved Healthcare Access ({recent_year})",
                          value=millify(kcol_total, precision=2),
                          delta=millify(delta_kcol_total, precision=2))

                style_metric_cards(border_left_color="#3ABEF9")

        cont3 = st.container()
        with cont3:
            col1, col2 = st.columns(2)
            with col1:
                csb_totals = []
                for year in selected_years:
                    csb_yearly_total = df_selected_years[df_selected_years["Years"] == year][
                        "Couple Years Protection (CYP)CSB"].sum()
                    csb_totals.append(csb_yearly_total)

                health_totals = []
                for year in selected_years:
                    health_yearly_total = df_selected_years[df_selected_years["Years"] == year][
                        "Number of Population reached with improved access to health services"].sum()
                    health_totals.append(health_yearly_total)

                # Create a combined DataFrame for plotting
                combined_df = pd.DataFrame({
                    "Years": selected_years,
                    "CYP Totals": csb_totals,
                    "Health Access Totals": health_totals
                })

                # Sort DataFrame by Years
                combined_df.sort_values(by="Years", inplace=True)

                # Plot the data on the same graph
                fig = go.Figure()

                # Add trace for Couple Years Protection (CYP) CSB
                fig.add_trace(go.Scatter(x=combined_df["Years"], y=combined_df["CYP Totals"], mode='lines+markers',
                                         name='CYP Totals'))

                # Add trace for Population reached with improved access to health services
                fig.add_trace(
                    go.Scatter(x=combined_df["Years"], y=combined_df["Health Access Totals"], mode='lines+markers',
                               name='Health Access Totals'))

                # Customize layout
                fig.update_layout(
                    title="Yearly Totals",
                    xaxis_title="Years",
                    yaxis_title="Totals",
                    legend_title="Metrics",
                    hovermode="x unified",
                    height = 500
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                yearly_average = []
                for year in selected_years:
                    avg = df_selected_years[df_selected_years["Years"] == year][
                        "Couple Years Protection (CYP)CSB"].mean()
                    yearly_average.append(avg)

                # Create a DataFrame for plotting
                plot_df = pd.DataFrame({
                    "Years": selected_years,
                    "Yearly Average": yearly_average
                })

                # Sort DataFrame by Years
                plot_df.sort_values(by="Years", inplace=True)

                # Plot the data
                fig = px.line(plot_df, x="Years", y="Yearly Average",
                              title="Yearly Average Couple Years Protection (CYP)CSB")

                fig.update_layout(
                    height=250  # Set a specific height in pixels
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig)

                yearly_average2 = []
                for year in selected_years:
                    avg2 = df_selected_years[df_selected_years["Years"] == year][
                        "Number of Population reached with improved access to health services"].mean()
                    yearly_average2.append(avg2)

                # Create a DataFrame for plotting
                plot_df2 = pd.DataFrame({
                    "Years": selected_years,
                    "Yearly Average": yearly_average2
                })

                # Sort DataFrame by Years
                plot_df2.sort_values(by="Years", inplace=True)

                # Plot the data
                fig2 = px.line(plot_df2, x="Years", y="Yearly Average",
                              title="Yearly Average of Population Reached with Improved Access to Health Services")

                fig2.update_layout(
                    height=250  # Set a specific height in pixels
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig2)

        cont4 = st.container()
        with cont4:
            st.header("Proportion Totals and Averages")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                mean_value = df_selected_years[
                    "Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_gcol = mean_value - previous_data[
                    'Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level'].mean()

                min_value = df_selected_years[
                    "Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].min()
                max_value = df_selected_years[
                    "Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].max()

                st.metric(label=f"Average Neonatal Death ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_gcol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average Neonatal Death"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#050C9C"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

            with col2:
                mean_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for diarrhea"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_hcol = mean_value - previous_data[
                    'Proportion of children under five years receiving appropriate treatment for diarrhea'].mean()

                min_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for diarrhea"].min()
                max_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for diarrhea"].max()

                st.metric(label=f"Average treated diarrhea ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_hcol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average treated Diarrhea"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#3572EF"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

            with col3:
                mean_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for malaria"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_icol = mean_value - previous_data[
                    'Proportion of children under five years receiving appropriate treatment for malaria'].mean()

                min_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for malaria"].min()
                max_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for malaria"].max()

                st.metric(label=f"Average treated Malaria ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_icol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average treated Malaria"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#3ABEF9"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

            with col4:
                mean_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for pneumonia"].mean()
                formatted_value = millify(int(np.round(mean_value)), precision=2)
                avg_delta_jcol = mean_value - previous_data[
                    'Proportion of children under five years receiving appropriate treatment for pneumonia'].mean()

                min_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for pneumonia"].min()
                max_value = df_selected_years[
                    "Proportion of children under five years receiving appropriate treatment for pneumonia"].max()

                st.metric(label=f"Average treated pneumonia ({formatted_value})",
                          value=millify(mean_value, precision=2) + "%",
                          delta=millify(avg_delta_jcol, precision=2))

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=mean_value,
                    title={"text": "Average treated Pneumonia"},
                    gauge={
                        "axis": {"range": [min_value, max_value]},
                        "bar": {"color": "#A7E6FF"},
                        "steps": [
                            {"range": [min_value, mean_value], "color": "#e6f5ff"},
                            {"range": [mean_value, max_value], "color": "#cceeff"}
                        ]
                    },
                    number={"suffix": "%"}
                ))

                fig.update_layout(
                    width=250,  # Set width
                    height=250,  # Set height
                    margin=dict(l=20, r=20, t=50, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)

        cont5 = st.container()
        with cont5:
            gcol_totals = []
            for year in selected_years:
                total = df_selected_years[df_selected_years["Years"] == year][
                    "Proportion Neonatal Death ( 0-28 days) in local health system (CSB+Villages) level"].sum()
                gcol_totals.append(total)

            gcol_total_df = pd.DataFrame({
                "Years": selected_years,
                "Neonatal Deaths": gcol_totals
            })

            hcol_totals = []
            for year in selected_years:
                total = df_selected_years[df_selected_years["Years"] == year][
                    "Proportion of children under five years receiving appropriate treatment for diarrhea"].sum()
                hcol_totals.append(total)

            hcol_total_df = pd.DataFrame({
                "Years": selected_years,
                "Treated for Diarrhea": hcol_totals
            })

            icol_totals = []
            for year in selected_years:
                total = df_selected_years[df_selected_years["Years"] == year][
                    "Proportion of children under five years receiving appropriate treatment for malaria"].sum()
                icol_totals.append(total)

            icol_total_df = pd.DataFrame({
                "Years": selected_years,
                "Treated for Malaria": icol_totals
            })

            jcol_totals = []
            for year in selected_years:
                total = df_selected_years[df_selected_years["Years"] == year][
                    "Proportion of children under five years receiving appropriate treatment for pneumonia"].sum()
                jcol_totals.append(total)

            jcol_total_df = pd.DataFrame({
                "Years": selected_years,
                "Treated for Pneumonia": jcol_totals
            })

            # Sort DataFrame by Years
            plot_df.sort_values(by="Years", inplace=True)

            # Combine data for grouped bar chart
            combined_totals_df = pd.DataFrame({
                "Years": selected_years,
                "Neonatal Deaths": gcol_totals,
                "Treated for Diarrhea": hcol_totals,
                "Treated for Malaria": icol_totals,
                "Treated for Pneumonia": jcol_totals
            })

            # Melt the DataFrame to long format
            melted_df = combined_totals_df.melt(id_vars=["Years"], var_name="Metrics", value_name="Values")

            # Create grouped bar chart
            fig3 = px.bar(melted_df, x="Years", y="Values", color="Metrics", barmode="group",
                          title="Grouped Bar Chart of Yearly Totals for Various Proportions",
                          color_discrete_sequence=["#050C9C", "#3572EF", "#3ABEF9", "#A7E6FF"])

            # Display the grouped bar chart
            st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Please upload a CSV file.")
