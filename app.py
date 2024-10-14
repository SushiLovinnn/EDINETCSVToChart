from flask import Flask, render_template, request, send_file
import os
from main import CSVProcessor, Barchart, isIFRS, check_missing_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    processor = CSVProcessor(file_path)
    processor.load_csv()
    processor.process_data()
    processor.save_to_json()
    processor.rename_csv_file()

    chart = Barchart(processor.json_file_path, True, isIFRS=isIFRS(processor.data))
    chart.plot()
    check_missing_data(processor, chart.is_missing_data, isIFRS=isIFRS(processor.data))

    return render_template('result.html')

@app.route('/plot')
def plot():
    return send_file('plot.png', mimetype='image/png')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)