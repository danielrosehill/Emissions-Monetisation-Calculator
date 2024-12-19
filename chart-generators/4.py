import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Load the data from the CSV file
file_path = '/home/daniel/Git/Emissions-Monetisation-Calculator/proposals/versions/latest/scc-proposals.csv'
df = pd.read_csv(file_path)

# Convert 'date' to datetime objects
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert 'usd_proposed_value' to numeric, handling errors
df['usd_proposed_value'] = pd.to_numeric(df['usd_proposed_value'], errors='coerce')

# Filter out invalid rows.
df_filtered = df.dropna(subset=['date', 'usd_proposed_value']).copy()

# Sort by date
df_filtered = df_filtered.sort_values('date')

# Create a dictionary for shortened organization names
org_name_map = {
    "International Foundation for Valuing Impacts": "IFVI",
    "Environmental Protection Agency": "EPA",
     "University of California, Davis": "UC Davis",
    "International Monetary Fund": "IMF",
    "New York State Agencies": "NY State",
    "Biden Administration Interagency Working Group": "Biden Admin",
    "Trump Administration": "Trump Admin",
    "Climate Leadership Council": "CLC",
    "Obama Administration Interagency Working Group": "Obama Admin",
    "UK Government Economic Service": "UK Gov",
    "Stern Review": "Stern",
    "Government of Canada": "Canada Gov",
    "Yale University": "Yale",
    "Resources for the Future": "RFF",
     "University College London": "UCL",
     "Cambridge University": "Cambridge"
}

# Apply shortened names to the DataFrame
df_filtered['short_org'] = df_filtered['organization_name'].map(org_name_map)


# Create the line plot
plt.figure(figsize=(14, 8))

# Plot with the short names.
sns.lineplot(x='date',
            y='usd_proposed_value',
            hue='short_org',
            data=df_filtered,
            marker="o",  # Add markers
            markersize=8, # Enlarge markers
            linewidth=1
           )

plt.xlabel('Date')
plt.ylabel('Proposed Social Cost of Carbon (USD/ton)')
plt.title('Social Cost of Carbon Proposals Over Time by Organization')
plt.legend(title='Organization', loc='upper left', bbox_to_anchor=(1, 1))

# Format x-axis date display
date_fmt = mdates.DateFormatter('%Y-%b')
plt.gca().xaxis.set_major_formatter(date_fmt)
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=45, ha='right')

plt.tight_layout(rect=[0, 0, .9, 1])

# Annotate each data point with name, hyphen, dollar symbol, number.
for index, row in df_filtered.iterrows():
    plt.annotate(f"{row['short_org']} - ${int(row['usd_proposed_value'])}",
                 xy=(row['date'], row['usd_proposed_value']),
                 xytext=(0, 8),  # Adjust text position above the marker
                 textcoords='offset points',
                 ha='center',  # Center text horizontally
                 fontsize=8, # Set text size to be readable
                 color='black'
                 )


plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()