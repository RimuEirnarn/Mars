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

def validate(n, a, s):
    if len(n) >= 512 or len(a) >= 512 or len(s) >= 512:
        return 400, "Either name, address, or size exceed the limit"
    return None, None

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/mars", methods=["POST"])
def web_mars_post():
    name = request.form['name']
    address = request.form['address']
    size = request.form['size']
    c, r = validate(name, address, size)
    if c:
        return r, c
    if not size.isnumeric():
        return jsonify({"status": "error", "message": "Size not an integer"})
    mars.insert_one({
        'name': name,
        'address': address,
        'size': int(size)
    })
    return jsonify({'status': 'success', 'message': "Purchase success!"})


@app.route("/mars", methods=["GET"])
def web_mars_get():
    reqs = list(mars.find({}, {'_id': False}))
    return jsonify({'status': 'success', 'request': reqs})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
