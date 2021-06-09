from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from random import randint
import Mars_Scraping

# Create an instance of Flask
app = Flask(__name__, static_folder='static')

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Nasa")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

@app.route("/new")
def new():
    # mars = mongo.db.mars_data.aggregate([{ $sample: { size: 1 } }])
    RandomNumber = randint(0, 15)
    mars = mongo.db.mars_data.find().limit(-1).skip(RandomNumber).next()
    
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape functiona
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = Mars_Scraping.scrape_mars()

    # Update the Mongo database using update and upsert=True
    # mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
