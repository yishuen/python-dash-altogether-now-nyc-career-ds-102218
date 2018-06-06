# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
#import dash
import dash

# initialize new dash app
app = dash.Dash(__name__, url_base_pathname='/dashboard')

# add configurations and database
app.server.config['DEBUG'] = True
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(app.server)

from dashaltogethernow import dash_layout

from dashaltogethernow import routes
