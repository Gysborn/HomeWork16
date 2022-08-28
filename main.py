from flask import Flask
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
    as_executor_in_offers = db.relationship('Offer', foreign_keys='Offer.executor_id')# Положит список всех оферов в которых он указан как исполнитель
    as_executor_in_orders = db.relationship('Order', foreign_keys='Order.executor_id')
    as_customer_in_orders = db.relationship('Order', foreign_keys='Order.customer_id')
    # order = relationship("Order")
    # offers = relationship("Offer")




class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    start_date = db.Column(db.String(255))
    end_date = db.Column(db.String(255))
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    as_order_in_offers = db.relationship('Offer')# Ищет в Офере внешний ключ ссылающийся на него самого и кладет в переменную



class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    order = db.relationship('Order', back_populates="as_order_in_offers", foreign_keys=[order_id])#кладет экз. заказа на который ссылается внешний ключ order_id(as_order_in_offers)
    executor = db.relationship('User', back_populates="as_executor_in_offers", foreign_keys=[executor_id])#
    # offer = relationship("Order")
    # offers = relationship("User")


db.drop_all()
db.create_all()


def migrate_data(data, model):
    try:
        for d in data:
            new_inst = model(**d)
            db.session.add(new_inst)

        db.session.commit()
        #print(User.query.get(2).__repr__())
    except Exception as e:
        print(f'Ощибочка вышла {e}')



migrate_data(users_data, User)
migrate_data(orders_data, Order)
migrate_data(offers_data, Offer)
x = 1

if __name__ == '__main__':
    app.run(debug=True)

# db.drop_all()
# db.create_all()
