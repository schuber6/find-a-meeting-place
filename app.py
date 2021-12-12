# importing Flask and other modules
from flask import Flask, request, render_template
import folium
import numpy as np
import math

from geopy.geocoders import Nominatim

# Flask constructor
app = Flask(__name__)


def meeting_place(locs: list):
    locator = Nominatim(user_agent="find-a-meeting-place")
    locations = [locator.geocode(i) for i in locs]
    lats = [i.latitude for i in locations]
    lons = [i.longitude for i in locations]

    meeting = find_center(lats, lons)
    start_coords = (meeting['latitude'], meeting['longitude'])

    #return f'({meeting["latitude"]}, {meeting["longitude"]})'
    folium_map = folium.Map(location=start_coords)
    for i, loc in enumerate(locs):
        folium.Marker(
            [lats[i], lons[i]], popup=loc, tooltip=loc
        ).add_to(folium_map)
    folium.Marker(
        location=start_coords,
        popup=f"Center.  Find Restaurants here: https://www.google.com/maps/search/Restaurants/@{start_coords[0]},{start_coords[1]},11z",
        tooltip="Center",
        icon=folium.Icon(color="green", icon="ok"),
    ).add_to(folium_map)

    sw = [min(lats), min(lons)]
    ne = [max(lats), max(lons)]

    width = ne[0] - sw[0]
    height = ne[1] - sw[1]

    p = 0.2

    sw[0] -= width * p
    sw[1] -= height * p
    ne[0] += width * p
    ne[1] += height * p

    folium_map.fit_bounds([sw, ne])
    return folium_map._repr_html_()


def find_center(lats: list, lons: list) -> dict:
    xs = []
    ys = []
    zs = []
    for lat, lon in zip(lats, lons):
        lat_rad = lat * np.pi / 180
        lon_rad = lon * np.pi / 180
        xs.append(math.cos(lat_rad) * math.cos(lon_rad))
        ys.append(math.cos(lat_rad) * math.sin(lon_rad))
        zs.append(math.sin(lat_rad))

    x = np.mean(xs)
    y = np.mean(ys)
    z = np.mean(zs)

    return {'latitude': math.atan2(z, np.sqrt(x * x + y * y)) * 180 / np.pi,
            'longitude': math.atan2(y, x) * 180 / np.pi}


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        loc1 = request.form.get("Address1")
        # getting input with name = lname in HTML form
        loc2 = request.form.get("Address2")
        locations = []
        for i in range(int(request.form.get("member"))):
            location = request.form.get(f'Address{i + 1}')
            if location != '' and location is not None:
                locations.append(location)
        return meeting_place(locations)
        #return "Your (Lat, Long) is " + meeting_place(loc1, loc2)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()