import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_work import select, insert
from sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache

blueprint_market = Blueprint('bp_market', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
def market_index():
    configDB = current_app.config['dbconfig']
    cache_config = current_app.config['cache']
    cached_func = fetch_from_cache('all_items_cached', cache_config)(select)

    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = cached_func(configDB, sql)
        basket_items = session.get('basket', {})
        return render_template('market.html', title='Маркет', items=items[0], basket_items=basket_items)
    else:
        prod_id = request.form['prod_id']
        sql = provider.get('all_items.sql')
        items = cached_func(configDB, sql)

        item_description = []
        for i in range(len(items[0])):
            if str(items[0][i][0]) == str(prod_id):
                print(items[0][i])
                item_description.append(items[0][i])

        if not item_description:
            return render_template('item_missing.html', title='Товар на складе отсутствует')

        item_description = item_description[0]
        curr_basket = session.get('basket', {})

        if prod_id in curr_basket:
            curr_basket[prod_id]['price'] = curr_basket[prod_id]['price'] + item_description[2]
            curr_basket[prod_id]['cnt'] = curr_basket[prod_id]['cnt'] + 1
        else:
            curr_basket[prod_id] = {
                'name': item_description[1],
                'price': item_description[2],
                'cnt': 1
            }
        session['basket'] = curr_basket
        session.permanent = True

        return redirect(url_for('bp_market.market_index'))


@blueprint_market.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.market_index'))


@blueprint_market.route('/checkout', methods=['POST'])
def checkout():
    configDB = current_app.config['dbconfig']
    basket_items = session.get('basket', {})
    if basket_items:
        order_details = list()
        for item in basket_items.items():
            sql = provider.insert('new_order.sql',
                                  prod_name=item[1]['name'],
                                  prod_quantity=item[1]['cnt'],
                                  prod_total=item[1]['price'])
            insert(configDB, sql)
            order_details.append({
                'product_name': item[1]['name'],
                'quantity': item[1]['cnt'],
                'price': item[1]['price']
            })
        session.pop('basket')
        return render_template('order_confirmed.html', title='Заказ подтвержден', order_details=order_details)
    else:
        return "Корзина пуста"
    return redirect(url_for('bp_market.market_index'))
