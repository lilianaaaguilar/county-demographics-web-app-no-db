from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def home():
	states = get_state_options()
	state = request.args.get('state', '')
	if not state:
		with open('demographics.json') as file:
			counties = json.load(file)
			state = counties[0]["State"]

	states = get_state_options(selected_state=state)
	county_options = get_county_options(state)

	return render_template('home.html', state_options=states, county_options=county_options, selected_state=state)

@app.route('/showFact')
def render_fact():
	state = request.args.get('state', '')
	selected_county = request.args.get('county', '')
	states = get_state_options(selected_state=state)

	county1 = county_most_under_18(state)
	fact1 = "In " + state + ", the county with the highest percentage of under 18 year olds is " + county1 + "."
	county2 = county_most_other_lang(state)
	fact2= "In " + state + ", the county with the highest percentage of citzens who speak a language other than English at home is " + county2 + "."
	county3 = county_highest_pop(state)
	fact3 = "In " + state + ", the county with the highest population from 2014 is " + county3 + "."
    
	funFact4 = None
	county_options = None
	if state:
		county_options = get_county_options(state)
	if selected_county:
		funFact4 = f"In {selected_county}, {county_bachelors_percent(state, selected_county)}% of people have a bachelor's degree or higher."

	county_dropdown = get_county_options(state, selected_county) if state else None
    
	return render_template('home.html', state_options=states, county_options=county_dropdown, funFact1=fact1, funFact2=fact2, funFact3=fact3, funFact4=funFact4)
   
   
def get_state_options(selected_state=""):
	"""Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
	with open('demographics.json') as demographics_data:
		counties = json.load(demographics_data)
	states=[]
	for c in counties:
		if c["State"] not in states:
			states.append(c["State"])
	options=""
	for s in states:
		if s == selected_state:
			options += Markup(f'<option value="{s}" selected>{s}</option>')
		else:
			options += Markup(f'<option value="{s}">{s}</option>')
	return options
    
def get_county_options(state, selected_county=''):
	"""Return HTML <option> tags for all counties in the selected state."""
	with open('demographics.json') as demographics_data:
		counties = json.load(demographics_data)

	options = ""
	for c in counties:
		if c["State"] == state:
			if c["County"] == selected_county:
				options += Markup(f'<option value="{c["County"]}" selected>{c["County"]}</option>')
			else:
				options += Markup(f'<option value="{c["County"]}">{c["County"]}</option>')
	return options

def county_most_under_18(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county
    
def county_most_other_lang(state):
	"""Return the name of a county in the given state with the highest percent of a spoken Language Other than English at Home."""
	with open('demographics.json') as demographics_data:
		counties = json.load(demographics_data)
	highest = 0
	county = ""
	for c in counties:
		if c["State"] == state:
			if c["Miscellaneous"]["Language Other than English at Home"] > highest:
				highest = c["Miscellaneous"]["Language Other than English at Home"]
				county = c["County"]
	return county
    
def county_highest_pop(state):
	"""Return the name of a county in the given state with the highest population from 2014."""
	with open('demographics.json') as demographics_data:
		counties = json.load(demographics_data)
	highest = 0
	county = ""
	for c in counties:
		if c["State"] == state:
			if c["Population"]["2014 Population"] > highest:
				highest = c["Population"]["2014 Population"]
				county = c["County"]
	return county
	
def county_most_bachelors(state):
    with open('demographics.json') as f:
        counties = json.load(f)
    highest = 0
    county = ""
    for c in counties:
        if c["State"] == state and c["Education"]["Bachelor's Degree or Higher"] > highest:
            highest = c["Education"]["Bachelor's Degree or Higher"]
            county = c["County"]
    return county

def county_bachelors_percent(state, county_name):
    with open('demographics.json') as f:
        counties = json.load(f)
    for c in counties:
        if c["State"] == state and c["County"] == county_name:
            return c["Education"]["Bachelor's Degree or Higher"]
    return 0
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
