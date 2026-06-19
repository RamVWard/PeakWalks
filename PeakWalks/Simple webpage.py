# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

import folium
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from pyexpat.errors import messages
from wtforms import StringField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

pubsgroup = folium.FeatureGroup(name="PubsGroup", control=False)
folium.GeoJson(
    "https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/pubs.geojson", marker=folium.Marker(icon=folium.Icon(color='red', icon='wine-glass', prefix='fa'))).add_to(
    pubsgroup)

cafesgroup = folium.FeatureGroup(name="CafesGroup", control=False)
folium.GeoJson(
    "https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/cafes.geojson", marker=folium.Marker(icon=folium.Icon(color='blue', icon='mug-saucer', prefix='fa'))).add_to(
    cafesgroup)

viewpointsgroup = folium.FeatureGroup(name="ViewpointsGroup", control=False)
folium.GeoJson(
    "https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/viewpoints.geojson", marker=folium.Marker(icon=folium.Icon(color='lightgray', icon='binoculars', prefix='fa'))).add_to(
    viewpointsgroup)

historicgroup = folium.FeatureGroup(name="HistoricGroup", control=False)
folium.GeoJson(
"https://raw.githubusercontent.com/RamVWard/PeakWalks/refs/heads/master/PeakWalks/geodata/historic.geojson", marker=folium.Marker(icon=folium.Icon(color='orange', icon='chess-rook', prefix='fa'))).add_to(
    historicgroup)


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
    villages = BooleanField("villages")
    other = BooleanField("other")


    walkLength = FloatField("Length of the walk in hours", validators=[NumberRange(min=0, max=24)], default=0)
    timePadding = FloatField("Extra time needed in minutes", validators=[NumberRange(min=0, max=600)], default=0)

    submit = SubmitField('Submit')

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/", methods=['GET', 'POST'])
def main():


    message = "bah"

    form = MainForm()

    pubs = False
    cafes = False
    viewpoints = False
    historic = False
    villages = False
    other = False

    if form.validate_on_submit():
        pubs = form.pubs.data
        cafes = form.cafes.data
        viewpoints = form.viewpoints.data
        historic = form.historic.data
        villages = form.villages.data
        other = form.other.data

    if pubs:
        message = "pubs true"

    map = iframe(pubs, cafes, viewpoints, historic, villages, other)

    return render_template('home.html', iframe=map, form=form, message=message)

def iframe(pubs, cafes, viewpoints, historic, villages, other):
    """Embed a map as an iframe on a page."""
    m = folium.Map(location=[53.34327329800715, -1.777631461025655], zoom_start=10)

    # set the iframe width and height
    m.get_root().width = "80%"
    m.get_root().height = "100%"

    if pubs:
        #get all pubs and add to the map
        pubsgroup.add_to(m)

    if cafes:
        cafesgroup.add_to(m)

    if viewpoints:
        viewpointsgroup.add_to(m)

    if historic:
        historicgroup.add_to(m)

    map = m.get_root()._repr_html_()
    return map


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()