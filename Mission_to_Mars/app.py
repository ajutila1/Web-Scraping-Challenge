from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

# Route to render index.html template using data from Mongo
@app.route('/')
def home():

    mars_data = mongo.db.collection.find_one()

    return render_template('index.html', mars_ref=mars_data)

# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():
    mars_web_info = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_web_info, upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)