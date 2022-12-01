import dash
import os
from flask_login import LoginManager, UserMixin
from model import db, User as base
from config import config

app = dash.Dash(__name__)
app.title = 'MDV'
app._favicon = "migration_ico.ico"
server = app.server
app.config.suppress_callback_exceptions = True

server.config.update(SECRET_KEY=os.urandom(12),
                     SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
                     SQLALCHEMY_TRACK_MODIFICATIONS=False)

db.init_app(server)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


class User(UserMixin, base):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
