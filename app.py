from flask import Flask, request, render_template, Response, make_response, redirect, url_for, session, flash
import pickle
import numpy as np
import pandas as pd
import json
import pdfkit
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'thisissecretkeytanush123'  # For session management

# Path to wkhtmltopdf.exe (adjust if needed)
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Load model and encoders
with open('unemployment_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('region_encoder.pkl', 'rb') as file:
    region_encoder = pickle.load(file)

with open('area_encoder.pkl', 'rb') as file:
    area_encoder = pickle.load(file)

# Load chart data
data = pd.read_csv('cleaned_unemployment_data.csv')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    state_group = data.groupby('Region')['Estimated Unemployment Rate'].mean().sort_values(ascending=False)
    states = state_group.index.tolist()
    state_values = [round(val, 2) for val in state_group.values]

    area_group = data.groupby('Area')['Estimated Unemployment Rate'].mean()
    area_values = [round(area_group.get('Urban', 0), 2), round(area_group.get('Rural', 0), 2)]

    year_group = data.groupby('Year')['Estimated Unemployment Rate'].mean()
    years = year_group.index.astype(str).tolist()
    year_values = [round(val, 2) for val in year_group.values]

    chart_data = {
        "states": states,
        "stateValues": state_values,
        "areaValues": area_values,
        "years": years,
        "yearValues": year_values
    }

    return render_template('index.html', chart_data=json.dumps(chart_data))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            conn.close()
            flash('Signup successful. Please log in.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            flash('Email already registered. Please log in.', 'danger')
            return redirect('/signup')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user'] = user[1]     # name
            session['email'] = user[2]    # email
            flash(f"Welcome, {user[1]}!", 'success')
            return redirect('/')
        else:
            flash('Invalid email or password.', 'danger')
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    flash('You have been logged out.', 'info')
    return redirect('/login')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        flash('Please login to make predictions.', 'warning')
        return redirect('/login')

    try:
        region = request.form['region']
        area = request.form['area']
        year = int(request.form['year'])
        gender = request.form['gender']
        education = request.form['education']
        age = int(request.form['age'])

        region_encoded = region_encoder.transform([region])[0]
        area_encoded = area_encoder.transform([area])[0]
        gender_val = 1 if gender.lower() == 'male' else 0

        edu_map = {'No Schooling': 0, 'Primary': 1, 'Secondary': 2, 'Graduate': 3, 'Postgraduate': 4}
        education_val = edu_map.get(education, 0)

        features = np.array([[region_encoded, area_encoded, year, gender_val, education_val, age]])
        prediction = model.predict(features)
        predicted_rate = round(prediction[0], 2)

        # Update chart data
        state_group = data.groupby('Region')['Estimated Unemployment Rate'].mean().sort_values(ascending=False)
        states = state_group.index.tolist()
        state_values = [round(val, 2) for val in state_group.values]

        area_group = data.groupby('Area')['Estimated Unemployment Rate'].mean()
        area_values = [round(area_group.get('Urban', 0), 2), round(area_group.get('Rural', 0), 2)]

        year_group = data.groupby('Year')['Estimated Unemployment Rate'].mean()
        years = year_group.index.astype(str).tolist()
        year_values = [round(val, 2) for val in year_group.values]

        chart_data = {
            "states": states,
            "stateValues": state_values,
            "areaValues": area_values,
            "years": years,
            "yearValues": year_values
        }

        return render_template('index.html',
            prediction_text=f"Predicted Unemployment Rate for {region}, {area} in {year}: {predicted_rate}%",
            chart_data=json.dumps(chart_data))

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}", chart_data=json.dumps({}))

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        region = request.form['region']
        area = request.form['area']
        year = request.form['year']
        gender = request.form['gender']
        age = request.form['age']
        education = request.form['education']
        prediction = request.form['prediction']

        rendered = render_template('result.html',
                                   region=region,
                                   area=area,
                                   year=year,
                                   gender=gender,
                                   age=age,
                                   education=education,
                                   prediction=prediction)

        pdf = pdfkit.from_string(rendered, False, configuration=PDFKIT_CONFIG)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=prediction_result.pdf'
        return response
    except Exception as e:
        return f"Error generating PDF: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
