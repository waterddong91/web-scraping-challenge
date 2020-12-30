# MongoDB and Flask Application


# Dependencies and Setup
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars


# Flask Setup
app = Flask(__name__)


# PyMongo Connection Setup
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars
#app.config["MONGO_URI"] = "mongodb://localhost:27017/fruits_db"
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

'''
print('-----------------------------------------------------------------')
#print('mongo', mongo)
print('mongo.db', mongo.db)
print('mongo.db.mars', mongo.db.mars_app)
print('-----------------------------------------------------------------')
'''

# Flask Routes
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    mars = collection.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    collection.drop()
    #mars = mongo.db.collection
    mars_data = scrape_mars.scrape_all()
    collection.insert_one(mars_data)
    #mars.update({}, mars_data, upsert=True)
    #return "Scraping Successful"
    return redirect ("/", code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)