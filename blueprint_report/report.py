import os
from flask import Blueprint, request, render_template, current_app
from db_work import select, call_proc
from sql_provider import SQLProvider
from access import login_required, group_required

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/')
def reports():
    return render_template('report.html', title='Страница работы с отчётами', reports=current_app.config['reports_config'])


@blueprint_report.route('/get', methods=['GET', 'POST'])
@login_required
@group_required
def getReport():
    if request.method == 'GET':
        return render_template('getReport.html', title='Страница поиска отчётов')
    else:
        year = request.form.get('inputYear')
        month = request.form.get('inputMonth')
        if year and month:
            _sql = provider.get('report.sql', year=year, month=month)
            getResult, getSchema = select(current_app.config['dbconfig'], _sql)
        else:
            getResult, getSchema = select(current_app.config['dbconfig'], "select * from report")
        return render_template('getReport.html', title='Страница поиска отчётов', schema=getSchema, result=getResult)


@blueprint_report.route('/create', methods=['GET', 'POST'])
@login_required
@group_required
def createReport():
    if request.method == 'GET':
        return render_template('createReport.html', title='Страница создание отчётов')
    else:
        year = request.form.get('inputYear')
        month = request.form.get('inputMonth')
        if year and month:
            year = int(year)
            month = int(month)
            call_proc(current_app.config['dbconfig'], 'createReport', year, month)

        _sql = provider.get('report.sql', year=year, month=month)
        createResult, createSchema = select(current_app.config['dbconfig'], _sql)
        return render_template('createReport.html', title='Страница создание отчётов', schema=createSchema, result=createResult)
