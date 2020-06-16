from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods = ['GET'])
def home():
    return 'this is the homepage'

def get_total_cases(days_after_22_mar):
    infection_speed_rate = 0.05072594814362884
    day_peak = 89.8232012535864
    max_infected_people = 53728.796289306054
    return max_infected_people/(1+np.exp(-infection_speed_rate*(days_after_22_mar-day_peak)))

@app.route('/covid-idn', methods = ['POST'])
def covid_idn():
    data = request.json
    input_start_date = data['start_date']
    input_end_date = data['end_date']

    input_format = '%d/%m/%Y'
    output_format = '%d %b %Y'

    day_0 = pd.to_datetime('22/3/2020', format=input_format)

    output_start_date = None
    total_cases_start_date = 0
    if input_start_date is not None:
        input_start_date_dt = pd.to_datetime(input_start_date, format=input_format)
        days_after_22_mar_start_date = (input_start_date_dt - day_0).days
        total_cases_start_date = int(get_total_cases(days_after_22_mar_start_date))
        output_start_date = input_start_date_dt.strftime(output_format)

    input_end_date_dt = pd.to_datetime(input_end_date, format=input_format)
    days_after_22_mar_end_date = (input_end_date_dt - day_0).days
    total_cases_end_date = int(get_total_cases(days_after_22_mar_end_date))
    output_end_date = input_end_date_dt.strftime(output_format)

    return jsonify(
        start_date = output_start_date,
        end_date = output_end_date,
        total_cases = total_cases_end_date - total_cases_start_date
    )

if __name__ == '__main__':
    app.run(debug = True)