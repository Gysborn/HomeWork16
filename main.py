from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from data import users_data, orders_data, offers_data

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(30))
    phone = db.Column(db.String(20))
    as_executor_in_offers = db.relationship('Offer', foreign_keys='Offer.executor_id')  # Положит список всех оферов
    # в которых он указан как исполнитель
    as_executor_in_orders = db.relationship('Order', foreign_keys='Order.executor_id')
    as_customer_in_orders = db.relationship('Order', foreign_keys='Order.customer_id')

    def to_dict(self):
        return {
            'id:': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'role': self.role,
            'phone': self.phone
        }


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    start_date = db.Column(db.String(255))
    end_date = db.Column(db.String(255))
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    as_order_in_offers = db.relationship('Offer')  # Ищет в Офере внешний ключ ссылающийся

    # на него самого и кладет в переменную

    def to_dict(self):
        return {
            'id:': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'price': self.price,
        }


class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    order = db.relationship('Order', back_populates="as_order_in_offers", foreign_keys=[order_id])  # кладет экз. заказа
    # на который ссылается внешний ключ
    # order_id(as_order_in_offers)
    executor = db.relationship('User', back_populates="as_executor_in_offers", foreign_keys=[executor_id])  #

    def to_dict(self):
        return {
            'id:': self.id,
            'order_id': self.order_id,
            'executor_id': self.executor_id
        }


def query_all_get(model):
    result = []
    try:
        for v in model.query.all():
            result.append(v.to_dict())
    except Exception as e:
        return f'Error {e}'
    return jsonify(result), 200


def query_get_by_id(model, idx):
    try:
        user = model.query.get(idx)
    except Exception as e:
        return f'Error {e}'
    return jsonify(user.to_dict())


def query_put_update(model, idx):
    try:
        new_data = request.json
        user_data = model.query.get(idx)
        [setattr(user_data, k, v) for k, v in new_data.items()]

        db.session.add(user_data)
    except Exception as e:
        return f'Ошибка {e}'
    db.session.commit()
    return f"Данные обновлены {model.query.get(idx).to_dict()}"


def query_post_add(model):
    try:
        user_data = request.json
        new_user = model(**user_data)
        db.session.add(new_user)
    except Exception as e:
        return f'Ошибка {e}'

    db.session.commit()
    return f"Пользователь добавлен {new_user.to_dict()}"


def query_delete(model, idx):
    try:
        user = model.query.get(idx)
        db.session.delete(user)
    except Exception as e:
        return f'Ошибка {e}'
    db.session.commit()
    return 'deleted', 200


db.drop_all()
db.create_all()


def migrate_data(data, model):
    try:
        for d in data:
            new_inst = model(**d)
            db.session.add(new_inst)

    except Exception as e:
        print(f'Ощибочка вышла {e}')
    db.session.commit()


migrate_data(users_data, User)
migrate_data(orders_data, Order)
migrate_data(offers_data, Offer)


@app.route('/')
def hello():
    return 'Let`s the party begin! Enter a query'


@app.route('/users', methods=['GET', 'POST'])
def get_post_users():
    if request.method == 'GET':
        return query_all_get(User)
    if request.method == 'POST':
        return query_post_add(User)
    else:
        return 'Неверный метод запроса', 500


@app.route('/users/<int:idx>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_user(idx):
    if request.method == 'GET':
        return query_get_by_id(User, idx)
    if request.method == 'PUT':
        return query_put_update(User, idx)
    if request.method == 'DELETE':
        return query_delete(User, idx)
    else:
        return 'Неверный метод запроса', 500


@app.route('/orders', methods=['GET', 'POST'])
def get_post_orders():
    if request.method == 'GET':
        return query_all_get(Order)
    if request.method == 'POST':
        return query_post_add(Order)
    else:
        return 'Неверный метод запроса', 500


@app.route('/orders/<int:idx>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_order(idx):
    if request.method == 'GET':
        return query_get_by_id(Order, idx)
    if request.method == 'PUT':
        return query_put_update(Order, idx)
    if request.method == 'DELETE':
        return query_delete(Order, idx)
    else:
        return 'Неверный метод запроса', 500


@app.route('/offers', methods=['GET', 'POST'])
def get_post_offers():
    if request.method == 'GET':
        return query_all_get(Offer)
    if request.method == 'POST':
        return query_post_add(Offer)
    else:
        return 'Неверный метод запроса', 500


@app.route('/offers/<int:idx>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_offer(idx):
    if request.method == 'GET':
        return query_get_by_id(Offer, idx)
    if request.method == 'PUT':
        return query_put_update(Offer, idx)
    if request.method == 'DELETE':
        return query_delete(Offer, idx)
    else:
        return 'Неверный метод запроса', 500


if __name__ == '__main__':
    app.run(debug=True)
