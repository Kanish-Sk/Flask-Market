from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# This statement is dictionary that accept some keys and values.URI-uniform resource allocator.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '5ae8433de648a33ff5359d57'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# We have to specify were our login router located.It accept string formatted input..
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes
