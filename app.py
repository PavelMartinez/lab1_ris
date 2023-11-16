from flask import Flask, render_template, json, url_for, redirect, session
from blueprint_query.query import blueprint_query
from blueprint_auth.auth import blueprint_auth
from blueprint_report.report import blueprint_report
from access import login_required

app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_query, url_prefix='/queries')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')

app.config['dbconfig'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def start():
    if 'user_id' in session:
        return render_template('start_page.html')
    else:
        return redirect(url_for('bp_auth.start_auth'))


@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return redirect(url_for('start'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)