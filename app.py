from flask import Flask, url_for, request, render_template, redirect, json
from query import blueprint_query

app = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/queries')

with open('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
    app.config['dbconfig'] = db_config


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('start_page.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)