from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Hotel_Reservation.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'customer.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  from Hotel_Reservation.customer.routes import customer
  from Hotel_Reservation.admin.routes import admin
  from Hotel_Reservation.main.routes import main_page
  from Hotel_Reservation.rooms.routes import rooms
  from Hotel_Reservation.errors.handlers import errors
  
  app.register_blueprint(customer)
  app.register_blueprint(admin)
  app.register_blueprint(main_page)
  app.register_blueprint(rooms)
  app.register_blueprint(errors)

  return app
