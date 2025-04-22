import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle

# Load cleaned dataset
df = pd.read_csv('cleaned_unemployment_data.csv')

# Drop missing
df = df.dropna(subset=['Estimated Unemployment Rate'])

# Simulate missing features
df['Gender'] = np.random.choice(['Male', 'Female'], size=len(df))
df['Age'] = np.random.randint(18, 60, size=len(df))
df['Education'] = np.random.choice(
    ['No Schooling', 'Primary', 'Secondary', 'Graduate', 'Postgraduate'],
    size=len(df)
)

# Encode Region and Area
le_region = LabelEncoder()
le_area = LabelEncoder()
df['Region_encoded'] = le_region.fit_transform(df['Region'])
df['Area_encoded'] = le_area.fit_transform(df['Area'])

# Encode Gender
df['Gender_val'] = df['Gender'].apply(lambda g: 1 if g == 'Male' else 0)

# Encode Education
edu_map = {
    'No Schooling': 0,
    'Primary': 1,
    'Secondary': 2,
    'Graduate': 3,
    'Postgraduate': 4
}
df['Education_val'] = df['Education'].map(edu_map)

# Features & Target
X = df[['Region_encoded', 'Area_encoded', 'Year', 'Gender_val', 'Education_val', 'Age']]
y = df['Estimated Unemployment Rate']

# Split & Train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
with open('unemployment_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('region_encoder.pkl', 'wb') as f:
    pickle.dump(le_region, f)
with open('area_encoder.pkl', 'wb') as f:
    pickle.dump(le_area, f)

print("✅ Model retrained with 6 features and saved!")
