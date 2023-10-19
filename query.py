import os
from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
def queries_list():
    if request.method == 'GET':
        return render_template('select_query.html')


@blueprint_query.route('/query/1', methods=['GET', 'POST'])
def query_1():
    if request.method == 'GET':
        return render_template('query_1_params.html')
    else:
        prod_price = request.form.get('prod_price')
        if prod_price:
            sql = provider.get('prod_price.sql', prod_price=prod_price)
            print(sql)
            product_result, schema = select(current_app.config['dbconfig'], sql)
            return render_template('query_1_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"


@blueprint_query.route('/query/2', methods=['GET', 'POST'])
def query_2():
    if request.method == 'GET':
        return render_template('query_2_params.html')
    else:
        prod_measure = request.form.get('prod_measure')
        if prod_measure:
            sql = provider.get('prod_measure.sql', prod_measure=prod_measure)
            product_result, schema = select(current_app.config['dbconfig'], sql)
            return render_template('query_2_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"