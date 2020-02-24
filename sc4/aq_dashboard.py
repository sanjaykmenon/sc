"""OpenAQ Air Quality Dashboard with Flask."""
# Section 1-4: Importing
from flask import Flask, render_template
import requests
import openaq
from flask_sqlalchemy import SQLAlchemy


# Section 1: setting flask
app = Flask(__name__)

# Section 3: Connecting SQLite and our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)

# Section 3: Create class here -- (reference: models.py from TwitOff doc)
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "Time{} : Value{}".format(self.datetime,self.value)

# Section 2: List comprehension
def get_data(city, parameter):
    """ Query OpenAQ for a city and corresponding air quality value """
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    observations = [(obs['date']['utc'], obs['value']) for obs in body['results']]
    return observations


#### ROUTES ####
@app.route('/')
def root():
    """This returns folder holding templates - home.html"""
    return str(Record.query.filter(Record.value >= 10.0).all())

@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
### Begin Sanjay code here ###
    for obs in get_data('Los Angeles', 'pm25'):
        store_data = Record(datetime = str(obs[0]), value = obs[1])
        DB.session.add(store_data)
### End Sanjay code here ###
    DB.session.commit()
    return 'Data refreshed!'

if __name__ == '__main__':
    app.run()