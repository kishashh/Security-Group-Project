from flask import Flask, render_template, request, url_for
import pyodbc
import os

# Set your connection details
server = 'computer-security-fortnite-group.database.windows.net'
database = 'is-this-you-db'
username = 'fortnite'
password = '5Nights!'
driver = '{ODBC Driver 17 for SQL Server}'  # Use the correct driver version

# Build the connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
template_dir = os.path.abspath('../../Software Engineering/Security-Group-Project')
#static_dir = os.path.abspath('../../Software Engineering/Security-Group-Project')

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    firstname = request.form['fname']
    lastname = request.form['lname']
    email = request.form['email']

    try:
        # Connect to the database
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute('INSERT INTO Users (firstname, lastname, email) VALUES (?, ?, ?)', (firstname, lastname, email))
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
    
    return 'Name and email insterted succesfully'

@app.route('/login_form', methods=['GET'])
def login_form():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)