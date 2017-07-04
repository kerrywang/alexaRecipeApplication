import os
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_dynamo import Dynamo

from itertools import izip_longest

app = Flask(__name__)
app.secret_key = '<;\x1b\x95\x94"\xd8\x9f\x89\xb5\xbb\x8d=\x9a\xdb\x91\xd54\xeb^\xc3\xdb\x82\xf9' # generated using os.urandom(24)

app.config['DYNAMO_TABLES'] = [
    Table('RecipesDB',
        schema=[HashKey('RecipeName')],
        connection=boto.dynamodb2.connect_to_region('us-east-1')
    )
]
dynamo = Dynamo(app)

# recipes = [{'RecipeName': 'Delicious Appetizer', 'ImageSRC': 'http://images.media-allrecipes.com/userphotos/250x250/01/11/92/1119294.jpg', 'IngredientsList': 'Appetizers\nThat are\nDelicious', 'PrepDirections': 'Make\nDelicious'},
#     {'RecipeName': 'Scrumptious Dessert', 'ImageSRC': 'http://images.media-allrecipes.com/userphotos/250x250/00/73/08/730824.jpg', 'IngredientsList': 'Dessert\nNot\nDesert', 'PrepDirections': 'Use scrumptiousification machine\nWait while skipping around kitchen 160 times'},
#     {'RecipeName': 'Cup of Coffee', 'ImageSRC': 'https://dncache-mauganscorp.netdna-ssl.com/thumbseg/1669/1669473-bigthumbnail.jpg', 'IngredientsList': 'Coffee\nAnd maybe\nA coffee machine', 'PrepDirections': 'Please read the manual on how to use coffee machine.'},
#     {'RecipeName': 'Flalfle', 'ImageSRC': 'http://hanoikids.org/testwp/wp-content/uploads/2015/06/chay-2-1024x683.jpg', 'IngredientsList': 'F x2\nA x2\nL x2\nE x1', 'PrepDirections': 'LERN\n2\nSPEL\nTHX\nBAI'},
#     {'RecipeName': 'Banana for scale', 'ImageSRC': 'https://www.bbcgoodfood.com/sites/default/files/glossary/banana-crop.jpg', 'IngredientsList': 'Banana', 'PrepDirections': 'For scale only.'}]

@app.route('/')
def home():
    if 'last_view' in session:
        if session['last_view'] == 'show':
            if 'recipe_id' in session:
                return redirect(url_for('show', recipe_name=session['recipe_name']))
        else:
            return redirect(url_for(session['last_view']))
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    flash('Page Not Found!')
    return redirect(url_for('index'))

@app.route('/recipes')
def index():
    session['last_view'] = 'index'
    recipe_groups = izip_longest(*([iter(dynamo.RecipesDB.scan())] * 3))
    return render_template('index.html', recipe_groups=recipe_groups)

@app.route('/recipes/<recipe_name>')
def show(recipe_name):
    session['last_view'], session['recipe_name'] = 'show', recipe_name
    recipe = dynamo.RecipesDB.get_item(RecipeName=str(recipe_name))
    if recipe:
        return render_template('show.html', recipe=recipe)
    else:
        flash('No recipe under that name was found!')
        return redirect(url_for('index'))

@app.route('/recipes/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        data = {
            'RecipeName': str(request.form['RecipeName']),
            'IngredientsList': str(request.form['Ingredients']),
            'PrepDirections': str(request.form['Directions']),
            'ImageSRC': str(request.form['Image'])
        }
        # sanitize data
        dynamo.RecipesDB.put_item(data=data)
        return redirect(url_for('index'))
    else:
        session['last_view'] = 'new'
        return render_template('new.html')

@app.route('/recipes/search')
def find():
    return unimplemented('Search functionality')

@app.route('/settings')
def settings():
    return unimplemented('Settings page')

def unimplemented(route):
    print 'WARNING: Route not implemented:', route
    flash(route + ' has not been implemented yet.')
    return render_template('layout.html')

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))