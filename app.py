from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#Using default sqlite DB for storing data
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#Using SQLAlchemy to create DB models
db = SQLAlchemy(app)


#DB Models for SQL Tables in our Database
#User table 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    orders=db.relationship('Order', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User <{self.name}>'


#Order table
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # order_items=db.relationship('OrderItem', backref='order', lazy='dynamic')
    items = db.relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f'Order <{self.id}>'

 #Item table
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), nullable=False)
    orders = db.relationship("OrderItem", back_populates="item")
	
    def __repr__(self):
        return f'OrderItem: <{self.name}>'

  #Association table between Order and Item table
class OrderItem(db.Model):
    order_id =db.Column(db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    item_count = db.Column(db.Integer)
    order = db.relationship("Order", back_populates="items")
    item = db.relationship("Item", back_populates="orders")

    def __repr__(self):
        return f'OrderItem: <{self.item_id}>'


#Using Marchmallow to serialize JSON objects from DB queries
ma = Marshmallow(app)

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    item = ma.Nested(ItemSchema)
    class Meta:
        model = OrderItem

class OrderSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(OrderItemSchema,many=True)
    class Meta:
        model = Order

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
orderitem_schema = OrderItemSchema()
orderitems_schema = OrderItemSchema(many=True)
           
#Flask API routes

@app.route('/')
def main():
    return 'TOGOHUB Food Ordering App.'

@app.route('/orders/')
def get_all_orders():
    all_orders = Order.query.all()
    return jsonify(orders_schema.dump(all_orders))

@app.route('/orders/<id>/')
def get_user_orders(id):
    user_orders = Order.query.filter_by(user_id=id).all()
    return jsonify(orders_schema.dump(user_orders))

@app.route('/order/<id>/')
def get_order(id):
    single_order = Order.query.filter_by(id=id).first_or_404()
    return jsonify(order_schema.dump(single_order))
@app.route('/items/')
def get_all_items():
    all_items = Item.query.all()
    return jsonify(items_schema.dump(all_items))

@app.route('/user/', methods=['POST'])
def create_user():
    data = request.get_json()

    user = User(name=data['name'],email=data['email'])
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)