from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)


#Flask API routes

@app.route('/')
def main():
    return 'TOGOHUB Food Ordering App.'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)