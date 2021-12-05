# importing Flask and other modules
from flask import Flask, request, render_template

from geopy.geocoders import Nominatim

# Flask constructor
app = Flask(__name__)


def meeting_place(loc1: str, loc2: str):
    locator = Nominatim(user_agent="find-a-meeting-place")
    location1 = locator.geocode(loc1)
    location2 = locator.geocode(loc2)

    return f'({location1.latitude}, {location1.longitude})'


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        loc1 = request.form.get("loc1")
        # getting input with name = lname in HTML form
        loc2 = request.form.get("loc2")
        return "Your (Lat, Long) is " + meeting_place(loc1, loc2)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()