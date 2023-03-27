"""App"""
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

load_dotenv(join(dirname(__file__), '.env'))

client = MongoClient(environ.get("MONGODB_URI"))
database = client[environ.get("DB_NAME")]
mars = database.mars

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/mars", methods=["POST"])
def web_mars_post():
    name = request.form['name']
    address = request.form['address']
    size = request.form['size']
    mars.insert_one({
        'name': name,
        'address': address,
        'size': size
    })
    return jsonify({'status': 'success', 'message': "Purchase success!"})


@app.route("/mars", methods=["GET"])
def web_mars_get():
    reqs = list(mars.find({}, {'_id': False}))
    return jsonify({'status': 'success', 'request': reqs})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
