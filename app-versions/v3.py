import streamlit as st
import pandas as pd
import plotly.express as px

# Path to the data file relative to the app.py file
DATA_PATH = "data.csv"
INSTRUCTIONS_PATH = "instructions.md"

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
        with open(INSTRUCTIONS_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Instructions file not found."


def format_currency(value, display_unit):
    if display_unit == "Millions":
        formatted_value = f"${value / 1_000_000:.2f} MN"
    elif display_unit == "Billions":
        formatted_value = f"${value / 1_000_000_000:.2f} BN"
    return formatted_value


def main():
    st.title("GHG Emissions Monetization Calculator")
    st.markdown(
        "The purpose of this tool and demonstration is to allow users to explore How monetizing companies proposed greenhouse gas emissions might work in practice."
    )
    st.markdown(
        "This calculator accompanies a repository shared on Github and Hugging Face which aggregates proposals for the social cost of carbon, which have been advanced at various points in time by various world bodies."
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
    tabs = st.tabs(["Calculator", "Instructions", "SCC Chart", "SCC Details"])

    with tabs[0]:  # Calculator tab
        with st.container():
            left, right = st.columns(2)

            with left:
                st.subheader("Input Values")
                scope1_emissions = st.number_input("Scope 1 Emissions", value=0.0)
                scope2_emissions = st.number_input("Scope 2 Emissions", value=0.0)
                scope3_emissions = st.number_input("Scope 3 Emissions", value=0.0)
                unit_of_reporting = st.selectbox("Unit of Reporting", ["TCO2E", "MTCO2E"])

                proposal_names = df['proposal_with_date'].tolist()
                selected_proposal = st.selectbox("Social cost of carbon", proposal_names)

            with right:
                st.subheader("Calculated Values")
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

        # Sort by date
        df = df.sort_values(by='date')

        # Create horizontal bar chart
        bar_fig = px.bar(
            df,
            x="usd_proposed_value",
            y="proposal_with_date",
            title="Social Cost of Carbon Proposals",
            labels={
                "usd_proposed_value": "USD Proposed Value",
                "proposal_with_date": "Proposal",
            },
            orientation='h'  # Set orientation to horizontal
        )

        st.plotly_chart(bar_fig)

        # Create line chart with data points and custom hover text
        line_fig = px.line(
            df,
            x="date",
            y="usd_proposed_value",
            title="Trend of Social Cost of Carbon Proposals Over Time",
            labels={
                "usd_proposed_value": "USD Proposed Value",
                "date": "Date",
            },
           hover_data={
                "usd_proposed_value": False,
                "proposal_with_date": True,
            },
            
        )
        
        line_fig.update_traces(
            mode="lines+markers",
            hovertemplate="<b>%{hovertext}</b>",  # Customize hover text
            text=df["proposal_with_date"], # Add the text data
           
        )

        st.plotly_chart(line_fig)

    with tabs[3]:  # SCC Details tab
        st.subheader("Social Cost of Carbon Proposal Details")
        proposal_names = df["proposal_with_date"].tolist()
        selected_proposal = st.selectbox("Select a proposal", proposal_names)

        if selected_proposal:
            selected_row = df[df["proposal_with_date"] == selected_proposal].iloc[0]

            # Prepare data for the table
            table_data = {
                "Field": [
                    "Organization Name",
                    "Organization Description",
                    "Date",
                    "Country",
                    "ISO3",
                    "ISO2",
                    "HDI Value",
                    "HDI Category",
                    "Details",
                    "Original Proposed Value",
                    "Average Value",
                    "USD Proposed Value",
                    "USD Proposed Value (Empty CO2e)",
                    "USD Conversion Date",
                    "Value Units",
                    "Environmental Units",
                    "Methodologies Used",
                    "Calculation Scope",
                    "Is Range",
                ],
                "Value": [
                    selected_row["organization_name"],
                    selected_row["organization_description"],
                    selected_row["date"].strftime('%Y-%m-%d'),
                    selected_row["country"],
                    selected_row["iso3"],
                    selected_row["iso2"],
                    selected_row["hdi_value"],
                    selected_row["hdi_category"],
                    selected_row["details"],
                    f"{selected_row['original_proposed_value']} {selected_row['original_currency_name']}",
                    selected_row["average_value"],
                    selected_row["usd_proposed_value"],
                     selected_row['use_proposed_value_mtco2e'],
                    selected_row["usd_conversion_date"],
                    selected_row["value_units"],
                    selected_row["environmental_units"],
                    selected_row["methodologies_used"],
                    selected_row["calculation_scope"],
                    selected_row["is_range"],
                ],
            }
            st.table(table_data)
    
    st.markdown(f'<a href="{GITHUB_LINK}"><img src="https://img.shields.io/badge/View%20on%20GitHub-blue?logo=github"></a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()