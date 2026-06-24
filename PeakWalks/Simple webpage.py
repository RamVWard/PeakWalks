# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

import folium
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from numpy.random.mtrand import triangular
from pyexpat.errors import messages
from wtforms import StringField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
import pyap
from geopy.geocoders import Nominatim

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

geo = Nominatim(user_agent="Simple webpage")

cafeMarker = folium.Marker(lazy = True, icon=folium.Icon(color='blue', icon='mug-saucer', prefix='fa'))
cafePopup = folium.GeoJsonPopup(fields=["name", "addr:postcode", "addr:street", "addr:city"], aliases=["Name", "Postcode", "Street", "City"], labels=False, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)
cafeTooltip = folium.GeoJsonTooltip(fields=["name", "addr:postcode", "addr:street"], aliases=["Name", "Postcode", "Street"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)

pubMarker = folium.Marker(lazy = True, icon=folium.Icon(color='red', icon='wine-glass', prefix='fa'))
pubPopup = folium.GeoJsonPopup(fields=["name", "addr:postcode", "addr:street", "addr:city"], aliases=["Name", "Postcode", "Street", "City"], style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)
pubTooltip = folium.GeoJsonTooltip(fields=["name", "addr:postcode", "addr:street"], aliases=["Name", "Postcode", "Street"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)

viewpointMarker = folium.Marker(lazy = True, icon=folium.Icon(color='lightgray', icon='binoculars', prefix='fa'))
viewpointPopup = folium.GeoJsonPopup(fields=["name"], style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)
viewpointTooltip = folium.GeoJsonTooltip(fields=["name"], aliases=["Name"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)

historicMarker = folium.Marker(lazy = True, icon=folium.Icon(color='orange', icon='chess-rook', prefix='fa'))
historicPopup = folium.GeoJsonPopup(fields=["name", "website", "historic"], aliases=["Name", "Website", "Historic"], style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)
historicTooltip = folium.GeoJsonTooltip(fields=["name", "historic"], aliases=["Name", "Historic"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)

busMarker = folium.Marker(lazy = True, icon=folium.Icon(color='lightgreen', icon='bus-simple', prefix='fa'))
busPopup = folium.GeoJsonPopup(fields=["name", "naptan:NaptanCode", "naptan:AtcoCode", "shelter", "bench", "bin"], aliases=["Name", "Naptan", "Atco", "Shelter", "Bench", "Bin"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)
busTooltip = folium.GeoJsonTooltip(fields=["name", "naptan:NaptanCode", "naptan:AtcoCode"], aliases=["Name", "Naptan", "Atco"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)

trainMarker = folium.Marker(lazy = True, icon=folium.Icon(color='green', icon='train', prefix='fa'))
trainPopup = folium.GeoJsonPopup(fields=["name", "network:website", "naptan:AtcoCode", "ref:crs", "wikipedia"], aliases=["Name", "Website", "AtcoCode", "Reference", "Wikipedia"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)
trainTooltip = folium.GeoJsonTooltip(fields=["name", "network:website", "naptan:AtcoCode"], aliases=["Name", "Website", "AtcoCode"], sticky=False, labels=True, style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)

pubsGroup = folium.FeatureGroup(name="PubsGroup", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/pubs.geojson",
               marker=pubMarker, tooltip=pubTooltip, popup=pubPopup).add_to(pubsGroup)

cafesGroup = folium.FeatureGroup(name="CafesGroup", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/cafes.geojson",
               marker=cafeMarker, tooltip=cafeTooltip, popup=cafePopup).add_to(cafesGroup)

viewpointsGroup = folium.FeatureGroup(name="ViewpointsGroup", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/viewpoints.geojson",
               marker=viewpointMarker, tooltip=viewpointTooltip, popup=viewpointPopup).add_to(viewpointsGroup)

historicGroup = folium.FeatureGroup(name="HistoricGroup", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/historic.geojson",
               marker=historicMarker, tooltip=historicTooltip, popup=historicPopup).add_to(historicGroup)

busSheff = folium.FeatureGroup(name="BusSheff", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/bussheff.geojson",
               marker=busMarker, tooltip=busTooltip, popup=busPopup).add_to(busSheff)

busPeaks= folium.FeatureGroup(name="BusPeaks", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/buspeaks.geojson",
               marker=busMarker, tooltip=busTooltip, popup=busPopup).add_to(busPeaks)

trainSheff = folium.FeatureGroup(name="TrainSheff", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/trainsheff.geojson",
               marker=trainMarker, tooltip=trainTooltip, popup=trainPopup).add_to(trainSheff)

trainPeaks = folium.FeatureGroup(name="TrainPeaks", control=False)
folium.GeoJson("https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/trainpeaks.geojson",
               marker=trainMarker, tooltip=trainTooltip, popup=trainPopup).add_to(trainPeaks)


app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class MainForm(FlaskForm):
    id = "form"
    pubs = BooleanField("pubs")
    cafes = BooleanField("cafes")
    viewpoints = BooleanField("viewpoints")
    historic = BooleanField("historic")
    #villages = BooleanField("villages")
    #other = BooleanField("other")
    busses = BooleanField("busses")
    trains = BooleanField("trains")

    startLocation = StringField("Start Location")

    walkLength = FloatField("Length of the walk in hours", validators=[NumberRange(min=0, max=24)], default=0)
    timePadding = FloatField("Extra time needed in minutes", validators=[NumberRange(min=0, max=600)], default=0)

    submit = SubmitField('Submit')

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/", methods=['GET', 'POST'])
def main():
    form = MainForm()
    pubs = False
    cafes = False
    viewpoints = False
    historic = False
    #villages = False
    #other = False
    busses = False
    trains = False
    startLocation = ""
    walkLength = 0
    timePadding = 0

    if form.validate_on_submit():
        pubs = form.pubs.data
        cafes = form.cafes.data
        viewpoints = form.viewpoints.data
        historic = form.historic.data
        #villages = form.villages.data
        #other = form.other.data
        busses = form.busses.data
        trains = form.trains.data
        startLocation = form.startLocation.data
        walkLength = form.walkLength.data
        timePadding = form.timePadding.data




    peakmap = iframe(pubs, cafes, viewpoints, historic, busses, trains, startLocation)

    return render_template('home.html', iframe=peakmap, form=form)

def iframe(pubs, cafes, viewpoints, historic, busses, trains, startLocation):
    """Embed a map as an iframe on a page."""
    m = folium.Map(location=[53.34327329800715, -1.777631461025655], zoom_start=10)

    # set the iframe width and height
    m.get_root().width = "80%"
    m.get_root().height = "100%"

    if pubs:
        #get all pubs and add to the map
        pubsGroup.add_to(m)

    if cafes:
        cafesGroup.add_to(m)

    if viewpoints:
        viewpointsGroup.add_to(m)

    if historic:
        historicGroup.add_to(m)

    if busses:
        busPeaks.add_to(m)
        busSheff.add_to(m)

    if trains:
        trainPeaks.add_to(m)
        trainSheff.add_to(m)


    if startLocation != "":
        startAddress = geo.geocode(startLocation).raw
        lat = startAddress['lat']
        lon = startAddress['lon']
        folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='house', prefix='fa')).add_to(m)


    peakmap = m.get_root()._repr_html_()
    return peakmap


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()