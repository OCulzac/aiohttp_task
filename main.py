from aiohttp import web
import json

from aiohttp_store.crud import session_scope, recreate_database, load_yaml
from aiohttp_store.models import Base, Order, User, Book, Shop, OrderItem

recreate_database()
load_yaml()

'''------------------------'''


async def sort(request):
    """returns sorted query data

    :param request: user input on which datapoint to sort by
    :return: sorted data from db
    """
    with session_scope() as s:
        try:
            q = request.query['sort by']
            if q == 'user_id':
                orders = s.query(Order).order_by(Order.user_id.desc())
            elif q == 'id':
                orders = s.query(Order).order_by(Order.id.desc())
            elif q == 'reg_date':
                orders = s.query(Order).order_by(Order.reg_date.desc())
            else:
                raise Exception('query should be: user_id or id or reg_date')
            return web.Response(text=json.dumps([(order.id, order.reg_date, order.user_id)
                                                 for order in orders], default=str), status=200)
        except Exception as e:
            response_obj = {'status': 'failed', 'message': str(e)}
            return web.Response(text=json.dumps(response_obj), status=500)


'''------------------------'''


async def users(request):
    """users func

    :param request: recieves get request
    :return: all available user info in database
    """
    with session_scope() as s:
        users = s.query(User)
        return web.Response(text=json.dumps([(user.id, user.last_name, user.first_name, user.email) for user in users]),
                            status=200)


'''------------------------'''


async def store_book_info(request):
    """book shop func

    :param request: accepts user input on store name
    :return: book name, author, shop name and address of chosen book store
    """
    try:
        store_name = request.query['store name']
        with session_scope() as s:
            q = s.query(Book.name, Book.author, Shop.name, Shop.address).filter(
                OrderItem.book_id == Book.id
            ).filter(
                OrderItem.shop_id == Shop.id
            ).filter(
                Shop.name == store_name
            ).all()

        response_obj = {'status': 'success', 'message': ['Books ordered from {} are:'.format(store_name)], 'details': q}
        return web.Response(text=json.dumps(response_obj, default=str))

    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


'''------------------------'''


async def handle(request):
    """simple get request handler

    :param request: received get request
    :return: text with basic api endpoint information
    """
    response_obj = {'status': 'success', 'endpoints': ['/users - for all user info',
                                                       '/user_orders - for user order history',
                                                       '/sort - order info sorted ',
                                                       '/new_order - insert a new order into db',
                                                       '/book_shop - books ordered by a particular store']}
    return web.Response(text=json.dumps(response_obj, default=str))


'''------------------------'''


async def order_history(request):
    """order history func

    :param request: takes user input first name and last name
    :return: returns order history for that particular user
    """
    try:
        first_name = request.query['first name']
        last_name = request.query['surname']

        with session_scope() as s:
            q = s.query(User.first_name, User.last_name, Book.name, OrderItem.book_quantity).filter(
                User.id == Order.user_id
            ).filter(
                Order.id == OrderItem.order_id
            ).filter(
                OrderItem.book_id == Book.id
            ).filter(
                User.last_name == last_name
            ).filter(
                User.first_name == first_name
            ).all()
        response_obj = {'status': 'success',
                        'message': ['The details for the user: {} {}'.format(first_name, last_name)], 'details': q}
        return web.Response(text=json.dumps(response_obj, default=str), status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


'''------------------------'''


async def new_order(request):
    """ new order func

    :param request: accepts user input order date, user id, book id, shop id ad book quantity and creates a new order
    :return: None
    """
    try:
        order_date = request.query['order date']
        user_id = request.query['user id']
        book_id = request.query['book id']
        shop_id = request.query['shop id']
        book_quantity = request.query['book quantity']

        with session_scope() as s:
            order_new = Order(reg_date=order_date, user_id=user_id)
            s.add(order_new)

        with session_scope() as s:
            order_id = s.query(Order.id).order_by(Order.id)[-1]
            orderitem_new = OrderItem(order_id=order_id, book_id=book_id, shop_id=shop_id,
                                      book_quantity=book_quantity)
            s.add(orderitem_new)

        response_obj = {'status': 'success',
                        'message': ['the order:', order_date, user_id, order_id, book_id, shop_id, book_quantity,
                                    'created successfully']}
        return web.Response(text=json.dumps(response_obj), status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


'''------------------------'''
app = web.Application()
app.router.add_get('/', handle)
app.router.add_post('/user_orders', order_history)
app.router.add_get('/users', users)
app.router.add_get('/sort', sort)
app.router.add_post('/book_shop', store_book_info)
app.router.add_post('/new_order', new_order)
web.run_app(app)
