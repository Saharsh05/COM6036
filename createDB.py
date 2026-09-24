from app import app
from extensions import db

import models

# Create the database tables when this script is run.
with app.app_context():

    db.create_all()

    print("Database tables created successfully.")