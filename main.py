from flask import Flask
from flask_pymongo import PyMongo
import urllib.parse
from flask_cors import CORS
app = Flask(__name__)
cors=CORS(app)
app.config["MONGO_URI"]=url="mongodb+srv://naveenkumar:"+urllib.parse.quote("Naveen@1")+"@cluster0.r2ewe.mongodb.net/classroom?retryWrites=true&w=majority"
print("connected to the MongoDB server....")
app.secret_key="Naveen@1"
client=PyMongo(app)