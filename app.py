from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Initialize flask app
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
    #Nestes schemas to include relationship tables as part of json output
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

#Get all the orders from the Database
@app.route('/orders/')
def get_all_orders():
    all_orders = Order.query.all()
    return jsonify(orders_schema.dump(all_orders))

#Get all the orders of a specific user
@app.route('/orders/<id>/')
def get_user_orders(id):
    user_orders = Order.query.filter_by(user_id=id).all()
    return jsonify(orders_schema.dump(user_orders))

#Get details of a specific order
@app.route('/order/<id>/')
def get_order(id):
    single_order = Order.query.filter_by(id=id).first_or_404()
    return jsonify(order_schema.dump(single_order))

#Get all food items available in the app
@app.route('/items/')
def get_all_items():
    all_items = Item.query.all()
    return jsonify(items_schema.dump(all_items))

#Create a new user in the app
@app.route('/user/', methods=['POST'])
def create_user():
    data = request.get_json()

    user = User(name=data['name'],email=data['email'])
    db.session.add(user)
    db.session.commit()

    return { 'message': 'User Created', 'user_id': user.id}

#Add a new food item to the app    
@app.route('/item/', methods=['POST'])
def create_item():
    data = request.get_json()

    item = Item(name=data['name'])
    db.session.add(item)
    db.session.commit()

    return { 'message': 'Item Created', 'item_id': item.id}

#Create a new order
@app.route('/order/', methods=['POST'])
def create_order():
    data = request.get_json()
    #Create a new order entry in Order table
    order = Order(user_id=data['user_id'])
    db.session.add(order)
    db.session.commit()
    #For each order item in the order, create a new entry in Association table
    for item in data['order_items']:
        orderitem = OrderItem(order_id=order.id, item_id=item['item_id'], item_count=item['item_count'])
        db.session.add(orderitem)
    db.session.commit()

    return { 'message': 'Order Created', 'order_id': order.id}



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)