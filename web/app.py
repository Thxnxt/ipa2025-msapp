import os

from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://mongo:27017/")
mydb = client["ipa2025"]
mycol = mydb["router"]

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

sample = Flask(__name__)

data = []

@sample.route("/")
def main():
    return render_template("index.html", data=mycol.find({}))

@sample.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        mycol.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_router():
    try:
        idx = request.form.get("idx")
        if idx:
            mycol.delete_one({"_id": ObjectId(idx)})
    except Exception as e:
            print("Delete failed:", e)
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)