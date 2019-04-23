from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DB_URL

app = Flask('chat')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




