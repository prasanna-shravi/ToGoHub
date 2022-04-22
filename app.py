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
             
#Flask API routes

@app.route('/')
def main():
    return 'TOGOHUB Food Ordering App.'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)