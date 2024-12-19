import streamlit as st
import pandas as pd
import plotly.express as px
import requests  # Import the requests library


# Path to the data file relative to the app.py file
DATA_PATH = "https://huggingface.co/spaces/danielrosehill/Monetised-GHG-Emissions-Calculator/raw/main/calculator-app/data.csv"
INSTRUCTIONS_PATH = "https://huggingface.co/spaces/danielrosehill/Monetised-GHG-Emissions-Calculator/raw/main/calculator-app/instructions.md"

GITHUB_LINK = "https://github.com/danielrosehill/Emissions-Monetisation-Calculator"


def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        st.error(
            f"Error: Could not find the data file at {DATA_PATH}. Please ensure the file exists."
        )
        return None


def load_instructions():
    try:
        response = requests.get(INSTRUCTIONS_PATH)  # Fetch the content of the URL
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text  # return the text of the response
    except requests.exceptions.RequestException as e:
        return f"Error: Could not fetch instructions file: {e}"


def format_currency(value, display_unit):
    if display_unit == "Millions":
        formatted_value = f"${value / 1_000_000:.2f} MN"
    elif display_unit == "Billions":
        formatted_value = f"${value / 1_000_000_000:.2f} BN"
    return formatted_value


def main():
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        border: 1px solid #e6e6e6;
        border-radius: 5px;
        padding: 1em;
        margin-bottom: 1em;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("GHG Emissions Monetization Calculator")
    st.markdown(
        "This tool explores the potential financial implications of proposed greenhouse gas emissions costs. It accompanies a repository on Github and Hugging Face that aggregates proposals for the social cost of carbon."
    )
    st.markdown(
        "The social cost of carbon represents the economic damages associated with emitting one additional ton of carbon dioxide into the atmosphere."
    )
    st.markdown(
        "Detailed notes and instructions about the use of this calculator can be found in the Instructions tab."
    )
    st.markdown(
        "This calculator was developed by Daniel Rosehill in December 2024 (danielrosehill.com)."
    )


    # Load the data and instructions
    df = load_data()
    instructions = load_instructions()
    if df is None:
        return  # Don't proceed if data can't be loaded

    # Tabs for calculator, instructions and SCC proposals
    tabs = st.tabs(["Calculator", "Instructions", "SCC Chart", "SCC Details", "Data"])

    with tabs[0]:  # Calculator tab
        with st.container():
            st.markdown("### Input your emissions and proposal of interest")
            left, right = st.columns(2)

            with left:
                st.subheader("Input Values")
                st.markdown("Enter your company's greenhouse gas emissions:")
                scope1_emissions = st.number_input("Scope 1 Emissions", value=0.0)
                st.markdown("*(Direct emissions from owned or controlled sources)*")
                scope2_emissions = st.number_input("Scope 2 Emissions", value=0.0)
                st.markdown("*(Indirect emissions from the generation of purchased energy)*")
                scope3_emissions = st.number_input("Scope 3 Emissions", value=0.0)
                st.markdown("*(All other indirect emissions that occur in a company's value chain)*")
                unit_of_reporting = st.selectbox("Unit of Reporting", ["TCO2E", "MTCO2E"])
                proposal_names = df['proposal_with_date'].tolist()
                selected_proposal = st.selectbox("Social cost of carbon proposal", proposal_names)
                calculate_button = st.button("Calculate Monetized Emissions")
                
            with right:
                st.subheader("Calculated Values")
                if calculate_button:
                # Calculated emissions
                    scope1_2_emissions = scope1_emissions + scope2_emissions
                    all_scopes_emissions = (
                        scope1_emissions + scope2_emissions + scope3_emissions
                    )
                    st.markdown(
                        f"Scope 1 and 2 Emissions: {scope1_2_emissions:.2f} {unit_of_reporting}"
                    )
                    st.markdown(
                        f"All Scopes Emissions: {all_scopes_emissions:.2f} {unit_of_reporting}"
                    )

                # Find the value in USD per ton
                    selected_row = df[df['proposal_with_date'] == selected_proposal].iloc[0]
                    multiplier = selected_row['usd_proposed_value']

                    st.subheader("Monetized Emissions")
                    display_unit = st.radio("Display units", ["Millions", "Billions"])

                    if unit_of_reporting == "MTCO2E":
                        scope1_emissions = scope1_emissions * 1_000_000
                        scope2_emissions = scope2_emissions * 1_000_000
                        scope3_emissions = scope3_emissions * 1_000_000
                        all_scopes_emissions = all_scopes_emissions * 1_000_000

                # Monetization calculations
                    monetized_scope1 = scope1_emissions * multiplier
                    monetized_scope2 = scope2_emissions * multiplier
                    monetized_scope3 = scope3_emissions * multiplier
                    monetized_all_scopes = all_scopes_emissions * multiplier

                    st.markdown(f"Scope 1: {format_currency(monetized_scope1, display_unit)}")
                    st.markdown(f"Scope 2: {format_currency(monetized_scope2, display_unit)}")
                    st.markdown(f"Scope 3: {format_currency(monetized_scope3, display_unit)}")
                    st.markdown(
                        f"All Scopes: {format_currency(monetized_all_scopes, display_unit)}"
                    )

    with tabs[1]:  # Instructions tab
        st.markdown(instructions)

    with tabs[2]:  # SCC Chart tab
        st.subheader("Social Cost of Carbon Proposals")
        
        # Convert the 'date' column to datetime objects for proper sorting
        df['date'] = pd.to_datetime(df['date'])
        # Sort by value
        df_sorted = df.sort_values(by='usd_proposed_value', ascending=True)

        # Create horizontal bar chart
        bar_fig = px.bar(
            df_sorted,
            x="usd_proposed_value",
            y="proposal_with_date",
            title="Social Cost of Carbon Proposals",
            labels={
                "usd_proposed_value": "USD Proposed Value",
                "proposal_with_date": "Proposal",
            },
            orientation='h',  # Set orientation to horizontal
             hover_data={
                "usd_proposed_value": True,
             }
        )
        bar_fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')
        st.plotly_chart(bar_fig)

        # Organization filter
        organizations = df['organization_name'].unique().tolist()
        selected_org = st.selectbox("Filter by organization", ["All"] + organizations)

        # Filter data
        if selected_org != "All":
            filtered_df = df[df['organization_name'] == selected_org]
        else:
            filtered_df = df

        # Sort the data by date before creating the line chart
        filtered_df = filtered_df.sort_values(by='date')

        # Create line chart with data points and custom hover text
        show_points = st.checkbox("Display Data Points", value=True)
        line_fig = px.line(
            filtered_df,
            x="date",
            y="usd_proposed_value",
            title="Trend of Social Cost of Carbon Proposals Over Time",
            labels={
                "usd_proposed_value": "USD Proposed Value",
                "date": "Date",
            },
            hover_data={
                "usd_proposed_value": True,
                "proposal_with_date": True,
                "organization_name": True,
             },
        )

        line_fig.update_traces(
            mode="lines+markers" if show_points else "lines",
            hovertemplate="USD Value: %{y:.2f}<br>Proposal: %{customdata[0]}<br>Organization: %{customdata[1]}",
            text=filtered_df["proposal_with_date"],
            marker=dict(size=6),
            customdata=filtered_df[["proposal_with_date","organization_name"]]
        )

        st.plotly_chart(line_fig)


    with tabs[3]:  # SCC Details tab
        st.subheader("Social Cost of Carbon Proposal Details")
        proposal_names = df["proposal_with_date"].tolist()
        selected_proposal = st.selectbox("Select a proposal", proposal_names)

        if selected_proposal:
            selected_row = df[df["proposal_with_date"] == selected_proposal].iloc[0]

            # Prepare data for the table
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(" **Organization Name:**")
                st.markdown(" **Organization Description:**")
                st.markdown(" **Date:**")
                st.markdown(" **Country:**")
                st.markdown(" **ISO3:**")
                st.markdown(" **ISO2:**")
                st.markdown(" **HDI Value:**")
                st.markdown(" **HDI Category:**")
                st.markdown(" **Details:**")
            with col2:
                st.markdown(selected_row["organization_name"])
                st.markdown(selected_row["organization_description"])
                st.markdown(selected_row["date"].strftime('%Y-%m-%d'))
                st.markdown(selected_row["country"])
                st.markdown(selected_row["iso3"])
                st.markdown(selected_row["iso2"])
                st.markdown(str(selected_row["hdi_value"]))
                st.markdown(selected_row["hdi_category"])
                st.markdown(selected_row["details"])

            col3, col4 = st.columns(2)
            with col3:
                 st.markdown(" **Original Proposed Value:**")
                 st.markdown(" **Average Value:**")
                 st.markdown(" **USD Proposed Value:**")
                 st.markdown(" **USD Proposed Value (Empty CO2e):**")
                 st.markdown(" **USD Conversion Date:**")
                 st.markdown(" **Value Units:**")
                 st.markdown(" **Environmental Units:**")
                 st.markdown(" **Methodologies Used:**")
                 st.markdown(" **Calculation Scope:**")
                 st.markdown(" **Is Range:**")
            with col4:
                st.markdown(f"{selected_row['original_proposed_value']} {selected_row['original_currency_name']}")
                st.markdown(str(selected_row["average_value"]))
                st.markdown(str(selected_row["usd_proposed_value"]))
                st.markdown(str(selected_row['use_proposed_value_mtco2e']))
                st.markdown(str(selected_row["usd_conversion_date"]))
                st.markdown(selected_row["value_units"])
                st.markdown(selected_row["environmental_units"])
                st.markdown(selected_row["methodologies_used"])
                st.markdown(selected_row["calculation_scope"])
                st.markdown(str(selected_row["is_range"]))

    with tabs[4]: # Data Tab
        st.subheader("Data")
        st.dataframe(df)
        st.markdown("#### Download Data")
        
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='scc_data.csv',
            mime='text/csv',
        )
    
    st.markdown(f'<a href="{GITHUB_LINK}"><img src="https://img.shields.io/badge/View%20on%20GitHub-blue?logo=github"></a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()