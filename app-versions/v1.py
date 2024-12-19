import streamlit as st
import pandas as pd

# Path to the data file relative to the app.py file
DATA_PATH = "data.csv"
INSTRUCTIONS_PATH = "instructions.md"


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

    # Tabs for calculator and instructions
    tabs = st.tabs(["Calculator", "Instructions"])

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


if __name__ == "__main__":
    main()