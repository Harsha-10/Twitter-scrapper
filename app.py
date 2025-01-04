from flask import Flask, render_template, redirect, url_for
import scraper
from pymongo import MongoClient
import json
import requests
from bson import ObjectId
from datetime import datetime
app = Flask(__name__)
MONGO_URI = "mongodb+srv://docsuser:docsuser123@cluster0.lb8gg2f.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["twitter_scrapper"]
collection = db["trending"]

def mongo_object_to_dict(mongo_obj):
    mongo_dict = mongo_obj.copy()
    for key, value in mongo_dict.items():
        if isinstance(value, ObjectId):
            mongo_dict[key] = str(value)
    return mongo_dict

@app.route('/')
def home():
    last_four = list(collection.find().sort("_id", -1).limit(4))
    last_four = [mongo_object_to_dict(record) for record in last_four]
    ip_address = requests.get('https://api64.ipify.org?format=json').json().get('ip')
    script_completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("index.html", last_four=last_four, script_time=script_completion_time, ip_address=ip_address, json_data=last_four)

@app.route('/run-scraper', methods=['POST'])
def run_script():
    scraper_instance = scraper.TwitterScraper()
    scraper_instance.run()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
