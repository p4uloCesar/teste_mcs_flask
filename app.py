from dateutil import parser
from datetime import datetime

from flask import Flask, render_template, request
import pandas as pd
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

app = Flask(__name__)

Bootstrap(app)
datepicker(app)


@app.route('/', methods={'GET', 'POST'})
def range_date_info():
    if request.method == 'POST':
        xls = request.form['upload-xls']
        df = pd.read_excel(xls)
        df['data'] = df['data'].apply(lambda _: _ if type(_) == pd.Timestamp else datetime.strptime(_, "%d/%m/%Y"))
        sum_last_months = 0
        try:
            max_date = datetime.strptime(request.form['final-date'], '%Y-%m-%d')
            min_date = datetime.strptime(request.form['init-date'], '%Y-%m-%d')
            list_months = pd.date_range(min_date, max_date, freq='MS')
        except:
            list_months = pd.date_range(pd.to_datetime(max(df.data.values), dayfirst=True) - pd.DateOffset(months=12),
                                        pd.to_datetime(max(df.data.values), dayfirst=True), freq='MS')
        for values_month in list_months:
            array = [values_xls[1] for values_xls in df.values.tolist()
                     if pd.Timestamp(values_xls[0]) == pd.to_datetime(values_month, dayfirst=True)]
            if array:
                sum_last_months += array[0]
        return render_template('index.html', values=sum_last_months)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
