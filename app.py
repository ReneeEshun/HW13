
from flask import Flask, render_template
import pymongo
from datetime import datetime
from scrapping import scrape_all

app=Flask(__name__)

#Set up database and collections
CLIENT=pymongo.MongoClient()
PAST_SCRAPES=CLIENT.mars.scrapes

#Route to read from database and show data index.html page
@app.route("/")
def index():
    data=PAST_SCRAPES.find().sort("timestamp",pymongo.DESCENDING).next()
    return render_template("index.html",data=data)
    
#insert most recent data into database using datetime and return string to show scrape is complete
@app.route("/scrapping")
def scrape():
    data=scrape_all()
    data["timestamp"]=datetime.utcnow()
    PAST_SCRAPES.insert_one(data)
    return "Scrape Complete!"


if __name__=="__main__":
    app.run()
