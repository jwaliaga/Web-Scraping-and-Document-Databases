from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

#Use Pymongo to establish Mongo Connection
#mongo = PyMongo(app,url="mongodb://localhost:27017/mars_app")
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():

    #Run the scrape function
    mars_dict = scrape_mars.scrape()

    #Update the mongo database using update and upsert=True
    mongo.db.collection.update({},mars_dict,upsert=True)
    
    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data = destination_data)


@app.route("/scrape")
def scrape():
    #Run the scrape function
    mars_dict = scrape_mars.scrape()

    #Update the mongo database using update and upsert=True
    mongo.db.collection.update({},mars_dict,upsert=True)

    # Redirect back to home page
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)