from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from plot_web import Barchart  
from main import isIFRS



app = Flask(__name__)

@app.route('/')
def index():
    json_files = os.listdir('json_file')
    return render_template('index.html', json_files=json_files)

@app.route('/search_json', methods=['GET'])
def search_json():
    query = request.args.get('query', '')
    json_files = [f for f in os.listdir('json_file') if query.lower() in f.lower()]
    return render_template('index.html', json_files=json_files)

@app.route('/process_json', methods=['POST'])
def process_json():
    json_file = request.form['json_file']
    json_file_path = os.path.join('json_file', json_file)
    
    # プロット生成
    barchart = Barchart(json_file_path, show_chart=True)
    barchart.plot()
    
    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/plot')
def plot():
    return send_file('plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)