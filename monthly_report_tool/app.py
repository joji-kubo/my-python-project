from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
from database import insert_report, get_monthly_report

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        content = request.form['content']
        
        insert_report(date, start_time, end_time, content)
        return redirect('/')
    
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    month = request.form['month']
    df = get_monthly_report(month)
    
    return render_template('index.html', tables=[df.to_html(classes='data')], month=month)

@app.route('/export', methods=['POST'])
def export():
    month = request.form['month']
    df = get_monthly_report(month)
    file_path = f"monthly_report_{month}.csv"
    df.to_csv(file_path, index=False)
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
