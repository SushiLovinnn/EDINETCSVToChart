from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
import os
import json
import uuid
from plot_web import Barchart
from plot_saver import PlotSaver
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

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
    
    # 一意の識別子を生成
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id

    # Barchartクラスを使用してプロットを作成
    barchart = Barchart(json_file_path, show_chart=True)
    plot = barchart.plot()

    # PlotSaverクラスを使用してプロットを保存
    plot_saver = PlotSaver()
    plot_paths = plot_saver.save_plots([plot])
    session['plot_paths'] = plot_paths

    flash(f'Plot generated for {json_file}')
    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/plot/<filename>')
def plot(filename):
    return send_file(os.path.join('static', 'plots', filename), mimetype='image/png')

@app.route('/cleanup')
def cleanup():
    plot_paths = session.get('plot_paths', [])
    plot_saver = PlotSaver()
    plot_saver.delete_plots(plot_paths)
    session.pop('plot_paths', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)