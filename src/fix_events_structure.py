# fix_events_structure.py
import pandas as pd

# Define the correct structure
correct_data = [
    # date, event_name, event_type, description, region, expected_impact, source
    ["1990-08-02", "Gulf War", "Geopolitical Conflict", "Iraq invades Kuwait", "Middle East", "High", "Historical"],
    ["2001-09-11", "9/11 Attacks", "Terrorism", "Terrorist attacks on US", "Global", "Medium", "Historical"],
    ["2003-03-20", "Iraq War", "Geopolitical Conflict", "US-led invasion of Iraq", "Middle East", "High", "Historical"],
    ["2008-09-15", "Global Financial Crisis", "Economic", "Lehman Brothers collapse", "Global", "High", "Historical"],
    ["2011-02-15", "Arab Spring", "Geopolitical Conflict", "Political uprisings", "Middle East", "Medium", "Historical"],
    ["2014-06-01", "OPEC Price War", "OPEC Policy", "OPEC maintains production", "Global", "High", "Historical"],
    ["2015-12-12", "Paris Agreement", "Policy", "Global climate accord", "Global", "Low", "Historical"],
    ["2016-01-16", "Iran Nuclear Deal", "Sanctions", "Sanctions lifted on Iran", "Middle East", "Medium", "Historical"],
    ["2019-09-14", "Abqaiq Attack", "Conflict", "Drone attacks on Saudi facilities", "Saudi Arabia", "High", "Historical"],
    ["2020-01-30", "COVID-19 Pandemic", "Health", "WHO declares pandemic", "Global", "High", "Historical"],
    ["2020-03-06", "OPEC+ Price War", "OPEC Policy", "Russia-Saudi oil price war", "Global", "High", "Historical"],
    ["2020-04-20", "Negative Oil Prices", "Economic", "First-ever negative oil prices", "Global", "High", "Historical"],
    ["2021-01-20", "Biden Inauguration", "Policy", "US rejoins Paris Agreement", "USA", "Medium", "Historical"],
    ["2022-02-24", "Russia-Ukraine War", "Geopolitical Conflict", "Military invasion begins", "Europe", "High", "Recent"],
    ["2022-10-05", "OPEC+ Production Cut", "OPEC Policy", "2 million barrel/day cut", "Global", "High", "Recent"]
]

# Create DataFrame with correct column order
columns = ['date', 'event_name', 'event_type', 'description', 'region', 'expected_impact', 'source']
events_df = pd.DataFrame(correct_data, columns=columns)

# Save to CSV
events_df.to_csv('../data/events/key_events_correct.csv', index=False)

print("✅ Created correctly structured events file: data/events/key_events_correct.csv")
print("\nFirst 3 rows:")
print(events_df.head(3))
print("\nColumn order:")
print(list(events_df.columns))