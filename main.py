from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from data import users_data

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(30))
    phone = db.Column(db.String(20))

    order = relationship("Order")
    offers = relationship("Offer")

    def __repr__(self):
        return {'first_name': self.first_name}


class Order(db.Model):
    __tablename__ = "Orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.NVARCHAR(100))
    description = db.Column(db.NVARCHAR(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    executer_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = relationship("User")
    offer = relationship("Offer")
    customer = db.relationship('User', foreign_keys=[customer_id, executer_id])
    # executer = db.relationship('User', foreign_keys=[executer_id])


class Offer(db.Model):
    __tablename__ = "Offers"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.id))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))
    offer = relationship("Order")
    offers = relationship("User")


def migrate_data(data):
    for d in data:
        new_inst = User(**d)
        db.session.add(new_inst)

    db.session.commit()
    # print(User.query.get(2).__repr__())
db.drop_all()
db.create_all()

migrate_data(users_data)

# db.drop_all()
# db.create_all()
