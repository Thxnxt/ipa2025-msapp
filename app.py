from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://mongo:27017/")
mydb = client["ipa2025"]
mycol = mydb["router"]

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
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)