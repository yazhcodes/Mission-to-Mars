from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_apps"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars_apps.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars_apps
   scraped_data = scraping.scrape_all()
   mars.update({}, scraped_data, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run(debug=True)