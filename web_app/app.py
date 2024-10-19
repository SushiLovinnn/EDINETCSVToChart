from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file, g
import os
import json
import uuid
from plot_web import Barchart
from plot_saver import PlotSaver
from dotenv import load_dotenv
from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(minutes=5)  # セッションの有効期限

def cleanup_expired_sessions():
    now = datetime.now()
    session_dir = os.path.join('web_app', 'static', 'plots')
    for session_id in os.listdir(session_dir):
        session_path = os.path.join(session_dir, session_id)
        if os.path.isdir(session_path):
            session_mtime = datetime.fromtimestamp(os.path.getmtime(session_path))
            if now - session_mtime > app.permanent_session_lifetime:
                for root, dirs, files in os.walk(session_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(session_path)
                print(f"Expired session directory removed: {session_path}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_expired_sessions, trigger="interval", minutes=5)
scheduler.start()

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
    
    # セッションを永続化しない
    session.permanent = False

    # 一意の識別子を生成
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    g.session_id = session_id  # グローバル変数に保存

    # セッションごとに一意のディレクトリを作成
    session_dir = os.path.join('web_app', 'static', 'plots', session_id)
    os.makedirs(session_dir, exist_ok=True)

    # Barchartクラスを使用してプロットを作成
    barchart = Barchart(json_file_path, show_chart=True)

    # PlotSaverクラスを使用してプロットを保存
    plot_saver = PlotSaver(session_dir=session_dir, show_chart=False)
    plot_paths = plot_saver.save_plots([barchart])
    session['plot_paths'] = plot_paths

    flash(f'Plot generated for {json_file}')
    return redirect(url_for('result', session_id=session_id))

@app.route('/result')
def result():
    session_id = request.args.get('session_id')
    return render_template('result.html', session_id=session_id)

@app.route('/static/plots/<session_id>/<filename>')
def plot(session_id, filename):
    return send_file(os.path.join('static', 'plots', session_id, filename), mimetype='image/png')

@app.route('/cleanup')
def cleanup():
    session_id = request.args.get('session_id')
    if not session_id:
        return "Session ID is missing", 400

    plot_paths = session.get('plot_paths', [])
    plot_saver = PlotSaver(session_dir=os.path.join('static', 'plots', session_id))
    plot_saver.delete_plots(plot_paths)
    session.pop('plot_paths', None)
    return redirect(url_for('index'))

@app.teardown_appcontext
def cleanup_session(exception=None):
    session_id = getattr(g, 'session_id', None)
    if session_id:
        session_dir = os.path.join('static', 'plots', session_id)
        if os.path.exists(session_dir):
            for root, dirs, files in os.walk(session_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(session_dir)
            print(f"Directory removed: {session_dir}")

@app.route('/session_info')
def session_info():
    if 'session_id' not in session:
        return "No active session", 400
    return f"Session ID: {session['session_id']}, Permanent: {session.permanent}, Expires: {session.get('_permanent', 'N/A')}"

if __name__ == '__main__':
    app.run(debug=True)