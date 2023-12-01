import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from db_work import select_dict
from sql_provider import SQLProvider


blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login:
            user_info = define_user(login, password)
            if user_info:
                user_dict = user_info[0]
                session['user_id'] = user_dict['user_id']
                session['user_group'] = user_dict['user_group']
                session['user_login'] = login
                session.permanent = True
                return redirect(url_for('start'))
            else:
                return render_template('input_login.html', message='Пользователь не найден')
        return render_template('input_login.html', message='Повторите ввод')


def define_user(login: str, password: str) -> Optional[Dict]:
    sql = provider.get('user.sql', login=login, password=password)

    user_info = None

    _user_info = select_dict(current_app.config['dbconfig'], sql)
    print('_user_info=', _user_info)
    if _user_info:
        user_info = _user_info
        del _user_info

    return user_info