import pyodbc

# Set your connection details
server = 'computer-security-fortnite-group.database.windows.net'
database = 'is-this-you-db'
username = 'fortnite'
password = '5Nights!'
driver = '{ODBC Driver 17 for SQL Server}'  # Use the correct driver version

# Build the connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Connect to the database
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    create_table_query = '''
    CREATE TABLE SampleTable (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(255),
        Age INT
    )
    '''

    cursor.execute(create_table_query)
    connection.commit()

    # Insert some data into the table
    insert_data_query = '''
    INSERT INTO SampleTable (Name, Age)
    VALUES
        ('John Doe', 30),
        ('Jane Smith', 25),
        ('Bob Johnson', 35)
    '''

    cursor.execute(insert_data_query)
    connection.commit()

    # Query the data from the table
    select_query = 'SELECT * FROM SampleTable'
    cursor.execute(select_query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection
    if 'connection' in locals():
        connection.close()
