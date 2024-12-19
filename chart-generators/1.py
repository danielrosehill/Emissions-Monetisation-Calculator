import pandas as pd
import io
import plotly.graph_objects as go

# Load the data from the provided CSV string
csv_data = """proposal_with_date,organization_name,organization_description,date,country,iso3,iso2,hdi_value,hdi_category,details,original_proposed_value,original_currency_name,original_currency_iso,average_value,usd_proposed_value,use_proposed_value_mtco2e,usd_conversion_date,value_units,environmental_units,methodologies_used,calculation_scope,is_range,
International Foundation for Valuing Impacts (Apr 2024),International Foundation for Valuing Impacts,A non-profit organization working to standardize impact valuation.,2024-04-01,United States,USA,US,0.92,Very High,Proposed a standardized approach for companies to report GHG emissions monetarily.,$236,US dollars,USD,236,236,236000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Standardized impact valuation,Social Cost of Carbon,0,
EPA (Final Report) (Dec 2023),Environmental Protection Agency,The primary federal agency responsible for environmental protection.,2023-12-01,United States,USA,US,0.92,Very High,Updated SCC values using advanced methodologies and lower discount rates.,$120-$340,US dollars,USD,230,230,230000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Advanced methodologies,Social Cost of Carbon,1,
U.S. EPA (Updated Proposal) (Dec 2023),Environmental Protection Agency,The primary federal agency responsible for environmental protection.,2023-12-01,United States,USA,US,0.92,Very High,"Finalized updated SCC values, reflecting significant increases based on best science.",$190,US dollars,USD,190,190,190000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Best available science,Social Cost of Carbon,0,
UC Davis (July 2023),University of California, Davis,2023-07-01,United States,USA,US,0.92,Very High,Equity-weighted SCC emphasizing climate damages and uncertainty.,$283,US dollars,USD,283,283,283000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,tons of carbon dioxide equivalents,Social Cost of Carbon,0,
IMF (Jan 2023),International Monetary Fund,An international organization promoting global financial stability.,2023-01-01,United States,USA,US,0.92,Very High,Proposed international carbon price floor based on income levels of countries.,$15-$50,US dollars,USD,32.5,32.5,32500000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Income-based carbon price floor,Carbon Pricing,1,
New York State Agencies (Jan 2021),New York State Agencies,Various state agencies working on climate policy.,2021-01-01,United States,USA,US,0.92,Very High,Guidance under Climate Leadership Act to reduce emissions and achieve net-zero.,$125,US dollars,USD,125,125,125000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Climate Leadership Act guidance,Social Cost of Carbon,0,
Biden Administration (IWG Interim Update) (Feb 2021),Biden Administration Interagency Working Group,A temporary group that develops guidance for federal agencies.,2021-02-01,United States,USA,US,0.92,Very High,Interim update reinstating Obama-era methodology with adjustments.,$51,US dollars,USD,51,51,51000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Obama-era methodology with adjustments,Social Cost of Carbon,0,
Trump Administration (Oct 2017),Trump Administration,The executive branch of the US Federal government under Donald Trump.,2017-10-01,United States,USA,US,0.92,Very High,Lowered SCC estimates focusing on domestic impacts with higher discount rates.,$3-$5,US dollars,USD,4,4,4000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Domestic impacts,Social Cost of Carbon,1,
Climate Leadership Council (Feb 2017),Climate Leadership Council,A coalition advocating for a carbon dividends plan.,2017-02-01,United States,USA,US,0.92,Very High,"Carbon dividends plan starting at $40/ton, increasing annually by 5% above inflation.",$40-$50,US dollars,USD,45,45,45000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Carbon dividends plan,Carbon Pricing,1,
Obama Administration (IWG Update) (Nov 2013),Obama Administration Interagency Working Group,A temporary group that develops guidance for federal agencies.,2013-11-01,United States,USA,US,0.92,Very High,Updated SCC values for regulatory impact analyses under federal guidelines.,$37,US dollars,USD,37,37,37000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Updated SCC methodology,Social Cost of Carbon,0,
UK Government Economic Service (2002-01-01),UK Government Economic Service,The professional body of economists in the UK Civil Service.,2002-01-01,United Kingdom,GBR,GB,0.88,Very High,Recommended illustrative SCC range for policy appraisal across government sectors.,£35-£140,British pounds,GBP,87.5,109.475,109475000,2024-11-20,pounds per ton CO2e,tons of carbon dioxide equivalents,Illustrative SCC range,Social Cost of Carbon,1,
Stern Review (Oct 2006),Stern Review,A landmark report on the economics of climate change.,2006-10-01,United Kingdom,GBR,GB,0.88,Very High,Early influential report advocating for strong climate action.,~$85,US dollars,USD,85,85,85000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Economic modeling,Social Cost of Carbon,0,
Canada Government (Aug 2023),Government of Canada,The federal government of Canada.,2023-08-01,Canada,CAN,CA,0.93,Very High,The Federal Carbon Price was increased to CAD$65 per tonne CO2e in 2023.,CAD$65,Canadian dollars,CAD,65,48.01,48010000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Federal carbon pricing,Carbon Pricing,0,
Nordhaus DICE Model (2017),Yale University,Integrated assessment model of climate change and economics.,2017-01-01,United States,USA,US,0.92,Very High,Highly influential integrated assessment model for climate policy.,$31,US dollars,USD,31,31,31000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Integrated assessment modeling,Social Cost of Carbon,0,
RFF (2021),Resources for the Future,Independent research institution focusing on environmental and natural resource issues.,2021-01-01,United States,USA,US,0.92,Very High,Research and analysis on the social cost of carbon.,$51,US dollars,USD,51,51,51000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,SCC modeling analysis,Social Cost of Carbon,0,
FUND Model (2019),University College London,A climate economy model.,2019-01-01,United Kingdom,GBR,GB,0.88,Very High,Climate economy model focused on policy evaluation.,$25-$60,US dollars,USD,42.5,42.5,42500000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Climate economy modeling,Social Cost of Carbon,1,
PAGE Model (2019),Cambridge University,Policy Analysis model of climate damages.,2019-01-01,United Kingdom,GBR,GB,0.88,Very High,Policy Analysis model for Social Cost of Carbon.,$100-$200,US dollars,USD,150,150,150000000,2024-11-20,dollars per ton CO2e,tons of carbon dioxide equivalents,Policy Analysis Modeling,Social Cost of Carbon,1,
"""

df = pd.read_csv(io.StringIO(csv_data))

# Convert 'average_value' to numeric
df['average_value'] = pd.to_numeric(df['average_value'], errors='coerce')

# Sort by 'average_value' in descending order
df_sorted = df.sort_values(by='average_value', ascending=False)

# Create the Plotly bar chart
fig = go.Figure(data=[go.Bar(
    x=df_sorted['organization_name'],
    y=df_sorted['average_value'],
    text=df_sorted['average_value'],
    textposition='outside',
    marker_color='skyblue'
)])

# Update layout
fig.update_layout(
    title='Social Cost of Carbon Proposals (Highest to Lowest)',
    xaxis_title='Organization',
    yaxis_title='Proposed Value (USD per ton CO2e)',
    plot_bgcolor='white',
    xaxis=dict(tickangle=-45, gridcolor='lightgray'),
    yaxis=dict(gridcolor='lightgray')
)

fig.show()