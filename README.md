# COM6036
Smarter

Smarter is a Flask-based flashcard revision application that allows users to create subjects and flashcards, review cards, record confidence ratings, view review history, and receive revision priorities based on confidence, whether a card is new, and whether it is overdue.

Requirements

Before running the application, make sure you have:

Python installed

Git installed (optional, if cloning from GitHub)

Access to the Supabase PostgreSQL database used by the application

1. Download or clone the project

If using Git:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd COM6036

Alternatively, download the project as a ZIP file and extract it.

2. Create a virtual environment

From the project folder, run:

python -m venv venv

Activate the virtual environment

Using Git Bash on Windows:

source venv/Scripts/activate

Using PowerShell:

.\venv\Scripts\Activate.ps1

Using Command Prompt:

venv\Scripts\activate.bat

3. Install the required packages

With the virtual environment activated, run:

pip install -r requirements.txt

4. Create the environment file

Create a file called .env in the root project folder.

Add the following values:

DATABASE_URL=your_supabase_postgresql_connection_string
SECRET_KEY=your_secret_key

Replace the example values with the real configuration values for your environment.

Do not upload the .env file to GitHub. It should remain listed in .gitignore.

5. Create the database tables

If the database tables have not already been created, run:

python createDB.py

This creates the database tables required by the application.

6. Run the application

Start the Flask application with:

python app.py

If required, Flask can also be started with:

python -m flask --app app run --debug

Once the server starts, open a browser and go to:

http://127.0.0.1:5000/register

7. Using Smarter

After opening the application:

Register a new account.

Log in.

Create a subject.

Create flashcards for that subject.

Review flashcards and reveal the answer.

Record a confidence rating from 0 to 5.

View the dashboard to see revision priorities and recommended cards.

Use the flashcards page to search, filter, edit, delete, or view review history.

Running the automated tests

From the project root, with the virtual environment activated, run:

python -m pytest

Pytest will discover and run the automated tests in the tests folder.

Project structure

COM6036/
├── app.py
├── models.py
├── extensions.py
├── revisionService.py
├── createDB.py
├── requirements.txt
├── .env
├── templates/
├── static/
└── tests/

Security

Sensitive information such as the database connection string and Flask secret key must be stored in .env and must not be committed to source control.