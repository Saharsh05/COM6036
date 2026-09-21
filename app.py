import os

from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import text

from extensions import db, login_manager, csrf


load_dotenv()


app = Flask(__name__)




app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


database_url = os.getenv("DATABASE_URL")

# Supabase normally gives us postgresql://
# psycopg uses postgresql+psycopg://
if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )


app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db.init_app(app)

login_manager.init_app(app)

csrf.init_app(app)


# @app.route("/")
# def home():
#     return "<h1>StudyForge</h1><p>Flask is working.</p>"

@app.route("/database-test")
def database_test():

    try:
        db.session.execute(text("SELECT 1"))

        return "Database connection successful!"

    except Exception as error:

        return f"Database connection failed: {error}"

if __name__ == "__main__":
    app.run(debug=True)