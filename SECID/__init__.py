from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '70898ff6cf8c6fc9a940820e7c211072'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:VoZfcHBKDAeIvFVPVhfvaZzMHWmSuEeh@autorack.proxy.rlwy.net:30030/railway'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'


from SECID import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()



from SECID import routes