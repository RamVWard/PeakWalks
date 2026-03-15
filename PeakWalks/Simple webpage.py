# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect, url_for
import folium
import requests

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/", methods=['GET', 'POST'])
def main():
    map = iframe()
    return render_template('home.html', iframe=map)

def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map(location=[53.34327329800715, -1.777631461025655], zoom_start=10)

    # set the iframe width and height
    m.get_root().width = "80%"
    m.get_root().height = "100%"

    pubsgroup = folium.FeatureGroup(name="PubsGroup", control=False)
    folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/pubnodes.geojson").add_to(pubsgroup)


    folium.LayerControl().add_to(m)

    pubs, cafes, viewpoints, historic, villages, other = index()

    if pubs:
        #get all pubs and add to the map
        pubsgroup.add_to(m)

    map = m.get_root()._repr_html_()
    return map

def index():
    pubs = request.form.get("poi-pubs")
    cafes = request.form.get("poi-cafes")
    viewpoints = request.form.get("poi-viewpoints")
    historic = request.form.get("poi-historic")
    villages = request.form.get("poi-villages")
    other = request.form.get("poi-other")

    return pubs, cafes, viewpoints, historic, villages, other

@app.route("/submit", methods=['POST'])
def submit():
    redirect(url_for('main'))


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()