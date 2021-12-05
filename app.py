# importing Flask and other modules
from flask import Flask, request, render_template

import requests
import urllib.parse

# Flask constructor
app = Flask(__name__)


def meeting_place(loc1: str, loc2, str):
    url1 = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(loc1) + '?format=json'
    url2 = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(loc2) + '?format=json'

    response1 = requests.get(url1).json()
    response2 = requests.get(url2).json()

    return f'({response1[0]["lat"]}, {response1[0]["lon"]})'


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("loc1")
        # getting input with name = lname in HTML form
        last_name = request.form.get("loc2")
        return "Your (Lat, Long) is " + meeting_place(loc1, loc2)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()