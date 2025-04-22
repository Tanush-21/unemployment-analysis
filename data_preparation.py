import pandas as pd

# Load the dataset
df = pd.read_csv('Unemployment in India.csv')

# Show initial info
print("Initial Data:")
print(df.head())

# Rename columns
df.columns = ['Region', 'Date', 'Frequency', 'Estimated Unemployment Rate', 'Estimated Employed', 'Estimated Labour Participation Rate', 'Area']

# Drop unnecessary columns
df = df.drop(columns=['Estimated Employed', 'Estimated Labour Participation Rate', 'Frequency'])

# Convert Date to datetime and extract year
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Save cleaned data
df.to_csv('cleaned_unemployment_data.csv', index=False)

print("\n✅ Cleaned data saved as 'cleaned_unemployment_data.csv'")
